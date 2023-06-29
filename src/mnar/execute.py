import os
import subprocess

from mnar.file import write_to_tmp_file
from mnar.language import LanguageProfile

def execute(command: str) -> tuple[str, str]:
    """Execute the given command and return the stdout and stderr."""
    result = subprocess.run(command, capture_output=True)
    return (result.stdout.decode(), result.stderr.decode())

def get_output(language_profile: LanguageProfile, code: str) -> tuple[str, str]:
    """Write code to file, execute it, and return the stdout and stderr."""
    file_path = write_to_tmp_file(code)
    output = execute(language_profile.generate_command(file_path))
    os.remove(file_path)
    return output