from parser.parser import (
    Program, Function, PrintStatement, ReturnStatement,
    StringLiteral, NumberLiteral
)


class CCompiler:
    def __init__(self, ast):
        self.ast = ast
        self.indent_level = 0
    
    def indent(self):
        return "    " * self.indent_level
    
    def compile(self):
        c_code = "#include <stdio.h>\n\n"
        
        for function in self.ast.functions:
            c_code += self.compile_function(function)
            c_code += "\n"
        
        return c_code
    
    def compile_function(self, function):
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
    
    def compile_print(self, statement):
        value = statement.value
        
        if isinstance(value, StringLiteral):
            return f'{self.indent()}printf("{value.value}");\n'
        elif isinstance(value, NumberLiteral):
            return f'{self.indent()}printf("%d", {value.value});\n'
    
    def compile_return(self, statement):
        value = statement.value
        
        if isinstance(value, NumberLiteral):
            return f'{self.indent()}return {value.value};\n'
        elif isinstance(value, StringLiteral):
            return f'{self.indent()}return 0;\n'
