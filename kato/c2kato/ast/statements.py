from .nodes import CASTNode


class CProgram(CASTNode):
    def __init__(self, declarations):
        self.declarations = declarations


class CFunctionDef(CASTNode):
    def __init__(self, return_type, name, params, body):
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body


class CVarDeclaration(CASTNode):
    def __init__(self, var_type, name, value=None):
        self.var_type = var_type
        self.name = name
        self.value = value


class CArrayDeclaration(CASTNode):
    def __init__(self, array_type, name, size, values=None):
        self.array_type = array_type
        self.name = name
        self.size = size
        self.values = values


class CAssignment(CASTNode):
    def __init__(self, target, value):
        self.target = target
        self.value = value


class CIfStatement(CASTNode):
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body


class CWhileStatement(CASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class CForStatement(CASTNode):
    def __init__(self, init, condition, increment, body):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body


class CReturnStatement(CASTNode):
    def __init__(self, value):
        self.value = value


class CExpressionStatement(CASTNode):
    def __init__(self, expression):
        self.expression = expression
