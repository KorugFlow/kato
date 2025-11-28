from parser.ast import Program, Function
from ..ast import CProgram, CFunctionDef
from .expression_converter import ExpressionConverter
from .statement_converter import StatementConverter
from .type_mapper import map_c_type_to_kato


class Converter:
    def __init__(self):
        self.expr_converter = ExpressionConverter()
        self.stmt_converter = StatementConverter(self.expr_converter)
    
    def convert(self, c_ast):
        if not isinstance(c_ast, CProgram):
            raise ValueError("Expected CProgram")
        
        kato_functions = []
        
        for decl in c_ast.declarations:
            if isinstance(decl, CFunctionDef):
                kato_func = self.convert_function(decl)
                kato_functions.append(kato_func)
        
        return Program(kato_functions)
    
    def convert_function(self, c_func):
        name = c_func.name
        params = [param[1] for param in c_func.params]
        
        body = []
        for stmt in c_func.body:
            converted = self.stmt_converter.convert_statement(stmt)
            if converted:
                body.append(converted)
        
        return Function(name, params, body)
