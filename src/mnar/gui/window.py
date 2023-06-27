from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget

from mnar.gui.editor import Editor

class CentralWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setLayout(MainLayout())

class MainLayout(QVBoxLayout):
    def __init__(self) -> None:
        super().__init__()
        self.addWidget(Editor())
        self.addWidget(QLabel("Output:"))
        self.addWidget(OutputWidget())

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Mnar")
        self.setCentralWidget(CentralWidget())

class OutputWidget(QPlainTextEdit):
    def __init__(self) -> None:
        super().__init__()
        self.setReadOnly(True)