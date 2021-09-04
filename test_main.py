import string
import unittest
import argparse
import random

import main


class ArgumentParserTestCase (unittest.TestCase):
    def test_images_dir(self):
        test_dir_name = "test_dir"

        parser = main.get_argument_parser()
        args = parser.parse_args(["--images_dir", test_dir_name])
        self.assertEqual(args.images_dir, test_dir_name)

    def test_missing_images_dir(self):
        parser = main.get_argument_parser()

        with self.assertRaises((argparse.ArgumentError, SystemExit)):
            parser.parse_args(["--images_dir"])

    def test_catalog_page_urls(self):
        test_dir_name = "test_dir"
        catalog_page_url_prefix = "https://safebooru.org/index.php?page=post&s=list&tags="
        catalog_page_url_suffix_len_range = (1, 100)

        parser = main.get_argument_parser()

        for catalog_page_url_count in range(100):
            with self.subTest(catalog_page_url_count=catalog_page_url_count):
                # Create a list of random test catalog URLs.
                catalog_page_urls = []
                for _ in range(catalog_page_url_count):
                    random_tag_name = "".join(random.choices(string.ascii_lowercase + "+" + "-", k=random.randint(catalog_page_url_suffix_len_range[0], catalog_page_url_suffix_len_range[1])))
                    catalog_page_urls.append(catalog_page_url_prefix + random_tag_name)

                args_list = ["--images_dir", test_dir_name, "--catalog_page_urls"] + catalog_page_urls

                args = parser.parse_args(args_list)
                self.assertEqual(args.catalog_page_urls, catalog_page_urls)


if __name__ == "__main__":
    unittest.main()
