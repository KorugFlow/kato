from ..ast import CProgram, CFunctionDef
from ..errors import C2KatoError
from .expression_parser import CExpressionParser
from .statement_parser import CStatementParser


class CParser:
    VALID_TYPES = {"int", "float", "char", "void", "int*", "float*", "char*"}
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.declared_functions = {}
        self.current_function = None
        self.declared_variables = set()
        
        self.expr_parser = CExpressionParser(self)
        self.stmt_parser = CStatementParser(self, self.expr_parser)
    
    def current_token(self):
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]
    
    def peek_token(self, offset=1):
        peek_pos = self.pos + offset
        if peek_pos >= len(self.tokens):
            return None
        return self.tokens[peek_pos]
    
    def advance(self):
        self.pos += 1
    
    def expect(self, token_type):
        token = self.current_token()
        if token is None:
            raise C2KatoError(f"Expected {token_type}, but reached end of file")
        if token.type != token_type:
            raise C2KatoError(f"Expected {token_type}, but got {token.type}", token.line, token.column)
        self.advance()
        return token
    
    def parse(self):
        declarations = []
        
        while self.current_token() and self.current_token().type != "EOF":
            token = self.current_token()
            
            if token.type == "HASH":
                self.skip_preprocessor()
            elif token.type in ["INT_TYPE", "FLOAT_TYPE", "CHAR_TYPE", "VOID_TYPE"]:
                result = self.parse_function_or_declaration()
                if result is not None:
                    declarations.append(result)
            elif token.type == "IDENTIFIER":
                similar = self._find_similar_keyword(token.value)
                if similar:
                    raise C2KatoError(f"Unknown identifier '{token.value}' at top level (did you mean '{similar}'?)", token.line, token.column)
                else:
                    raise C2KatoError(f"Unexpected token at top level: {token.type}", token.line, token.column)
            else:
                raise C2KatoError(f"Unexpected token at top level: {token.type}", token.line, token.column)
        
        return CProgram(declarations)
    
    def _find_similar_keyword(self, word):
        keywords = ["return", "int", "float", "char", "void", "if", "else", "while", "for", "switch", "case", "break", "continue"]
        for kw in keywords:
            if self._levenshtein_distance(word.lower(), kw) <= 2:
                return kw
        return None
    
    def _levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]
    
    def skip_preprocessor(self):
        self.advance()
        while self.current_token() and self.current_token().type != "EOF":
            if self.current_token().type in ["INT_TYPE", "FLOAT_TYPE", "CHAR_TYPE", "VOID_TYPE"]:
                break
            self.advance()
    
    def parse_function_or_declaration(self):
        return_type_token = self.current_token()
        if not return_type_token:
            raise C2KatoError("Unexpected end of file while parsing declaration")
        
        return_type = return_type_token.value
        type_line, type_col = return_type_token.line, return_type_token.column
        self.advance()
        
        if self.current_token() and self.current_token().type == "ASTERISK":
            return_type += "*"
            self.advance()
        
        if return_type not in self.VALID_TYPES:
            raise C2KatoError(f"Invalid type '{return_type}'", type_line, type_col)
        
        if not self.current_token() or self.current_token().type != "IDENTIFIER":
            token = self.current_token()
            raise C2KatoError(f"Expected identifier after type '{return_type}'", token.line if token else None, token.column if token else None)
        
        name_token = self.expect("IDENTIFIER")
        name = name_token.value
        
        if self.current_token() and self.current_token().type == "LPAREN":
            result = self.parse_function(return_type, name, name_token.line, name_token.column)
            return result
        else:
            raise C2KatoError("Global variable declarations not supported", name_token.line, name_token.column)
    
    def parse_function(self, return_type, name, name_line, name_col):
        if name in self.declared_functions:
            prev_def = self.declared_functions[name]
            raise C2KatoError(f"Redefinition of function '{name}' (previously defined at {prev_def['line']}:{prev_def['column']})", name_line, name_col)
        
        self.expect("LPAREN")
        
        params = []
        param_names = set()
        
        if self.current_token() and self.current_token().type == "RPAREN":
            self.expect("RPAREN")
        else:
            while True:
                if not self.current_token():
                    raise C2KatoError("Unexpected end of file in parameter list")
                
                if self.current_token().type not in ["INT_TYPE", "FLOAT_TYPE", "CHAR_TYPE", "VOID_TYPE"]:
                    token = self.current_token()
                    raise C2KatoError(f"Expected parameter type, got '{token.type}'", token.line, token.column)
                
                param_type_token = self.current_token()
                param_type = param_type_token.value
                self.advance()
                
                if self.current_token() and self.current_token().type == "ASTERISK":
                    param_type += "*"
                    self.advance()
                
                if param_type not in self.VALID_TYPES:
                    raise C2KatoError(f"Invalid parameter type '{param_type}'", param_type_token.line, param_type_token.column)
                
                if not self.current_token() or self.current_token().type != "IDENTIFIER":
                    token = self.current_token()
                    raise C2KatoError(f"Expected parameter name after type '{param_type}'", token.line if token else None, token.column if token else None)
                
                param_name_token = self.current_token()
                param_name = param_name_token.value
                
                if param_name in param_names:
                    raise C2KatoError(f"Duplicate parameter name '{param_name}'", param_name_token.line, param_name_token.column)
                
                param_names.add(param_name)
                self.advance()
                params.append((param_type, param_name))
                
                if self.current_token() and self.current_token().type == "COMMA":
                    self.advance()
                    if self.current_token() and self.current_token().type == "RPAREN":
                        token = self.current_token()
                        raise C2KatoError("Expected parameter after ','" , token.line, token.column)
                elif self.current_token() and self.current_token().type == "RPAREN":
                    self.expect("RPAREN")
                    break
                else:
                    token = self.current_token()
                    raise C2KatoError(f"Expected ',' or ')' in parameter list, got '{token.type}'", token.line, token.column)
        
        if self.current_token() and self.current_token().type == "SEMICOLON":
            self.advance()
            self.declared_functions[name] = {"return_type": return_type, "params": params, "line": name_line, "column": name_col}
            return None
        
        if not self.current_token() or self.current_token().type != "LBRACE":
            token = self.current_token()
            if token and token.type == "SEMICOLON":
                raise C2KatoError(f"Unexpected ';' after function definition (did you mean to declare or define?)", token.line, token.column)
            raise C2KatoError(f"Expected '{{' or ';' after function signature", token.line if token else None, token.column if token else None)
        
        self.expect("LBRACE")
        self.current_function = {"name": name, "return_type": return_type}
        self.declared_variables = set()
        for param_type, param_name in params:
            self.declared_variables.add(param_name)
        
        body = []
        while self.current_token() and self.current_token().type != "RBRACE":
            stmt = self.stmt_parser.parse_statement()
            if stmt is not None:
                body.append(stmt)
        
        self.expect("RBRACE")
        
        if self.current_token() and self.current_token().type == "SEMICOLON":
            token = self.current_token()
            raise C2KatoError("Unexpected ';' after function body (remove the semicolon)", token.line, token.column)
        
        self.declared_functions[name] = {"return_type": return_type, "params": params, "line": name_line, "column": name_col}
        self.current_function = None
        
        return CFunctionDef(return_type, name, params, body)
