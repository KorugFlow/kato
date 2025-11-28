import argparse
import sys
import os
import subprocess
from pathlib import Path

from lexer.lexer import Lexer
from parser.parser import Parser, KatoSyntaxError
from compiler.compiler import CCompiler


def find_c_compiler():
    
    compilers = ['gcc', 'clang', 'cl']
    
    for compiler in compilers:
        try:
            result = subprocess.run(
                [compiler, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return compiler
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    return None


def compile_c_to_exe(c_file, output_file):
    
    compiler = find_c_compiler()
    
    if not compiler:
        print("i need compiler")
        print(f"ok: {c_file}")
        return False
    
    print(f"Using compiler: {compiler}")
    
    try:
        if compiler == 'cl':
            cmd = [compiler, c_file, f'/Fe{output_file}']
        else:
            cmd = [compiler, c_file, '-o', output_file]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"succesfly: {output_file}")
            return True
        else:
            print(f"fail! loser:")
            print(result.stderr)
            return False
    
    except Exception as e:
        print(f"erorr: {e}")
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
    parser.add_argument('-debug', '--debug', action='store_true', help='Show AST')
    parser.add_argument('-adv_debug', '--advanced-debug', action='store_true', help='Show tokens, AST, and C code')
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    
    if not input_path.exists():
        print(f"Error: File '{args.input_file}' not found")
        sys.exit(1)
    
    if not input_path.suffix == '.kato':
        print(f"Warning: File does not have .kato extension")
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    try:
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        if args.advanced_debug:
            print("\n" + "="*60)
            print("TOKENS:")
            print("="*60)
            for token in tokens:
                print(token)
            print()
        
        parser_obj = Parser(tokens, source_code)
        ast = parser_obj.parse()
        
        if args.debug or args.advanced_debug:
            print("\n" + "="*60)
            print("AST:")
            print("="*60)
            print_ast(ast)
            print()
        
        compiler = CCompiler(ast)
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
        
        compile_c_to_exe(str(c_file), output_file)
    
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
