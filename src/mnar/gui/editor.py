from PyQt6 import sip
from PyQt6.Qsci import QsciLexer, QsciScintilla
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette
from PyQt6.QtWidgets import QFrame, QWidget

class Editor(QsciScintilla):
    """Editor widget."""
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setCaretForegroundColor(self.palette().color(QPalette.ColorRole.Text))
        self.setMarginsBackgroundColor(self.palette().color(QPalette.ColorRole.Base))
        self.setMarginsForegroundColor(Qt.GlobalColor.darkGray)
        self.setMarginLineNumbers(0, True)
        self.setMarginWidth(1, 0)
        self._lexer_copy = None

    def setFont(self, f: QFont) -> None:
        """
        Reimplementation of setFont so that we can set a proper line number
        margin width for the new font.

        Note that there's currently a bug that only affects calls to this
        function after the first one. The first call will set the correct line
        number margin width, but subsequent calls will set the width based on
        the previous font value instead of the current one. This may be due to a
        delay in the underlying scintilla library receiving the new font info.
        """
        super().setFont(f)
        margin_width = self.SendScintilla(QsciScintilla.SCI_TEXTWIDTH, QsciScintilla.STYLE_LINENUMBER, sip.voidptr(b"0"))
        self.setMarginWidth(0, round(margin_width * 2.5))

    def setLexer(self, lexer: QsciLexer) -> None:
        """
        Reimplementation of setLexer so that we can keep an external reference
        to the lexer.

        This is needed because the lexer() method currently has a bug where it
        does not return the lexer previously set with setLexer().
        """
        self._lexer_copy = lexer
        return super().setLexer(lexer)

    def lexer(self) -> QsciLexer | None:
        """
        Reimplementation of lexer that returns our own copy of the lexer set
        with setLexer().

        This is needed because the lexer() method currently has a bug where it
        does not return the lexer previously set with setLexer().
        """
        return self._lexer_copy