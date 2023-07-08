from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStyleHints
from PyQt6.QtWidgets import QApplication

from mnar.gui.icon import IconSet
from mnar.gui.theme import Theme
from mnar.gui.window import MainWindow
from mnar.project_path import get_themes_path

def run() -> None:
    """Create and display the application window."""
    app = QApplication([])
    app.setOrganizationName("davidscholberg")
    app.setApplicationName("mnar")
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