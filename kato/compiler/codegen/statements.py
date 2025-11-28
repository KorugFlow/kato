from parser.ast import (
    PrintStatement, ReturnStatement, VarDeclaration,
    CallStatement, IfStatement, Assignment,
    WhileStatement, IncrementStatement, DecrementStatement,
    StringLiteral, NumberLiteral, FloatLiteral, Identifier, BinaryOp, InptCall
)
import re


class StatementCodegen:
    def __init__(self, compiler, expr_codegen):
        self.compiler = compiler
        self.expr_codegen = expr_codegen
    
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
        elif isinstance(statement, WhileStatement):
            return self.compile_while(statement)
        elif isinstance(statement, IncrementStatement):
            return self.compile_increment(statement)
        elif isinstance(statement, DecrementStatement):
            return self.compile_decrement(statement)
    
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
                        if var_name in self.compiler.variables:
                            var_type = self.compiler.variables[var_name]
                            
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
                if var_name in self.compiler.variables:
                    var_type = self.compiler.variables[var_name]
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
                printf_args.append(self.expr_codegen.compile_expr(value))
        
        format_string = "".join(format_parts)
        escaped_string = format_string.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r').replace('"', '\\"')
        
        if printf_args:
            args_str = ", ".join(printf_args)
            return f'{self.compiler.indent()}printf("{escaped_string}", {args_str});\n'
        else:
            return f'{self.compiler.indent()}printf("{escaped_string}");\n'
    
    def compile_return(self, statement):
        value = statement.value
        
        if isinstance(value, NumberLiteral):
            return f'{self.compiler.indent()}return {value.value};\n'
        elif isinstance(value, FloatLiteral):
            return f'{self.compiler.indent()}return (int){value.value};\n'
        elif isinstance(value, StringLiteral):
            return f'{self.compiler.indent()}return 0;\n'
        elif isinstance(value, Identifier):
            return f'{self.compiler.indent()}return {value.name};\n'
    
    def compile_var_declaration(self, statement):
        var_type = statement.var_type
        var_name = statement.name
        var_value = statement.value
        
        self.compiler.variables[var_name] = var_type
        
        c_type_map = {
            "int": "int",
            "float": "float",
            "char": "char",
            "string": "char*"
        }
        c_type = c_type_map.get(var_type, "int")
        
        if isinstance(var_value, InptCall):
            prompt = self.expr_codegen.compile_expr(var_value.prompt)
            code = f'{self.compiler.indent()}{c_type} {var_name};\n'
            code += f'{self.compiler.indent()}printf({prompt});\n'
            
            if var_type == "int":
                code += f'{self.compiler.indent()}scanf("%d", &{var_name});\n'
            elif var_type == "float":
                code += f'{self.compiler.indent()}scanf("%f", &{var_name});\n'
            elif var_type == "char":
                code += f'{self.compiler.indent()}scanf(" %c", &{var_name});\n'
            elif var_type == "string":
                code += f'{self.compiler.indent()}{var_name} = (char*)malloc(4096);\n'
                code += f'{self.compiler.indent()}fgets({var_name}, 4096, stdin);\n'
                code += f'{self.compiler.indent()}{var_name}[strcspn({var_name}, "\\n")] = 0;\n'
            
            return code
        else:
            c_value = self.expr_codegen.compile_expr(var_value, var_type)
            return f'{self.compiler.indent()}{c_type} {var_name} = {c_value};\n'
    
    def compile_call(self, statement):
        func_name = statement.func_name
        arguments = statement.arguments
        
        if arguments:
            compiled_args = []
            for arg in arguments:
                compiled_args.append(self.expr_codegen.compile_expr(arg))
            args_str = ", ".join(compiled_args)
            return f'{self.compiler.indent()}{func_name}({args_str});\n'
        
        return f'{self.compiler.indent()}{func_name}();\n'
    
    def compile_if(self, statement):
        condition = self.expr_codegen.compile_expr(statement.condition)
        
        code = f'{self.compiler.indent()}if ({condition}) {{\n'
        self.compiler.indent_level += 1
        for stmt in statement.if_body:
            code += self.compile_statement(stmt)
        self.compiler.indent_level -= 1
        code += f'{self.compiler.indent()}}}'
        
        for elif_condition, elif_body in statement.elif_parts:
            elif_cond = self.expr_codegen.compile_expr(elif_condition)
            code += f' else if ({elif_cond}) {{\n'
            self.compiler.indent_level += 1
            for stmt in elif_body:
                code += self.compile_statement(stmt)
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}}'
        
        if statement.else_body:
            code += f' else {{\n'
            self.compiler.indent_level += 1
            for stmt in statement.else_body:
                code += self.compile_statement(stmt)
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}}'
        
        code += '\n'
        return code
    
    def compile_assignment(self, statement):
        var_name = statement.name
        var_value = statement.value
        
        var_type = self.compiler.variables.get(var_name, "int")
        
        if isinstance(var_value, InptCall):
            prompt = self.expr_codegen.compile_expr(var_value.prompt)
            code = f'{self.compiler.indent()}printf({prompt});\n'
            
            if var_type == "int":
                code += f'{self.compiler.indent()}scanf("%d", &{var_name});\n'
            elif var_type == "float":
                code += f'{self.compiler.indent()}scanf("%f", &{var_name});\n'
            elif var_type == "char":
                code += f'{self.compiler.indent()}scanf(" %c", &{var_name});\n'
            elif var_type == "string":
                code += f'{self.compiler.indent()}fgets({var_name}, 4096, stdin);\n'
                code += f'{self.compiler.indent()}{var_name}[strcspn({var_name}, "\\n")] = 0;\n'
            
            return code
        else:
            c_value = self.expr_codegen.compile_expr(var_value, var_type)
            return f'{self.compiler.indent()}{var_name} = {c_value};\n'

    def compile_while(self, statement):
        condition = self.expr_codegen.compile_expr(statement.condition)
        
        code = f'{self.compiler.indent()}while ({condition}) {{\n'
        self.compiler.indent_level += 1
        for stmt in statement.body:
            code += self.compile_statement(stmt)
        self.compiler.indent_level -= 1
        code += f'{self.compiler.indent()}}}\n'
        
        return code
    
    def compile_increment(self, statement):
        return f'{self.compiler.indent()}{statement.name}++;\n'
    
    def compile_decrement(self, statement):
        return f'{self.compiler.indent()}{statement.name}--;\n'
