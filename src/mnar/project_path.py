from pathlib import Path

def get_project_root() -> Path:
    """Get path of project root."""
    return Path(__file__).parent

def get_resources_path() -> Path:
    """Get path of resources directory."""
    return get_project_root() / "resources"

def get_language_profiles_path() -> Path:
    """Get path of language profiles directory."""
    return get_resources_path() / "language_profiles"

def get_language_profile_paths() -> tuple[Path]:
    """Get paths of all language profiles."""
    parent_dir = get_language_profiles_path()
    return tuple(parent_dir.glob("*.toml"))