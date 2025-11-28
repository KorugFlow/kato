class KatoSyntaxError(Exception):
    def __init__(self, message, line, column, source_code=None):
        self.message = message
        self.line = line
        self.column = column
        self.source_code = source_code
        super().__init__(self.format_error())
    
    def format_error(self):
        RED = '\033[91m'
        YELLOW = '\033[93m'
        CYAN = '\033[96m'
        GRAY = '\033[90m'
        BOLD = '\033[1m'
        RESET = '\033[0m'
        
        error_msg = f"\n{RED}{'='*60}{RESET}\n"
        error_msg += f"{BOLD}{RED}  Kato Syntax Error{RESET}\n"
        error_msg += f"{RED}{'='*60}{RESET}\n\n"
        error_msg += f"{BOLD}  {self.message}{RESET}\n"
        error_msg += f"{GRAY}  at line {self.line}, column {self.column}{RESET}\n\n"
        
        if self.source_code:
            lines = self.source_code.split('\n')
            if 0 < self.line <= len(lines):
                error_line = lines[self.line - 1]
                
                error_msg += f"{CYAN}{'─'*60}{RESET}\n"
                
                if self.line > 1:
                    error_msg += f"{GRAY}  {self.line - 1:4d} | {lines[self.line - 2]}{RESET}\n"
                
                error_msg += f"{YELLOW}  {self.line:4d} | {error_line}{RESET}\n"
                error_msg += f"{RED}       | {' ' * (self.column - 1)}^{RESET}\n"
                
                if self.line < len(lines):
                    error_msg += f"{GRAY}  {self.line + 1:4d} | {lines[self.line]}{RESET}\n"
                
                error_msg += f"{CYAN}{'─'*60}{RESET}\n"
        
        return error_msg
