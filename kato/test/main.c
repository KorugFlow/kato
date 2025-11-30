#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int calc(int a, int b, int op);

int calc(int a, int b, int op) {
    if ((op == '+')) {
        printf("Result: %d + %d = %d\n", a, b, (a + b));
    } else if ((op == '-')) {
        printf("Result: %d - %d = %d\n", a, b, (a - b));
    } else if ((op == '*')) {
        printf("Result: %d * %d = %d\n", a, b, (a * b));
    } else if ((op == '/')) {
        printf("Result: %d / %d = %d\n", a, b, (a / b));
    } else if ((op == '%')) {
        printf("Result: %d % %d = %d\n", a, b, (a % b));
    } else {
        printf("Ты чё за хуйню ввёл?\n");
    }
}

int main() {
    float a;
    printf("Enter first number: ");
    scanf("%f", &a);
    float b;
    printf("Enter second number: ");
    scanf("%f", &b);
    char op;
    printf("Enter operator (+ - * / %): ");
    scanf(" %c", &op);
    calc(a, b, op);
    return 0;
}

