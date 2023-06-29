from pathlib import Path
import platform
import tomllib

from mnar.project_path import get_language_profile_paths

class LanguageProfile:
    """
    Execution information for a programming language.

    Each instance of this class corresponds to a config file that specifies how
    to execute files for a particular language.
    """
    def __init__(self, profile_config_path: Path) -> None:
        with open(profile_config_path, "rb") as f:
            profile_data = tomllib.load(f)
            self._name: str = profile_data["name"]
            self._id: str = profile_data["id"]
            self._command: str = profile_data["command"]["default"]
            this_system = platform.system()
            if this_system in profile_data["command"]:
                self._command = profile_data["command"][this_system]

    @property
    def name(self) -> str:
        """The display name of this profile."""
        return self._name

    @property
    def id(self) -> str:
        """The id of this profile, meant to be a unique internal identifier."""
        return self._id

    @property
    def command(self) -> str:
        """The command template used to execute a file for this language."""
        return self._command

    def generate_command(self, file_path: str) -> str:
        """Generate command string from this profile's template."""
        return self._command.format(file_path=file_path)

def get_language_profiles() -> tuple[LanguageProfile]:
    """Return tuple of all language profiles."""
    return tuple(map(LanguageProfile, get_language_profile_paths()))