#include <stdio.h>
#include <string.h>
#include <stdlib.h>


int main() {
    printf("calculator\n");
    int a;
    printf("enter first number: ");
    scanf("%d", &a);
    int b;
    printf("enter second number: ");
    scanf("%d", &b);
    char op;
    printf("enter operation (+, -, *, /): ");
    scanf(" %c", &op);
    if ((op == '+')) {
        printf("result: %d\n", (a + b));
    } else if ((op == '-')) {
        printf("result: %d\n", (a - b));
    } else if ((op == '*')) {
        printf("result: %d\n", (a * b));
    } else if ((op == '/')) {
        if ((b == 0)) {
            printf("я не дебил\n");
            return 666;
        } else {
            printf("result: %d\n", (a / b));
        }
    } else {
        printf("unknown operation\n");
    }
    return 0;
}

