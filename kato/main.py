import argparse
import sys
import os
import subprocess
from pathlib import Path

from lexer.lexer import Lexer
from parser.parser import Parser
from parser.errors import KatoSyntaxError
from compiler.compiler import CCompiler
from compiler.optimizer import Optimizer


def find_c_compiler():
    tcc_path = Path(__file__).parent / 'tcc' / 'tcc.exe'
    if tcc_path.exists():
        return str(tcc_path)
    return None


def compile_c_to_exe(c_file, output_file, c_imports=None):
    compiler = find_c_compiler()
    
    if not compiler:
        print("TCC compiler not found at kato/tcc/tcc.exe")
        return False
    
    print(f"Using compiler: {compiler}")
    
    try:
        cmd = [compiler, c_file, '-o', output_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Successfully compiled: {output_file}")
            return True
        else:
            print(f"Compilation failed:")
            print(result.stderr)
            return False
    
    except Exception as e:
        print(f"Error: {e}")
        return False


def print_ast(node, indent=0):
    
    prefix = "  " * indent
    
    if hasattr(node, '__class__'):
        class_name = node.__class__.__name__
        print(f"{prefix}{class_name}")
        
        if hasattr(node, '__dict__'):
            for key, value in node.__dict__.items():
                if isinstance(value, list):
                    print(f"{prefix}  {key}:")
                    for item in value:
                        print_ast(item, indent + 2)
                elif hasattr(value, '__class__') and hasattr(value, '__dict__'):
                    print(f"{prefix}  {key}:")
                    print_ast(value, indent + 2)
                else:
                    print(f"{prefix}  {key}: {repr(value)}")


def main():
    parser = argparse.ArgumentParser(description='Kato compiler - compiles .kato files to C and optionally to .exe')
    parser.add_argument('input_file', help='Input .kato file')
    parser.add_argument('-o', '--output', help='Output binary name (without extension)', default=None)
    parser.add_argument('-c', '--c-only', action='store_true', help='Generate C code only, do not compile to binary')
    parser.add_argument('-c2kato', '--c2kato', action='store_true', help='Convert C code to Kato')
    parser.add_argument('-debug', '--debug', action='store_true', help='Show AST')
    parser.add_argument('-adv_debug', '--advanced-debug', action='store_true', help='Show tokens, AST, and C code')
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    
    if not input_path.exists():
        print(f"Error: File '{args.input_file}' not found")
        sys.exit(1)
    
    if args.c2kato:
        if not input_path.suffix == '.c':
            print(f"Warning: File does not have .c extension for c2kato")
    elif not input_path.suffix == '.kato':
        print(f"Warning: File does not have .kato extension")
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    if args.c2kato:
        from c2kato.c2kato import convert_c_to_kato
        
        try:
            kato_code = convert_c_to_kato(source_code, debug=args.debug)
            
            if not kato_code:
                print("Warning: Generated Kato code is empty")
            
            if args.output:
                output_file = f"{args.output}.kato"
            else:
                output_file = input_path.with_suffix('.kato')
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(kato_code)
            
            print(f"Kato code generated: {output_file}")
            
            if args.debug:
                print("\nGenerated Kato code:")
                print(kato_code)
        
        except Exception as e:
            print(f"c2kato error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        
        return
    
    try:
        from compiler.preprocessor import Preprocessor
        
        preprocessor = Preprocessor(input_path)
        processed_source, imported_functions, imported_function_return_types = preprocessor.process(source_code)
        
        lexer = Lexer(processed_source)
        tokens = lexer.tokenize()
        
        if args.advanced_debug:
            print("\n" + "="*60)
            print("TOKENS:")
            print("="*60)
            for token in tokens:
                print(token)
            print()
        
        parser_obj = Parser(tokens, processed_source)
        
        for func_name in imported_functions.keys():
            parser_obj.defined_functions.add(func_name)
        
        for func_name, return_type in imported_function_return_types.items():
            parser_obj.function_return_types[func_name] = return_type
        
        if "filesystem" in preprocessor.stdlib_imports:
            from compiler.std.filesystem import FILESYSTEM_FUNCTIONS
            for func_name, func_info in FILESYSTEM_FUNCTIONS.items():
                parser_obj.builtin_functions.add(func_name)
                parser_obj.function_return_types[func_name] = func_info["return_type"]
        
        if "os" in preprocessor.stdlib_imports:
            from compiler.std.os import OS_FUNCTIONS
            for func_name, func_info in OS_FUNCTIONS.items():
                parser_obj.builtin_functions.add(func_name)
                parser_obj.function_return_types[func_name] = func_info["return_type"]
        
        ast = parser_obj.parse()
        
        for func_name, func in imported_functions.items():
            ast.functions.insert(0, func)
        
        if args.debug or args.advanced_debug:
            print("\n" + "="*60)
            print("AST (Before Optimization):")
            print("="*60)
            print_ast(ast)
            print()
        
        optimizer = Optimizer(ast)
        optimized_ast = optimizer.optimize()
        
        if args.debug or args.advanced_debug:
            print("\n" + "="*60)
            print("AST (After Optimization):")
            print("="*60)
            print_ast(optimized_ast)
            print()
        
        
        preprocessor.check_unused_imports(optimized_ast, imported_functions, source_code)
        
        compiler = CCompiler(optimized_ast, stdlib_imports=preprocessor.stdlib_imports, c_imports=preprocessor.c_imports)
        c_code = compiler.compile()
        
        if args.advanced_debug:
            print("\n" + "="*60)
            print("C CODE:")
            print("="*60)
            print(c_code)
            print()
        
        c_file = input_path.with_suffix('.c')
        with open(c_file, 'w', encoding='utf-8') as f:
            f.write(c_code)
        
        print(f"C code generated: {c_file}")
        
        if args.c_only:
            print("C-only mode: skipping binary compilation")
            return
        
        if args.output:
            output_name = args.output
        else:
            output_name = input_path.stem
        
        if sys.platform == 'win32':
            output_file = f"{output_name}.exe"
        else:
            output_file = output_name
        
        compile_c_to_exe(str(c_file), output_file, compiler.c_imports)
    
    except KatoSyntaxError as e:
        print(str(e))
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
