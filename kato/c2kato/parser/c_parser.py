from ..ast import CProgram, CFunctionDef
from ..errors import C2KatoError
from .expression_parser import CExpressionParser
from .statement_parser import CStatementParser


class CParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        
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
                declarations.append(self.parse_function_or_declaration())
            else:
                self.advance()
        
        return CProgram(declarations)
    
    def skip_preprocessor(self):
        self.advance()
        while self.current_token() and self.current_token().type != "EOF":
            if self.current_token().type in ["INT_TYPE", "FLOAT_TYPE", "CHAR_TYPE", "VOID_TYPE"]:
                break
            self.advance()
    
    def parse_function_or_declaration(self):
        return_type_token = self.current_token()
        return_type = return_type_token.value
        self.advance()
        
        name_token = self.expect("IDENTIFIER")
        name = name_token.value
        
        if self.current_token() and self.current_token().type == "LPAREN":
            return self.parse_function(return_type, name)
        else:
            raise C2KatoError("Variable declarations not yet supported", name_token.line, name_token.column)
    
    def parse_function(self, return_type, name):
        self.expect("LPAREN")
        
        params = []
        while self.current_token() and self.current_token().type != "RPAREN":
            if self.current_token().type in ["INT_TYPE", "FLOAT_TYPE", "CHAR_TYPE", "VOID_TYPE"]:
                param_type = self.current_token().value
                self.advance()
                
                if self.current_token() and self.current_token().type == "IDENTIFIER":
                    param_name = self.current_token().value
                    self.advance()
                    params.append((param_type, param_name))
            
            if self.current_token() and self.current_token().type == "COMMA":
                self.advance()
        
        self.expect("RPAREN")
        self.expect("LBRACE")
        
        body = []
        while self.current_token() and self.current_token().type != "RBRACE":
            body.append(self.stmt_parser.parse_statement())
        
        self.expect("RBRACE")
        
        return CFunctionDef(return_type, name, params, body)
