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
            self._language_id: str = profile_data["language_id"]
            self._compile: bool = profile_data["compile"]
            self._command: tuple[str] = tuple(profile_data["command"]["default"])
            this_system = platform.system()
            if this_system in profile_data["command"]:
                self._command = tuple(profile_data["command"][this_system])

    @property
    def name(self) -> str:
        """The display name of this profile."""
        return self._name

    @property
    def language_id(self) -> str:
        """The ID of the language to use with this profile."""
        return self._language_id

    @property
    def compile(self) -> bool:
        """
        Whether or not this profile requires separate compilation and execution
        stages.
        """
        return self._compile

    @property
    def command(self) -> tuple[str]:
        """
        The command template used to compile or execute a file for this profile.
        """
        return self._command

    def generate_command(self, file_path: str, executable_path: str | None = None) -> tuple[str]:
        """
        Generate command tuple from this profile's template.

        If the current profile requires a compilation step, executable_path must
        be set to a writeable path. Conversely, if the current profile does not
        require a compilation step, executable_path must be None.
        """
        if self._compile and executable_path is None:
            raise RuntimeError("executable path must be set for compile profiles")
        if not self._compile and executable_path is not None:
            raise RuntimeError("executable path must not be set for non-compile profiles")
        command_args = []
        file_path_template_found = False
        executable_path_template_found = False
        for arg in self._command:
            if arg == r"{file_path}":
                arg = arg.format(file_path=file_path)
                file_path_template_found = True
            elif self._compile and arg == r"{executable_path}":
                arg = arg.format(executable_path=executable_path)
                executable_path_template_found = True
            command_args.append(arg)
        if not file_path_template_found:
            raise RuntimeError("command template did not contain a file path template")
        if self._compile and not executable_path_template_found:
            raise RuntimeError("command template did not contain an executable path template")
        return tuple(command_args)

def get_language_profiles() -> tuple[LanguageProfile]:
    """Return tuple of all language profiles."""
    return tuple(map(LanguageProfile, get_language_profile_paths()))