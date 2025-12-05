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
        "return_type": "string",
        "params": ["string"],
        "c_code": """
char* os_system(const char* command) {
    FILE* pipe = _popen(command, "r");
    if (!pipe) return "";
    char* result = (char*)malloc(65536);
    result[0] = '\\0';
    char buffer[256];
    while (fgets(buffer, sizeof(buffer), pipe)) {
        strcat(result, buffer);
    }
    _pclose(pipe);
    return result;
}
"""
    },
    "os_cmd": {
        "return_type": "string",
        "params": ["string"],
        "c_code": """
char* os_cmd(const char* command) {
    char cmd[512];
    sprintf(cmd, "cmd /c %s", command);
    FILE* pipe = _popen(cmd, "r");
    if (!pipe) return "";
    char* result = (char*)malloc(65536);
    result[0] = '\\0';
    char buffer[256];
    while (fgets(buffer, sizeof(buffer), pipe)) {
        strcat(result, buffer);
    }
    _pclose(pipe);
    return result;
}
"""
    },
    "os_is_admin": {
        "return_type": "int",
        "params": [],
        "c_code": """
int os_is_admin() {
    BOOL isAdmin = FALSE;
    PSID adminGroup = NULL;
    SID_IDENTIFIER_AUTHORITY ntAuthority = SECURITY_NT_AUTHORITY;
    if (AllocateAndInitializeSid(&ntAuthority, 2, SECURITY_BUILTIN_DOMAIN_RID, DOMAIN_ALIAS_RID_ADMINS, 0, 0, 0, 0, 0, 0, &adminGroup)) {
        CheckTokenMembership(NULL, adminGroup, &isAdmin);
        FreeSid(adminGroup);
    }
    return isAdmin ? 1 : 0;
}
"""
    },
    "os_runas": {
        "return_type": "int",
        "params": ["string"],
        "c_code": """
int os_runas(const char* mode) {
    char exePath[MAX_PATH];
    GetModuleFileNameA(NULL, exePath, MAX_PATH);
    SHELLEXECUTEINFOA sei = {0};
    sei.cbSize = sizeof(sei);
    sei.fMask = SEE_MASK_NOCLOSEPROCESS;
    sei.lpVerb = (strcmp(mode, "admin") == 0) ? "runas" : "open";
    sei.lpFile = exePath;
    sei.nShow = SW_NORMAL;
    if (ShellExecuteExA(&sei)) {
        if (sei.hProcess) {
            CloseHandle(sei.hProcess);
        }
        return 1;
    }
    return 0;
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
