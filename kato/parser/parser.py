from lexer.lexer import Token


class KatoSyntaxError(Exception):
    def __init__(self, message, line, column, source_code=None):
        self.message = message
        self.line = line
        self.column = column
        self.source_code = source_code
        super().__init__(self.format_error())
    
    def format_error(self):
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


class VarDeclaration(ASTNode):
    def __init__(self, var_type, name, value):
        self.var_type = var_type
        self.name = name
        self.value = value


class CallStatement(ASTNode):
    def __init__(self, func_name, arguments):
        self.func_name = func_name
        self.arguments = arguments


class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class NumberLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class FloatLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class CharLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name


class BinaryOp(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Parser:
    def __init__(self, tokens, source_code=None):
        self.tokens = tokens
        self.pos = 0
        self.source_code = source_code
        self.defined_functions = set()
        self.builtin_functions = {"print"}
    
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
        elif token.type == "VAR":
            return self.parse_var_declaration()
        elif token.type == "CALL":
            return self.parse_call_statement()
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
        
        values = []
        while self.current_token() and self.current_token().type != "RPAREN":
            values.append(self.parse_expression())
            
            if self.current_token() and self.current_token().type != "RPAREN":
                if self.current_token().type in ["STRING", "NUMBER", "FLOAT_NUMBER", "IDENTIFIER", "ASTERISK", "LPAREN"]:
                    continue
                else:
                    break
        
        self.expect("RPAREN")
        
        semicolon_token = self.current_token()
        if semicolon_token is None or semicolon_token.type != "SEMICOLON":
            raise KatoSyntaxError(
                "Missing semicolon ';' after print statement",
                print_token.line, print_token.column + len("print"),
                self.source_code
            )
        self.expect("SEMICOLON")
        
        return PrintStatement(values)
    
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
        return self.parse_additive()
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        
        while self.current_token() and self.current_token().type in ["PLUS", "MINUS"]:
            op_token = self.current_token()
            operator = op_token.value
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, operator, right)
        
        return left
    
    def parse_multiplicative(self):
        left = self.parse_primary()
        
        while self.current_token() and self.current_token().type in ["ASTERISK", "SLASH", "DOUBLE_SLASH", "PERCENT"]:
            if self.current_token().type == "ASTERISK":
                next_token = self.peek_token()
                if next_token and next_token.type == "IDENTIFIER":
                    peek_after = self.peek_token(2)
                    if peek_after and peek_after.type == "ASTERISK":
                        break
            
            op_token = self.current_token()
            if op_token.type == "DOUBLE_SLASH":
                operator = "//"
            else:
                operator = op_token.value
            self.advance()
            right = self.parse_primary()
            left = BinaryOp(left, operator, right)
        
        return left
    
    def parse_primary(self):
        token = self.current_token()
        
        if token.type == "STRING":
            self.advance()
            return StringLiteral(token.value)
        elif token.type == "NUMBER":
            self.advance()
            return NumberLiteral(token.value)
        elif token.type == "FLOAT_NUMBER":
            self.advance()
            return FloatLiteral(token.value)
        elif token.type == "IDENTIFIER":
            self.advance()
            return Identifier(token.value)
        elif token.type == "ASTERISK":
            self.advance()
            var_token = self.expect("IDENTIFIER")
            self.expect("ASTERISK")
            return Identifier(var_token.value)
        elif token.type == "LPAREN":
            self.advance()
            expr = self.parse_expression()
            self.expect("RPAREN")
            return expr
        else:
            raise KatoSyntaxError(
                f"Expected expression (string, number, or identifier), got '{token.value}'",
                token.line, token.column,
                self.source_code
            )
    
    def parse_var_declaration(self):
        var_token = self.current_token()
        self.expect("VAR")
        
        type_token = self.current_token()
        if type_token.type not in ["INT", "FLOAT", "CHAR", "STRING_TYPE"]:
            raise KatoSyntaxError(
                f"Expected variable type (int, float, char, string), got '{type_token.value}'",
                type_token.line, type_token.column,
                self.source_code
            )
        var_type = type_token.value
        self.advance()
        
        name_token = self.expect("IDENTIFIER")
        name = name_token.value
        
        self.expect("EQUALS")
        
        value = self.parse_expression()
        
        semicolon_token = self.current_token()
        if semicolon_token is None or semicolon_token.type != "SEMICOLON":
            raise KatoSyntaxError(
                "Missing semicolon ';' after variable declaration",
                var_token.line, var_token.column,
                self.source_code
            )
        self.expect("SEMICOLON")
        
        return VarDeclaration(var_type, name, value)
    
    def parse_call_statement(self):
        call_token = self.current_token()
        self.expect("CALL")
        
        func_name_token = self.expect("IDENTIFIER")
        func_name = func_name_token.value
        
        if func_name not in self.defined_functions and func_name not in self.builtin_functions:
            raise KatoSyntaxError(
                f"Unknown function '{func_name}'",
                func_name_token.line, func_name_token.column,
                self.source_code
            )
        
        lparen_token = self.current_token()
        if lparen_token is None or lparen_token.type != "LPAREN":
            raise KatoSyntaxError(
                f"Function call without arguments (missing parentheses)",
                func_name_token.line, func_name_token.column + len(func_name),
                self.source_code
            )
        self.expect("LPAREN")
        
        arguments = []
        while self.current_token() and self.current_token().type != "RPAREN":
            arguments.append(self.parse_expression())
            
            if self.current_token() and self.current_token().type == "COMMA":
                self.advance()
        
        self.expect("RPAREN")
        
        semicolon_token = self.current_token()
        if semicolon_token is None or semicolon_token.type != "SEMICOLON":
            raise KatoSyntaxError(
                "Missing semicolon ';' after function call",
                call_token.line, call_token.column,
                self.source_code
            )
        self.expect("SEMICOLON")
        
        return CallStatement(func_name, arguments)

