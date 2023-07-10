from tempfile import mkstemp

def write_to_tmp_file(contents: str, file_extension: str, directory: str | None = None) -> str:
    """
    Write given contents to temporary file (optionally in the given directory)
    and return file path.
    """
    suffix = "." + file_extension if file_extension else None
    fd, path = mkstemp(dir=directory, suffix=suffix)
    with open(fd, "w", newline="") as tmp_file:
        tmp_file.write(contents)
    return path