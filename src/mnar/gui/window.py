from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QLabel, QLayout, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget

from mnar.gui.editor import Editor

class OutputWidget(QPlainTextEdit):
    def __init__(self) -> None:
        super().__init__()
        self.setReadOnly(True)

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Mnar")
        self._editor = Editor()
        self._output_widget = OutputWidget()
        self.setCentralWidget(self._make_central_widget())
        QShortcut(QKeySequence("Ctrl+r"), self).activated.connect(self.on_run)

    def on_run(self) -> None:
        editor_text = self._editor.text()
        self._output_widget.setPlainText(editor_text)

    def _make_central_widget(self) -> QWidget:
        central_widget = QWidget()
        central_widget.setLayout(self._make_layout())
        return central_widget

    def _make_layout(self) -> QLayout:
        layout = QVBoxLayout()
        layout.addWidget(self._editor)
        layout.addWidget(QLabel("Output:"))
        layout.addWidget(self._output_widget)
        return layout