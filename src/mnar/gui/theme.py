from pathlib import Path
from xml.etree import ElementTree

from PyQt6.QtGui import QColor, QPalette

class Theme:
    """
    Holds theme data.

    Internally, this class imports Notepad++ theme files and provides convenient
    access to the relevant data.
    """
    def __init__(self, theme_path: Path) -> None:
        tree = ElementTree.parse(theme_path)
        self._root = tree.getroot()

    def get_global_background_color(self) -> str:
        """Get the globally-defined background color."""
        return self._get_global_override_node().attrib["bgColor"]

    def get_global_text_color(self) -> str:
        """Get the globally-defined text color."""
        return self._get_global_override_node().attrib["fgColor"]

    def get_lexer_color_map(self, lexer_name: str) -> dict[int, str]:
        """Get map of style IDs to colors for the given lexer."""
        lexer_color_map = {}
        for word_style_node in self._get_lexer_node(lexer_name):
            lexer_color_map[int(word_style_node.attrib["styleID"])] = "#" + word_style_node.attrib["fgColor"]
        return lexer_color_map

    def _get_global_override_node(self) -> ElementTree.Element:
        """Get xml node with global override theme data."""
        global_override_node = self._root.find("./GlobalStyles/WidgetStyle[@name='Global Override']")
        if global_override_node is None:
            raise RuntimeError("couldn't find global override node in current theme")
        return global_override_node

    def _get_lexer_node(self, lexer_name: str) -> ElementTree.Element:
        """Get xml node with styles for the given lexer."""
        lexer_node = self._root.find(f"./LexerStyles/LexerType[@name='{lexer_name}']")
        if lexer_node is None:
            raise RuntimeError(f"couldn't find lexer node for '{lexer_name}' in current theme")
        return lexer_node

def get_themed_palette(theme: Theme, palette: QPalette) -> QPalette:
    """
    Create a palette based on the given one with the current theme applied.
    """
    themed_palette = QPalette(palette)
    global_text_color = theme.get_global_text_color()
    themed_palette.setColor(QPalette.ColorRole.Text, QColor(global_text_color))
    themed_palette.setColor(QPalette.ColorRole.WindowText, QColor(global_text_color))
    global_background_color = theme.get_global_background_color()
    themed_palette.setColor(QPalette.ColorRole.Base, QColor(global_background_color))
    themed_palette.setColor(QPalette.ColorRole.Window, QColor(global_background_color))
    return themed_palette

def get_uniform_palette(palette: QPalette) -> QPalette:
    """
    Create a palette based on the given one with more uniform colors.

    The goal with this palette is to make widgets blend together better and to
    prevent widgets from displaying different colors when the window is out of
    focus.
    """
    uniform_palette = QPalette(palette)
    uniform_palette.setColor(QPalette.ColorRole.Base, palette.color(QPalette.ColorRole.Base))
    uniform_palette.setColor(QPalette.ColorRole.Button, palette.color(QPalette.ColorRole.Button))
    uniform_palette.setColor(QPalette.ColorRole.ButtonText, palette.color(QPalette.ColorRole.ButtonText))
    uniform_palette.setColor(QPalette.ColorRole.Window, palette.color(QPalette.ColorRole.Base))
    return uniform_palette