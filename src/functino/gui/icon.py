from functino.project_path import get_icons_path


class IconSet:
    """
    Loads icon data based on color mode.
    """

    Dark = 0
    Light = 1

    def __init__(self, color_mode: int) -> None:
        """
        Create instance based on color mode.

        Color mode can only be one of IconSet.Dark and IconSet.Light.
        """
        icons_path = get_icons_path()
        match color_mode:
            case self.Dark:
                self._play_icon_data = icons_path.joinpath("play_dark.svg").read_bytes()
                self._settings_icon_data = icons_path.joinpath(
                    "settings_dark.svg"
                ).read_bytes()
            case self.Light:
                self._play_icon_data = icons_path.joinpath(
                    "play_light.svg"
                ).read_bytes()
                self._settings_icon_data = icons_path.joinpath(
                    "settings_light.svg"
                ).read_bytes()
            case _:
                raise ValueError(f"invalid color mode {color_mode}")

    @property
    def play_icon_data(self) -> bytes:
        """
        Return the data for the play icon.
        """
        return self._play_icon_data

    @property
    def settings_icon_data(self) -> bytes:
        """
        Return the data for the settings icon.
        """
        return self._settings_icon_data
