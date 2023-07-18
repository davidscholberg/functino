from importlib.abc import Traversable
from importlib.resources import files


def get_resources_path() -> Traversable:
    """
    Get path of resources directory.
    """
    return files("functino.resources")


def get_icons_path() -> Traversable:
    """
    Get path of icons directory.
    """
    return get_resources_path() / "icons"


def get_built_in_language_profiles_path() -> Traversable:
    """
    Get path of built-in language profiles directory.
    """
    return get_resources_path() / "language_profiles"


def get_themes_path() -> Traversable:
    """
    Get path of themes directory.
    """
    return get_resources_path() / "themes"
