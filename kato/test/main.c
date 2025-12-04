#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>


int main() {
    srand(time(NULL));
    int a;
    printf("Enter a number 1 : ");
    scanf("%d", &a);
    int b;
    printf("Enter a number 2 : ");
    scanf("%d", &b);
    char c;
    printf("Enter a op : ");
    scanf(" %c", &c);
    switch (c) {
        case '+':
            printf("%d", (a + b));
            break;
            break;
        case '-':
            printf("%d", (a - b));
            break;
            break;
        case '*':
            printf("%d", (a * b));
            break;
            break;
        case '/':
            printf("%d", (a / b));
            break;
            break;
    }
    return 0;
}

