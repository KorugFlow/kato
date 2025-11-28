from .ast.statements import (
    PrintStatement, ReturnStatement, VarDeclaration,
    CallStatement, IfStatement, Assignment,
    WhileStatement, IncrementStatement, DecrementStatement
)
from .errors import KatoSyntaxError


class StatementParser:
    def __init__(self, parser, expr_parser):
        self.parser = parser
        self.expr_parser = expr_parser
    
    def parse_statement(self):
        token = self.parser.current_token()
        
        if token.type == "PRINT":
            return self.parse_print_statement()
        elif token.type == "RETURN":
            return self.parse_return_statement()
        elif token.type == "VAR":
            return self.parse_var_declaration()
        elif token.type == "CALL":
            return self.parse_call_statement()
        elif token.type == "IF":
            return self.parse_if_statement()
        elif token.type == "WHILE":
            return self.parse_while_statement()
        elif token.type == "IDENTIFIER":
            next_token = self.parser.peek_token()
            if next_token and next_token.type == "PLUS_PLUS":
                return self.parse_increment()
            elif next_token and next_token.type == "MINUS_MINUS":
                return self.parse_decrement()
            else:
                return self.parse_assignment()
        else:
            raise KatoSyntaxError(
                f"Unknown statement type '{token.value}'",
                token.line, token.column,
                self.parser.source_code
            )
    
    def parse_print_statement(self):
        print_token = self.parser.current_token()
        self.parser.expect("PRINT")
        self.parser.expect("LPAREN")
        
        values = []
        while self.parser.current_token() and self.parser.current_token().type != "RPAREN":
            values.append(self.expr_parser.parse_expression())
            
            if self.parser.current_token() and self.parser.current_token().type != "RPAREN":
                if self.parser.current_token().type in ["STRING", "NUMBER", "FLOAT_NUMBER", "IDENTIFIER", "ASTERISK", "LPAREN"]:
                    continue
                else:
                    break
        
        self.parser.expect("RPAREN")
        
        semicolon_token = self.parser.current_token()
        if semicolon_token is None or semicolon_token.type != "SEMICOLON":
            raise KatoSyntaxError(
                "Missing semicolon ';' after print statement",
                print_token.line, print_token.column + len("print"),
                self.parser.source_code
            )
        self.parser.expect("SEMICOLON")
        
        return PrintStatement(values)
    
    def parse_return_statement(self):
        return_token = self.parser.current_token()
        self.parser.expect("RETURN")
        
        value = self.expr_parser.parse_expression()
        
        semicolon_token = self.parser.current_token()
        if semicolon_token is None or semicolon_token.type != "SEMICOLON":
            raise KatoSyntaxError(
                "Missing semicolon ';' after return statement",
                return_token.line, return_token.column + len("return"),
                self.parser.source_code
            )
        self.parser.expect("SEMICOLON")
        
        return ReturnStatement(value)
    
    def parse_var_declaration(self):
        var_token = self.parser.current_token()
        self.parser.expect("VAR")
        
        type_token = self.parser.current_token()
        if type_token.type not in ["INT", "FLOAT", "CHAR", "STRING_TYPE"]:
            raise KatoSyntaxError(
                f"Expected variable type (int, float, char, string), got '{type_token.value}'",
                type_token.line, type_token.column,
                self.parser.source_code
            )
        var_type = type_token.value
        self.parser.advance()
        
        name_token = self.parser.expect("IDENTIFIER")
        name = name_token.value
        
        if name in self.parser.defined_variables:
            raise KatoSyntaxError(
                f"Variable '{name}' is already defined",
                name_token.line, name_token.column,
                self.parser.source_code
            )
        
        self.parser.defined_variables.add(name)
        
        self.parser.expect("EQUALS")
        
        value = self.expr_parser.parse_expression()
        
        semicolon_token = self.parser.current_token()
        if semicolon_token is None or semicolon_token.type != "SEMICOLON":
            raise KatoSyntaxError(
                "Missing semicolon ';' after variable declaration",
                var_token.line, var_token.column,
                self.parser.source_code
            )
        self.parser.expect("SEMICOLON")
        
        return VarDeclaration(var_type, name, value)
    
    def parse_call_statement(self):
        call_token = self.parser.current_token()
        self.parser.expect("CALL")
        
        func_name_token = self.parser.expect("IDENTIFIER")
        func_name = func_name_token.value
        
        if func_name not in self.parser.defined_functions and func_name not in self.parser.builtin_functions:
            raise KatoSyntaxError(
                f"Unknown function '{func_name}'",
                func_name_token.line, func_name_token.column,
                self.parser.source_code
            )
        
        lparen_token = self.parser.current_token()
        if lparen_token is None or lparen_token.type != "LPAREN":
            raise KatoSyntaxError(
                f"Function call without arguments (missing parentheses)",
                func_name_token.line, func_name_token.column + len(func_name),
                self.parser.source_code
            )
        self.parser.expect("LPAREN")
        
        arguments = []
        while self.parser.current_token() and self.parser.current_token().type != "RPAREN":
            arguments.append(self.expr_parser.parse_expression())
            
            if self.parser.current_token() and self.parser.current_token().type == "COMMA":
                self.parser.advance()
        
        self.parser.expect("RPAREN")
        
        semicolon_token = self.parser.current_token()
        if semicolon_token is None or semicolon_token.type != "SEMICOLON":
            raise KatoSyntaxError(
                "Missing semicolon ';' after function call",
                call_token.line, call_token.column,
                self.parser.source_code
            )
        self.parser.expect("SEMICOLON")
        
        return CallStatement(func_name, arguments)
    
    def parse_if_statement(self):
        self.parser.expect("IF")
        
        condition = self.expr_parser.parse_comparison()
        
        self.parser.expect("LBRACE")
        if_body = []
        while self.parser.current_token() and self.parser.current_token().type != "RBRACE":
            if_body.append(self.parse_statement())
        self.parser.expect("RBRACE")
        
        elif_parts = []
        while self.parser.current_token() and self.parser.current_token().type == "ELIF":
            self.parser.advance()
            elif_condition = self.expr_parser.parse_comparison()
            self.parser.expect("LBRACE")
            elif_body = []
            while self.parser.current_token() and self.parser.current_token().type != "RBRACE":
                elif_body.append(self.parse_statement())
            self.parser.expect("RBRACE")
            elif_parts.append((elif_condition, elif_body))
        
        else_body = None
        if self.parser.current_token() and self.parser.current_token().type == "ELSE":
            self.parser.advance()
            self.parser.expect("LBRACE")
            else_body = []
            while self.parser.current_token() and self.parser.current_token().type != "RBRACE":
                else_body.append(self.parse_statement())
            self.parser.expect("RBRACE")
        
        return IfStatement(condition, if_body, elif_parts, else_body)
    
    def parse_assignment(self):
        name_token = self.parser.current_token()
        name = name_token.value
        
        if name not in self.parser.defined_variables:
            raise KatoSyntaxError(
                f"Variable '{name}' is not defined",
                name_token.line, name_token.column,
                self.parser.source_code
            )
        
        self.parser.advance()
        
        self.parser.expect("EQUALS")
        
        value = self.expr_parser.parse_expression()
        
        semicolon_token = self.parser.current_token()
        if semicolon_token is None or semicolon_token.type != "SEMICOLON":
            raise KatoSyntaxError(
                "Missing semicolon ';' after assignment",
                name_token.line, name_token.column,
                self.parser.source_code
            )
        self.parser.expect("SEMICOLON")
        
        return Assignment(name, value)

    def parse_while_statement(self):
        self.parser.expect("WHILE")
        self.parser.expect("LPAREN")
        
        condition = self.expr_parser.parse_comparison()
        
        self.parser.expect("RPAREN")
        self.parser.expect("LBRACE")
        
        body = []
        while self.parser.current_token() and self.parser.current_token().type != "RBRACE":
            body.append(self.parse_statement())
        
        self.parser.expect("RBRACE")
        
        return WhileStatement(condition, body)
    
    def parse_increment(self):
        name_token = self.parser.current_token()
        name = name_token.value
        
        if name not in self.parser.defined_variables:
            raise KatoSyntaxError(
                f"Variable '{name}' is not defined",
                name_token.line, name_token.column,
                self.parser.source_code
            )
        
        self.parser.advance()
        self.parser.expect("PLUS_PLUS")
        
        semicolon_token = self.parser.current_token()
        if semicolon_token is None or semicolon_token.type != "SEMICOLON":
            raise KatoSyntaxError(
                "Missing semicolon ';' after increment",
                name_token.line, name_token.column,
                self.parser.source_code
            )
        self.parser.expect("SEMICOLON")
        
        return IncrementStatement(name)
    
    def parse_decrement(self):
        name_token = self.parser.current_token()
        name = name_token.value
        
        if name not in self.parser.defined_variables:
            raise KatoSyntaxError(
                f"Variable '{name}' is not defined",
                name_token.line, name_token.column,
                self.parser.source_code
            )
        
        self.parser.advance()
        self.parser.expect("MINUS_MINUS")
        
        semicolon_token = self.parser.current_token()
        if semicolon_token is None or semicolon_token.type != "SEMICOLON":
            raise KatoSyntaxError(
                "Missing semicolon ';' after decrement",
                name_token.line, name_token.column,
                self.parser.source_code
            )
        self.parser.expect("SEMICOLON")
        
        return DecrementStatement(name)
