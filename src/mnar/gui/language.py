from typing import Type

from PyQt6.Qsci import QsciLexer, QsciLexerCPP, QsciLexerPython

def get_lexer_class(language_id: str) -> Type[QsciLexer] | None:
    """
    Get the lexer class associated with the language ID or none if there is no
    lexer class found.
    """
    match language_id:
        case "c" | "cpp":
            return QsciLexerCPP
        case "python":
            return QsciLexerPython
        case _:
            return None