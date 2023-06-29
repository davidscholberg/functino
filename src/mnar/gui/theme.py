from PyQt6.QtGui import QPalette

def get_uniform_palette(palette: QPalette) -> QPalette:
    """Create a palette based on the given one with more uniform colors."""
    uniform_palette = QPalette(palette)
    uniform_palette.setColor(QPalette.ColorRole.Window, palette.color(QPalette.ColorRole.Base))
    return uniform_palette