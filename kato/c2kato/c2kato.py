from .lexer import CLexer
from .parser import CParser
from .converter import Converter
from .generator import KatoGenerator
from .errors import C2KatoError


def convert_c_to_kato(c_source_code, debug=False):
    try:
        lexer = CLexer(c_source_code)
        tokens = lexer.tokenize()
        
        if debug:
            print(f"Tokens: {len(tokens)}")
        
        parser = CParser(tokens)
        c_ast = parser.parse()
        
        if debug:
            print(f"C AST declarations: {len(c_ast.declarations)}")
        
        converter = Converter()
        kato_ast = converter.convert(c_ast)
        
        if debug:
            print(f"Kato AST functions: {len(kato_ast.functions)}")
        
        generator = KatoGenerator()
        kato_code = generator.generate(kato_ast)
        
        if debug:
            print(f"Generated code length: {len(kato_code)}")
        
        return kato_code
    
    except C2KatoError as e:
        raise e
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise C2KatoError(f"Unexpected error: {e}")
