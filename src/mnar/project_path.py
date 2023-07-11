from pathlib import Path

def get_project_root() -> Path:
    """Get path of project root."""
    return Path(__file__).parent

def get_resources_path() -> Path:
    """Get path of resources directory."""
    return get_project_root() / "resources"

def get_icons_path() -> Path:
    """Get path of icons directory."""
    return get_resources_path() / "icons"

def get_built_in_language_profiles_path() -> Path:
    """Get path of language profiles directory."""
    return get_resources_path() / "language_profiles"

def get_themes_path() -> Path:
    """Get path of themes directory."""
    return get_resources_path() / "themes"