from PyQt6 import sip
from PyQt6.Qsci import QsciLexer, QsciScintilla
from PyQt6.QtCore import Qt, QTimer
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

        Note that this function does not set the new margin width right away;
        instead, a one-shot timer with a small delay is used to do the update.
        The reason for this is that scintilla is apparently not notified of font
        changes right away, making the delay necessary. A simple sleep statement
        doesn't seem to suffice since apparently the notification happens at
        some other point in the event loop.
        """
        super().setFont(f)
        QTimer.singleShot(10, self.reset_line_number_margin_width)

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

    def reset_line_number_margin_width(self) -> None:
        """Recalculate line number margin width based on current font size."""
        margin_width = self.SendScintilla(QsciScintilla.SCI_TEXTWIDTH, QsciScintilla.STYLE_LINENUMBER, sip.voidptr(b"0"))
        self.setMarginWidth(0, round(margin_width * 2.5))