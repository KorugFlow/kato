class FunctionCodegen:
    def __init__(self, compiler, stmt_codegen):
        self.compiler = compiler
        self.stmt_codegen = stmt_codegen
    
    def infer_param_types(self, function, ast):
        from parser.ast import CallStatement, VarDeclaration, NumberLiteral, FloatLiteral, StringLiteral, CharLiteral, Identifier, FunctionCall
        
        param_types = {param: "int" for param in function.params}
        
        def check_statement(statement):
            if isinstance(statement, CallStatement) and statement.func_name == function.name:
                if statement.arguments:
                    for i, arg in enumerate(statement.arguments):
                        if i < len(function.params):
                            param_name = function.params[i]
                            if isinstance(arg, NumberLiteral):
                                if param_types[param_name] != "string" and param_types[param_name] != "char":
                                    param_types[param_name] = "int"
                            elif isinstance(arg, FloatLiteral):
                                if param_types[param_name] != "string" and param_types[param_name] != "char":
                                    param_types[param_name] = "float"
                            elif isinstance(arg, StringLiteral):
                                param_types[param_name] = "string"
                            elif isinstance(arg, CharLiteral):
                                param_types[param_name] = "char"
            elif isinstance(statement, VarDeclaration):
                if isinstance(statement.value, FunctionCall) and statement.value.name == function.name:
                    if statement.value.arguments:
                        for i, arg in enumerate(statement.value.arguments):
                            if i < len(function.params):
                                param_name = function.params[i]
                                if isinstance(arg, NumberLiteral):
                                    if param_types[param_name] != "string" and param_types[param_name] != "char":
                                        param_types[param_name] = "int"
                                elif isinstance(arg, FloatLiteral):
                                    if param_types[param_name] != "string" and param_types[param_name] != "char":
                                        param_types[param_name] = "float"
                                elif isinstance(arg, StringLiteral):
                                    param_types[param_name] = "string"
                                elif isinstance(arg, CharLiteral):
                                    param_types[param_name] = "char"
        
        for func in ast.functions:
            for statement in func.body:
                check_statement(statement)
        
        return param_types
    
    def infer_return_type(self, function):
        from parser.ast import ReturnStatement, Identifier, StringLiteral, CharLiteral, FloatLiteral
        
        if function.name == "main":
            return "int"
        
        param_types = getattr(function, 'param_types', {})
        has_return_with_value = False
        
        for statement in function.body:
            if isinstance(statement, ReturnStatement):
                if statement.value:
                    has_return_with_value = True
                    if isinstance(statement.value, Identifier):
                        if statement.value.name in param_types:
                            return param_types[statement.value.name]
                    elif isinstance(statement.value, StringLiteral):
                        return "string"
                    elif isinstance(statement.value, CharLiteral):
                        return "char"
                    elif isinstance(statement.value, FloatLiteral):
                        return "float"
        
        return "void" if not has_return_with_value else "int"
    
    def get_function_signature(self, function):
        return_type = getattr(function, 'return_type', 'void')
        c_type_map = {"int": "int", "float": "float", "char": "char", "string": "char*", "void": "void"}
        c_return_type = c_type_map.get(return_type, 'int')
        
        if function.params:
            param_types = getattr(function, 'param_types', {param: "int" for param in function.params})
            params_str = ", ".join([f"{c_type_map.get(param_types.get(param, 'int'), 'int')} {param}" for param in function.params])
            return f"{c_return_type} {function.name}({params_str})"
        return f"{c_return_type} {function.name}()"
    
    def compile_function(self, function):
        from parser.ast import ReturnStatement
        
        self.compiler.variables = {}
        
        return_type = getattr(function, 'return_type', 'void')
        c_type_map = {"int": "int", "float": "float", "char": "char", "string": "char*", "void": "void"}
        c_return_type = c_type_map.get(return_type, 'int')
        
        if function.params:
            param_types = getattr(function, 'param_types', {param: "int" for param in function.params})
            for param in function.params:
                self.compiler.variables[param] = param_types.get(param, "int")
            
            params_str = ", ".join([f"{c_type_map.get(param_types.get(param, 'int'), 'int')} {param}" for param in function.params])
            c_code = f"{c_return_type} {function.name}({params_str}) {{\n"
        else:
            c_code = f"{c_return_type} {function.name}() {{\n"
        
        self.compiler.indent_level += 1
        
        if function.name == "main":
            c_code += self.compiler.indent() + "srand(time(NULL));\n"
        
        for statement in function.body:
            c_code += self.stmt_codegen.compile_statement(statement)
        
        self.compiler.indent_level -= 1
        has_return = any(isinstance(stmt, ReturnStatement) for stmt in function.body)
        if return_type != "void" and not has_return:
            c_code += self.compiler.indent() + "return 0;\n"
        c_code += "}\n"
        
        return c_code
