from parser.ast import (
    Program, Function, PrintStatement, ReturnStatement,
    VarDeclaration, CallStatement
)


class Optimizer:
    def __init__(self, ast):
        self.ast = ast
    
    def optimize(self):
        optimized_functions = []
        
        for function in self.ast.functions:
            if function.name == "main":
                optimized_functions.append(self.optimize_main(function))
            else:
                optimized_functions.append(function)
        
        optimized_program = Program(optimized_functions)
        
        if hasattr(self.ast, 'c_imports'):
            optimized_program.c_imports = self.ast.c_imports
        
        return optimized_program
    
    def optimize_main(self, function):
        optimized_body = []
        found_return = False
        
        for statement in function.body:
            if found_return:
                break
            
            optimized_body.append(statement)
            
            if isinstance(statement, ReturnStatement):
                found_return = True
        
        return Function(function.name, function.params, optimized_body)
