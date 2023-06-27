from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Mnar")
        self.setFixedSize(QSize(400, 300))
        self.setCentralWidget(QPushButton("Push me fam"))