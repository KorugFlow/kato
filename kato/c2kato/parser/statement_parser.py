from ..ast import (
    CVarDeclaration, CArrayDeclaration, CAssignment,
    CIfStatement, CWhileStatement, CForStatement,
    CReturnStatement, CExpressionStatement, CFunctionCall,
    CSwitchStatement, CCaseClause
)
from ..errors import C2KatoError


class CStatementParser:
    def __init__(self, parser, expr_parser):
        self.parser = parser
        self.expr_parser = expr_parser
    
    def parse_statement(self):
        token = self.parser.current_token()
        
        if not token:
            raise C2KatoError("Unexpected end of file while parsing statement")
        
        if token.type in ["INT_TYPE", "FLOAT_TYPE", "CHAR_TYPE"]:
            return self.parse_declaration()
        elif token.type == "IF":
            return self.parse_if_statement()
        elif token.type == "WHILE":
            return self.parse_while_statement()
        elif token.type == "FOR":
            return self.parse_for_statement()
        elif token.type == "SWITCH":
            return self.parse_switch_statement()
        elif token.type == "RETURN":
            return self.parse_return_statement()
        elif token.type == "PRINTF":
            return self.parse_printf_statement()
        elif token.type == "SCANF":
            return self.parse_scanf_statement()
        elif token.type == "IDENTIFIER":
            similar = self.parser._find_similar_keyword(token.value)
            if similar:
                raise C2KatoError(f"Unknown identifier '{token.value}' (did you mean '{similar}'?)", token.line, token.column)
            return self.parse_assignment_or_expression()
        elif token.type in ["RBRACE", "SEMICOLON"]:
            return None
        else:
            raise C2KatoError(f"Unexpected token in statement: {token.type}", token.line, token.column)
    
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
    
    def parse_scanf_statement(self):
        self.parser.expect("SCANF")
        self.parser.expect("LPAREN")
        
        arguments = []
        while self.parser.current_token() and self.parser.current_token().type != "RPAREN":
            arguments.append(self.expr_parser.parse_expression())
            
            if self.parser.current_token() and self.parser.current_token().type == "COMMA":
                self.parser.advance()
        
        self.parser.expect("RPAREN")
        self.parser.expect("SEMICOLON")
        
        from ..ast import CFunctionCall
        return CFunctionCall("scanf", arguments)
    
    def parse_declaration(self):
        type_token = self.parser.current_token()
        if not type_token:
            raise C2KatoError("Unexpected end of file while parsing declaration")
        
        var_type = type_token.value
        type_line, type_col = type_token.line, type_token.column
        self.parser.advance()
        
        if self.parser.current_token() and self.parser.current_token().type == "ASTERISK":
            var_type += "*"
            self.parser.advance()
        
        if var_type not in self.parser.VALID_TYPES:
            raise C2KatoError(f"Invalid type '{var_type}'", type_line, type_col)
        
        declarations = []
        declared_names = set()
        
        while True:
            if not self.parser.current_token() or self.parser.current_token().type != "IDENTIFIER":
                token = self.parser.current_token()
                raise C2KatoError(f"Expected identifier after type '{var_type}'", token.line if token else None, token.column if token else None)
            
            name_token = self.parser.expect("IDENTIFIER")
            name = name_token.value
            
            if name in declared_names:
                raise C2KatoError(f"Redeclaration of variable '{name}' in the same statement", name_token.line, name_token.column)
            declared_names.add(name)
            self.parser.declared_variables.add(name)
            
            if self.parser.current_token() and self.parser.current_token().type == "LBRACKET":
                self.parser.advance()
                
                size = None
                if self.parser.current_token() and self.parser.current_token().type == "NUMBER":
                    size_token = self.parser.current_token()
                    size = size_token.value
                    if int(size) <= 0:
                        raise C2KatoError(f"Array size must be positive, got {size}", size_token.line, size_token.column)
                    self.parser.advance()
                elif self.parser.current_token() and self.parser.current_token().type != "RBRACKET":
                    token = self.parser.current_token()
                    raise C2KatoError(f"Expected array size or ']', got '{token.type}'", token.line, token.column)
                
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
                
                declarations.append(CArrayDeclaration(var_type, name, size, values))
            else:
                value = None
                if self.parser.current_token() and self.parser.current_token().type == "EQUALS":
                    self.parser.advance()
                    value = self.expr_parser.parse_expression()
                
                declarations.append(CVarDeclaration(var_type, name, value))
            
            if self.parser.current_token() and self.parser.current_token().type == "COMMA":
                self.parser.advance()
            else:
                break
        
        self.parser.expect("SEMICOLON")
        
        if len(declarations) == 1:
            return declarations[0]
        else:
            from ..ast import CMultiDeclaration
            return CMultiDeclaration(declarations)
    
    def parse_if_statement(self):
        self.parser.expect("IF")
        self.parser.expect("LPAREN")
        
        if not self.parser.current_token():
            raise C2KatoError("Expected condition in if statement")
        
        condition_start = self.parser.pos
        condition = self.expr_parser.parse_expression()
        
        if self.parser.pos > condition_start:
            check_token = self.parser.tokens[condition_start]
            if check_token.type == "IDENTIFIER" and self.parser.current_token() and self.parser.current_token().type == "EQUALS":
                var_name = check_token.value
                raise C2KatoError(f"Assignment in condition (use '==' for comparison, not '=')", check_token.line, check_token.column)
        
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
        
        if not self.parser.current_token():
            raise C2KatoError("Expected condition in while statement")
        
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
        
        if not self.parser.current_token():
            raise C2KatoError("Expected initialization in for statement")
        
        init = self.parse_statement()
        
        if not self.parser.current_token():
            raise C2KatoError("Expected condition in for statement")
        
        condition = self.expr_parser.parse_expression()
        self.parser.expect("SEMICOLON")
        
        if not self.parser.current_token():
            raise C2KatoError("Expected increment in for statement")
        
        increment = self.expr_parser.parse_expression()
        
        self.parser.expect("RPAREN")
        self.parser.expect("LBRACE")
        
        body = []
        while self.parser.current_token() and self.parser.current_token().type != "RBRACE":
            body.append(self.parse_statement())
        
        self.parser.expect("RBRACE")
        
        return CForStatement(init, condition, increment, body)
    
    def parse_return_statement(self):
        return_token = self.parser.current_token()
        self.parser.expect("RETURN")
        
        value = None
        if self.parser.current_token() and self.parser.current_token().type != "SEMICOLON":
            value = self.expr_parser.parse_expression()
        
        if self.parser.current_function:
            func_return_type = self.parser.current_function["return_type"]
            if func_return_type == "void" and value is not None:
                raise C2KatoError(f"Void function '{self.parser.current_function['name']}' should not return a value", return_token.line, return_token.column)
            elif func_return_type != "void" and value is None:
                raise C2KatoError(f"Non-void function '{self.parser.current_function['name']}' must return a value", return_token.line, return_token.column)
        
        self.parser.expect("SEMICOLON")
        
        return CReturnStatement(value)
    
    def parse_assignment_or_expression(self):
        name_token = self.parser.current_token()
        name = name_token.value
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
            if not self.parser.current_token() or self.parser.current_token().type == "SEMICOLON":
                token = self.parser.current_token()
                raise C2KatoError(f"Expected expression after '='", token.line if token else None, token.column if token else None)
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
                    if self.parser.current_token() and self.parser.current_token().type == "RPAREN":
                        token = self.parser.current_token()
                        raise C2KatoError("Expected argument after ','" , token.line, token.column)
            
            self.parser.expect("RPAREN")
            
            if not self.parser.current_token() or self.parser.current_token().type != "SEMICOLON":
                token = self.parser.current_token()
                raise C2KatoError(f"Expected ';' after function call", token.line if token else None, token.column if token else None)
            
            self.parser.expect("SEMICOLON")
            
            return CFunctionCall(name, arguments)
        else:
            token = self.parser.current_token()
            raise C2KatoError(f"Expected '=', '(', '++', or '--' after identifier '{name}'", name_token.line, name_token.column)
    
    def parse_switch_statement(self):
        self.parser.expect("SWITCH")
        self.parser.expect("LPAREN")
        
        if not self.parser.current_token():
            raise C2KatoError("Expected expression in switch statement")
        
        expression = self.expr_parser.parse_expression()
        
        self.parser.expect("RPAREN")
        self.parser.expect("LBRACE")
        
        cases = []
        default_body = None
        
        while self.parser.current_token() and self.parser.current_token().type != "RBRACE":
            if self.parser.current_token().type == "CASE":
                self.parser.advance()
                
                case_value = self.expr_parser.parse_expression()
                self.parser.expect("COLON")
                
                case_body = []
                while self.parser.current_token() and self.parser.current_token().type not in ["CASE", "DEFAULT", "RBRACE"]:
                    if self.parser.current_token().type == "BREAK":
                        self.parser.advance()
                        self.parser.expect("SEMICOLON")
                        break
                    else:
                        stmt = self.parse_statement()
                        if stmt:
                            case_body.append(stmt)
                
                cases.append(CCaseClause(case_value, case_body))
                
            elif self.parser.current_token().type == "DEFAULT":
                self.parser.advance()
                self.parser.expect("COLON")
                
                default_body = []
                while self.parser.current_token() and self.parser.current_token().type != "RBRACE":
                    if self.parser.current_token().type == "BREAK":
                        self.parser.advance()
                        self.parser.expect("SEMICOLON")
                        break
                    else:
                        stmt = self.parse_statement()
                        if stmt:
                            default_body.append(stmt)
            else:
                self.parser.advance()
        
        self.parser.expect("RBRACE")
        
        return CSwitchStatement(expression, cases, default_body)
