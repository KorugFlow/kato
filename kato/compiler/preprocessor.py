import os
from pathlib import Path
from parser.errors import KatoSyntaxError, KatoWarning
from parser.ast import CallStatement, IfStatement, WhileStatement, PrintStatement, ReturnStatement, VarDeclaration, Assignment, BinaryOp, InptCall, FunctionCall

STDLIBS = {
    "filesystem": "compiler.std.filesystem"
}


class Preprocessor:
    def __init__(self, main_file_path):
        self.main_file_path = Path(main_file_path)
        self.base_dir = self.main_file_path.parent
        self.processed_files = set()
        self.imported_functions = {}
        self.imported_function_return_types = {}
        self.all_functions = []
        self.stdlib_imports = set()
        self.c_imports = set()
    
    def process(self, source_code):
        imports = self.extract_imports(source_code)
        self.import_lines = {}
        
        lines = source_code.split('\n')
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('import '):
                if stripped.endswith(';'):
                    import_path = stripped[7:-1].strip()
                else:
                    import_path = stripped[7:].strip()
                self.import_lines[import_path] = line_num
        
        for import_path in imports:
            if import_path in STDLIBS:
                self.stdlib_imports.add(import_path)
            else:
                self.process_import(import_path)
        
        source_without_imports = self.remove_imports(source_code)
        
        return source_without_imports, self.imported_functions, self.imported_function_return_types
    
    def extract_imports(self, source_code):
        imports = []
        lines = source_code.split('\n')
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('import '):
                if stripped.endswith(';'):
                    import_path = stripped[7:-1].strip()
                else:
                    import_path = stripped[7:].strip()
                imports.append(import_path)
        
        return imports
    
    def remove_imports(self, source_code):
        lines = source_code.split('\n')
        result = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped.startswith('import '):
                result.append(line)
        
        return '\n'.join(result)
    
    def process_import(self, import_path):
        kh_path = self.base_dir / import_path
        
        if not kh_path.exists():
            raise KatoSyntaxError(
                f"Cannot find import file: {import_path}",
                1, 1
            )
        
        if str(kh_path) in self.processed_files:
            return
        
        self.processed_files.add(str(kh_path))
        
        with open(kh_path, 'r', encoding='utf-8') as f:
            kh_content = f.read()
        
        exports = self.parse_kh_file(kh_content, kh_path)
        
        for export_file in exports:
            self.process_export(export_file, kh_path.parent)
    
    def parse_kh_file(self, content, kh_path):
        exports = []
        lines = content.split('\n')
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('$export '):
                export_line = stripped[8:].strip()
                
                if ' from ' in export_line:
                    parts = export_line.split(' from ')
                    func_name = parts[0].strip()
                    file_name = parts[1].strip()
                    exports.append((func_name, file_name))
                else:
                    raise KatoSyntaxError(
                        f"Invalid export syntax in {kh_path}. Use: $export func_name from file.kato",
                        1, 1
                    )
        
        return exports
    
    def process_export(self, export_info, base_dir):
        func_name, export_file = export_info
        kato_path = base_dir / export_file
        
        if not kato_path.exists():
            raise KatoSyntaxError(
                f"Cannot find export file: {export_file}",
                1, 1
            )
        
        file_key = f"{kato_path}:{func_name}"
        if file_key in self.processed_files:
            return
        
        self.processed_files.add(file_key)
        
        with open(kato_path, 'r', encoding='utf-8') as f:
            kato_content = f.read()
        
        from lexer.lexer import Lexer
        from parser.parser import Parser
        
        lexer = Lexer(kato_content)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens, kato_content)
        ast = parser.parse()
        
        found = False
        for func in ast.functions:
            if func.name == func_name:
                found = True
                
                if func.name == "main":
                    raise KatoSyntaxError(
                        f"Cannot import 'main' function from {export_file}",
                        1, 1
                    )
                
                if func.name in self.imported_functions:
                    raise KatoSyntaxError(
                        f"Function '{func.name}' is already imported",
                        1, 1
                    )
                
                self.imported_functions[func.name] = func
                self.all_functions.append(func)
                
                return_type = self.infer_return_type(func.body)
                self.imported_function_return_types[func.name] = return_type
                
                break
        
        if not found:
            raise KatoSyntaxError(
                f"Function '{func_name}' not found in {export_file}",
                1, 1
            )
    
    def check_unused_imports(self, ast, imported_functions, source_code):
        used_stdlib = set()
        used_functions = set()
        
        stdlib_functions = {}
        for stdlib_name in self.stdlib_imports:
            if stdlib_name == "filesystem":
                from compiler.std.filesystem import FILESYSTEM_FUNCTIONS
                stdlib_functions[stdlib_name] = FILESYSTEM_FUNCTIONS
        
        def check_expr(expr):
            if expr is None:
                return
            if isinstance(expr, list):
                for item in expr:
                    check_expr(item)
            elif isinstance(expr, BinaryOp):
                check_expr(expr.left)
                check_expr(expr.right)
            elif isinstance(expr, InptCall):
                check_expr(expr.prompt)
            elif isinstance(expr, FunctionCall):
                func_name = expr.name
                for stdlib_name, funcs in stdlib_functions.items():
                    if func_name in funcs:
                        used_stdlib.add(stdlib_name)
                if func_name in imported_functions:
                    used_functions.add(func_name)
                if expr.arguments:
                    for arg in expr.arguments:
                        check_expr(arg)
        
        def check_stmt(statement):
            if isinstance(statement, CallStatement):
                func_name = statement.func_name
                for stdlib_name, funcs in stdlib_functions.items():
                    if func_name in funcs:
                        used_stdlib.add(stdlib_name)
                if func_name in imported_functions:
                    used_functions.add(func_name)
                if statement.arguments:
                    for arg in statement.arguments:
                        check_expr(arg)
            elif isinstance(statement, IfStatement):
                check_expr(statement.condition)
                for stmt in statement.if_body:
                    check_stmt(stmt)
                for elif_condition, elif_body in statement.elif_parts:
                    check_expr(elif_condition)
                    for stmt in elif_body:
                        check_stmt(stmt)
                if statement.else_body:
                    for stmt in statement.else_body:
                        check_stmt(stmt)
            elif isinstance(statement, WhileStatement):
                check_expr(statement.condition)
                for stmt in statement.body:
                    check_stmt(stmt)
            elif isinstance(statement, PrintStatement):
                check_expr(statement.value)
            elif isinstance(statement, ReturnStatement):
                check_expr(statement.value)
            elif isinstance(statement, VarDeclaration):
                check_expr(statement.value)
            elif isinstance(statement, Assignment):
                check_expr(statement.value)
        
        for function in ast.functions:
            for statement in function.body:
                check_stmt(statement)
        
        for stdlib_name in self.stdlib_imports:
            if stdlib_name not in used_stdlib:
                line = self.import_lines.get(stdlib_name, 1)
                warning = KatoWarning(f"Unused import: '{stdlib_name}'", line, 1, source_code)
                print(warning.format_warning())
        
        for func_name in imported_functions.keys():
            if func_name not in used_functions:
                line = 1
                warning = KatoWarning(f"Unused imported function: '{func_name}'", line, 1, source_code)
                print(warning.format_warning())
    
    def infer_return_type(self, body):
        from parser.ast import ReturnStatement, StringLiteral, CharLiteral, FloatLiteral, Identifier
        
        has_return_with_value = False
        
        for statement in body:
            if isinstance(statement, ReturnStatement):
                if statement.value:
                    has_return_with_value = True
                    if isinstance(statement.value, StringLiteral):
                        return "string"
                    elif isinstance(statement.value, CharLiteral):
                        return "char"
                    elif isinstance(statement.value, FloatLiteral):
                        return "float"
                    elif isinstance(statement.value, Identifier):
                        return "int"
        
        return "void" if not has_return_with_value else "int"
