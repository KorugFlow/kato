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
        
        format_str = format_string.value
        
        pattern = r'%\.?\d*[dfsci]|%lf|%\.?\d*lf'
        parts = re.split(pattern, format_str)
        specifiers = re.findall(pattern, format_str)
        
        if not specifiers:
            return [StringLiteral(format_str)]
        
        result_parts = []
        var_index = 0
        
        for i, part in enumerate(parts):
            if part:
                result_parts.append(StringLiteral(part))
            
            if i < len(specifiers) and var_index < len(variables):
                spec = specifiers[i]
                var = variables[var_index]
                
                if spec in ['%d', '%i', '%f', '%lf'] or 'lf' in spec or 'f' in spec:
                    if isinstance(var, Identifier):
                        result_parts.append(StringLiteral(f"*{var.name}*"))
                    elif isinstance(var, ArrayAccess):
                        result_parts.append(StringLiteral(f"*{var.name}[{self.expr_to_str(var.index)}]*"))
                    else:
                        result_parts.append(var)
                else:
                    if isinstance(var, Identifier):
                        result_parts.append(StringLiteral(f"*{var.name}*"))
                    elif isinstance(var, ArrayAccess):
                        result_parts.append(StringLiteral(f"*{var.name}[{self.expr_to_str(var.index)}]*"))
                    else:
                        result_parts.append(var)
                
                var_index += 1
        
        return result_parts
    
    def expr_to_str(self, expr):
        if isinstance(expr, Identifier):
            return expr.name
        elif hasattr(expr, 'value'):
            return str(expr.value)
        else:
            return "0"
