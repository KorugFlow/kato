from ..ast import (
    CIdentifier, CNumber, CString, CChar,
    CBinaryOp, CArrayAccess, CFunctionCall
)
from ..errors import C2KatoError


class CExpressionParser:
    def __init__(self, parser):
        self.parser = parser
    
    def parse_expression(self):
        return self.parse_logical_or()
    
    def parse_logical_or(self):
        left = self.parse_logical_and()
        
        while self.parser.current_token() and self.parser.current_token().type == "OR":
            op = self.parser.current_token().value
            self.parser.advance()
            right = self.parse_logical_and()
            left = CBinaryOp(left, op, right)
        
        return left
    
    def parse_logical_and(self):
        left = self.parse_comparison()
        
        while self.parser.current_token() and self.parser.current_token().type == "AND":
            op = self.parser.current_token().value
            self.parser.advance()
            right = self.parse_comparison()
            left = CBinaryOp(left, op, right)
        
        return left
    
    def parse_comparison(self):
        left = self.parse_additive()
        
        while self.parser.current_token() and self.parser.current_token().type in ["EQUAL_EQUAL", "NOT_EQUAL", "LESS", "GREATER", "LESS_EQUAL", "GREATER_EQUAL"]:
            op = self.parser.current_token().value
            self.parser.advance()
            right = self.parse_additive()
            left = CBinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        
        while self.parser.current_token() and self.parser.current_token().type in ["PLUS", "MINUS"]:
            op = self.parser.current_token().value
            self.parser.advance()
            right = self.parse_multiplicative()
            left = CBinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self):
        left = self.parse_primary()
        
        while self.parser.current_token() and self.parser.current_token().type in ["ASTERISK", "SLASH", "PERCENT"]:
            op = self.parser.current_token().value
            self.parser.advance()
            right = self.parse_primary()
            left = CBinaryOp(left, op, right)
        
        return left
    
    def parse_primary(self):
        token = self.parser.current_token()
        
        if not token:
            raise C2KatoError("Unexpected end of file in expression")
        
        if token.type == "AMPERSAND":
            self.parser.advance()
            expr = self.parse_primary()
            if isinstance(expr, CIdentifier):
                return CIdentifier(f"&{expr.name}")
            return expr
        
        if token.type == "NUMBER":
            self.parser.advance()
            return CNumber(token.value)
        elif token.type == "FLOAT_NUMBER":
            self.parser.advance()
            return CNumber(token.value)
        elif token.type == "STRING":
            self.parser.advance()
            return CString(token.value)
        elif token.type == "CHAR":
            self.parser.advance()
            return CChar(token.value)
        elif token.type == "IDENTIFIER":
            name = token.value
            
            if name not in self.parser.declared_variables and name not in self.parser.declared_functions:
                raise C2KatoError(f"Undeclared variable '{name}'", token.line, token.column)
            
            self.parser.advance()
            
            if self.parser.current_token() and self.parser.current_token().type == "LPAREN":
                return self.parse_function_call(name)
            elif self.parser.current_token() and self.parser.current_token().type == "LBRACKET":
                self.parser.advance()
                index = self.parse_expression()
                self.parser.expect("RBRACKET")
                return CArrayAccess(name, index)
            
            return CIdentifier(name)
        elif token.type == "LPAREN":
            self.parser.advance()
            expr = self.parse_expression()
            self.parser.expect("RPAREN")
            return expr
        else:
            raise C2KatoError(f"Unexpected token in expression: {token.type}", token.line, token.column)
    
    def parse_function_call(self, name):
        self.parser.expect("LPAREN")
        
        arguments = []
        while self.parser.current_token() and self.parser.current_token().type != "RPAREN":
            if not self.parser.current_token():
                raise C2KatoError(f"Unexpected end of file in function call {name}")
            
            arguments.append(self.parse_expression())
            
            if self.parser.current_token() and self.parser.current_token().type == "COMMA":
                self.parser.advance()
            elif self.parser.current_token() and self.parser.current_token().type != "RPAREN":
                token = self.parser.current_token()
                raise C2KatoError(f"Expected ',' or ')' in function call, got {token.type}", token.line, token.column)
        
        self.parser.expect("RPAREN")
        
        return CFunctionCall(name, arguments)
