from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QLabel, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget

from mnar.gui.editor import Editor

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Mnar")
        layout = QVBoxLayout()
        layout.addWidget(Editor())
        layout.addWidget(QLabel("Output:"))
        output_widget = QPlainTextEdit()
        output_widget.setReadOnly(True)
        layout.addWidget(output_widget)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)