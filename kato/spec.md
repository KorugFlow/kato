Kato - простой яп написанный на пайтон который компилируеться в C. При возможности компилятор kato будет автоматически комилировать C в .exe если доступны компиляторы в Path.

## Переменные

Kato поддерживает 4 типа переменных:
- `int` - целое число
- `float` - число с плавающей точкой
- `char` - один символ (как в C). **ВАЖНО:** char литералы должны быть в одинарных кавычках `'a'`
- `string` - строка (как char* в C). Строки должны быть в двойных кавычках `"text"`

Объявление переменных:
```
var type name = значение;
```

Изменение переменных:
```
x = 30;
```

Пример:
```
var int x = 20;
var float pi = 3.14;
var char letter = 'A';      // одинарные кавычки для char!
var string text = "Hello";  // двойные кавычки для string!
x = 50;
```

## Массивы

Объявление массивов:
```
mass type name = {элемент1, элемент2, элемент3};
```

Типы массивов: `int`, `float`, `char`, `string`

Доступ к элементам:
```
mass int numbers = {1, 2, 3, 4, 5};
print(*numbers[0]*);  // выведет 1
print("Value: *numbers[2]*\n");  // выведет "Value: 3"
```

Изменение элементов:
```
numbers[0] = 10;
```

Пример:
```
mass int arr = {10, 20, 30};
var int i = 0;
while (i < 3) {
    print(*arr[i]* "\n");
    i++;
}
```

## Функция print

Функция print в Kato работает не как в C (без %). Для вывода переменных используются идентификаторы `*var*`:

```
var int age = 20;
print("My age is: *age*\n");
```



print может выводить:
- Строки: `print("Hello\n");`
- Числа: `print(20);`
- Переменные напрямую: `print(x);`
- Переменные через `*var*`: `print(*x*);` (только для int и float)
- Переменные в строке через идентификаторы: `print("Value: *x*");`
- Арифметические выражения: `print(*x* + *y*);` или `print(x + y);`
- Несколько значений: `print("hello" 20 "how are you\n");`

## Функция inpt

Функция inpt используется для ввода данных. Тип возвращаемого значения определяется автоматически по типу переменной:

```
var int a = inpt("enter number");
var float b = inpt("enter float");
var char c = inpt("enter char");
var string s = inpt("enter text");
```

**ВАЖНО:** inpt можно использовать только при объявлении или изменении переменных!

## Условия

Kato поддерживает условные операторы:

```
if условие {
    // код
}
elif условие {
    // код
}
else {
    // код
}
```

Операторы сравнения:
- `==` - равно
- `!=` - не равно
- `<` - меньше
- `>` - больше
- `<=` - меньше или равно
- `>=` - больше или равно

Пример:
```
var int x = 10;
if x > 5 {
    print("x больше 5\n");
}
elif x == 5 {
    print("x равно 5\n");
}
else {
    print("x меньше 5\n");
}

var char op = '+';
if op == '+' {  // char сравнение в одинарных кавычках!
    print("plus\n");
}
```

## Арифметика

Kato поддерживает арифметические операции:
- `+` - сложение
- `-` - вычитание
- `*` - умножение
- `/` - деление
- `//` - целочисленное деление
- `%` - остаток от деления

Примеры:
```
var int x = 20;
var int b = 10;
var int sum = *x* + *b*;
var int result = (*x* + *b*) * 2;
print(*x* + *b*);
```

## Пользовательские функции

Можно создавать свои функции. Типы функций динамические.

Объявление функции:
```
func name(arg1, arg2) {
    // код
}
```

Вызов функции через `call`:
```
call name(arg1, arg2);
```

Аргументы функций могут быть только типов: `int`, `float`, `string`, `char`.

Пример:
```
func printF(text) {
    print(text);
}

func main() {
    call printF("hello world\n");
}
```

## Циклы

Kato поддерживает цикл while:

```
var int i = 0;
while (i < 10) {
    print(*i* "\n");
    i++;
}
```

## Инкремент и декремент

Увеличение и уменьшение переменной на 1:
- `var++;` - увеличить на 1
- `var--;` - уменьшить на 1

