#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int add(int a, int b);
char* save_var_allias(char* text);

int add(int a, int b) {
    return (a + b);
}

char* save_var_allias(char* text) {
    return text;
}

int main() {
    add(8, 2);
    char* b = save_var_allias("hello");
    printf("%s", b);
}

