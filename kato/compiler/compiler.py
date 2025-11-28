from .codegen import ExpressionCodegen, StatementCodegen, FunctionCodegen


class CCompiler:
    def __init__(self, ast):
        self.ast = ast
        self.indent_level = 0
        self.variables = {}
        
        self.expr_codegen = ExpressionCodegen(self)
        self.stmt_codegen = StatementCodegen(self, self.expr_codegen)
        self.func_codegen = FunctionCodegen(self, self.stmt_codegen)
    
    def indent(self):
        return "    " * self.indent_level
    
    def compile(self):
        c_code = "#include <stdio.h>\n"
        c_code += "#include <string.h>\n"
        c_code += "#include <stdlib.h>\n\n"
        
        for function in self.ast.functions:
            if function.name != "main":
                c_code += self.func_codegen.get_function_signature(function) + ";\n"
        
        c_code += "\n"
        
        for function in self.ast.functions:
            c_code += self.func_codegen.compile_function(function)
            c_code += "\n"
        
        return c_code
