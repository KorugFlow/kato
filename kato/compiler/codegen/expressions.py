from parser.ast import (
    StringLiteral, NumberLiteral, FloatLiteral, CharLiteral,
    Identifier, BinaryOp, InptCall, ArrayAccess, FunctionCall,
    ConvertExpression
)


class ExpressionCodegen:
    def __init__(self, compiler):
        self.compiler = compiler
    
    def compile_expr(self, expr, var_type=None):
        if isinstance(expr, StringLiteral):
            escaped_string = expr.value.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r').replace('"', '\\"')
            return f'"{escaped_string}"'
        elif isinstance(expr, CharLiteral):
            if len(expr.value) == 1:
                return f"'{expr.value}'"
            else:
                return f"'{expr.value[0]}'"
        elif isinstance(expr, NumberLiteral):
            return str(expr.value)
        elif isinstance(expr, FloatLiteral):
            return str(expr.value)
        elif isinstance(expr, Identifier):
            return expr.name
        elif isinstance(expr, ArrayAccess):
            index = self.compile_expr(expr.index, var_type)
            return f"{expr.name}[{index}]"
        elif isinstance(expr, BinaryOp):
            left = self.compile_expr(expr.left, var_type)
            right = self.compile_expr(expr.right, var_type)
            return f"({left} {expr.operator} {right})"
        elif isinstance(expr, InptCall):
            prompt = self.compile_expr(expr.prompt, var_type)
            
            if var_type == "int":
                return f"(printf({prompt}), scanf(\"%d\", &(int){{0}}), (int){{0}})"
            elif var_type == "float":
                return f"(printf({prompt}), scanf(\"%f\", &(float){{0.0}}), (float){{0.0}})"
            elif var_type == "char":
                return f"(printf({prompt}), getchar())"
            elif var_type == "string":
                return f"(printf({prompt}), (char[256]){{0}})"
            else:
                return f"(printf({prompt}), 0)"
        elif isinstance(expr, FunctionCall):
            return_type = self.compiler.get_function_return_type(expr.name)
            
            if return_type == "void":
                raise ValueError(f"Cannot use void function '{expr.name}' in expression")
            
            if expr.name == "random":
                if len(expr.arguments) == 2:
                    min_val = self.compile_expr(expr.arguments[0])
                    max_val = self.compile_expr(expr.arguments[1])
                    return f"({min_val} + rand() % (({max_val}) - ({min_val}) + 1))"
                else:
                    return "0"
            else:
                args = ", ".join([self.compile_expr(arg) for arg in expr.arguments])
                return f"{expr.name}({args})"
        elif isinstance(expr, ConvertExpression):
            return f"__convert_temp__"
        else:
            return "0"
