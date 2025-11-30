#include <stdio.h>
#include <string.h>
#include <stdlib.h>


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
    content[size] = '\0';
    fclose(file);
    return content;
}


int file_write(const char* filename, const char* content) {
    FILE* file = fopen(filename, "w");
    if (file == NULL) {
        return 0;
    }
    fputs(content, file);
    fclose(file);
    return 1;
}


int file_append(const char* filename, const char* content) {
    FILE* file = fopen(filename, "a");
    if (file == NULL) {
        return 0;
    }
    fputs(content, file);
    fclose(file);
    return 1;
}


int file_exists(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        return 0;
    }
    fclose(file);
    return 1;
}


int file_delete(const char* filename) {
    return remove(filename) == 0 ? 1 : 0;
}


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

