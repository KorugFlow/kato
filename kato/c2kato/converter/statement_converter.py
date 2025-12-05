from parser.ast import (
    VarDeclaration, ArrayDeclaration, Assignment,
    IfStatement, WhileStatement, ReturnStatement,
    IncrementStatement, DecrementStatement, PrintStatement,
    SwitchStatement, CaseClause, InptCall
)
from ..ast import (
    CVarDeclaration, CArrayDeclaration, CAssignment,
    CIfStatement, CWhileStatement, CForStatement,
    CReturnStatement, CExpressionStatement, CFunctionCall,
    CSwitchStatement, CCaseClause
)
from .type_mapper import map_c_type_to_kato
from .printf_converter import PrintfConverter


class StatementConverter:
    def __init__(self, expr_converter):
        self.expr_converter = expr_converter
        self.printf_converter = PrintfConverter()
        self.last_printf_output = None
        self.used_stdlib = set()  
    
    def convert_statement(self, c_stmt):
        if c_stmt is None:
            return None
        
        from ..ast import CMultiDeclaration
        if isinstance(c_stmt, CMultiDeclaration):
            results = []
            for decl in c_stmt.declarations:
                converted = self.convert_statement(decl)
                if converted:
                    results.append(converted)
            return results if len(results) > 1 else (results[0] if results else None)
        
        if isinstance(c_stmt, CFunctionCall):
            if c_stmt.name == "printf":
                converted_args = [self.expr_converter.convert_expression(arg) for arg in c_stmt.arguments]
                print_values = self.printf_converter.convert_printf_to_print(converted_args)
                self.last_printf_output = print_values
                return PrintStatement(print_values)
            elif c_stmt.name == "scanf":
                result = self.convert_scanf(c_stmt)
                return result
            
            elif c_stmt.name == "system":
                self.used_stdlib.add("os")
                from parser.ast import CallStatement
                arguments = [self.expr_converter.convert_expression(arg) for arg in c_stmt.arguments] if c_stmt.arguments else []
                return CallStatement("os_system", arguments)
            
            elif c_stmt.name == "getpid":
                self.used_stdlib.add("os")
                from parser.ast import CallStatement
                return CallStatement("os_get_pid", [])
           
            elif c_stmt.name == "remove":
                self.used_stdlib.add("filesystem")
                from parser.ast import CallStatement
                arguments = [self.expr_converter.convert_expression(arg) for arg in c_stmt.arguments] if c_stmt.arguments else []
                return CallStatement("file_delete", arguments)
            else:
                from parser.ast import CallStatement
                arguments = [self.expr_converter.convert_expression(arg) for arg in c_stmt.arguments] if c_stmt.arguments else []
                return CallStatement(c_stmt.name, arguments)
        
        if isinstance(c_stmt, CVarDeclaration):
            from parser.ast import NumberLiteral, FloatLiteral
            kato_type = map_c_type_to_kato(c_stmt.var_type)
            if c_stmt.value:
                value = self.expr_converter.convert_expression(c_stmt.value)
            else:
                if kato_type == "float":
                    value = FloatLiteral(0.0)
                else:
                    value = NumberLiteral(0)
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
            from parser.ast import NumberLiteral, InfStatement
            from ..ast import CNumber
            
            condition = self.expr_converter.convert_expression(c_stmt.condition)
            body = [self.convert_statement(s) for s in c_stmt.body if s]
            
            
            is_infinite = False
            if isinstance(condition, NumberLiteral) and condition.value == 1:
                is_infinite = True
            elif isinstance(c_stmt.condition, CNumber) and c_stmt.condition.value == 1:
                is_infinite = True
            elif isinstance(c_stmt.condition, str) and c_stmt.condition.lower() in ['1', 'true']:
                is_infinite = True
            
            if is_infinite:
                return InfStatement(body)
            
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
        
        elif isinstance(c_stmt, CSwitchStatement):
            expression = self.expr_converter.convert_expression(c_stmt.expression)
            kato_cases = []
            for c_case in c_stmt.cases:
                case_value = self.expr_converter.convert_expression(c_case.value)
                case_body = [self.convert_statement(s) for s in c_case.body if s]
                kato_cases.append(CaseClause(case_value, case_body))
            
            default_body = None
            if c_stmt.default_body:
                default_body = [self.convert_statement(s) for s in c_stmt.default_body if s]
            
            return SwitchStatement(expression, kato_cases, default_body)
        
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
    
    def convert_scanf(self, scanf_call):
        from parser.ast import StringLiteral
        from ..ast import CIdentifier, CString
        
        if len(scanf_call.arguments) < 2:
            return None
        
        var_arg = scanf_call.arguments[1]
        var_name = None
        
        if isinstance(var_arg, CIdentifier):
            var_name = var_arg.name
            if var_name.startswith('&'):
                var_name = var_name[1:]
        elif isinstance(var_arg, str):
            var_name = var_arg
            if var_name.startswith('&'):
                var_name = var_name[1:]
        
        if not var_name:
            return None
        
        prompt_text = ""
        if self.last_printf_output and len(self.last_printf_output) > 0:
            for val in self.last_printf_output:
                if isinstance(val, StringLiteral):
                    prompt_text += val.value
        
        prompt = StringLiteral(prompt_text)
        inpt_call = InptCall(prompt)
        
        return Assignment(var_name, inpt_call)
