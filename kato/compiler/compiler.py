from .codegen import ExpressionCodegen, StatementCodegen, FunctionCodegen


class CCompiler:
    def __init__(self, ast, stdlib_imports=None):
        self.ast = ast
        self.indent_level = 0
        self.variables = {}
        self.stdlib_imports = stdlib_imports or set()
        
        self.expr_codegen = ExpressionCodegen(self)
        self.stmt_codegen = StatementCodegen(self, self.expr_codegen)
        self.func_codegen = FunctionCodegen(self, self.stmt_codegen)
    
    def indent(self):
        return "    " * self.indent_level
    
    def compile(self):
        c_code = "#include <stdio.h>\n"
        c_code += "#include <string.h>\n"
        c_code += "#include <stdlib.h>\n\n"
        
        if "filesystem" in self.stdlib_imports:
            from .std.filesystem import get_filesystem_functions
            c_code += get_filesystem_functions() + "\n"
        
        for function in self.ast.functions:
            if function.name != "main":
                c_code += self.func_codegen.get_function_signature(function) + ";\n"
        
        c_code += "\n"
        
        for function in self.ast.functions:
            c_code += self.func_codegen.compile_function(function)
            c_code += "\n"
        
        return c_code
