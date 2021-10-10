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


# region Read URL from File
COMMENT_PREFIXES: typing.Final = ["#"]


def get_urls_from_file(filename: str) -> typing.List[str]:
    """
    Read URLs from the specified file.

    Empty lines and lines starting with `COMMENT_PREFIXES` are ignored.

    :param filename: Filename of the URLs file. Raises `OSError` if it doesn't exist.
    :return:
    """
    return_value = []

    with open(filename) as f:
        for line in f:
            # Lines read this way contain a trailing '\n' (except for the last line)
            if line.endswith('\n'):
                line = line[:-1]

            # Ignore empty lines.
            if not line:
                continue

            # Ignore comment lines.
            is_comment = False
            for seq in COMMENT_PREFIXES:
                if line.startswith(seq):
                    is_comment = True
                    break

            if is_comment:
                # This line is a comment.
                continue

            return_value.append(line)

    return return_value

# endregion
