from ..ast import (
    CVarDeclaration, CArrayDeclaration, CAssignment,
    CIfStatement, CWhileStatement, CForStatement,
    CReturnStatement, CExpressionStatement, CFunctionCall
)
from ..errors import C2KatoError


class CStatementParser:
    def __init__(self, parser, expr_parser):
        self.parser = parser
        self.expr_parser = expr_parser
    
    def parse_statement(self):
        token = self.parser.current_token()
        
        if token.type in ["INT_TYPE", "FLOAT_TYPE", "CHAR_TYPE"]:
            return self.parse_declaration()
        elif token.type == "IF":
            return self.parse_if_statement()
        elif token.type == "WHILE":
            return self.parse_while_statement()
        elif token.type == "FOR":
            return self.parse_for_statement()
        elif token.type == "RETURN":
            return self.parse_return_statement()
        elif token.type == "PRINTF":
            return self.parse_printf_statement()
        elif token.type == "IDENTIFIER":
            return self.parse_assignment_or_expression()
        else:
            self.parser.advance()
            return None
    
    def parse_printf_statement(self):
        self.parser.expect("PRINTF")
        self.parser.expect("LPAREN")
        
        arguments = []
        while self.parser.current_token() and self.parser.current_token().type != "RPAREN":
            arguments.append(self.expr_parser.parse_expression())
            
            if self.parser.current_token() and self.parser.current_token().type == "COMMA":
                self.parser.advance()
        
        self.parser.expect("RPAREN")
        self.parser.expect("SEMICOLON")
        
        from ..ast import CFunctionCall
        return CFunctionCall("printf", arguments)
    
    def parse_declaration(self):
        var_type = self.parser.current_token().value
        self.parser.advance()
        
        if self.parser.current_token() and self.parser.current_token().type == "ASTERISK":
            var_type += "*"
            self.parser.advance()
        
        name_token = self.parser.expect("IDENTIFIER")
        name = name_token.value
        
        if self.parser.current_token() and self.parser.current_token().type == "LBRACKET":
            self.parser.advance()
            
            size = None
            if self.parser.current_token() and self.parser.current_token().type == "NUMBER":
                size = self.parser.current_token().value
                self.parser.advance()
            
            self.parser.expect("RBRACKET")
            
            values = None
            if self.parser.current_token() and self.parser.current_token().type == "EQUALS":
                self.parser.advance()
                self.parser.expect("LBRACE")
                
                values = []
                while self.parser.current_token() and self.parser.current_token().type != "RBRACE":
                    values.append(self.expr_parser.parse_expression())
                    
                    if self.parser.current_token() and self.parser.current_token().type == "COMMA":
                        self.parser.advance()
                
                self.parser.expect("RBRACE")
            
            self.parser.expect("SEMICOLON")
            return CArrayDeclaration(var_type, name, size, values)
        else:
            value = None
            if self.parser.current_token() and self.parser.current_token().type == "EQUALS":
                self.parser.advance()
                value = self.expr_parser.parse_expression()
            
            self.parser.expect("SEMICOLON")
            return CVarDeclaration(var_type, name, value)
    
    def parse_if_statement(self):
        self.parser.expect("IF")
        self.parser.expect("LPAREN")
        
        condition = self.expr_parser.parse_expression()
        
        self.parser.expect("RPAREN")
        
        if self.parser.current_token() and self.parser.current_token().type == "LBRACE":
            self.parser.advance()
            if_body = []
            while self.parser.current_token() and self.parser.current_token().type != "RBRACE":
                if_body.append(self.parse_statement())
            self.parser.expect("RBRACE")
        else:
            if_body = [self.parse_statement()]
        
        else_body = None
        if self.parser.current_token() and self.parser.current_token().type == "ELSE":
            self.parser.advance()
            
            if self.parser.current_token() and self.parser.current_token().type == "LBRACE":
                self.parser.advance()
                else_body = []
                while self.parser.current_token() and self.parser.current_token().type != "RBRACE":
                    else_body.append(self.parse_statement())
                self.parser.expect("RBRACE")
            else:
                else_body = [self.parse_statement()]
        
        return CIfStatement(condition, if_body, else_body)
    
    def parse_while_statement(self):
        self.parser.expect("WHILE")
        self.parser.expect("LPAREN")
        
        condition = self.expr_parser.parse_expression()
        
        self.parser.expect("RPAREN")
        self.parser.expect("LBRACE")
        
        body = []
        while self.parser.current_token() and self.parser.current_token().type != "RBRACE":
            body.append(self.parse_statement())
        
        self.parser.expect("RBRACE")
        
        return CWhileStatement(condition, body)
    
    def parse_for_statement(self):
        self.parser.expect("FOR")
        self.parser.expect("LPAREN")
        
        init = self.parse_statement()
        condition = self.expr_parser.parse_expression()
        self.parser.expect("SEMICOLON")
        
        increment = self.expr_parser.parse_expression()
        
        self.parser.expect("RPAREN")
        self.parser.expect("LBRACE")
        
        body = []
        while self.parser.current_token() and self.parser.current_token().type != "RBRACE":
            body.append(self.parse_statement())
        
        self.parser.expect("RBRACE")
        
        return CForStatement(init, condition, increment, body)
    
    def parse_return_statement(self):
        self.parser.expect("RETURN")
        
        value = None
        if self.parser.current_token() and self.parser.current_token().type != "SEMICOLON":
            value = self.expr_parser.parse_expression()
        
        self.parser.expect("SEMICOLON")
        
        return CReturnStatement(value)
    
    def parse_assignment_or_expression(self):
        name = self.parser.current_token().value
        self.parser.advance()
        
        if self.parser.current_token() and self.parser.current_token().type == "LBRACKET":
            self.parser.advance()
            index = self.expr_parser.parse_expression()
            self.parser.expect("RBRACKET")
            
            if self.parser.current_token() and self.parser.current_token().type == "EQUALS":
                self.parser.advance()
                value = self.expr_parser.parse_expression()
                self.parser.expect("SEMICOLON")
                return CAssignment(f"{name}[{index}]", value)
        
        if self.parser.current_token() and self.parser.current_token().type == "EQUALS":
            self.parser.advance()
            value = self.expr_parser.parse_expression()
            self.parser.expect("SEMICOLON")
            return CAssignment(name, value)
        elif self.parser.current_token() and self.parser.current_token().type in ["PLUS_PLUS", "MINUS_MINUS"]:
            op = self.parser.current_token().value
            self.parser.advance()
            
            if self.parser.current_token() and self.parser.current_token().type == "SEMICOLON":
                self.parser.expect("SEMICOLON")
                return CExpressionStatement(f"{name}{op}")
            else:
                return CExpressionStatement(f"{name}{op}")
        elif self.parser.current_token() and self.parser.current_token().type == "LPAREN":
            self.parser.advance()
            
            arguments = []
            while self.parser.current_token() and self.parser.current_token().type != "RPAREN":
                arguments.append(self.expr_parser.parse_expression())
                if self.parser.current_token() and self.parser.current_token().type == "COMMA":
                    self.parser.advance()
            
            self.parser.expect("RPAREN")
            
            if self.parser.current_token() and self.parser.current_token().type == "SEMICOLON":
                self.parser.expect("SEMICOLON")
            
            return CFunctionCall(name, arguments)
        else:
            if self.parser.current_token() and self.parser.current_token().type == "SEMICOLON":
                self.parser.expect("SEMICOLON")
            return CExpressionStatement(name)
