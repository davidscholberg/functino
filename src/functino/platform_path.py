from pathlib import Path

from PyQt6.QtCore import QStandardPaths

def get_user_config_path() -> Path:
    """Get user configuration directory for this application."""
    user_config_path_str = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)
    if user_config_path_str == "":
        raise RuntimeError("could not determine user config path for this application")
    return Path(user_config_path_str)

def get_user_language_profiles_path() -> Path:
    """Get path of user language profiles directory."""
    return get_user_config_path() / "language_profiles"