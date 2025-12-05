from .ast.expressions import (
    StringLiteral, NumberLiteral, FloatLiteral, CharLiteral,
    Identifier, BinaryOp, InptCall, ArrayAccess, FunctionCall,
    ConvertExpression, FindCall
)
from .errors import KatoSyntaxError


class ExpressionParser:
    def __init__(self, parser):
        self.parser = parser
    
    def parse_expression(self):
        return self.parse_logical_or()
    
    def parse_logical_or(self):
        left = self.parse_logical_and()
        
        while self.parser.current_token() and self.parser.current_token().type == "OR":
            op_token = self.parser.current_token()
            operator = op_token.value
            self.parser.advance()
            right = self.parse_logical_and()
            left = BinaryOp(left, operator, right)
        
        return left
    
    def parse_logical_and(self):
        left = self.parse_comparison_expr()
        
        while self.parser.current_token() and self.parser.current_token().type == "AND":
            op_token = self.parser.current_token()
            operator = op_token.value
            self.parser.advance()
            right = self.parse_comparison_expr()
            left = BinaryOp(left, operator, right)
        
        return left
    
    def parse_comparison_expr(self):
        left = self.parse_additive()
        
        token = self.parser.current_token()
        if token and token.type in ["EQUAL_EQUAL", "NOT_EQUAL", "LESS", "GREATER", "LESS_EQUAL", "GREATER_EQUAL"]:
            operator = token.value
            self.parser.advance()
            right = self.parse_additive()
            return BinaryOp(left, operator, right)
        
        return left
    
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
                
                if name in self.parser.function_return_types:
                    return_type = self.parser.function_return_types[name]
                    if return_type == "void":
                        raise KatoSyntaxError(
                            f"Cannot use void function '{name}' in expression",
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
                
                if name == "random":
                    if len(arguments) != 2:
                        raise KatoSyntaxError(
                            f"Function 'random' requires exactly 2 arguments (min, max), but got {len(arguments)}",
                            token.line, token.column,
                            self.parser.source_code
                        )
                
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
        elif token.type == "MINUS":
            self.parser.advance()
            next_token = self.parser.current_token()
            if next_token.type == "NUMBER":
                self.parser.advance()
                return NumberLiteral(-next_token.value)
            elif next_token.type == "FLOAT_NUMBER":
                self.parser.advance()
                return FloatLiteral(-next_token.value)
            else:
                raise KatoSyntaxError(
                    f"Expected number after '-', got '{next_token.value}'",
                    next_token.line, next_token.column,
                    self.parser.source_code
                )
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
        elif token.type == "FIND":
            self.parser.advance()
            self.parser.expect("LPAREN")
            target_token = self.parser.current_token()
            target = self.parse_expression()
            
            if isinstance(target, Identifier) and target.name not in self.parser.defined_variables:
                raise KatoSyntaxError(
                    f"Undefined variable '{target.name}' in find()",
                    target_token.line, target_token.column,
                    self.parser.source_code
                )
            
            self.parser.expect("COMMA")
            pattern = self.parse_expression()
            self.parser.expect("RPAREN")
            return FindCall(target, pattern)
        elif token.type == "CONVERT":
            self.parser.advance()
            expr = self.parse_primary()
            self.parser.expect("GREATER")
            type_token = self.parser.current_token()
            if type_token.type not in ["INT", "FLOAT", "CHAR", "STRING_TYPE"]:
                raise KatoSyntaxError(
                    f"Expected type (int, float, char, string), got '{type_token.value}'",
                    type_token.line, type_token.column,
                    self.parser.source_code
                )
            target_type = type_token.value
            self.parser.advance()
            return ConvertExpression(expr, target_type)
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
        
        return self.parse_expression()
