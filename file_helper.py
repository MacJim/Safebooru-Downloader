import os


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
