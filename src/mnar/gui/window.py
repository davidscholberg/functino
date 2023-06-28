from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QLabel, QMainWindow, QPlainTextEdit, QSplitter, QVBoxLayout, QWidget

from mnar.execute import get_output
from mnar.gui.editor import Editor

class OutputWidget(QPlainTextEdit):
    """Widget for displaying the results of executing the code in the editor."""
    def __init__(self) -> None:
        super().__init__()
        self.setReadOnly(True)

class MainWindow(QMainWindow):
    """Main window for this application."""
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Mnar")
        self._editor = Editor()
        self._output_widget = OutputWidget()
        self.setCentralWidget(self._make_central_widget())
        QShortcut(QKeySequence("Ctrl+r"), self).activated.connect(self.on_run)

    def on_run(self) -> None:
        """Callback to run code from the editor."""
        editor_text = self._editor.text()
        stdout, stderr = get_output(editor_text)
        output_str = f"stderr:\n{stderr}\nstdout:\n{stdout}"
        self._output_widget.setPlainText(output_str)

    def _make_central_widget(self) -> QWidget:
        """Create and return the central widget for this window."""
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self._editor)
        output_container = QWidget()
        output_layout = QVBoxLayout()
        output_layout.addWidget(QLabel("Output:"))
        output_layout.addWidget(self._output_widget)
        output_container.setLayout(output_layout)
        splitter.addWidget(output_container)
        return splitter