from parser.ast import (
    Program, Function, VarDeclaration, ArrayDeclaration,
    Assignment, IfStatement, WhileStatement,
    ReturnStatement, IncrementStatement, DecrementStatement,
    PrintStatement, CallStatement, SwitchStatement, CaseClause,
    StringLiteral, NumberLiteral, FloatLiteral, CharLiteral,
    Identifier, BinaryOp, ArrayAccess, InptCall, InfStatement, StopStatement
)
from .formatter import KatoFormatter


class KatoGenerator:
    def __init__(self):
        self.formatter = KatoFormatter()
        self.indent_level = 0
    
    def indent(self):
        return "    " * self.indent_level
    
    def generate(self, kato_ast):
        if not isinstance(kato_ast, Program):
            raise ValueError("Expected Program")
        
        code = []
        
        for func in kato_ast.functions:
            code.append(self.generate_function(func))
            code.append("")
        
        return "\n".join(code)
    
    def generate_function(self, func):
        params_str = ", ".join(func.params) if func.params else ""
        code = f"func {func.name}({params_str}) {{\n"
        
        self.indent_level += 1
        
        for stmt in func.body:
            stmt_code = self.generate_statement(stmt)
            if stmt_code:
                code += stmt_code
        
        self.indent_level -= 1
        code += "}\n"
        
        return code
    
    def generate_statement(self, stmt):
        if isinstance(stmt, VarDeclaration):
            value_str = self.generate_expression(stmt.value) if stmt.value else "0"
            return f"{self.indent()}var {stmt.var_type} {stmt.name} = {value_str};\n"
        
        elif isinstance(stmt, ArrayDeclaration):
            elements_str = ", ".join([self.generate_expression(e) for e in stmt.elements])
            return f"{self.indent()}mass {stmt.array_type} {stmt.name} = {{{elements_str}}};\n"
        
        elif isinstance(stmt, Assignment):
            value_str = self.generate_expression(stmt.value)
            return f"{self.indent()}{stmt.name} = {value_str};\n"
        
        elif isinstance(stmt, IfStatement):
            condition_str = self.generate_expression(stmt.condition)
            
            if condition_str.startswith("(") and condition_str.endswith(")"):
                condition_str = condition_str[1:-1]
            
            code = f"{self.indent()}if ({condition_str}) {{\n"
            
            self.indent_level += 1
            for s in stmt.if_body:
                code += self.generate_statement(s)
            self.indent_level -= 1
            
            code += f"{self.indent()}}}"
            
            if stmt.else_body:
                code += " else {\n"
                self.indent_level += 1
                for s in stmt.else_body:
                    code += self.generate_statement(s)
                self.indent_level -= 1
                code += f"{self.indent()}}}"
            
            code += "\n"
            return code
        
        elif isinstance(stmt, InfStatement):
            code = f"{self.indent()}inf {{\n"
            
            self.indent_level += 1
            for s in stmt.body:
                code += self.generate_statement(s)
            self.indent_level -= 1
            
            code += f"{self.indent()}}}\n"
            return code
        
        elif isinstance(stmt, WhileStatement):
            condition_str = self.generate_expression(stmt.condition)
            
            if condition_str.startswith("(") and condition_str.endswith(")"):
                condition_str = condition_str[1:-1]
            
            code = f"{self.indent()}while ({condition_str}) {{\n"
            
            self.indent_level += 1
            for s in stmt.body:
                code += self.generate_statement(s)
            self.indent_level -= 1
            
            code += f"{self.indent()}}}\n"
            return code
        
        elif isinstance(stmt, ReturnStatement):
            value_str = self.generate_expression(stmt.value) if stmt.value else "0"
            return f"{self.indent()}return {value_str};\n"
        
        elif isinstance(stmt, IncrementStatement):
            return f"{self.indent()}{stmt.name}++;\n"
        
        elif isinstance(stmt, DecrementStatement):
            return f"{self.indent()}{stmt.name}--;\n"
        
        elif isinstance(stmt, StopStatement):
            return f"{self.indent()}stop;\n"
        
        elif isinstance(stmt, PrintStatement):
            values = stmt.value if isinstance(stmt.value, list) else [stmt.value]
            
            result_parts = []
            for v in values:
                if isinstance(v, StringLiteral):
                    result_parts.append(f'"{v.value}"')
                elif isinstance(v, Identifier):
                    result_parts.append(v.name)
                elif isinstance(v, BinaryOp):
                    result_parts.append(self.generate_expression(v))
                else:
                    result_parts.append(self.generate_expression(v))
            
            values_str = " ".join(result_parts)
            return f"{self.indent()}print({values_str});\n"
        
        elif isinstance(stmt, CallStatement):
            args_str = ", ".join([self.generate_expression(arg) for arg in stmt.arguments]) if stmt.arguments else ""
            return f"{self.indent()}call {stmt.func_name}({args_str});\n"
        
        elif isinstance(stmt, SwitchStatement):
            expr_str = self.generate_expression(stmt.expression)
            
            code = f"{self.indent()}switch ({expr_str}) {{\n"
            self.indent_level += 1
            
            for case in stmt.cases:
                case_value_str = self.generate_expression(case.value)
                code += f"{self.indent()}case {case_value_str}\n"
                
                self.indent_level += 1
                for s in case.body:
                    code += self.generate_statement(s)
                self.indent_level -= 1
            
            if stmt.default_body:
                code += f"{self.indent()}default {{\n"
                self.indent_level += 1
                for s in stmt.default_body:
                    code += self.generate_statement(s)
                self.indent_level -= 1
                code += f"{self.indent()}}}\n"
            
            self.indent_level -= 1
            code += f"{self.indent()}}}\n"
            return code
        
        return ""
    
    def generate_expression(self, expr):
        from parser.ast import FunctionCall
        
        if isinstance(expr, NumberLiteral):
            return str(expr.value)
        elif isinstance(expr, FloatLiteral):
            return str(expr.value)
        elif isinstance(expr, StringLiteral):
            return f'"{expr.value}"'
        elif isinstance(expr, CharLiteral):
            return f"'{expr.value}'"
        elif isinstance(expr, Identifier):
            return expr.name
        elif isinstance(expr, FunctionCall):
            args_str = ", ".join([self.generate_expression(arg) for arg in expr.arguments]) if expr.arguments else ""
            return f"{expr.name}({args_str})"
        elif isinstance(expr, BinaryOp):
            left = self.generate_expression(expr.left)
            right = self.generate_expression(expr.right)
            
            if left.startswith("(") and left.endswith(")"):
                left = left[1:-1]
            if right.startswith("(") and right.endswith(")"):
                right = right[1:-1]
            
            return f"{left} {expr.operator} {right}"
        elif isinstance(expr, ArrayAccess):
            index = self.generate_expression(expr.index)
            return f"{expr.name}[{index}]"
        elif isinstance(expr, InptCall):
            prompt = self.generate_expression(expr.prompt)
            return f"inpt({prompt})"
        else:
            return "0"
