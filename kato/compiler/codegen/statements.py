from parser.ast import (
    PrintStatement, ReturnStatement, VarDeclaration,
    CallStatement, IfStatement, Assignment,
    WhileStatement, IncrementStatement, DecrementStatement,
    ArrayDeclaration, ArrayAssignment, SwitchStatement, CaseClause,
    ConvertStatement, CImportStatement, CCallStatement,
    BreakStatement, ContinueStatement, InfStatement, StopStatement, ForStatement,
    StructVarDeclaration, StructFieldAssignment, PointerAssignment,
    StringLiteral, NumberLiteral, FloatLiteral, Identifier, BinaryOp, InptCall, ArrayAccess, CharLiteral,
    ConvertExpression, FunctionCall, StructAccess
)
import re


class StatementCodegen:
    def __init__(self, compiler, expr_codegen):
        self.compiler = compiler
        self.expr_codegen = expr_codegen
    
    def compile_statement(self, statement):
        line_comment = f" // {statement.source_line}" if hasattr(statement, 'source_line') and statement.source_line else ""
        if isinstance(statement, BreakStatement):
            return f'{self.compiler.indent()}break;{line_comment}\n'
        elif isinstance(statement, ContinueStatement):
            return f'{self.compiler.indent()}continue;{line_comment}\n'
        elif isinstance(statement, CImportStatement):
            return self.compile_c_import(statement)
        elif isinstance(statement, CCallStatement):
            return self.compile_c_call(statement)
        elif isinstance(statement, PrintStatement):
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
        elif isinstance(statement, ArrayDeclaration):
            return self.compile_array_declaration(statement)
        elif isinstance(statement, ArrayAssignment):
            return self.compile_array_assignment(statement)
        elif isinstance(statement, SwitchStatement):
            return self.compile_switch(statement)
        elif isinstance(statement, ConvertStatement):
            return self.compile_convert(statement)
        elif isinstance(statement, InfStatement):
            return self.compile_inf(statement)
        elif isinstance(statement, StopStatement):
            return f'{self.compiler.indent()}break;{line_comment}\n'
        elif isinstance(statement, ForStatement):
            return self.compile_for(statement)
        elif isinstance(statement, StructVarDeclaration):
            return self.compile_struct_var_declaration(statement)
        elif isinstance(statement, StructFieldAssignment):
            return self.compile_struct_field_assignment(statement)
        elif isinstance(statement, PointerAssignment):
            return self.compile_pointer_assignment(statement)
        else:
            raise ValueError(f"Unknown statement type: {type(statement).__name__}")
    
    def compile_print(self, statement):
        line_comment = f" // {statement.source_line}" if hasattr(statement, 'source_line') and statement.source_line else ""
        values = statement.value if isinstance(statement.value, list) else [statement.value]
        
        format_parts = []
        printf_args = []
        
        for value in values:
            if isinstance(value, StringLiteral):
                string_value = value.value
                
                var_pattern = r'\*([\w\.]+)\*'
                vars_in_string = re.findall(var_pattern, string_value)
                
                if vars_in_string:
                    format_string = string_value
                    
                    for var_expr in vars_in_string:
                        if '.' in var_expr:
                            parts = var_expr.split('.')
                            struct_name = parts[0]
                            field_name = parts[1]
                            if struct_name in self.compiler.variables:
                                struct_type = self.compiler.variables[struct_name]
                                if struct_type in self.compiler.struct_definitions:
                                    field_type = self.compiler.struct_definitions[struct_type].get(field_name)
                                    if field_type == "int":
                                        format_string = format_string.replace(f"*{var_expr}*", "%d", 1)
                                    elif field_type == "float":
                                        format_string = format_string.replace(f"*{var_expr}*", "%f", 1)
                                    elif field_type == "char":
                                        format_string = format_string.replace(f"*{var_expr}*", "%c", 1)
                                    elif field_type == "string":
                                        format_string = format_string.replace(f"*{var_expr}*", "%s", 1)
                                    printf_args.append(f"{struct_name}.{field_name}")
                        elif var_expr in self.compiler.variables:
                            var_type = self.compiler.variables[var_expr]
                            
                            if var_type.endswith('*'):
                                base_type = var_type[:-1]
                                if base_type == "int":
                                    format_string = format_string.replace(f"*{var_expr}*", "%d", 1)
                                    printf_args.append(f"(*{var_expr})")
                                elif base_type == "float":
                                    format_string = format_string.replace(f"*{var_expr}*", "%f", 1)
                                    printf_args.append(f"(*{var_expr})")
                                elif base_type == "char":
                                    format_string = format_string.replace(f"*{var_expr}*", "%c", 1)
                                    printf_args.append(f"(*{var_expr})")
                                elif base_type == "string":
                                    format_string = format_string.replace(f"*{var_expr}*", "%s", 1)
                                    printf_args.append(f"(*{var_expr})")
                            else:
                                if var_type == "int":
                                    format_string = format_string.replace(f"*{var_expr}*", "%d", 1)
                                elif var_type == "float":
                                    format_string = format_string.replace(f"*{var_expr}*", "%f", 1)
                                elif var_type == "char":
                                    format_string = format_string.replace(f"*{var_expr}*", "%c", 1)
                                elif var_type == "string":
                                    format_string = format_string.replace(f"*{var_expr}*", "%s", 1)
                                
                                printf_args.append(var_expr)
                    
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
                    if var_type.endswith('*'):
                        format_parts.append("%p")
                        printf_args.append(f"(void*){var_name}")
                    elif var_type == "int":
                        format_parts.append("%d")
                        printf_args.append(var_name)
                    elif var_type == "float":
                        format_parts.append("%f")
                        printf_args.append(var_name)
                    elif var_type == "char":
                        format_parts.append("%c")
                        printf_args.append(var_name)
                    elif var_type == "string":
                        format_parts.append("%s")
                        printf_args.append(var_name)
                    else:
                        printf_args.append(var_name)
                else:
                    format_parts.append("%s")
                    printf_args.append(var_name)
            elif isinstance(value, ArrayAccess):
                array_name = value.name
                if array_name in self.compiler.variables:
                    var_type = self.compiler.variables[array_name]
                    if var_type == "int":
                        format_parts.append("%d")
                    elif var_type == "float":
                        format_parts.append("%f")
                    elif var_type == "char":
                        format_parts.append("%c")
                    elif var_type == "string":
                        format_parts.append("%s")
                    printf_args.append(self.expr_codegen.compile_expr(value))
                else:
                    format_parts.append("%s")
                    printf_args.append(self.expr_codegen.compile_expr(value))
            elif isinstance(value, BinaryOp):
                format_parts.append("%d")
                printf_args.append(self.expr_codegen.compile_expr(value))
            elif isinstance(value, FunctionCall):
                func_name = value.name
                if func_name == "file_read":
                    format_parts.append("%s")
                elif func_name == "file_exists" or func_name == "file_write" or func_name == "file_append" or func_name == "file_delete":
                    format_parts.append("%d")
                elif func_name == "random":
                    format_parts.append("%d")
                else:
                    format_parts.append("%s")
                printf_args.append(self.expr_codegen.compile_expr(value))
        
   
        format_string = "".join(format_parts)
        escaped_string = format_string.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r').replace('"', '\\"')
        
        if printf_args:
            args_str = ", ".join(printf_args)
            return f'{self.compiler.indent()}printf("{escaped_string}", {args_str});{line_comment}\n'
        else:
            return f'{self.compiler.indent()}printf("{escaped_string}");{line_comment}\n'
    
    def compile_return(self, statement):
        line_comment = f" // {statement.source_line}" if hasattr(statement, 'source_line') and statement.source_line else ""
        value = statement.value
        
        if isinstance(value, NumberLiteral):
            return f'{self.compiler.indent()}return {value.value};{line_comment}\n'
        elif isinstance(value, FloatLiteral):
            return f'{self.compiler.indent()}return (int){value.value};{line_comment}\n'
        elif isinstance(value, StringLiteral):
            return f'{self.compiler.indent()}return 0;{line_comment}\n'
        elif isinstance(value, Identifier):
            return f'{self.compiler.indent()}return {value.name};{line_comment}\n'
        elif isinstance(value, BinaryOp):
            return f'{self.compiler.indent()}return {self.expr_codegen.compile_expr(value)};{line_comment}\n'
        else:
            
            return f'{self.compiler.indent()}return {self.expr_codegen.compile_expr(value)};{line_comment}\n'
    
    def compile_var_declaration(self, statement):
        line_comment = f" // {statement.source_line}" if hasattr(statement, 'source_line') and statement.source_line else ""
        var_type = statement.var_type
        var_name = statement.name
        var_value = statement.value
        
        self.compiler.variables[var_name] = var_type
        
        c_type_map = {
            "int": "int",
            "float": "float",
            "char": "char",
            "string": "char*",
            "int*": "int*",
            "float*": "float*",
            "char*": "char*",
            "string*": "char**"
        }
        c_type = c_type_map.get(var_type, "int")
        
        if isinstance(var_value, InptCall):
            prompt = self.expr_codegen.compile_expr(var_value.prompt)
            code = f'{self.compiler.indent()}{c_type} {var_name}; {line_comment}\n'
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
        elif isinstance(var_value, ConvertExpression):
            self.compiler.uses_conversion = True
            source_expr = self.expr_codegen.compile_expr(var_value.expression)
            target_type = var_value.target_type
            
            code = f'{self.compiler.indent()}{c_type} {var_name}; {line_comment}\n'
            code += f'{self.compiler.indent()}{{\n'
            self.compiler.indent_level += 1
            
            if target_type == "string":
                # Converting to string
                source_var = var_value.expression.name if isinstance(var_value.expression, Identifier) else None
                if source_var and source_var in self.compiler.variables:
                    source_type = self.compiler.variables[source_var]
                    code += f'{self.compiler.indent()}{var_name} = (char*)malloc(32);\n'
                    if source_type == "int":
                        code += f'{self.compiler.indent()}sprintf({var_name}, "%d", {source_expr});\n'
                    elif source_type == "float":
                        code += f'{self.compiler.indent()}sprintf({var_name}, "%f", {source_expr});\n'
                    elif source_type == "char":
                        code += f'{self.compiler.indent()}sprintf({var_name}, "%c", {source_expr});\n'
                    else:
                        code += f'{self.compiler.indent()}strcpy({var_name}, {source_expr});\n'
            
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}}\n'
            return code
        else:
            c_value = self.expr_codegen.compile_expr(var_value, var_type)
            return f'{self.compiler.indent()}{c_type} {var_name} = {c_value};{line_comment}\n'
    
    def compile_call(self, statement):
        line_comment = f" // {statement.source_line}" if hasattr(statement, 'source_line') and statement.source_line else ""
        func_name = statement.func_name
        arguments = statement.arguments
        
        if arguments:
            compiled_args = []
            for arg in arguments:
                compiled_args.append(self.expr_codegen.compile_expr(arg))
            args_str = ", ".join(compiled_args)
            return f'{self.compiler.indent()}{func_name}({args_str});{line_comment}\n'
        
        return f'{self.compiler.indent()}{func_name}();{line_comment}\n'
    
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
            code = f'{self.compiler.indent()}printf({prompt}); {line_comment}\n'
            
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
        line_comment = f" // {statement.source_line}" if hasattr(statement, 'source_line') and statement.source_line else ""
        return f'{self.compiler.indent()}{statement.name}++;{line_comment}\n'
    
    def compile_decrement(self, statement):
        line_comment = f" // {statement.source_line}" if hasattr(statement, 'source_line') and statement.source_line else ""
        return f'{self.compiler.indent()}{statement.name}--;{line_comment}\n'

    def compile_array_declaration(self, statement):
        array_type = statement.array_type
        array_name = statement.name
        elements = statement.elements
        
        self.compiler.variables[array_name] = array_type
        
        c_type_map = {
            "int": "int",
            "float": "float",
            "char": "char",
            "string": "char*"
        }
        c_type = c_type_map.get(array_type, "int")
        
        array_size = len(elements)
        compiled_elements = []
        for elem in elements:
            compiled_elements.append(self.expr_codegen.compile_expr(elem, array_type))
        
        elements_str = ", ".join(compiled_elements)
        
        return f'{self.compiler.indent()}{c_type} {array_name}[{array_size}] = {{{elements_str}}};\n'
    
    def compile_array_assignment(self, statement):
        line_comment = f" // {statement.source_line}" if hasattr(statement, 'source_line') and statement.source_line else ""
        array_name = statement.name
        index = self.expr_codegen.compile_expr(statement.index)
        value = self.expr_codegen.compile_expr(statement.value)
        
        return f'{self.compiler.indent()}{array_name}[{index}] = {value};{line_comment}\n'
    
    def compile_switch(self, statement):
        switch_expr = self.expr_codegen.compile_expr(statement.expression)
        
        code = f'{self.compiler.indent()}switch ({switch_expr}) {{\n'
        self.compiler.indent_level += 1
        
        for case in statement.cases:
            case_value = self.expr_codegen.compile_expr(case.value)
            code += f'{self.compiler.indent()}case {case_value}:\n'
            
            self.compiler.indent_level += 1
            has_break = any(isinstance(stmt, BreakStatement) for stmt in case.body)
            for stmt in case.body:
                code += self.compile_statement(stmt)
            if not has_break:
                code += f'{self.compiler.indent()}break;\n'
            self.compiler.indent_level -= 1
        
        if statement.default_body:
            code += f'{self.compiler.indent()}default:\n'
            self.compiler.indent_level += 1
            has_break = any(isinstance(stmt, BreakStatement) for stmt in statement.default_body)
            for stmt in statement.default_body:
                code += self.compile_statement(stmt)
            if not has_break:
                code += f'{self.compiler.indent()}break;\n'
            self.compiler.indent_level -= 1
        
        self.compiler.indent_level -= 1
        code += f'{self.compiler.indent()}}}\n'
        
        return code
    
    def compile_convert(self, statement):
        self.compiler.uses_conversion = True
        
        var_name = None
        if isinstance(statement.expression, Identifier):
            var_name = statement.expression.name
        
        expr = self.expr_codegen.compile_expr(statement.expression)
        target_type = statement.target_type
        
        c_type_map = {
            "int": "int",
            "float": "float",
            "char": "char",
            "string": "char*"
        }
        c_target = c_type_map.get(target_type, "int")
        
        temp_var = f"__convert_temp_{var_name}" if var_name else "__convert_temp"
        
        code = ""
        
        if target_type == "int":
            code += f'{self.compiler.indent()}int {temp_var} = 0;\n'
            code += f'{self.compiler.indent()}{{\n'
            self.compiler.indent_level += 1
            code += f'{self.compiler.indent()}if (strcmp({expr}, "") == 0) {{\n'
            self.compiler.indent_level += 1
            code += f'{self.compiler.indent()}fprintf(stderr, "Error: Cannot convert empty string to int\\n");\n'
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}} else {{\n'
            self.compiler.indent_level += 1
            code += f'{self.compiler.indent()}char* endptr;\n'
            code += f'{self.compiler.indent()}long val = strtol({expr}, &endptr, 10);\n'
            code += f'{self.compiler.indent()}if (*endptr != \'\\0\') {{\n'
            self.compiler.indent_level += 1
            code += f'{self.compiler.indent()}fprintf(stderr, "Error: Cannot convert \\"" "%s" "\\" to int\\n", {expr});\n'
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}} else {{\n'
            self.compiler.indent_level += 1
            code += f'{self.compiler.indent()}{temp_var} = (int)val;\n'
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}}  \n'
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}}  \n'
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}}\n'
            if var_name:
                code += f'{self.compiler.indent()}#define {var_name} {temp_var}\n'
                self.compiler.variables[var_name] = "int"
        
        elif target_type == "float":
            code += f'{self.compiler.indent()}float {temp_var} = 0.0;\n'
            code += f'{self.compiler.indent()}{{\n'
            self.compiler.indent_level += 1
            code += f'{self.compiler.indent()}if (strcmp({expr}, "") == 0) {{\n'
            self.compiler.indent_level += 1
            code += f'{self.compiler.indent()}fprintf(stderr, "Error: Cannot convert empty string to float\\n");\n'
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}} else {{\n'
            self.compiler.indent_level += 1
            code += f'{self.compiler.indent()}char* endptr;\n'
            code += f'{self.compiler.indent()}double val = strtod({expr}, &endptr);\n'
            code += f'{self.compiler.indent()}if (*endptr != \'\\0\') {{\n'
            self.compiler.indent_level += 1
            code += f'{self.compiler.indent()}fprintf(stderr, "Error: Cannot convert \\"" "%s" "\\" to float\\n", {expr});\n'
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}} else {{\n'
            self.compiler.indent_level += 1
            code += f'{self.compiler.indent()}{temp_var} = (float)val;\n'
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}}  \n'
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}}  \n'
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}}\n'
            if var_name:
                code += f'{self.compiler.indent()}#define {var_name} {temp_var}\n'
                self.compiler.variables[var_name] = "float"
        
        elif target_type == "char":
            code += f'{self.compiler.indent()}if (strlen({expr}) > 0) {{\n'
            self.compiler.indent_level += 1
            code += f'{self.compiler.indent()}{expr}[1] = \'\\0\';\n'
            self.compiler.indent_level -= 1
            code += f'{self.compiler.indent()}}}  \n'
        
        elif target_type == "string":
            pass
        
        return code

    def compile_c_import(self, statement):
        self.compiler.c_imports.add(statement.header_name)
        return ""
    
    def compile_c_call(self, statement):
        args = ", ".join([self.expr_codegen.compile_expr(arg) for arg in statement.arguments]) if statement.arguments else ""
        return f'{self.compiler.indent()}{statement.func_name}({args});\n'
    
    def compile_inf(self, statement):
        code = f'{self.compiler.indent()}while (1) {{\n'
        self.compiler.indent_level += 1
        for stmt in statement.body:
            code += self.compile_statement(stmt)
        self.compiler.indent_level -= 1
        code += f'{self.compiler.indent()}}}\n'
        return code
    
    def compile_for(self, statement):
        iterable = statement.iterable
        counter = statement.counter
        condition = self.expr_codegen.compile_expr(statement.condition)
        
        code = ""
        
        if isinstance(counter, VarDeclaration):
            counter_name = counter.name
            code += self.compile_var_declaration(counter)
        else:
            counter_name = counter
        
        code += f'{self.compiler.indent()}while ({condition}) {{\n'
        self.compiler.indent_level += 1
        
        for stmt in statement.body:
            code += self.compile_statement(stmt)
        
        code += f'{self.compiler.indent()}{counter_name}++;\n'
        
        self.compiler.indent_level -= 1
        code += f'{self.compiler.indent()}}}\n'
        
        return code

    def compile_struct_var_declaration(self, statement):
        struct_type = statement.struct_type
        var_name = statement.name
        field_values = statement.field_values
        
        self.compiler.variables[var_name] = struct_type
        
        code = f'{self.compiler.indent()}{struct_type} {var_name} = {{'
        field_codes = []
        for field_name, field_value in field_values.items():
            field_codes.append(f'.{field_name} = {self.expr_codegen.compile_expr(field_value)}')
        code += ', '.join(field_codes)
        code += '};\n'
        return code
    
    def compile_struct_field_assignment(self, statement):
        struct_name = statement.struct_name
        field_name = statement.field_name
        value = self.expr_codegen.compile_expr(statement.value)
        return f'{self.compiler.indent()}{struct_name}.{field_name} = {value};\n'

    def compile_pointer_assignment(self, statement):
        pointer_name = statement.pointer
        value = self.expr_codegen.compile_expr(statement.value)
        return f'{self.compiler.indent()}(*{pointer_name}) = {value};\n'
