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
