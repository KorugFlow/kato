from parser.ast import (
    Identifier, NumberLiteral, FloatLiteral, CharLiteral,
    StringLiteral, BinaryOp, ArrayAccess
)
from ..ast import (
    CIdentifier, CNumber, CString, CChar,
    CBinaryOp, CArrayAccess, CFunctionCall
)


class ExpressionConverter:
    def convert_expression(self, c_expr):
        if isinstance(c_expr, CNumber):
            if isinstance(c_expr.value, float):
                return FloatLiteral(c_expr.value)
            return NumberLiteral(c_expr.value)
        elif isinstance(c_expr, CString):
            return StringLiteral(c_expr.value)
        elif isinstance(c_expr, CChar):
            return CharLiteral(c_expr.value)
        elif isinstance(c_expr, CIdentifier):
            return Identifier(c_expr.name)
        elif isinstance(c_expr, CBinaryOp):
            left = self.convert_expression(c_expr.left)
            right = self.convert_expression(c_expr.right)
            return BinaryOp(left, c_expr.operator, right)
        elif isinstance(c_expr, CArrayAccess):
            return ArrayAccess(c_expr.array, self.convert_expression(c_expr.index))
        elif isinstance(c_expr, CFunctionCall):
            if c_expr.name == "printf":
                return StringLiteral("printf_call")
            return Identifier(f"call_{c_expr.name}")
        else:
            return Identifier("unknown")
