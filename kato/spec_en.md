Kato is a simple programming language written in Python that compiles into C and automatically into .exe using the built-in TCC compiler. No external compilers or linkers required!

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
- Function calls: `print(file_read("file.txt"));` or `print(random(1, 10));`

## inpt Function

The inpt function is used for input. The return type is automatically determined by the variable type:

```
var int a = inpt("enter number");
var float b = inpt("enter float");
var char c = inpt("enter char");
var string s = inpt("enter text");
```

**IMPORTANT:** inpt can only be used when declaring or assigning variables!

## random Function

The random function returns a random integer within a specified range (inclusive):

```
var int a = random(min, max);
```

Parameters:
- `min` - minimum value (inclusive)
- `max` - maximum value (inclusive)

Returns: `int` - random number from min to max

Example:
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

**IMPORTANT:** 
- The function requires exactly 2 arguments (min, max)
- Both arguments must be integers
- The random number generator is automatically initialized in the main() function

## find Function

The find function searches for a pattern in a string or array and returns the index of the first match:

```
var int index = find(target, pattern);
```

Parameters:
- `target` - string or array to search in
- `pattern` - pattern to search for (string or character)

Returns: `int` - index of first match or -1 if not found

Example:
```kato
func main() {
    var string text = "Hello World";
    var int pos = find(text, "World");
    if pos != -1 {
        print("Found at position: *pos*\n");
    } else {
        print("Not found\n");
    }
    
    var string data = "abcdef";
    var int idx = find(data, "cd");
    print("Index: *idx*\n");
    
    return 0;
}
```

**IMPORTANT:**
- The function requires exactly 2 arguments (target, pattern)
- Returns -1 if pattern is not found
- Search is case-sensitive

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

Logical operators:
- `&&` - logical AND
- `||` - logical OR

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

// Logical operators
var int age = 25;
var int score = 85;
if age >= 18 && score >= 80 {
    print("Allowed to take exam\n");
}

