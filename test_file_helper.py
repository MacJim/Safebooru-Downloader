import unittest
import tempfile
import os
import random

import file_helper


class ImageExistsTestCase (unittest.TestCase):
    def test_existing_image(self):
        test_ids = [str(random.randint(100000, 300000)) for _ in range(10)]
        test_extensions = [".jpg", ".png"]

        with tempfile.TemporaryDirectory() as dir_name:
            for test_id in test_ids:
                extension = random.choice(test_extensions)
                filename = f"{test_id}{extension}"
                filename = os.path.join(dir_name, filename)

                # Create the test file.
                with open(filename, "a"):
                    pass

                self.assertTrue(file_helper.image_exists(test_id, dir_name))


if __name__ == "__main__":
    unittest.main()
