class C2KatoError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.format_error())
    
    def format_error(self):
        if self.line and self.column:
            return f"c2kato Error at {self.line}:{self.column}: {self.message}"
        return f"c2kato Error: {self.message}"
