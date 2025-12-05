#ifndef _SHELLAPI_H
#define _SHELLAPI_H

#include <windows.h>

#define SEE_MASK_NOCLOSEPROCESS 0x00000040
#define SW_NORMAL 1

typedef struct _SHELLEXECUTEINFOA {
    DWORD cbSize;
    ULONG fMask;
    HWND hwnd;
    LPCSTR lpVerb;
    LPCSTR lpFile;
    LPCSTR lpParameters;
    LPCSTR lpDirectory;
    int nShow;
    HINSTANCE hInstApp;
    LPVOID lpIDList;
    LPCSTR lpClass;
    HKEY hkeyClass;
    DWORD dwHotKey;
    union {
        HANDLE hIcon;
        HANDLE hMonitor;
    } DUMMYUNIONNAME;
    HANDLE hProcess;
} SHELLEXECUTEINFOA, *LPSHELLEXECUTEINFOA;

BOOL WINAPI ShellExecuteExA(LPSHELLEXECUTEINFOA lpExecInfo);

#endif
