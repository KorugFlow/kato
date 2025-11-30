from .tokens import tokens as token_map


class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.line}:{self.column})"


class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.keywords = token_map.tokens
    
    def current_char(self):
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset=1):
        peek_pos = self.pos + offset
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]
    
    def advance(self):
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r\n':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            if self.current_char() == '\n':
                self.advance()
    
    def read_string(self):
        start_line = self.line
        start_column = self.column
        quote_char = self.current_char()
        self.advance()
        
        string_value = ""
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\n':
                quote_type = "single quote (')" if quote_char == "'" else "double quote (\")"
                raise SyntaxError(f"Unclosed {quote_type} at line {start_line}, column {start_column}")
            if self.current_char() == '\\':
                self.advance()
                escape_char = self.current_char()
                if escape_char == 'n':
                    string_value += '\n'
                elif escape_char == 't':
                    string_value += '\t'
                elif escape_char == 'r':
                    string_value += '\r'
                elif escape_char == '\\':
                    string_value += '\\'
                elif escape_char == quote_char:
                    string_value += quote_char
                else:
                    string_value += escape_char
                self.advance()
            else:
                string_value += self.current_char()
                self.advance()
        
        if self.current_char() == quote_char:
            self.advance()
        else:
            quote_type = "single quote (')" if quote_char == "'" else "double quote (\")"
            raise SyntaxError(f"Unclosed {quote_type} at line {start_line}, column {start_column}")
        
        if quote_char == "'":
            return Token("CHAR", string_value, start_line, start_column)
        else:
            return Token("STRING", string_value, start_line, start_column)
    
    def read_number(self):
        start_line = self.line
        start_column = self.column
        number_str = ""
        is_float = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if is_float:
                    break
                is_float = True
            number_str += self.current_char()
            self.advance()
        
        if is_float:
            return Token("FLOAT_NUMBER", float(number_str), start_line, start_column)
        else:
            return Token("NUMBER", int(number_str), start_line, start_column)
    
    def read_identifier(self):
        start_line = self.line
        start_column = self.column
        identifier = ""
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            identifier += self.current_char()
            self.advance()
        
        if identifier in self.keywords:
            token_type = self.keywords[identifier]
            return Token(token_type, identifier, start_line, start_column)
        else:
            return Token("IDENTIFIER", identifier, start_line, start_column)
    
    def tokenize(self):
        while self.current_char():
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            if self.current_char() == '/' and self.peek_char() == '/':
                if not self.tokens or self.tokens[-1].type in ["SEMICOLON", "LBRACE", "RBRACE"]:
                    self.skip_comment()
                    continue
            
            char = self.current_char()
            start_line = self.line
            start_column = self.column
            
            if char in '"\'':
                self.tokens.append(self.read_string())
            elif char.isdigit():
                self.tokens.append(self.read_number())
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            elif char == '{':
                self.tokens.append(Token("LBRACE", char, start_line, start_column))
                self.advance()
            elif char == '}':
                self.tokens.append(Token("RBRACE", char, start_line, start_column))
                self.advance()
            elif char == '(':
                self.tokens.append(Token("LPAREN", char, start_line, start_column))
                self.advance()
            elif char == ')':
                self.tokens.append(Token("RPAREN", char, start_line, start_column))
                self.advance()
            elif char == '[':
                self.tokens.append(Token("LBRACKET", char, start_line, start_column))
                self.advance()
            elif char == ']':
                self.tokens.append(Token("RBRACKET", char, start_line, start_column))
                self.advance()
            elif char == ';':
                self.tokens.append(Token("SEMICOLON", char, start_line, start_column))
                self.advance()
            elif char == '=':
                if self.peek_char() == '=':
                    self.tokens.append(Token("EQUAL_EQUAL", "==", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token("EQUALS", char, start_line, start_column))
                    self.advance()
            elif char == ',':
                self.tokens.append(Token("COMMA", char, start_line, start_column))
                self.advance()
            elif char == '*':
                self.tokens.append(Token("ASTERISK", char, start_line, start_column))
                self.advance()
            elif char == '+':
                if self.peek_char() == '+':
                    self.tokens.append(Token("PLUS_PLUS", "++", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token("PLUS", char, start_line, start_column))
                    self.advance()
            elif char == '-':
                if self.peek_char() == '-':
                    self.tokens.append(Token("MINUS_MINUS", "--", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token("MINUS", char, start_line, start_column))
                    self.advance()
            elif char == '/':
                if self.peek_char() == '/':
                    self.tokens.append(Token("DOUBLE_SLASH", "//", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token("SLASH", char, start_line, start_column))
                    self.advance()
            elif char == '%':
                self.tokens.append(Token("PERCENT", char, start_line, start_column))
                self.advance()
            elif char == '<':
                if self.peek_char() == '=':
                    self.tokens.append(Token("LESS_EQUAL", "<=", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token("LESS", char, start_line, start_column))
                    self.advance()
            elif char == '>':
                if self.peek_char() == '=':
                    self.tokens.append(Token("GREATER_EQUAL", ">=", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token("GREATER", char, start_line, start_column))
                    self.advance()
            elif char == '!':
                if self.peek_char() == '=':
                    self.tokens.append(Token("NOT_EQUAL", "!=", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    raise SyntaxError(f"Dude, what even is '{char}' at {start_line}:{start_column}? I have no idea what you want from me here.")
            elif char == '&':
                if self.peek_char() == '&':
                    self.tokens.append(Token("AND", "&&", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    raise SyntaxError(f"Dude, what even is '{char}' at {start_line}:{start_column}? I have no idea what you want from me here.")
            elif char == '|':
                if self.peek_char() == '|':
                    self.tokens.append(Token("OR", "||", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    raise SyntaxError(f"Dude, what even is '{char}' at {start_line}:{start_column}? I have no idea what you want from me here.")
            else:
                raise SyntaxError(f"Dude, what even is '{char}' at {start_line}:{start_column}? I have no idea what you want from me here.")
        
        self.tokens.append(Token("EOF", None, self.line, self.column))
        return self.tokens
