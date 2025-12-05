Kato - простой язык программирования написанный на Python, который компилируется в C и автоматически в .exe с помощью встроенного TCC компилятора. Не требует установки внешних компиляторов или линкеров!

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
- Вызовы функций: `print(file_read("file.txt"));` или `print(random(1, 10));`

## Функция inpt

Функция inpt используется для ввода данных. Тип возвращаемого значения определяется автоматически по типу переменной:

```
var int a = inpt("enter number");
var float b = inpt("enter float");
var char c = inpt("enter char");
var string s = inpt("enter text");
```

**ВАЖНО:** inpt можно использовать только при объявлении или изменении переменных!

## Функция random

Функция random возвращает случайное целое число в заданном диапазоне (включительно):

```
var int a = random(min, max);
```

Параметры:
- `min` - минимальное значение (включительно)
- `max` - максимальное значение (включительно)

Возвращает: `int` - случайное число от min до max

Пример:
```kato
func main() {
    var int dice = random(1, 6);
    print("Dice rolled: *dice*\n");
    
    var int randomAge = random(18, 65);
    print("Random age: *randomAge*\n");
    
    var int coinFlip = random(0, 1);
    if coinFlip == 0 {
        print("Heads\n");
    } else {
        print("Tails\n");
    }
    
    return 0;
}
```

**ВАЖНО:** 
- Функция требует ровно 2 аргумента (min, max)
- Оба аргумента должны быть целыми числами
- Генератор случайных чисел автоматически инициализируется в функции main()

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

Логические операторы:
- `&&` - логическое И (AND)
- `||` - логическое ИЛИ (OR)

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

// Логические операторы
var int age = 25;
var int score = 85;
if age >= 18 && score >= 80 {
    print("Допущен к экзамену\n");
}

