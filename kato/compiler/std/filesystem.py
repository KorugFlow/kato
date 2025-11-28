FILESYSTEM_FUNCTIONS = {
    "file_read": {
        "return_type": "string",
        "params": ["string"],
        "c_code": """
char* file_read(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        return "";
    }
    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    fseek(file, 0, SEEK_SET);
    char* content = (char*)malloc(size + 1);
    fread(content, 1, size, file);
    content[size] = '\\0';
    fclose(file);
    return content;
}
"""
    },
    "file_write": {
        "return_type": "int",
        "params": ["string", "string"],
        "c_code": """
int file_write(const char* filename, const char* content) {
    FILE* file = fopen(filename, "w");
    if (file == NULL) {
        return 0;
    }
    fputs(content, file);
    fclose(file);
    return 1;
}
"""
    },
    "file_append": {
        "return_type": "int",
        "params": ["string", "string"],
        "c_code": """
int file_append(const char* filename, const char* content) {
    FILE* file = fopen(filename, "a");
    if (file == NULL) {
        return 0;
    }
    fputs(content, file);
    fclose(file);
    return 1;
}
"""
    },
    "file_exists": {
        "return_type": "int",
        "params": ["string"],
        "c_code": """
int file_exists(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        return 0;
    }
    fclose(file);
    return 1;
}
"""
    },
    "file_delete": {
        "return_type": "int",
        "params": ["string"],
        "c_code": """
int file_delete(const char* filename) {
    return remove(filename) == 0 ? 1 : 0;
}
"""
    }
}

def get_filesystem_includes():
    return ""

def get_filesystem_functions():
    code = ""
    for func_name, func_info in FILESYSTEM_FUNCTIONS.items():
        code += func_info["c_code"] + "\n"
    return code
