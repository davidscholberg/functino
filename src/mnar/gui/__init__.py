from PyQt6.QtWidgets import QApplication

from mnar.gui.window import MainWindow

def run() -> None:
    """Create and display the application window."""
    app = QApplication([])
    app.setOrganizationName("davidscholberg")
    app.setApplicationName("mnar")
    main_window = MainWindow()
    main_window.show()
    app.exec()