from parser.ast import (
    Program, Function, VarDeclaration, ArrayDeclaration,
    Assignment, IfStatement, WhileStatement,
    ReturnStatement, IncrementStatement, DecrementStatement,
    PrintStatement, CallStatement,
    StringLiteral, NumberLiteral, FloatLiteral, CharLiteral,
    Identifier, BinaryOp, ArrayAccess
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
        
        elif isinstance(stmt, PrintStatement):
            values = stmt.value if isinstance(stmt.value, list) else [stmt.value]
            values_str = " ".join([self.generate_expression(v) for v in values])
            return f"{self.indent()}print({values_str});\n"
        
        return ""
    
    def generate_expression(self, expr):
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
        else:
            return "0"
