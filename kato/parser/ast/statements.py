from .nodes import ASTNode


class Program(ASTNode):
    def __init__(self, functions):
        self.functions = functions


class Function(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body


class PrintStatement(ASTNode):
    def __init__(self, value):
        self.value = value


class ReturnStatement(ASTNode):
    def __init__(self, value):
        self.value = value


class VarDeclaration(ASTNode):
    def __init__(self, var_type, name, value):
        self.var_type = var_type
        self.name = name
        self.value = value


class CallStatement(ASTNode):
    def __init__(self, func_name, arguments):
        self.func_name = func_name
        self.arguments = arguments


class IfStatement(ASTNode):
    def __init__(self, condition, if_body, elif_parts, else_body):
        self.condition = condition
        self.if_body = if_body
        self.elif_parts = elif_parts
        self.else_body = else_body


class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class IncrementStatement(ASTNode):
    def __init__(self, name):
        self.name = name


class DecrementStatement(ASTNode):
    def __init__(self, name):
        self.name = name


class ArrayDeclaration(ASTNode):
    def __init__(self, array_type, name, elements):
        self.array_type = array_type
        self.name = name
        self.elements = elements


class ArrayAssignment(ASTNode):
    def __init__(self, name, index, value):
        self.name = name
        self.index = index
        self.value = value


class SwitchStatement(ASTNode):
    def __init__(self, expression, cases, default_body):
        self.expression = expression
        self.cases = cases
        self.default_body = default_body


class CaseClause(ASTNode):
    def __init__(self, value, body):
        self.value = value
        self.body = body


class ConvertStatement(ASTNode):
    def __init__(self, expression, target_type):
        self.expression = expression
        self.target_type = target_type


class CImportStatement(ASTNode):
    def __init__(self, header_name):
        self.header_name = header_name


class CCallStatement(ASTNode):
    def __init__(self, func_name, arguments):
        self.func_name = func_name
        self.arguments = arguments


class BreakStatement(ASTNode):
    pass


class ContinueStatement(ASTNode):
    pass


class InfStatement(ASTNode):
    def __init__(self, body):
        self.body = body


class StopStatement(ASTNode):
    pass
