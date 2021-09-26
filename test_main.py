import unittest
import argparse
import itertools

import main
from random_test_case_helper import get_random_catalog_page_url, get_random_detail_page_url


class ArgumentParserTestCase (unittest.TestCase):
    # region Images Dir
    def test_images_dir_without_url(self):
        test_dir_name = "test_dir"

        parser = main.get_argument_parser()
        args = parser.parse_args(["--images_dir", test_dir_name])

        self.assertIsInstance(args.images_dir, str)
        self.assertEqual(args.images_dir, test_dir_name)

        self.assertIsInstance(args.catalog_page_urls, list)
        self.assertFalse(args.catalog_page_urls)    # Should be empty.

        self.assertIsInstance(args.detail_page_urls, list)
        self.assertFalse(args.detail_page_urls)    # Should be empty.

    def test_missing_images_dir(self):
        parser = main.get_argument_parser()

        with self.assertRaises((argparse.ArgumentError, SystemExit)):
            parser.parse_args(["--images_dir"])

    # endregion

    # region URLs
    def test_catalog_page_urls(self):
        test_dir_name = "test_dir"

        parser = main.get_argument_parser()

        for (catalog_page_url_count, detail_page_url_count) in itertools.product(range(100), repeat=2):
            with self.subTest(catalog_page_url_count=catalog_page_url_count, detail_page_url_count=detail_page_url_count):
                catalog_page_urls = [get_random_catalog_page_url() for _ in range(catalog_page_url_count)]
                detail_page_urls = [get_random_detail_page_url() for _ in range(detail_page_url_count)]

                args_list = ["--images_dir", test_dir_name, "--catalog_page_urls"] + catalog_page_urls + ["--detail_page_urls"] + detail_page_urls

                args = parser.parse_args(args_list)

                self.assertIsInstance(args.catalog_page_urls, list)
                self.assertEqual(args.catalog_page_urls, catalog_page_urls)

                self.assertIsInstance(args.detail_page_urls, list)
                self.assertEqual(args.detail_page_urls, detail_page_urls)

    # endregion


if __name__ == "__main__":
    unittest.main()
