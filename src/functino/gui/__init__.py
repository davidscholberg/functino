from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStyleHints
from PyQt6.QtWidgets import QApplication

from functino.gui.icon import IconSet
from functino.gui.theme import Theme
from functino.gui.window import MainWindow
from functino.project_path import get_themes_path

def run() -> None:
    """Create and display the application window."""
    app = QApplication([])
    app.setOrganizationName("functinodev")
    app.setApplicationName("functino")
    app.setStyle("fusion")
    theme = None
    icon_set = None
    match app.styleHints().colorScheme():
        case Qt.ColorScheme.Light:
            theme = Theme(get_themes_path() / "light.xml")
            icon_set = IconSet(IconSet.Light)
        case _:
            theme = Theme(get_themes_path() / "dark.xml")
            icon_set = IconSet(IconSet.Dark)
    main_window = MainWindow(theme, icon_set)
    main_window.show()
    app.exec()
