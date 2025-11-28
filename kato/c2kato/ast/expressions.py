from .nodes import CASTNode


class CIdentifier(CASTNode):
    def __init__(self, name):
        self.name = name


class CNumber(CASTNode):
    def __init__(self, value):
        self.value = value


class CString(CASTNode):
    def __init__(self, value):
        self.value = value


class CChar(CASTNode):
    def __init__(self, value):
        self.value = value


class CBinaryOp(CASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class CArrayAccess(CASTNode):
    def __init__(self, array, index):
        self.array = array
        self.index = index


class CFunctionCall(CASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
