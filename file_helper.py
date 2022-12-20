import os
import typing


# region File Exists
def image_exists(image_id: str, images_dir: str) -> bool:
    """
    Tests if the image with `image_id` is already downloaded in `images_dir` or its sub-dir.

    :param image_id:
    :param images_dir:
    :return:
    """
    for _, _, filenames in os.walk(images_dir):
        filenames_without_extensions = [os.path.splitext(f)[0] for f in filenames]

        if image_id in filenames_without_extensions:
            return True

    return False

# endregion


# region Load File
COMMENT_PREFIXES: typing.Final = ["#"]


def _process_line(line: str) -> typing.Optional[str]:
    """
    :return: `None` if the line is a comment or is empty; The line stripped of the trailing '\n' otherwise.
    """
    # Lines read this way contain a trailing '\n' (except for the last line)
    if line.endswith('\n'):
        line = line[:-1]

    # Ignore empty lines.
    if not line:
        return None

    # Ignore comment lines.
    for seq in COMMENT_PREFIXES:
        if line.startswith(seq):
            return None

    return line


def get_urls_from_file(filename: str) -> typing.List[str]:
    """
    Read URLs from the specified file.
    1 URL per line.

    Empty lines and lines starting with `COMMENT_PREFIXES` are ignored.

    :param filename: Filename of the URLs file. Raises `FileNotFoundError` if it doesn't exist.
    :return:
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"`{filename}` isn't a file.")

    return_value = []

    with open(filename) as f:
        for line in f:
            line = _process_line(line)
            if line:
                return_value.append(line)

    return return_value


def get_ids_from_file(filename: str) -> typing.Set[str]:
    """
    Read numeric IDs from the specified file.
    1 ID per line.

    - Empty lines and lines starting with `COMMENT_PREFIXES` are ignored
    - Invalid lines will cause a `ValueError` to be raised

    :param filename: Filename of the URLs file. Raises `FileNotFoundError` if it doesn't exist.
    :return: A set of ignored IDs (`str`, not `int`)
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"`{filename}` isn't a file.")

    return_value = set()

    with open(filename) as f:
        for line in f:
            line = _process_line(line)
            if line:
                if line.isdigit():
                    return_value.add(line)
                else:
                    raise ValueError(f"Line `{line}` contains non-digits.")

    return return_value

# endregion
