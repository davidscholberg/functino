import os
import subprocess
from tempfile import TemporaryDirectory, mkstemp
from typing import cast

from functino.file import write_to_tmp_file
from functino.language import LanguageProfile

def get_output(language_profile: LanguageProfile, code: str) -> tuple[str, str]:
    """
    Write code to file, execute it, and return the stdout and stderr.

    If the given language profile requires compilation and if the compilation
    fails, the results of the compilation will be returned.
    """
    with TemporaryDirectory() as temp_dir_path:
        source_file_path = write_to_tmp_file(code, language_profile.source_file_extension, temp_dir_path)
        executable_file_path: str | None = None
        if language_profile.compile:
            fd, executable_file_path = mkstemp(dir=temp_dir_path, suffix=".exe")
            os.close(fd)
        command = language_profile.generate_command(source_file_path, executable_file_path)
        result = subprocess.run(command, capture_output=True, shell=False)
        if language_profile.compile and result.returncode == 0:
            result = subprocess.run((cast(str, executable_file_path),), capture_output=True, shell=False)
        return (result.stdout.decode(), result.stderr.decode())
