class CToken:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"CToken({self.type}, {repr(self.value)}, {self.line}:{self.column})"
