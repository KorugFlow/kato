from .nodes import ASTNode


class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class NumberLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class FloatLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class CharLiteral(ASTNode):
    def __init__(self, value):
        self.value = value


class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name


class ArrayAccess(ASTNode):
    def __init__(self, name, index):
        self.name = name
        self.index = index


class BinaryOp(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class InptCall(ASTNode):
    def __init__(self, prompt):
        self.prompt = prompt


class FunctionCall(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class ConvertExpression(ASTNode):
    def __init__(self, expression, target_type):
        self.expression = expression
        self.target_type = target_type


class FindCall(ASTNode):
    def __init__(self, target, pattern):
        self.target = target
        self.pattern = pattern
