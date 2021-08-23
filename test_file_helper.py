import string
import typing
import unittest
import tempfile
import os
import random

import file_helper


class ImageExistsTestCase (unittest.TestCase):
    # MARK: - Helpers
    @staticmethod
    def get_random_image_id_and_filename() -> typing.Tuple[str, str]:
        image_id = str(random.randint(100000, 300000))
        extension = random.choice([".jpg", ".png", ".webp"])

        return (image_id, f"{image_id}{extension}")

    # MARK: - Tests
    def test_existing_images_in_root_dir(self):
        with tempfile.TemporaryDirectory() as dir_name:
            for _ in range(10):
                image_id, filename = ImageExistsTestCase.get_random_image_id_and_filename()
                filename = os.path.join(dir_name, filename)

                # Create the test file.
                with open(filename, "a"):
                    pass

                self.assertTrue(file_helper.image_exists(image_id, dir_name))

    def test_existing_images_in_sub_dirs(self):
        with tempfile.TemporaryDirectory() as root_dir_name:
            for sub_dir_len in range(3, 10):
                dir_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=sub_dir_len))
                dir_name = os.path.join(root_dir_name, dir_name)
                os.mkdir(dir_name)

                for _ in range(5):
                    image_id, filename = ImageExistsTestCase.get_random_image_id_and_filename()
                    filename = os.path.join(dir_name, filename)

                    # Create the test file.
                    with open(filename, "a"):
                        pass

                    self.assertTrue(file_helper.image_exists(image_id, root_dir_name))

    def test_absent_images_in_root_dir(self):
        test_ids = [str(random.randint(100000, 300000)) for _ in range(10)]

        with tempfile.TemporaryDirectory() as dir_name:
            for test_id in test_ids:
                self.assertFalse(file_helper.image_exists(test_id, dir_name))


if __name__ == "__main__":
    unittest.main()
