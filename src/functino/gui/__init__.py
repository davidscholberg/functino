from typing import cast

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStyleHints
from PyQt6.QtWidgets import QApplication

from functino.gui.exception import pop_up_error_message
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
    try:
        match app.styleHints().colorScheme():
            case Qt.ColorScheme.Light:
                theme = Theme(get_themes_path() / "light.xml")
                icon_set = IconSet(IconSet.Light)
            case _:
                theme = Theme(get_themes_path() / "dark.xml")
                icon_set = IconSet(IconSet.Dark)
    except Exception as e:
        pop_up_error_message(e)
        return
    main_window = MainWindow(cast(Theme, theme), cast(IconSet, icon_set))
    main_window.show()
    app.exec()
