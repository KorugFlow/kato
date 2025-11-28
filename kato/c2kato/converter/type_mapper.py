C_TO_KATO_TYPES = {
    "int": "int",
    "float": "float",
    "char": "char",
    "void": "int",
}


def map_c_type_to_kato(c_type):
    return C_TO_KATO_TYPES.get(c_type, "int")
