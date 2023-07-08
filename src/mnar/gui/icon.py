from pathlib import Path
from mnar.project_path import get_icons_path

class IconSet:
    """Manages paths to icons based on color mode."""
    Dark = 0
    Light = 1

    def __init__(self, color_mode: int) -> None:
        """
        Create instance based on color mode.

        Color mode can only be one of IconSet.Dark and IconSet.Light.
        """
        match color_mode:
            case self.Dark:
                self._play_path = get_icons_path() / "play_dark.svg"
            case self.Light:
                self._play_path = get_icons_path() / "play_light.svg"
            case _:
                raise ValueError(f"invalid color mode {color_mode}")

    @property
    def play_path(self) -> Path:
        """Return the path to the play icon."""
        return self._play_path