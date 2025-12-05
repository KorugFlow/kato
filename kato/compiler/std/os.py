OS_FUNCTIONS = {
    "os_kill": {
        "return_type": "int",
        "params": ["int"],
        "c_code": """
int os_kill(int pid) {
    HANDLE hProcess = OpenProcess(PROCESS_TERMINATE, FALSE, pid);
    if (hProcess == NULL) {
        return 0;
    }
    int result = TerminateProcess(hProcess, 0) ? 1 : 0;
    CloseHandle(hProcess);
    return result;
}
"""
    },
    "os_list_processes": {
        "return_type": "string",
        "params": [],
        "c_code": """
char* os_list_processes() {
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnapshot == INVALID_HANDLE_VALUE) {
        return "";
    }
    PROCESSENTRY32 pe32;
    pe32.dwSize = sizeof(PROCESSENTRY32);
    char* result = (char*)malloc(65536);
    result[0] = '\\0';
    if (Process32First(hSnapshot, &pe32)) {
        do {
            char buffer[32];
            sprintf(buffer, "%lu\\n", pe32.th32ProcessID);
            strcat(result, buffer);
        } while (Process32Next(hSnapshot, &pe32));
    }
    CloseHandle(hSnapshot);
    return result;
}
"""
    },
    "os_run": {
        "return_type": "int",
        "params": ["string"],
        "c_code": """
int os_run(const char* path) {
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));
    char cmd[MAX_PATH];
    strcpy(cmd, path);
    if (!CreateProcess(NULL, cmd, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        return 0;
    }
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    return 1;
}
"""
    },
    "os_process_exists": {
        "return_type": "int",
        "params": ["int"],
        "c_code": """
int os_process_exists(int pid) {
    HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, pid);
    if (hProcess == NULL) {
        return 0;
    }
    DWORD exitCode;
    GetExitCodeProcess(hProcess, &exitCode);
    CloseHandle(hProcess);
    return exitCode == STILL_ACTIVE ? 1 : 0;
}
"""
    },
    "os_get_pid": {
        "return_type": "int",
        "params": [],
        "c_code": """
int os_get_pid() {
    return GetCurrentProcessId();
}
"""
    },
    "os_system": {
        "return_type": "int",
        "params": ["string"],
        "c_code": """
int os_system(const char* command) {
    return system(command);
}
"""
    }
}

def get_os_includes():
    return ""

def get_os_functions():
    code = ""
    for func_name, func_info in OS_FUNCTIONS.items():
        code += func_info["c_code"] + "\n"
    return code
