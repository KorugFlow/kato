from .ast.expressions import (
    StringLiteral, NumberLiteral, FloatLiteral, CharLiteral,
    Identifier, BinaryOp, InptCall, ArrayAccess, FunctionCall
)
from .errors import KatoSyntaxError


class ExpressionParser:
    def __init__(self, parser):
        self.parser = parser
    
    def parse_expression(self):
        return self.parse_additive()
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        
        while self.parser.current_token() and self.parser.current_token().type in ["PLUS", "MINUS"]:
            op_token = self.parser.current_token()
            operator = op_token.value
            self.parser.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, operator, right)
        
        return left
    
    def parse_multiplicative(self):
        left = self.parse_primary()
        
        while self.parser.current_token() and self.parser.current_token().type in ["ASTERISK", "SLASH", "DOUBLE_SLASH", "PERCENT"]:
            if self.parser.current_token().type == "ASTERISK":
                next_token = self.parser.peek_token()
                if next_token and next_token.type == "IDENTIFIER":
                    peek_after = self.parser.peek_token(2)
                    if peek_after and peek_after.type == "ASTERISK":
                        break
            
            op_token = self.parser.current_token()
            if op_token.type == "DOUBLE_SLASH":
                operator = "//"
            else:
                operator = op_token.value
            self.parser.advance()
            right = self.parse_primary()
            left = BinaryOp(left, operator, right)
        
        return left
    
    def parse_primary(self):
        token = self.parser.current_token()
        
        if token.type == "STRING":
            self.parser.advance()
            return StringLiteral(token.value)
        elif token.type == "CHAR":
            self.parser.advance()
            return CharLiteral(token.value)
        elif token.type == "NUMBER":
            self.parser.advance()
            return NumberLiteral(token.value)
        elif token.type == "FLOAT_NUMBER":
            self.parser.advance()
            return FloatLiteral(token.value)
        elif token.type == "IDENTIFIER":
            name = token.value
            self.parser.advance()
            
            if self.parser.current_token() and self.parser.current_token().type == "LPAREN":
                if name not in self.parser.defined_functions and name not in self.parser.builtin_functions:
                    raise KatoSyntaxError(
                        f"Unknown function '{name}'",
                        token.line, token.column,
                        self.parser.source_code
                    )
                self.parser.advance()
                arguments = []
                while self.parser.current_token() and self.parser.current_token().type != "RPAREN":
                    arg_token = self.parser.current_token()
                    arg = self.parse_expression()
                    
                    if isinstance(arg, Identifier):
                        if arg.name not in self.parser.defined_variables:
                            raise KatoSyntaxError(
                                f"Undefined variable '{arg.name}'. If you meant a string, use double quotes: \"{arg.name}\". If you meant a char, use single quotes: '{arg.name}'",
                                arg_token.line, arg_token.column,
                                self.parser.source_code
                            )
                    
                    arguments.append(arg)
                    if self.parser.current_token() and self.parser.current_token().type == "COMMA":
                        self.parser.advance()
                self.parser.expect("RPAREN")
                return FunctionCall(name, arguments)
            elif self.parser.current_token() and self.parser.current_token().type == "LBRACKET":
                self.parser.advance()
                index = self.parse_expression()
                self.parser.expect("RBRACKET")
                return ArrayAccess(name, index)
            
            return Identifier(name)
        elif token.type in ["INT", "FLOAT", "CHAR", "STRING_TYPE"]:
            raise KatoSyntaxError(
                f"Cannot use type '{token.value}' as a variable. Did you mean to use a variable name?",
                token.line, token.column,
                self.parser.source_code
            )
        elif token.type == "ASTERISK":
            self.parser.advance()
            var_token = self.parser.expect("IDENTIFIER")
            
            if self.parser.current_token() and self.parser.current_token().type == "LBRACKET":
                name = var_token.value
                self.parser.advance()
                index = self.parse_expression()
                self.parser.expect("RBRACKET")
                self.parser.expect("ASTERISK")
                return ArrayAccess(name, index)
            
            self.parser.expect("ASTERISK")
            return Identifier(var_token.value)
        elif token.type == "LPAREN":
            self.parser.advance()
            expr = self.parse_expression()
            self.parser.expect("RPAREN")
            return expr
        elif token.type == "INPT":
            self.parser.advance()
            self.parser.expect("LPAREN")
            prompt = self.parse_expression()
            self.parser.expect("RPAREN")
            return InptCall(prompt)
        else:
            raise KatoSyntaxError(
                f"Expected expression (string, number, or identifier), got '{token.value}'",
                token.line, token.column,
                self.parser.source_code
            )
    
    def parse_comparison(self):
        left_token = self.parser.current_token()
        
        if left_token and left_token.type in ["INT", "FLOAT", "CHAR", "STRING_TYPE"]:
            raise KatoSyntaxError(
                f"Cannot use type '{left_token.value}' as a variable. Did you mean to use a variable name?",
                left_token.line, left_token.column,
                self.parser.source_code
            )
        
        left = self.parse_expression()
        
        token = self.parser.current_token()
        if token and token.type in ["EQUAL_EQUAL", "NOT_EQUAL", "LESS", "GREATER", "LESS_EQUAL", "GREATER_EQUAL"]:
            operator = token.value
            self.parser.advance()
            right = self.parse_expression()
            
            if isinstance(left, Identifier) and isinstance(right, StringLiteral):
                raise KatoSyntaxError(
                    f"Cannot compare char with string. Use single quotes for char: '{right.value}' instead of \"{right.value}\"",
                    token.line, token.column,
                    self.parser.source_code
                )
            elif isinstance(left, StringLiteral) and isinstance(right, Identifier):
                raise KatoSyntaxError(
                    f"Cannot compare string with char. Use single quotes for char: '{left.value}' instead of \"{left.value}\"",
                    token.line, token.column,
                    self.parser.source_code
                )
            
            return BinaryOp(left, operator, right)
        
        return left
