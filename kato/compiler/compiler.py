from parser.parser import (
    Program, Function, PrintStatement, ReturnStatement,
    VarDeclaration, CallStatement,
    StringLiteral, NumberLiteral, FloatLiteral, CharLiteral, Identifier, BinaryOp
)
import re


class CCompiler:
    def __init__(self, ast):
        self.ast = ast
        self.indent_level = 0
        self.variables = {}
    
    def indent(self):
        return "    " * self.indent_level
    
    def compile(self):
        c_code = "#include <stdio.h>\n"
        c_code += "#include <string.h>\n\n"
        
        for function in self.ast.functions:
            if function.name != "main":
                c_code += self.get_function_signature(function) + ";\n"
        
        c_code += "\n"
        
        for function in self.ast.functions:
            c_code += self.compile_function(function)
            c_code += "\n"
        
        return c_code
    
    def get_function_signature(self, function):
        if function.params:
            params_str = ", ".join([f"char* {param}" for param in function.params])
            return f"int {function.name}({params_str})"
        return f"int {function.name}()"
    
    def compile_function(self, function):
        self.variables = {}
        
        if function.params:
            for param in function.params:
                self.variables[param] = "string"
            params_str = ", ".join([f"char* {param}" for param in function.params])
            c_code = f"int {function.name}({params_str}) {{\n"
        else:
            c_code = f"int {function.name}() {{\n"
        
        self.indent_level += 1
        
        for statement in function.body:
            c_code += self.compile_statement(statement)
        
        self.indent_level -= 1
        c_code += "}\n"
        
        return c_code
    
    def compile_statement(self, statement):
        if isinstance(statement, PrintStatement):
            return self.compile_print(statement)
        elif isinstance(statement, ReturnStatement):
            return self.compile_return(statement)
        elif isinstance(statement, VarDeclaration):
            return self.compile_var_declaration(statement)
        elif isinstance(statement, CallStatement):
            return self.compile_call(statement)
    
    def compile_print(self, statement):
        values = statement.value if isinstance(statement.value, list) else [statement.value]
        
        format_parts = []
        printf_args = []
        
        for value in values:
            if isinstance(value, StringLiteral):
                string_value = value.value
                
                var_pattern = r'\*(\w+)\*'
                vars_in_string = re.findall(var_pattern, string_value)
                
                if vars_in_string:
                    format_string = string_value
                    
                    for var_name in vars_in_string:
                        if var_name in self.variables:
                            var_type = self.variables[var_name]
                            
                            if var_type == "int":
                                format_string = format_string.replace(f"*{var_name}*", "%d", 1)
                            elif var_type == "float":
                                format_string = format_string.replace(f"*{var_name}*", "%f", 1)
                            elif var_type == "char":
                                format_string = format_string.replace(f"*{var_name}*", "%c", 1)
                            elif var_type == "string":
                                format_string = format_string.replace(f"*{var_name}*", "%s", 1)
                            
                            printf_args.append(var_name)
                    
                    format_parts.append(format_string)
                else:
                    format_parts.append(string_value)
            elif isinstance(value, NumberLiteral):
                format_parts.append("%d")
                printf_args.append(str(value.value))
            elif isinstance(value, FloatLiteral):
                format_parts.append("%f")
                printf_args.append(str(value.value))
            elif isinstance(value, Identifier):
                var_name = value.name
                if var_name in self.variables:
                    var_type = self.variables[var_name]
                    if var_type == "int":
                        format_parts.append("%d")
                    elif var_type == "float":
                        format_parts.append("%f")
                    elif var_type == "char":
                        format_parts.append("%c")
                    elif var_type == "string":
                        format_parts.append("%s")
                    printf_args.append(var_name)
                else:
                    format_parts.append("%s")
                    printf_args.append(var_name)
            elif isinstance(value, BinaryOp):
                format_parts.append("%d")
                printf_args.append(self.compile_expr(value))
        
        format_string = "".join(format_parts)
        escaped_string = format_string.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r').replace('"', '\\"')
        
        if printf_args:
            args_str = ", ".join(printf_args)
            return f'{self.indent()}printf("{escaped_string}", {args_str});\n'
        else:
            return f'{self.indent()}printf("{escaped_string}");\n'
    
    def compile_return(self, statement):
        value = statement.value
        
        if isinstance(value, NumberLiteral):
            return f'{self.indent()}return {value.value};\n'
        elif isinstance(value, FloatLiteral):
            return f'{self.indent()}return (int){value.value};\n'
        elif isinstance(value, StringLiteral):
            return f'{self.indent()}return 0;\n'
        elif isinstance(value, Identifier):
            return f'{self.indent()}return {value.name};\n'
    
    def compile_var_declaration(self, statement):
        var_type = statement.var_type
        var_name = statement.name
        var_value = statement.value
        
        self.variables[var_name] = var_type
        
        c_type_map = {
            "int": "int",
            "float": "float",
            "char": "char",
            "string": "char*"
        }
        c_type = c_type_map.get(var_type, "int")
        
        c_value = self.compile_expr(var_value)
        
        return f'{self.indent()}{c_type} {var_name} = {c_value};\n'
    
    def compile_call(self, statement):
        func_name = statement.func_name
        arguments = statement.arguments
        
        if arguments:
            compiled_args = []
            for arg in arguments:
                compiled_args.append(self.compile_expr(arg))
            args_str = ", ".join(compiled_args)
            return f'{self.indent()}{func_name}({args_str});\n'
        
        return f'{self.indent()}{func_name}();\n'
    
    def compile_expr(self, expr):
        if isinstance(expr, StringLiteral):
            escaped_string = expr.value.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r').replace('"', '\\"')
            return f'"{escaped_string}"'
        elif isinstance(expr, NumberLiteral):
            return str(expr.value)
        elif isinstance(expr, FloatLiteral):
            return str(expr.value)
        elif isinstance(expr, Identifier):
            return expr.name
        elif isinstance(expr, BinaryOp):
            left = self.compile_expr(expr.left)
            right = self.compile_expr(expr.right)
            return f"({left} {expr.operator} {right})"
        else:
            return "0"
