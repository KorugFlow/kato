from parser.ast import StringLiteral, Identifier, ArrayAccess
import re


class PrintfConverter:
    def convert_printf_to_print(self, printf_args):
        if not printf_args:
            return []
        
        format_string = printf_args[0]
        variables = printf_args[1:] if len(printf_args) > 1 else []
        
        if not isinstance(format_string, StringLiteral):
            return printf_args
        
        result_parts = []
        format_str = format_string.value
        
        pattern = r'%[dfsci]'
        parts = re.split(pattern, format_str)
        specifiers = re.findall(pattern, format_str)
        
        if not specifiers:
            return [StringLiteral(format_str)]
        
        result = ""
        var_index = 0
        
        for i, part in enumerate(parts):
            result += part
            
            if i < len(specifiers) and var_index < len(variables):
                var = variables[var_index]
                
                if isinstance(var, Identifier):
                    result += f"*{var.name}*"
                elif isinstance(var, ArrayAccess):
                    result += f"*{var.name}[{self.expr_to_str(var.index)}]*"
                else:
                    result += str(var)
                
                var_index += 1
        
        return [StringLiteral(result)]
    
    def expr_to_str(self, expr):
        if isinstance(expr, Identifier):
            return expr.name
        elif hasattr(expr, 'value'):
            return str(expr.value)
        else:
            return "0"
