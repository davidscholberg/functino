from pathlib import Path

from platformdirs import PlatformDirs, PlatformDirsABC

def get_platformdirs() -> PlatformDirsABC:
    """Get the PlatformDirs object for this application."""
    return PlatformDirs("mnar", "davidscholberg")

def get_user_config_path() -> Path:
    """Get user configuration directory for this application."""
    return Path(get_platformdirs().user_config_dir)

def get_user_language_profiles_path() -> Path:
    """Get path of user language profiles directory."""
    return get_user_config_path() / "language_profiles"