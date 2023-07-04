from PyQt6 import sip
from PyQt6.Qsci import QsciScintilla
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette
from PyQt6.QtWidgets import QFrame, QWidget

class Editor(QsciScintilla):
    """Editor widget."""
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setFont(QFont("Consolas", 12))
        self.setCaretForegroundColor(self.palette().color(QPalette.ColorRole.Text))
        self.setMarginsBackgroundColor(self.palette().color(QPalette.ColorRole.Base))
        self.setMarginsForegroundColor(Qt.GlobalColor.darkGray)
        self.setMarginLineNumbers(0, True)
        margin_width = self.SendScintilla(QsciScintilla.SCI_TEXTWIDTH, QsciScintilla.STYLE_LINENUMBER, sip.voidptr(b"0"))
        self.setMarginWidth(0, round(margin_width * 2.5))
        self.setMarginWidth(1, 0)