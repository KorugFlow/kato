from parser.parser import (
    Program, Function, PrintStatement, ReturnStatement,
    VarDeclaration, CallStatement, IfStatement, Assignment,
    StringLiteral, NumberLiteral, FloatLiteral, CharLiteral, Identifier, BinaryOp, InptCall
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
        c_code += "#include <string.h>\n"
        c_code += "#include <stdlib.h>\n\n"
        
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
        elif isinstance(statement, IfStatement):
            return self.compile_if(statement)
        elif isinstance(statement, Assignment):
            return self.compile_assignment(statement)
    
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
        
        if isinstance(var_value, InptCall):
            prompt = self.compile_expr(var_value.prompt)
            code = f'{self.indent()}{c_type} {var_name};\n'
            code += f'{self.indent()}printf({prompt});\n'
            
            if var_type == "int":
                code += f'{self.indent()}scanf("%d", &{var_name});\n'
            elif var_type == "float":
                code += f'{self.indent()}scanf("%f", &{var_name});\n'
            elif var_type == "char":
                code += f'{self.indent()}scanf(" %c", &{var_name});\n'
            elif var_type == "string":
                code += f'{self.indent()}{var_name} = (char*)malloc(256);\n'
                code += f'{self.indent()}scanf("%255s", {var_name});\n'
            
            return code
        else:
            c_value = self.compile_expr(var_value, var_type)
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
    
    def compile_expr(self, expr, var_type=None):
        if isinstance(expr, StringLiteral):
            escaped_string = expr.value.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r').replace('"', '\\"')
            return f'"{escaped_string}"'
        elif isinstance(expr, CharLiteral):
            if len(expr.value) == 1:
                return f"'{expr.value}'"
            else:
                return f"'{expr.value[0]}'"
        elif isinstance(expr, NumberLiteral):
            return str(expr.value)
        elif isinstance(expr, FloatLiteral):
            return str(expr.value)
        elif isinstance(expr, Identifier):
            return expr.name
        elif isinstance(expr, BinaryOp):
            left = self.compile_expr(expr.left, var_type)
            right = self.compile_expr(expr.right, var_type)
            return f"({left} {expr.operator} {right})"
        elif isinstance(expr, InptCall):
            prompt = self.compile_expr(expr.prompt, var_type)
            
            if var_type == "int":
                return f"(printf({prompt}), scanf(\"%d\", &(int){{0}}), (int){{0}})"
            elif var_type == "float":
                return f"(printf({prompt}), scanf(\"%f\", &(float){{0.0}}), (float){{0.0}})"
            elif var_type == "char":
                return f"(printf({prompt}), getchar())"
            elif var_type == "string":
                return f"(printf({prompt}), (char[256]){{0}})"
            else:
                return f"(printf({prompt}), 0)"
        else:
            return "0"

    def compile_if(self, statement):
        condition = self.compile_expr(statement.condition)
        
        code = f'{self.indent()}if ({condition}) {{\n'
        self.indent_level += 1
        for stmt in statement.if_body:
            code += self.compile_statement(stmt)
        self.indent_level -= 1
        code += f'{self.indent()}}}'
        
        for elif_condition, elif_body in statement.elif_parts:
            elif_cond = self.compile_expr(elif_condition)
            code += f' else if ({elif_cond}) {{\n'
            self.indent_level += 1
            for stmt in elif_body:
                code += self.compile_statement(stmt)
            self.indent_level -= 1
            code += f'{self.indent()}}}'
        
        if statement.else_body:
            code += f' else {{\n'
            self.indent_level += 1
            for stmt in statement.else_body:
                code += self.compile_statement(stmt)
            self.indent_level -= 1
            code += f'{self.indent()}}}'
        
        code += '\n'
        return code
    
    def compile_assignment(self, statement):
        var_name = statement.name
        var_value = statement.value
        
        var_type = self.variables.get(var_name, "int")
        
        if isinstance(var_value, InptCall):
            prompt = self.compile_expr(var_value.prompt)
            code = f'{self.indent()}printf({prompt});\n'
            
            if var_type == "int":
                code += f'{self.indent()}scanf("%d", &{var_name});\n'
            elif var_type == "float":
                code += f'{self.indent()}scanf("%f", &{var_name});\n'
            elif var_type == "char":
                code += f'{self.indent()}scanf(" %c", &{var_name});\n'
            elif var_type == "string":
                code += f'{self.indent()}scanf("%255s", {var_name});\n'
            
            return code
        else:
            c_value = self.compile_expr(var_value, var_type)
            return f'{self.indent()}{var_name} = {c_value};\n'
