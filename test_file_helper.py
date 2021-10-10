import string
import typing
import unittest
import tempfile
import os
import random

import file_helper
from random_test_case_helper import get_random_catalog_page_url, get_random_detail_page_url, get_random_filename


class ImageExistsTestCase (unittest.TestCase):
    # region Helpers
    @staticmethod
    def get_random_image_id_and_filename() -> typing.Tuple[str, str]:
        image_id = str(random.randint(100000, 300000))
        extension = random.choice([".jpg", ".png", ".webp"])

        return (image_id, f"{image_id}{extension}")

    # endregion

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


class GetURLFromFileTestCase (unittest.TestCase):
    # region Helpers
    @staticmethod
    def get_random_comment() -> str:
        """
        Gets a random comment string starting with a random comment prefix from `file_helper.COMMENT_PREFIXES`.
        """
        comment_start_seq = random.choice(file_helper.COMMENT_PREFIXES)

        line_length = random.randint(0, 50)
        return_value = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=line_length))
        return_value = comment_start_seq + return_value

        return return_value

    # endregion

    def test_non_existent_file(self):
        with tempfile.TemporaryDirectory() as root_dir_name:    # Use a temporary dir to prevent filename collisions.
            filename = get_random_filename()
            filename = os.path.join(root_dir_name, filename)

            with self.assertRaises(FileNotFoundError):
                file_helper.get_urls_from_file(filename)

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as root_dir_name:
            # Create an empty file.
            filename = get_random_filename()
            filename = os.path.join(root_dir_name, filename)
            with open(filename, "w"):
                pass

            # Should return no content.
            urls_from_file = file_helper.get_urls_from_file(filename)
            self.assertIsInstance(urls_from_file, list)
            self.assertEqual(len(urls_from_file), 0)
            self.assertFalse(urls_from_file)

    def test_comment_only_file(self):
        file_content = ""
        for _ in range(random.randint(5, 100)):
            file_content += GetURLFromFileTestCase.get_random_comment()
            file_content += "\n"

        with tempfile.TemporaryDirectory() as root_dir_name:
            # Create a comment-only file.
            filename = get_random_filename()
            filename = os.path.join(root_dir_name, filename)
            with open(filename, "w") as f:
                f.write(file_content)

            # Should return no content.
            urls_from_file = file_helper.get_urls_from_file(filename)
            self.assertIsInstance(urls_from_file, list)
            self.assertEqual(len(urls_from_file), 0)
            self.assertFalse(urls_from_file)

    def test_url_only_file(self):
        # Generate URLs.
        urls = []
        for _ in range(random.randint(5, 100)):
            urls.append(get_random_catalog_page_url())
        for _ in range(random.randint(5, 100)):
            urls.append(get_random_detail_page_url())
        random.shuffle(urls)

        # Generate file content from URLs.
        file_content = ""
        for url in urls:
            file_content += url
            file_content += "\n"

        with tempfile.TemporaryDirectory() as root_dir_name:
            # Create an URL-only file.
            filename = get_random_filename()
            filename = os.path.join(root_dir_name, filename)
            with open(filename, "w") as f:
                f.write(file_content)

            # Should return all URLs.
            urls_from_file = file_helper.get_urls_from_file(filename)
            self.assertIsInstance(urls_from_file, list)
            self.assertEqual(urls_from_file, urls_from_file)

    def test_url_comment_blank_mixture(self):
        # Generate URLs.
        urls = []

        for _ in range(random.randint(5, 100)):
            urls.append(get_random_catalog_page_url())
        for _ in range(random.randint(5, 100)):
            urls.append(get_random_detail_page_url())

        random.shuffle(urls)    # Need to shuffle URLs right away because we need to retain and check their order.

        # Generate comments and blank lines.
        comments_and_empty_lines = []

        for _ in range(random.randint(5, 100)):
            comments_and_empty_lines.append(GetURLFromFileTestCase.get_random_comment())
        for _ in range(random.randint(5, 100)):
            comments_and_empty_lines.append("")

        # Mix URLs and comments.
        urls_and_comments = comments_and_empty_lines + [None for _ in urls]
        random.shuffle(urls_and_comments)

        url_i = 0
        for i in range(len(urls_and_comments)):
            if urls_and_comments[i] is None:
                # Replace placeholders with true URLs.
                urls_and_comments[i] = urls[url_i]
                url_i += 1

        # Generate file content.
        file_content = ""
        for line in urls_and_comments:
            file_content += line
            file_content += "\n"

        with tempfile.TemporaryDirectory() as root_dir_name:
            # Create the file.
            filename = get_random_filename()
            filename = os.path.join(root_dir_name, filename)
            with open(filename, "w") as f:
                f.write(file_content)

            # Should return URLs in the correct order.
            urls_from_file = file_helper.get_urls_from_file(filename)
            self.assertIsInstance(urls_from_file, list)
            self.assertEqual(urls_from_file, urls)


if __name__ == "__main__":
    unittest.main()
