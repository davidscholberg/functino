from typing import Type

from PyQt6.Qsci import (
    QsciLexer,
    QsciLexerBash,
    QsciLexerBatch,
    QsciLexerCMake,
    QsciLexerCoffeeScript,
    QsciLexerCPP,
    QsciLexerCSharp,
    QsciLexerCSS,
    QsciLexerD,
    QsciLexerFortran,
    QsciLexerFortran77,
    QsciLexerHTML,
    QsciLexerJava,
    QsciLexerJavaScript,
    QsciLexerJSON,
    QsciLexerLua,
    QsciLexerMakefile,
    QsciLexerMatlab,
    QsciLexerPascal,
    QsciLexerPerl,
    QsciLexerPostScript,
    QsciLexerPython,
    QsciLexerRuby,
    QsciLexerSpice,
    QsciLexerSQL,
    QsciLexerSRec,
    QsciLexerTCL,
    QsciLexerTekHex,
    QsciLexerTeX,
    QsciLexerVerilog,
    QsciLexerVHDL,
    QsciLexerXML,
    QsciLexerYAML,
)


def get_lexer_class(language_id: str) -> Type[QsciLexer] | None:
    """
    Get the lexer class associated with the language ID or none if there is no lexer
    class found.
    """
    match language_id:
        case "bash":
            return QsciLexerBash
        case "batch":
            return QsciLexerBatch
        case "cmake":
            return QsciLexerCMake
        case "coffeescript":
            return QsciLexerCoffeeScript
        case "c" | "cpp":
            return QsciLexerCPP
        case "cs":
            return QsciLexerCSharp
        case "css":
            return QsciLexerCSS
        case "d":
            return QsciLexerD
        case "fortran":
            return QsciLexerFortran
        case "fortran77":
            return QsciLexerFortran77
        case "html":
            return QsciLexerHTML
        case "java":
            return QsciLexerJava
        case "javascript.js":
            return QsciLexerJavaScript
        case "json":
            return QsciLexerJSON
        case "lua":
            return QsciLexerLua
        case "makefile":
            return QsciLexerMakefile
        case "matlab":
            return QsciLexerMatlab
        case "pascal":
            return QsciLexerPascal
        case "perl":
            return QsciLexerPerl
        case "postscript":
            return QsciLexerPostScript
        case "python":
            return QsciLexerPython
        case "ruby":
            return QsciLexerRuby
        case "spice":
            return QsciLexerSpice
        case "sql":
            return QsciLexerSQL
        case "srec":
            return QsciLexerSRec
        case "tcl":
            return QsciLexerTCL
        case "tehex":
            return QsciLexerTekHex
        case "tex":
            return QsciLexerTeX
        case "verilog":
            return QsciLexerVerilog
        case "vhdl":
            return QsciLexerVHDL
        case "xml":
            return QsciLexerXML
        case "yaml":
            return QsciLexerYAML
        case _:
            return None
