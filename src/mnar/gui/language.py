from typing import Type

from PyQt6.Qsci import QsciLexer, QsciLexerPython

def get_lexer_class(language_id: str) -> Type[QsciLexer] | None:
    """
    Get the lexer class associated with the language ID or none if there is no
    lexer class found.
    """
    match language_id:
        case "python":
            return QsciLexerPython
        case _:
            return None