if age < 18 || score < 50 {
    print("Not allowed\n");
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



**IMPORTANT:** When passing string or character literals to functions:
- Use double quotes for strings: `"text"`
- Use single quotes for characters: `'a'`
- If passing a variable, it must be declared first

Example:
```
func printF(text) {
    print(text);
}

func main() {
    call printF("hello world\n");
    
    var string msg = "test";
    call printF(msg);
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

**Loop control:**
- `break;` - exit the loop
- `continue;` - skip to next iteration

### for Loop - Iterator

Kato supports a special `for` loop for iterating over arrays and variables:

```
for (iterable; counter; condition) {
    // code
}
```

**Parameters:**
- `iterable` - name of array or variable to iterate over
- `counter` - counter variable (can create new via `var type name = value` or use existing one)
- `condition` - continuation condition (e.g. `counter < 20`)

**How it works:**
- For iterates through array elements or variable bytes
- Counter automatically increments on each iteration
- Loop stops when condition becomes false

Example with new counter:
```
mass int numbers = {10, 20, 30, 40, 50};
for (numbers; var int i = 0; i < 5) {
    print("Element: *numbers[i]*\n");
}
```

Example with existing counter:
```
mass int arr = {1, 2, 3, 4, 5};
var int counter = 0;
for (arr; counter; counter < 3) {
    print(*arr[counter]* "\n");
}
```

Example with byte limit:
```
var string text = "Hello World";
for (text; var int i = 0; i < 5) {
    print("Processing byte *i*\n");
}
```

### Infinite loop inf

Kato supports a special infinite loop `inf` for easier usage:

```
inf {
    // code runs infinitely
    stop; // stops the loop
}
```

**inf loop control:**
- `stop;` - exit the infinite loop


Example:
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

Kato supports switch statement for multiple choice:

```
switch (variable) {
    case value1
        // code
        break;
    
    case value2
        // code
        break;
    
    default {
        // default code
    }
}
```

**Rules:**
- Switch accepts only variables (not expressions)
- Case can accept:
  - Character literals: `case 'a'`
  - String literals: `case "hello"`
  - Numeric literals: `case 42`
  - Variables: `case *var_name*`
- `break;` - exit switch (optional, cases don't fall through by default)
- default block is optional and must be in curly braces

Example:
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

Example with numbers:
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
var int x = 20;
```

## Type Conversion

Kato supports type conversion between variables using the `convert` operator:

```
convert *variable* > type;
```

**Conversion Rules:**

**String to Int/Float:**
- If the string contains a number (e.g., `"20"`), it converts successfully
- If the string contains text (e.g., `"hello"`), an error is displayed
- Empty string `""` also causes an error

**String to Char:**
- If the string is longer than 1 character, it is truncated to the first character
- Example: `"hello"` → `"h"`

**Int/Float to String:**
- Numbers are converted to their string representation

**Any type to String:**
- Always successful

Example:
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
- **Variables are unique per file** - you cannot declare a variable with the same name twice, even in different if/elif/else blocks or loops

## C Interop - Calling C Functions

Kato supports direct calling of C functions through importing .h files:

```kato
c.import stdio.h;
c.import windows.h;

func main() {
    c.printf("Hello from C!\n");
    return 0;
}
```

Rules:
- Import C headers: `c.import header.h;`
- Call C functions: `c.function_name(args);`
- C functions don't conflict with Kato functions
- Can use any C libraries (stdio, windows, wdk, etc.)

Example with Windows API:
```kato
c.import windows.h;

func main() {
    c.MessageBoxA(0, "Hello from Kato!", "Message", 0);
    return 0;
}
```

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

## Standard Library (stdlib)

### filesystem - File Operations

To work with files, import the filesystem library:

```kato
import filesystem;
```

Available functions:

**file_read(filename)** - Reads file content
- Parameters: `string filename` - file name
- Returns: `string` - file content or empty string on error

```kato
import filesystem;

func main() {
    var string content = file_read("hello.txt");
    print("*content*\n");
    return 0;
}
```

**file_write(filename, content)** - Writes content to file (overwrites)
- Parameters: `string filename`, `string content`
- Returns: `int` - 1 on success, 0 on error

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

**file_append(filename, content)** - Appends content to end of file
- Parameters: `string filename`, `string content`
- Returns: `int` - 1 on success, 0 on error

```kato
import filesystem;

func main() {
    var int result = file_append("log.txt", "New line\n");
    return 0;
}
```

**file_exists(filename)** - Checks if file exists
- Parameters: `string filename`
- Returns: `int` - 1 if file exists, 0 if not

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

**file_delete(filename)** - Deletes file
- Parameters: `string filename`
- Returns: `int` - 1 on success, 0 on error

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

### os - Process Management

To work with processes, import the os library:

```kato
import os;
```

Available functions:

**os_kill(pid)** - Terminates a process by PID
- Parameters: `int pid` - process identifier
- Returns: `int` - 1 on success, 0 on error

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

**os_list_processes()** - Returns a list of all running processes
- Parameters: none
- Returns: `string` - list of process PIDs (each on a new line)

```kato
import os;

func main() {
    var string processes = os_list_processes();
    print("Running processes:\n*processes*");
    return 0;
}
```

**os_run(path)** - Runs an executable file at the specified path
- Parameters: `string path` - path to .exe file
- Returns: `int` - 1 on success, 0 on error

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

**os_process_exists(pid)** - Checks if a process with the specified PID exists
- Parameters: `int pid` - process identifier
- Returns: `int` - 1 if process exists and is active, 0 if not

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

**os_get_pid()** - Returns the PID of the current process
- Parameters: none
- Returns: `int` - PID of the current process

```kato
import os;

func main() {
    var int my_pid = os_get_pid();
    print("My PID: *my_pid*\n");
    return 0;
}
```

**os_system(command)** - Executes a system command and returns output
- Parameters: `string command` - command to execute
- Returns: `string` - command output

```kato
import os;

func main() {
    var string output = os_system("dir");
    print("*output*");
    return 0;
}
```

**os_cmd(command)** - Executes a command through cmd.exe and returns output
- Parameters: `string command` - command to execute
- Returns: `string` - command output

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

**os_is_admin()** - Checks if the program is running with administrator privileges
- Parameters: none
- Returns: `int` - 1 if running as administrator, 0 if running as user

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

**os_runas(mode)** - Restarts the program with specified privileges
- Parameters: `string mode` - run mode ("admin" or "user")
- Returns: `int` - 1 on success, 0 on error

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

## c2kato - C to Kato Transpiler

Kato includes a transpiler from C to Kato:

```bash
python kato/main.py input.c -c2kato -o output
```

c2kato converts basic C code to Kato syntax:
- `int`, `float`, `char` types → Kato types
- `printf` → `print` with automatic conversion of `%d`, `%s` to `*var*`
- `scanf` → `inpt` with automatic type detection
- `for` loops → `while` loops
- `switch` statements → Kato switch statements
- C arrays → Kato arrays
- C functions → Kato functions

Example:
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

Converts to:
```kato
// output.kato
func main() {
    mass int arr = {10, 20, 30};
    print("Value: *arr[0]*\n");
    
    var int num = inpt("Enter number: ");
    
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
