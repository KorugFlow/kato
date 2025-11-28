class KatoFormatter:
    def __init__(self):
        self.indent_level = 0
    
    def indent(self):
        return "    " * self.indent_level
    
    def format_code(self, code_lines):
        formatted = []
        
        for line in code_lines:
            if line.strip():
                formatted.append(line)
        
        return "\n".join(formatted)
