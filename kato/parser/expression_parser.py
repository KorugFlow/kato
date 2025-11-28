from .ast.expressions import (
    StringLiteral, NumberLiteral, FloatLiteral, CharLiteral,
    Identifier, BinaryOp, InptCall, ArrayAccess
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
            
            if self.parser.current_token() and self.parser.current_token().type == "LBRACKET":
                self.parser.advance()
                index = self.parse_expression()
                self.parser.expect("RBRACKET")
                return ArrayAccess(name, index)
            
            return Identifier(name)
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
