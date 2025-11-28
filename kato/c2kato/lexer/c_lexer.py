from .token import CToken
from .c_tokens import C_KEYWORDS


class CLexer:
    def __init__(self, source_code):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
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
        elif self.current_char() == '/' and self.peek_char() == '*':
            self.advance()
            self.advance()
            while self.current_char():
                if self.current_char() == '*' and self.peek_char() == '/':
                    self.advance()
                    self.advance()
                    break
                self.advance()
    
    def read_string(self):
        start_line = self.line
        start_column = self.column
        quote_char = self.current_char()
        self.advance()
        
        string_value = ""
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                string_value += '\\'
                self.advance()
                if self.current_char():
                    string_value += self.current_char()
                    self.advance()
            else:
                string_value += self.current_char()
                self.advance()
        
        if self.current_char() == quote_char:
            self.advance()
        
        if quote_char == "'":
            return CToken("CHAR", string_value, start_line, start_column)
        else:
            return CToken("STRING", string_value, start_line, start_column)
    
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
            return CToken("FLOAT_NUMBER", float(number_str), start_line, start_column)
        else:
            return CToken("NUMBER", int(number_str), start_line, start_column)
    
    def read_identifier(self):
        start_line = self.line
        start_column = self.column
        identifier = ""
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            identifier += self.current_char()
            self.advance()
        
        if identifier in C_KEYWORDS:
            token_type = C_KEYWORDS[identifier]
            return CToken(token_type, identifier, start_line, start_column)
        else:
            return CToken("IDENTIFIER", identifier, start_line, start_column)
    
    def tokenize(self):
        while self.current_char():
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            if self.current_char() == '/' and self.peek_char() in ['/', '*']:
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
            elif char == '#':
                self.tokens.append(CToken("HASH", char, start_line, start_column))
                self.advance()
            elif char == '{':
                self.tokens.append(CToken("LBRACE", char, start_line, start_column))
                self.advance()
            elif char == '}':
                self.tokens.append(CToken("RBRACE", char, start_line, start_column))
                self.advance()
            elif char == '(':
                self.tokens.append(CToken("LPAREN", char, start_line, start_column))
                self.advance()
            elif char == ')':
                self.tokens.append(CToken("RPAREN", char, start_line, start_column))
                self.advance()
            elif char == '[':
                self.tokens.append(CToken("LBRACKET", char, start_line, start_column))
                self.advance()
            elif char == ']':
                self.tokens.append(CToken("RBRACKET", char, start_line, start_column))
                self.advance()
            elif char == ';':
                self.tokens.append(CToken("SEMICOLON", char, start_line, start_column))
                self.advance()
            elif char == ',':
                self.tokens.append(CToken("COMMA", char, start_line, start_column))
                self.advance()
            elif char == '=':
                if self.peek_char() == '=':
                    self.tokens.append(CToken("EQUAL_EQUAL", "==", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(CToken("EQUALS", char, start_line, start_column))
                    self.advance()
            elif char == '+':
                if self.peek_char() == '+':
                    self.tokens.append(CToken("PLUS_PLUS", "++", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(CToken("PLUS", char, start_line, start_column))
                    self.advance()
            elif char == '-':
                if self.peek_char() == '-':
                    self.tokens.append(CToken("MINUS_MINUS", "--", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(CToken("MINUS", char, start_line, start_column))
                    self.advance()
            elif char == '*':
                self.tokens.append(CToken("ASTERISK", char, start_line, start_column))
                self.advance()
            elif char == '/':
                self.tokens.append(CToken("SLASH", char, start_line, start_column))
                self.advance()
            elif char == '%':
                self.tokens.append(CToken("PERCENT", char, start_line, start_column))
                self.advance()
            elif char == '<':
                if self.peek_char() == '=':
                    self.tokens.append(CToken("LESS_EQUAL", "<=", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(CToken("LESS", char, start_line, start_column))
                    self.advance()
            elif char == '>':
                if self.peek_char() == '=':
                    self.tokens.append(CToken("GREATER_EQUAL", ">=", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(CToken("GREATER", char, start_line, start_column))
                    self.advance()
            elif char == '!':
                if self.peek_char() == '=':
                    self.tokens.append(CToken("NOT_EQUAL", "!=", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.advance()
            elif char == '&':
                if self.peek_char() == '&':
                    self.tokens.append(CToken("AND", "&&", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(CToken("AMPERSAND", char, start_line, start_column))
                    self.advance()
            elif char == '|':
                if self.peek_char() == '|':
                    self.tokens.append(CToken("OR", "||", start_line, start_column))
                    self.advance()
                    self.advance()
                else:
                    self.advance()
            else:
                self.advance()
        
        self.tokens.append(CToken("EOF", None, self.line, self.column))
        return self.tokens
