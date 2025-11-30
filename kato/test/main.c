#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

void welcome();

void welcome() {
    printf("hello to kato! hello, bro!");
}

int main() {
    srand(time(NULL));
    printf("hello");
    welcome();
    return 0;
}

