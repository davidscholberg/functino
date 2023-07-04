from tempfile import mkstemp

def write_to_tmp_file(contents: str) -> str:
    """Write given contents to temporary file and return file path."""
    fd, path = mkstemp()
    with open(fd, "w", newline="") as tmp_file:
        tmp_file.write(contents)
    return path