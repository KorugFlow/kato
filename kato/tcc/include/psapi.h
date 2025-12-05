#ifndef _PSAPI_H
#define _PSAPI_H

#include <windows.h>

BOOL WINAPI EnumProcesses(DWORD *lpidProcess, DWORD cb, LPDWORD lpcbNeeded);

#endif