if age < 18 || score < 50 {
    print("Не допущен\n");
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

**ВАЖНО:** При передаче строковых или символьных литералов в функции:
- Используйте двойные кавычки для строк: `"text"`
- Используйте одинарные кавычки для символов: `'a'`
- Если передаете переменную, она должна быть объявлена


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

**Управление циклом:**
- `break;` - выход из цикла
- `continue;` - переход к следующей итерации

### Цикл for - Переборщик

Kato поддерживает специальный цикл `for` для перебора массивов и переменных:

```
for (iterable; counter; condition) {
    // код
}
```

**Параметры:**
- `iterable` - имя массива или переменной для перебора
- `counter` - переменная-счётчик (можно создать новую через `var type name = value` или использовать существующую)
- `condition` - условие продолжения (например `counter < 20`)

**Как работает:**
- For перебирает элементы массива или байты переменной
- Счётчик автоматически увеличивается на каждой итерации
- Цикл останавливается когда условие становится ложным

Пример с новым счётчиком:
```
mass int numbers = {10, 20, 30, 40, 50};
for (numbers; var int i = 0; i < 5) {
    print("Element: *numbers[i]*\n");
}
```

Пример с существующим счётчиком:
```
mass int arr = {1, 2, 3, 4, 5};
var int counter = 0;
for (arr; counter; counter < 3) {
    print(*arr[counter]* "\n");
}
```

Пример с ограничением по байтам:
```
var string text = "Hello World";
for (text; var int i = 0; i < 5) {
    print("Processing byte *i*\n");
}
```

### Бесконечный цикл inf

Kato поддерживает специальный бесконечный цикл `inf` для упрощения работы:

```
inf {
    // код выполняется бесконечно
    stop; // останавливает цикл
}
```

**Управление inf циклом:**
- `stop;` - выход из бесконечного цикла


Пример:
```
var int i = 0;
while (i < 10) {
    i++;
    if i == 5 {
        continue;
    }
    if i == 8 {
        break;
    }
    print(*i* "\n");
}
```

## Switch

Kato поддерживает оператор switch для множественного выбора:

```
switch (переменная) {
    case значение1
        // код
        break;
    
    case значение2
        // код
        break;
    
    default {
        // код по умолчанию
    }
}
```

**Правила:**
- Switch принимает только переменные (не выражения)
- Case может принимать:
  - Символьные литералы: `case 'a'`
  - Строковые литералы: `case "hello"`
  - Числовые литералы: `case 42`
  - Переменные: `case *var_name*`
- `break;` - выход из switch (опционально, по умолчанию case не проваливается)
- default блок опционален и должен быть в фигурных скобках

Пример:
```
var char op = '+';
switch (op) {
    case '+'
        print("Addition\n");
    
    case '-'
        print("Subtraction\n");
    
    case '*'
        print("Multiplication\n");
    
    default {
        print("Unknown operation\n");
    }
}
```

Пример с числами:
```
var int day = 3;
switch (day) {
    case 1
        print("Monday\n");
    
    case 2
        print("Tuesday\n");
    
    case 3
        print("Wednesday\n");
    
    default {
        print("Other day\n");
    }
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
var int x = 20;
```

## Конвертация типов

Kato поддерживает конвертацию переменных между типами с помощью оператора `convert`:

```
convert *переменная* > тип;
```

**Правила конвертации:**

**String в Int/Float:**
- Если строка содержит число (например `"20"`), она конвертируется успешно
- Если строка содержит текст (например `"hello"`), выводится ошибка
- Пустая строка `""` также вызывает ошибку

**String в Char:**
- Если строка длиннее 1 символа, она обрезается до первого символа
- Пример: `"hello"` → `"h"`

**Int/Float в String:**
- Числа конвертируются в строковое представление

**Любой тип в String:**
- Всегда успешно

Пример:
```
func main() {
    var string num_str = "42";
    convert *num_str* > int;
    print("Number: *num_str*\n");
    
    var string text = "hello";
    convert *text* > char;
    print("First char: *text*\n");
    
    return 0;
}
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
- **Переменные уникальны на весь файл** - нельзя объявлять переменную с одинаковым именем дважды, даже в разных блоках if/elif/else или циклах

## C Interop - Вызов C функций

Kato поддерживает прямой вызов C функций через импорт .h файлов:

```kato
c.import stdio.h;
c.import windows.h;

func main() {
    c.printf("Hello from C!\n");
    return 0;
}
```

Правила:
- Импорт C заголовков: `c.import header.h;`
- Вызов C функций: `c.function_name(args);`
- C функции не конфликтуют с Kato функциями
- Можно использовать любые C библиотеки (stdio, windows, wdk и т.д.)

Пример с Windows API:
```kato
c.import windows.h;

func main() {
    c.MessageBoxA(0, "Hello from Kato!", "Message", 0);
    return 0;
}
```

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

## Стандартная библиотека (stdlib)

### filesystem - Работа с файлами

Для работы с файлами импортируйте библиотеку filesystem:

```kato
import filesystem;
```

Доступные функции:

**file_read(filename)** - Читает содержимое файла
- Параметры: `string filename` - имя файла
- Возвращает: `string` - содержимое файла или пустую строку при ошибке

```kato
import filesystem;

func main() {
    var string content = file_read("hello.txt");
    print("*content*\n");
    return 0;
}
```

**file_write(filename, content)** - Записывает содержимое в файл (перезаписывает)
- Параметры: `string filename`, `string content`
- Возвращает: `int` - 1 при успехе, 0 при ошибке

```kato
import filesystem;

func main() {
    var int result = file_write("output.txt", "Hello World");
    if result == 1 {
        print("File written successfully\n");
    }
    return 0;
}
```

**file_append(filename, content)** - Добавляет содержимое в конец файла
- Параметры: `string filename`, `string content`
- Возвращает: `int` - 1 при успехе, 0 при ошибке

```kato
import filesystem;

func main() {
    var int result = file_append("log.txt", "New line\n");
    return 0;
}
```

**file_exists(filename)** - Проверяет существование файла
- Параметры: `string filename`
- Возвращает: `int` - 1 если файл существует, 0 если нет

```kato
import filesystem;

func main() {
    var int exists = file_exists("data.txt");
    if exists == 1 {
        print("File exists\n");
    } else {
        print("File not found\n");
    }
    return 0;
}
```

**file_delete(filename)** - Удаляет файл
- Параметры: `string filename`
- Возвращает: `int` - 1 при успехе, 0 при ошибке

```kato
import filesystem;

func main() {
    var int result = file_delete("temp.txt");
    if result == 1 {
        print("File deleted\n");
    }
    return 0;
}
```

### os - Работа с процессами

Для работы с процессами импортируйте библиотеку os:

```kato
import os;
```

Доступные функции:

**os_kill(pid)** - Завершает процесс по PID
- Параметры: `int pid` - идентификатор процесса
- Возвращает: `int` - 1 при успехе, 0 при ошибке

```kato
import os;

func main() {
    var int result = os_kill(1234);
    if result == 1 {
        print("Process terminated\n");
    } else {
        print("Failed to terminate\n");
    }
    return 0;
}
```

**os_list_processes()** - Возвращает список всех запущенных процессов
- Параметры: нет
- Возвращает: `string` - список PID процессов (каждый на новой строке)

```kato
import os;

func main() {
    var string processes = os_list_processes();
    print("Running processes:\n*processes*");
    return 0;
}
```

**os_run(path)** - Запускает исполняемый файл по указанному пути
- Параметры: `string path` - путь к .exe файлу
- Возвращает: `int` - 1 при успехе, 0 при ошибке

```kato
import os;

func main() {
    var int result = os_run("C:\\Windows\\notepad.exe");
    if result == 1 {
        print("Program started\n");
    }
    return 0;
}
```

**os_process_exists(pid)** - Проверяет, существует ли процесс с указанным PID
- Параметры: `int pid` - идентификатор процесса
- Возвращает: `int` - 1 если процесс существует и активен, 0 если нет

```kato
import os;

func main() {
    var int pid = 1234;
    var int exists = os_process_exists(pid);
    if exists == 1 {
        print("Process is running\n");
    } else {
        print("Process not found\n");
    }
    return 0;
}
```

**os_get_pid()** - Возвращает PID текущего процесса
- Параметры: нет
- Возвращает: `int` - PID текущего процесса

```kato
import os;

func main() {
    var int my_pid = os_get_pid();
    print("My PID: *my_pid*\n");
    return 0;
}
```

**os_system(command)** - Выполняет системную команду и возвращает вывод
- Параметры: `string command` - команда для выполнения
- Возвращает: `string` - вывод команды

```kato
import os;

func main() {
    var string output = os_system("dir");
    print("*output*");
    return 0;
}
```

**os_cmd(command)** - Выполняет команду через cmd.exe и возвращает вывод
- Параметры: `string command` - команда для выполнения
- Возвращает: `string` - вывод команды

```kato
import os;

func main() {
    var string output = os_cmd("echo Hello from CMD!");
    print("*output*");
    var string files = os_cmd("dir /b");
    print("Files:\n*files*");
    return 0;
}
```

**os_is_admin()** - Проверяет, запущена ли программа с правами администратора
- Параметры: нет
- Возвращает: `int` - 1 если запущена от администратора, 0 если от пользователя

```kato
import os;

func main() {
    var int isAdmin = os_is_admin();
    if isAdmin == 1 {
        print("Running as Administrator\n");
    } else {
        print("Running as User\n");
    }
    return 0;
}
```

**os_runas(mode)** - Перезапускает программу с указанными правами
- Параметры: `string mode` - режим запуска ("admin" или "user")
- Возвращает: `int` - 1 при успехе, 0 при ошибке

```kato
import os;

func main() {
    var int isAdmin = os_is_admin();
    if isAdmin == 0 {
        print("Restarting as admin...\n");
        call os_runas("admin");
        return 0;
    }
    print("Running with admin rights!\n");
    return 0;
}
```

## c2kato - Транспилятор из C в Kato

Kato включает транспилятор из C в Kato:

```bash
python kato/main.py input.c -c2kato -o output
```

c2kato конвертирует базовый C код в синтаксис Kato:
- `int`, `float`, `char` типы → Kato типы
- `printf` → `print` с автоматической конвертацией `%d`, `%s` в `*var*`
- `scanf` → `inpt` с автоматическим определением типа
- `for` циклы → `while` циклы
- `switch` выражения → Kato switch выражения
- Массивы C → массивы Kato
- Функции C → функции Kato

Пример:
```c
// input.c
int main() {
    int arr[3] = {10, 20, 30};
    printf("Value: %d\n", arr[0]);
    
    int num;
    printf("Enter number: ");
    scanf("%d", &num);
    
    return 0;
}
```

Конвертируется в:
```kato
// output.kato
func main() {
    mass int arr = {10, 20, 30};
    print("Value: *arr[0]*\n");
    
    var int num = inpt("Enter number: ");
    
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
