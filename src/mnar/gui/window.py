from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QLabel, QLayout, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget

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
        central_widget = QWidget()
        central_widget.setLayout(self._make_layout())
        return central_widget

    def _make_layout(self) -> QLayout:
        """Create and return the layout for the central widget of this window."""
        layout = QVBoxLayout()
        layout.addWidget(self._editor)
        layout.addWidget(QLabel("Output:"))
        layout.addWidget(self._output_widget)
        return layout