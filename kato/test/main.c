#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>


int main() {
    srand(time(NULL));
    MessageBoxA(0, "Hello from Kato!", "Message", 0);
    return 0;
}