Пример:
```
var int x = 5;
x++;  // x = 6
x--;  // x = 5
```

## Комментарии

Однострочные комментарии:
```
// это комментарий
var int x = 20; // комментарий после кода
```

## Правила и ограничения

- После каждой команды обязательно писать `;`
- Функция `main` обязательна и не должна иметь аргументов
- Нельзя дублировать имена функций (встроенных или пользовательских)
- Функции должны быть объявлены до их вызова (компилятор читает сверху вниз)
- Вызов функции обязательно должен иметь скобки `()`, даже если аргументов нет
- Весь код должен быть внутри функций
- inpt можно использовать только при объявлении или изменении переменных

## Импорт функций

Kato поддерживает импорт функций из других файлов через .kh (Kato Header) файлы:

**welcome.kato:**
```kato
func welcome() {
    print("Hello to Kato!\n");
}
```

**welcome.kh:**
```
$export welcome from welcome.kato
```

**main.kato:**
```kato
import welcome.kh;

func main() {
    call welcome();
    return 0;
}
```

Правила:
- Все пути относительные
- Нельзя импортировать функцию `main`
- Нельзя дублировать имена функций
- Если файл не найден - ошибка

## c2kato - Транспилятор из C в Kato

Kato включает транспилятор из C в Kato:

```bash
python kato/main.py input.c -c2kato -o output
```

c2kato конвертирует базовый C код в синтаксис Kato:
- `int`, `float`, `char` типы → Kato типы
- `printf` → `print` с автоматической конвертацией `%d`, `%s` в `*var*`
- `for` циклы → `while` циклы
- Массивы C → массивы Kato
- Функции C → функции Kato

Пример:
```c
// input.c
int main() {
    int arr[3] = {10, 20, 30};
    printf("Value: %d\n", arr[0]);
    return 0;
}
```

Конвертируется в:
```kato
// output.kato
func main() {
    mass int arr = {10, 20, 30};
    print("Value: *arr[0]*\n");
    return 0;
}
```

## Ошибки

- Если нет функции `main` - ошибка
- Если код вне функции - ошибка
- Если дублируется имя функции - ошибка дублирования
- Если вызывается неизвестная функция - ошибка неизвестной функции
- Если вызов функции без скобок - ошибка вызова функции без аргументов
- Если `main` имеет аргументы - ошибка

## Hello World

```
func main() {
    print("Hello, World\n");
    return 0;
}
```

---

Kato is a simple programming language written in Python that compiles into C. When possible, the Kato compiler will automatically compile C into .exe if compilers are available in the Path.

## Variables

Kato supports 4 variable types:
- `int` - integer number
- `float` - floating point number
- `char` - single character (like in C). **IMPORTANT:** char literals must be in single quotes `'a'`
- `string` - string (like char* in C). Strings must be in double quotes `"text"`

Variable declaration:
```
var type name = value;
```

Variable assignment:
```
x = 30;
```

Example:
```
var int x = 20;
var float pi = 3.14;
var char letter = 'A';      // single quotes for char!
var string text = "Hello";  // double quotes for string!
x = 50;
```

## Arrays

Array declaration:
```
mass type name = {element1, element2, element3};
```

Array types: `int`, `float`, `char`, `string`

Accessing elements:
```
mass int numbers = {1, 2, 3, 4, 5};
print(*numbers[0]*);  // prints 1
print("Value: *numbers[2]*\n");  // prints "Value: 3"
```

Modifying elements:
```
numbers[0] = 10;
```

Example:
```
mass int arr = {10, 20, 30};
var int i = 0;
while (i < 3) {
    print(*arr[i]* "\n");
    i++;
}
```

## print Function

The print function in Kato works differently from C (no %). To output variables, use `*var*` identifiers:

```
var int age = 20;
print("My age is: *age*\n");
```



print can output:
- Strings: `print("Hello\n");`
- Numbers: `print(20);`
- Variables directly: `print(x);`
- Variables through `*var*`: `print(*x*);` (only for int and float)
- Variables in strings through identifiers: `print("Value: *x*");`
- Arithmetic expressions: `print(*x* + *y*);` or `print(x + y);`
- Multiple values: `print("hello" 20 "how are you\n");`

