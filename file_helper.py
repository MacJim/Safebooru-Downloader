import os


def image_exists(id: str, images_dir: str) -> bool:
    existing_filenames = os.listdir(images_dir)
    existing_filenames = [os.path.splitext(f)[0] for f in existing_filenames]
    if id in existing_filenames:
        return True
    else:
        return False
