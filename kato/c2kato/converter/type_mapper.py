C_TO_KATO_TYPES = {
    "int": "int",
    "float": "float",
    "double": "float",
    "char": "char",
    "char*": "string",
    "void": "int",
}


def map_c_type_to_kato(c_type):
    return C_TO_KATO_TYPES.get(c_type, "int")
