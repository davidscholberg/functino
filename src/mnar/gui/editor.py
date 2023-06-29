from PyQt6.Qsci import QsciScintilla
from PyQt6.QtWidgets import QFrame, QWidget

class Editor(QsciScintilla):
    """Editor widget."""
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMarginLineNumbers(1, True)
        self.setFrameStyle(QFrame.Shape.NoFrame)