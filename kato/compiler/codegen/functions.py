class FunctionCodegen:
    def __init__(self, compiler, stmt_codegen):
        self.compiler = compiler
        self.stmt_codegen = stmt_codegen
    
    def get_function_signature(self, function):
        if function.params:
            params_str = ", ".join([f"char* {param}" for param in function.params])
            return f"int {function.name}({params_str})"
        return f"int {function.name}()"
    
    def compile_function(self, function):
        self.compiler.variables = {}
        
        if function.params:
            for param in function.params:
                self.compiler.variables[param] = "string"
            params_str = ", ".join([f"char* {param}" for param in function.params])
            c_code = f"int {function.name}({params_str}) {{\n"
        else:
            c_code = f"int {function.name}() {{\n"
        
        self.compiler.indent_level += 1
        
        for statement in function.body:
            c_code += self.stmt_codegen.compile_statement(statement)
        
        self.compiler.indent_level -= 1
        c_code += "}\n"
        
        return c_code
