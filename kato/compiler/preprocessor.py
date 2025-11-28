import os
from pathlib import Path
from parser.errors import KatoSyntaxError


class Preprocessor:
    def __init__(self, main_file_path):
        self.main_file_path = Path(main_file_path)
        self.base_dir = self.main_file_path.parent
        self.processed_files = set()
        self.imported_functions = {}
        self.all_functions = []
        self.stdlib_imports = set()
    
    def process(self, source_code):
        imports = self.extract_imports(source_code)
        
        for import_path in imports:
            if import_path in ["filesystem"]:
                self.stdlib_imports.add(import_path)
            else:
                self.process_import(import_path)
        
        source_without_imports = self.remove_imports(source_code)
        
        return source_without_imports, self.imported_functions
    
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
                break
        
        if not found:
            raise KatoSyntaxError(
                f"Function '{func_name}' not found in {export_file}",
                1, 1
            )
