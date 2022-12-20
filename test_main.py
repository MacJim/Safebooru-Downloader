import unittest
import argparse
import itertools

import main
from random_test_case_helper import get_random_catalog_page_url, get_random_detail_page_url, get_random_filename


class ArgumentParserTestCase (unittest.TestCase):
    # region Images Dir
    def test_images_dir_without_url(self):
        test_dir_name = get_random_filename()

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

        with self.assertRaises((argparse.ArgumentError, SystemExit)):    # This still produces an error message :(
            parser.parse_args(["--images_dir"])

    # endregion

    # region URLs
    def test_urls(self):
        parser = main.get_argument_parser()

        for (catalog_page_url_count, detail_page_url_count) in itertools.product(range(100), repeat=2):
            with self.subTest(catalog_page_url_count=catalog_page_url_count, detail_page_url_count=detail_page_url_count):
                test_dir_name = get_random_filename()
                catalog_page_urls = [get_random_catalog_page_url() for _ in range(catalog_page_url_count)]
                detail_page_urls = [get_random_detail_page_url() for _ in range(detail_page_url_count)]

                args_list = ["--images_dir", test_dir_name, "--catalog_page_urls"] + catalog_page_urls + ["--detail_page_urls"] + detail_page_urls

                args = parser.parse_args(args_list)

                self.assertIsInstance(args.images_dir, str)
                self.assertEqual(args.images_dir, test_dir_name)

                self.assertIsInstance(args.catalog_page_urls, list)
                self.assertEqual(args.catalog_page_urls, catalog_page_urls)

                self.assertIsInstance(args.detail_page_urls, list)
                self.assertEqual(args.detail_page_urls, detail_page_urls)

    # endregion

    # region Filenames
    def test_filenames(self):
        test_dir_name = get_random_filename()
        filename_test_cases = []
        for i in range(10):
            filename_test_cases.append((None, None, [get_random_filename() for _ in range(i)]))
            filename_test_cases.append((get_random_filename(), None, [get_random_filename() for _ in range(i)]))
            filename_test_cases.append((None, get_random_filename(), [get_random_filename() for _ in range(i)]))
            filename_test_cases.append((get_random_filename(), get_random_filename(), [get_random_filename() for _ in range(i)]))

        parser = main.get_argument_parser()

        for catalog_page_urls_filename, detail_page_urls_filename, ignored_image_ids_filenames in filename_test_cases:
            # Construct and parse arguments.
            args_list = ["--images_dir", test_dir_name]
            if catalog_page_urls_filename:
                args_list += ["--catalog_page_urls_filename", catalog_page_urls_filename]
            if detail_page_urls_filename:
                args_list += ["--detail_page_urls_filename", detail_page_urls_filename]
            if ignored_image_ids_filenames:
                args_list.append("--ignored_image_ids_filenames")
                for filename in ignored_image_ids_filenames:
                    args_list.append(filename)

            args = parser.parse_args(args_list)

            # Assertions.
            self.assertIsInstance(args.images_dir, str)
            self.assertEqual(args.images_dir, test_dir_name)

            if catalog_page_urls_filename:
                self.assertIsInstance(args.catalog_page_urls_filename, str)
            self.assertEqual(args.catalog_page_urls_filename, catalog_page_urls_filename)

            if detail_page_urls_filename:
                self.assertIsInstance(args.detail_page_urls_filename, str)
            self.assertEqual(args.detail_page_urls_filename, detail_page_urls_filename)

            self.assertIsInstance(args.ignored_image_ids_filenames, list)
            self.assertEqual(args.ignored_image_ids_filenames, ignored_image_ids_filenames)

    # endregion


if __name__ == "__main__":
    unittest.main()
