import os
import subprocess

from mnar.file import write_to_tmp_file

def execute_file(file_path: str) -> tuple[str, str]:
    """Execute the given file and return the stdout and stderr."""
    result = subprocess.run(("python", file_path), capture_output=True)
    return (result.stdout.decode(), result.stderr.decode())

def get_output(code: str) -> tuple[str, str]:
    """Write code to file, execute it, and return the stdout and stderr."""
    file_path = write_to_tmp_file(code)
    output = execute_file(file_path)
    os.remove(file_path)
    return output