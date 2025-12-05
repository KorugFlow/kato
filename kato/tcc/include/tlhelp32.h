#ifndef _TLHELP32_H
#define _TLHELP32_H

#include <windows.h>

#define TH32CS_SNAPPROCESS 0x00000002

typedef struct tagPROCESSENTRY32 {
    DWORD dwSize;
    DWORD cntUsage;
    DWORD th32ProcessID;
    ULONG_PTR th32DefaultHeapID;
    DWORD th32ModuleID;
    DWORD cntThreads;
    DWORD th32ParentProcessID;
    LONG pcPriClassBase;
    DWORD dwFlags;
    CHAR szExeFile[260];
} PROCESSENTRY32, *PPROCESSENTRY32;

HANDLE WINAPI CreateToolhelp32Snapshot(DWORD dwFlags, DWORD th32ProcessID);
BOOL WINAPI Process32First(HANDLE hSnapshot, PPROCESSENTRY32 lppe);
BOOL WINAPI Process32Next(HANDLE hSnapshot, PPROCESSENTRY32 lppe);

#endif
