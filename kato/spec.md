Kato - простой яп написанный на пайтон который компилируеться в C. При возможности компилятор kato будет автоматически комилировать C в .exe если доступны компиляторы в Path.


hello world:
func main() {
    print("Hello, World\n");
    return 0;
}

Типы функций динамические.

print может выводить и Int Значения через такую обвязку: print(20);

после каждой функции обязательно писать ;
Если kato не найдет функцию main в программе будет ошибка
Если есть хоть одна команда вне функции будет ошибка


Kato is a simple programming languague written in Python that compiles into C. When possible, the Kato compiler will automatically compile C into .exe if compilers are available in the Path.

hello world:
func main() {
    print("Hello, World\n");
    return 0;
}

The types of functions are dynamic.

print can output Int values like this: print(20);

A semicolon must be written after each statement;
If kato does not find the main function in the program, there will be an error
If there is at least one command outside a function, there will be an error