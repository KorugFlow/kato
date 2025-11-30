#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>


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



int main() {
    srand(time(NULL));
    char* score_file = "score.txt";
    int best_score = 0;
    printf("%s", file_read(score_file));
    if ((file_exists(score_file) == 1)) {
        char* content = file_read(score_file);
        int __convert_temp_content = 0;
        {
            if (strcmp(content, "") == 0) {
                fprintf(stderr, "Error: Cannot convert empty string to int\n");
            } else {
                char* endptr;
                long val = strtol(content, &endptr, 10);
                if (*endptr != '\0') {
                    fprintf(stderr, "Error: Cannot convert \"" "%s" "\" to int\n", content);
                } else {
                    __convert_temp_content = (int)val;
                }  
            }  
        }
        #define content __convert_temp_content
        best_score = content;
    }
    printf("Welcome to 'Guess the Number'!\n");
    printf("I have chosen a number from 1 to 100. Try to guess it.\n");
    int number = (1 + rand() % ((100) - (1) + 1));
    int guess = 0;
    int attempts = 0;
    while ((guess != number)) {
        printf("Your guess: ");
        scanf("%d", &guess);
        attempts++;
        if ((guess < number)) {
            printf("The number is higher!\n");
        } else if ((guess > number)) {
            printf("The number is lower!\n");
        }
    }
    printf("Congratulations! You guessed the number in %d attempts.\n", attempts);
    if (((best_score == 0) || (attempts < best_score))) {
        best_score = attempts;
        char* best_str;
        {
            best_str = (char*)malloc(32);
            sprintf(best_str, "%d", best_score);
        }
        file_write(score_file, best_str);
        printf("New record!\n");
    } else {
        printf("Best record: %d attempts\n", best_score);
    }
    return 0;
}

