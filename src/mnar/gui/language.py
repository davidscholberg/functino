from typing import Type

from PyQt6.Qsci import QsciLexer, QsciLexerPython

def get_lexer_class(language_id: str) -> Type[QsciLexer]:
    match language_id:
        case "python":
            return QsciLexerPython
        case _:
            raise ValueError(f"unsupported language id: {language_id}")