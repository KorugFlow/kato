from parser.ast import (
    VarDeclaration, ArrayDeclaration, Assignment,
    IfStatement, WhileStatement, ReturnStatement,
    IncrementStatement, DecrementStatement, PrintStatement
)
from ..ast import (
    CVarDeclaration, CArrayDeclaration, CAssignment,
    CIfStatement, CWhileStatement, CForStatement,
    CReturnStatement, CExpressionStatement, CFunctionCall
)
from .type_mapper import map_c_type_to_kato
from .printf_converter import PrintfConverter


class StatementConverter:
    def __init__(self, expr_converter):
        self.expr_converter = expr_converter
        self.printf_converter = PrintfConverter()
    
    def convert_statement(self, c_stmt):
        if c_stmt is None:
            return None
        
        if isinstance(c_stmt, CFunctionCall):
            if c_stmt.name == "printf":
                converted_args = [self.expr_converter.convert_expression(arg) for arg in c_stmt.arguments]
                print_values = self.printf_converter.convert_printf_to_print(converted_args)
                return PrintStatement(print_values)
            else:
                from parser.ast import CallStatement
                arguments = [self.expr_converter.convert_expression(arg) for arg in c_stmt.arguments] if c_stmt.arguments else []
                return CallStatement(c_stmt.name, arguments)
        
        if isinstance(c_stmt, CVarDeclaration):
            kato_type = map_c_type_to_kato(c_stmt.var_type)
            value = self.expr_converter.convert_expression(c_stmt.value) if c_stmt.value else None
            return VarDeclaration(kato_type, c_stmt.name, value)
        
        elif isinstance(c_stmt, CArrayDeclaration):
            kato_type = map_c_type_to_kato(c_stmt.array_type)
            elements = [self.expr_converter.convert_expression(v) for v in c_stmt.values] if c_stmt.values else []
            return ArrayDeclaration(kato_type, c_stmt.name, elements)
        
        elif isinstance(c_stmt, CAssignment):
            value = self.expr_converter.convert_expression(c_stmt.value)
            return Assignment(c_stmt.target, value)
        
        elif isinstance(c_stmt, CIfStatement):
            condition = self.expr_converter.convert_expression(c_stmt.condition)
            if_body = [self.convert_statement(s) for s in c_stmt.if_body if s]
            else_body = [self.convert_statement(s) for s in c_stmt.else_body if s] if c_stmt.else_body else None
            return IfStatement(condition, if_body, [], else_body)
        
        elif isinstance(c_stmt, CWhileStatement):
            condition = self.expr_converter.convert_expression(c_stmt.condition)
            body = [self.convert_statement(s) for s in c_stmt.body if s]
            return WhileStatement(condition, body)
        
        elif isinstance(c_stmt, CForStatement):
            init = self.convert_statement(c_stmt.init)
            condition = self.expr_converter.convert_expression(c_stmt.condition)
            body = [self.convert_statement(s) for s in c_stmt.body if s]
            
            if isinstance(c_stmt.increment, str) and "++" in c_stmt.increment:
                var_name = c_stmt.increment.replace("++", "")
                body.append(IncrementStatement(var_name))
            elif isinstance(c_stmt.increment, str) and "--" in c_stmt.increment:
                var_name = c_stmt.increment.replace("--", "")
                body.append(DecrementStatement(var_name))
            
            return WhileStatement(condition, [init] + body if init else body)
        
        elif isinstance(c_stmt, CReturnStatement):
            value = self.expr_converter.convert_expression(c_stmt.value) if c_stmt.value else None
            return ReturnStatement(value)
        
        elif isinstance(c_stmt, CExpressionStatement):
            if isinstance(c_stmt.expression, str):
                if "++" in c_stmt.expression:
                    var_name = c_stmt.expression.replace("++", "")
                    return IncrementStatement(var_name)
                elif "--" in c_stmt.expression:
                    var_name = c_stmt.expression.replace("--", "")
                    return DecrementStatement(var_name)
                elif "printf" in c_stmt.expression:
                    return None
        
        return None