## inpt Function

The inpt function is used for input. The return type is automatically determined by the variable type:

```
var int a = inpt("enter number");
var float b = inpt("enter float");
var char c = inpt("enter char");
var string s = inpt("enter text");
```

**IMPORTANT:** inpt can only be used when declaring or assigning variables!

## Conditionals

Kato supports conditional statements:

```
if condition {
    // code
}
elif condition {
    // code
}
else {
    // code
}
```

Comparison operators:
- `==` - equal
- `!=` - not equal
- `<` - less than
- `>` - greater than
- `<=` - less than or equal
- `>=` - greater than or equal

Example:
```
var int x = 10;
if x > 5 {
    print("x is greater than 5\n");
}
elif x == 5 {
    print("x equals 5\n");
}
else {
    print("x is less than 5\n");
}

var char op = '+';
if op == '+' {  // char comparison in single quotes!
    print("plus\n");
}
```

## Arithmetic

Kato supports arithmetic operations:
- `+` - addition
- `-` - subtraction
- `*` - multiplication
- `/` - division
- `//` - integer division
- `%` - modulo

Examples:
```
var int x = 20;
var int b = 10;
var int sum = *x* + *b*;
var int result = (*x* + *b*) * 2;
print(*x* + *b*);
```

## User-defined Functions

You can create your own functions. Function types are dynamic.

Function declaration:
```
func name(arg1, arg2) {
    // code
}
```

Function call using `call`:
```
call name(arg1, arg2);
```

Function arguments can only be of types: `int`, `float`, `string`, `char`.

Example:
```
func printF(text) {
    print(text);
}

func main() {
    call printF("hello world\n");
}
```

## Loops

Kato supports while loop:

```
var int i = 0;
while (i < 10) {
    print(*i* "\n");
    i++;
}
```

## Increment and Decrement

Increase and decrease variable by 1:
- `var++;` - increment by 1
- `var--;` - decrement by 1

Example:
```
var int x = 5;
x++;  // x = 6
x--;  // x = 5
```

## Comments

Single-line comments:
```
// this is a comment
var int x = 20; // comment after code
```

## Rules and Restrictions

- A semicolon `;` must be written after each statement
- The `main` function is required and must not have arguments
- Function names cannot be duplicated (built-in or user-defined)
- Functions must be declared before they are called (compiler reads top to bottom)
- Function calls must have parentheses `()`, even if there are no arguments
- All code must be inside functions
- inpt can only be used when declaring or assigning variables

## Function Import

Kato supports importing functions from other files via .kh (Kato Header) files:

**welcome.kato:**
```kato
func welcome() {
    print("Hello to Kato!\n");
}
```

**welcome.kh:**
```
$export welcome from welcome.kato
```

**main.kato:**
```kato
import welcome.kh;

func main() {
    call welcome();
    return 0;
}
```

Rules:
- All paths are relative
- Cannot import `main` function
- Cannot duplicate function names
- If file not found - error

## c2kato - C to Kato Transpiler

Kato includes a transpiler from C to Kato:

```bash
python kato/main.py input.c -c2kato -o output
```

c2kato converts basic C code to Kato syntax:
- `int`, `float`, `char` types → Kato types
- `printf` → `print` with automatic conversion of `%d`, `%s` to `*var*`
- `for` loops → `while` loops
- C arrays → Kato arrays
- C functions → Kato functions

Example:
```c
// input.c
int main() {
    int arr[3] = {10, 20, 30};
    printf("Value: %d\n", arr[0]);
    return 0;
}
```

Converts to:
```kato
// output.kato
func main() {
    mass int arr = {10, 20, 30};
    print("Value: *arr[0]*\n");
    return 0;
}
```

## Errors

- If there is no `main` function - error
- If code is outside a function - error
- If a function name is duplicated - duplication error
- If an unknown function is called - unknown function error
- If function call without parentheses - function call without arguments error
- If `main` has arguments - error

## Hello World

```
func main() {
    print("Hello, World\n");
    return 0;
}
```
