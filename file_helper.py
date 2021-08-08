import os


def image_exists(image_id: str, images_dir: str) -> bool:
    """
    Tests if the image with `image_id` is already downloaded.

    :param image_id: 
    :param images_dir: 
    :return: 
    """
    existing_filenames = os.listdir(images_dir)
    existing_filenames = [os.path.splitext(f)[0] for f in existing_filenames]

    if image_id in existing_filenames:
        return True
    else:
        return False
