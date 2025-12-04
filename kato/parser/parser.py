from .ast import Program, Function
from .errors import KatoSyntaxError
from .expression_parser import ExpressionParser
from .statement_parser import StatementParser


class Parser:
    def __init__(self, tokens, source_code=None):
        self.tokens = tokens
        self.pos = 0
        self.source_code = source_code
        self.source_lines = source_code.split('\n') if source_code else []
        self.defined_functions = set()
        self.builtin_functions = {"print", "random"}
        self.defined_variables = set()
        self.function_return_types = {}
        
        self.expr_parser = ExpressionParser(self)
        self.stmt_parser = StatementParser(self, self.expr_parser)
    
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
            raise KatoSyntaxError(
                f"Expected {token_type}, but reached end of file",
                1, 1,
                self.source_code
            )
        if token.type != token_type:
            raise KatoSyntaxError(
                f"Expected {token_type}, but got {token.type}",
                token.line, token.column,
                self.source_code
            )
        self.advance()
        return token
    
    def parse(self):
        functions = []
        c_imports = []
        
        while self.current_token() and self.current_token().type != "EOF":
            if self.current_token().type == "C_IMPORT":
                c_imports.append(self.stmt_parser.parse_c_import())
            elif self.current_token().type == "FUNCTION":
                functions.append(self.parse_function())
            else:
                token = self.current_token()
                raise KatoSyntaxError(
                    f"All code must be inside functions. Found '{token.value}' outside any function",
                    token.line, token.column,
                    self.source_code
                )
        
        has_main = any(func.name == "main" for func in functions)
        if not has_main:
            raise KatoSyntaxError(
                "Program must have a 'main' function",
                1, 1,
                self.source_code
            )
        
        program = Program(functions)
        program.c_imports = c_imports
        return program
    
    def parse_function(self):
        self.expect("FUNCTION")
        
        name_token = self.expect("IDENTIFIER")
        name = name_token.value
        
        if name in self.defined_functions or name in self.builtin_functions:
            raise KatoSyntaxError(
                f"Function '{name}' is already defined",
                name_token.line, name_token.column,
                self.source_code
            )
        
        self.expect("LPAREN")
        
        params = []
        while self.current_token() and self.current_token().type != "RPAREN":
            param_token = self.expect("IDENTIFIER")
            params.append(param_token.value)
            
            if self.current_token() and self.current_token().type == "COMMA":
                self.advance()
        
        self.expect("RPAREN")
        
        if name == "main" and len(params) > 0:
            raise KatoSyntaxError(
                f"Function 'main' must not have any arguments",
                name_token.line, name_token.column,
                self.source_code
            )
        
        self.defined_functions.add(name)
        
        self.defined_variables = set()
        for param in params:
            self.defined_variables.add(param)
        
        lbrace_token = self.expect("LBRACE")
        
        body = []
        while self.current_token() and self.current_token().type != "RBRACE":
            if self.current_token().type == "EOF":
                raise KatoSyntaxError(
                    f"Function '{name}' is not closed. Missing closing brace '}}' for function that starts here",
                    lbrace_token.line, lbrace_token.column,
                    self.source_code
                )
            stmt = self.stmt_parser.parse_statement()
            if stmt is not None:
                body.append(stmt)
        
        if self.current_token() is None or self.current_token().type == "EOF":
            raise KatoSyntaxError(
                f"Function '{name}' is not closed. Missing closing brace '}}' for function that starts here",
                lbrace_token.line, lbrace_token.column,
                self.source_code
            )
        
        self.expect("RBRACE")
        
        return_type = self.infer_return_type(body)
        self.function_return_types[name] = return_type
        
        return Function(name, params, body)
    
    def infer_return_type(self, body):
        from .ast import ReturnStatement, StringLiteral, CharLiteral, FloatLiteral, Identifier
        
        has_return_with_value = False
        
        for statement in body:
            if isinstance(statement, ReturnStatement):
                if statement.value:
                    has_return_with_value = True
                    if isinstance(statement.value, StringLiteral):
                        return "string"
                    elif isinstance(statement.value, CharLiteral):
                        return "char"
                    elif isinstance(statement.value, FloatLiteral):
                        return "float"
                    elif isinstance(statement.value, Identifier):
                        return "int"
        
        return "void" if not has_return_with_value else "int"
