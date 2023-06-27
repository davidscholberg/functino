from PyQt6.QtWidgets import QApplication

from mnar.gui.window import MainWindow

def run() -> None:
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()