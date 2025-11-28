Kato - простой яп написанный на пайтон который компилируеться в C. При возможности компилятор kato будет автоматически комилировать C в .exe если доступны компиляторы в Path.

## Переменные

Kato поддерживает 4 типа переменных:
- `int` - целое число
- `float` - число с плавающей точкой
- `char` - один символ (как в C)
- `string` - строка (как char* в C)

Объявление переменных:
```
var type name = значение;
```

Пример:
```
var int x = 20;
var float pi = 3.14;
var char letter = 'A';
var string text = "Hello";
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

## Правила и ограничения

- После каждой команды обязательно писать `;`
- Функция `main` обязательна и не должна иметь аргументов
- Нельзя дублировать имена функций (встроенных или пользовательских)
- Функции должны быть объявлены до их вызова (компилятор читает сверху вниз)
- Вызов функции обязательно должен иметь скобки `()`, даже если аргументов нет
- Весь код должен быть внутри функций

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
- `char` - single character (like in C)
- `string` - string (like char* in C)

Variable declaration:
```
var type name = value;
```

Example:
```
var int x = 20;
var float pi = 3.14;
var char letter = 'A';
var string text = "Hello";
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

## Rules and Restrictions

- A semicolon `;` must be written after each statement
- The `main` function is required and must not have arguments
- Function names cannot be duplicated (built-in or user-defined)
- Functions must be declared before they are called (compiler reads top to bottom)
- Function calls must have parentheses `()`, even if there are no arguments
- All code must be inside functions

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