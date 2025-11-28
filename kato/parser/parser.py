from lexer.lexer import Token


class KatoSyntaxError(Exception):
    def __init__(self, message, line, column, source_code=None):
        self.message = message
        self.line = line
        self.column = column
        self.source_code = source_code
        super().__init__(self.format_error())
    
    def format_error(self):
        # ANSI цвета
        RED = '\033[91m'
        YELLOW = '\033[93m'
        CYAN = '\033[96m'
        GRAY = '\033[90m'
        BOLD = '\033[1m'
        RESET = '\033[0m'
        
        error_msg = f"\n{RED}{'='*60}{RESET}\n"
        error_msg += f"{BOLD}{RED}  Kato Syntax Error{RESET}\n"
        error_msg += f"{RED}{'='*60}{RESET}\n\n"
        error_msg += f"{BOLD}  {self.message}{RESET}\n"
        error_msg += f"{GRAY}  at line {self.line}, column {self.column}{RESET}\n\n"
        
        if self.source_code:
            lines = self.source_code.split('\n')
            if 0 < self.line <= len(lines):
                error_line = lines[self.line - 1]
                
                error_msg += f"{CYAN}{'─'*60}{RESET}\n"
                
                if self.line > 1:
                    error_msg += f"{GRAY}  {self.line - 1:4d} | {lines[self.line - 2]}{RESET}\n"
                
                error_msg += f"{YELLOW}  {self.line:4d} | {error_line}{RESET}\n"
                error_msg += f"{RED}       | {' ' * (self.column - 1)}^{RESET}\n"
                
                if self.line < len(lines):
                    error_msg += f"{GRAY}  {self.line + 1:4d} | {lines[self.line]}{RESET}\n"
                
                error_msg += f"{CYAN}{'─'*60}{RESET}\n"
        
        return error_msg


class ASTNode:
    pass


class Program(ASTNode):
    def __init__(self, functions):
        self.functions = functions


class Function(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class PrintStatement(ASTNode):
    def __init__(self, value):
        self.value = value


class ReturnStatement(ASTNode):
    def __init__(self, value):
        self.value = value


class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class NumberLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class Parser:
    def __init__(self, tokens, source_code=None):
        self.tokens = tokens
        self.pos = 0
        self.source_code = source_code
    
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
        
        while self.current_token() and self.current_token().type != "EOF":
            if self.current_token().type == "FUNCTION":
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
        
        return Program(functions)
    
    def parse_function(self):
        self.expect("FUNCTION")
        
        name_token = self.expect("IDENTIFIER")
        name = name_token.value
        
        self.expect("LPAREN")
        
        params = []
        while self.current_token() and self.current_token().type != "RPAREN":
            param_token = self.expect("IDENTIFIER")
            params.append(param_token.value)
        
        self.expect("RPAREN")
        self.expect("LBRACE")
        
        body = []
        while self.current_token() and self.current_token().type != "RBRACE":
            body.append(self.parse_statement())
        
        self.expect("RBRACE")
        
        return Function(name, params, body)
    
    def parse_statement(self):
        token = self.current_token()
        
        if token.type == "PRINT":
            return self.parse_print_statement()
        elif token.type == "RETURN":
            return self.parse_return_statement()
        else:
            raise KatoSyntaxError(
                f"Unknown statement type '{token.value}'",
                token.line, token.column,
                self.source_code
            )
    
    def parse_print_statement(self):
        print_token = self.current_token()
        self.expect("PRINT")
        self.expect("LPAREN")
        
        value = self.parse_expression()
        
        self.expect("RPAREN")
        
        semicolon_token = self.current_token()
        if semicolon_token is None or semicolon_token.type != "SEMICOLON":
            raise KatoSyntaxError(
                "Missing semicolon ';' after print statement",
                print_token.line, print_token.column + len("print"),
                self.source_code
            )
        self.expect("SEMICOLON")
        
        return PrintStatement(value)
    
    def parse_return_statement(self):
        return_token = self.current_token()
        self.expect("RETURN")
        
        value = self.parse_expression()
        
        semicolon_token = self.current_token()
        if semicolon_token is None or semicolon_token.type != "SEMICOLON":
            raise KatoSyntaxError(
                "Missing semicolon ';' after return statement",
                return_token.line, return_token.column + len("return"),
                self.source_code
            )
        self.expect("SEMICOLON")
        
        return ReturnStatement(value)
    
    def parse_expression(self):
        token = self.current_token()
        
        if token.type == "STRING":
            self.advance()
            return StringLiteral(token.value)
        elif token.type == "NUMBER":
            self.advance()
            return NumberLiteral(token.value)
        else:
            raise KatoSyntaxError(
                f"Expected expression (string or number), got '{token.value}'",
                token.line, token.column,
                self.source_code
            )

