import os
import unittest

import parser


class ServerOverloadTestCase (unittest.TestCase):
    def test_parse_normal(self):
        with open("test_cases/catalog_normal.html", "r") as f:
            page_html = f.read()

        self.assertFalse(parser.is_server_overloaded(page_html))

    def test_parse_last_page(self):
        with open("test_cases/catalog_last_page.html", "r") as f:
            page_html = f.read()

        self.assertFalse(parser.is_server_overloaded(page_html))

    def test_parse_overload_page(self):
        with open("test_cases/catalog_overload.html", "r") as f:
            page_html = f.read()

        self.assertTrue(parser.is_server_overloaded(page_html))


class CatalogPageTestCase (unittest.TestCase):
    # TODO:
    # previous_working_dir = None
    #
    # @classmethod
    # def setUpClass(cls) -> None:
    #     cls.previous_working_dir = os.getcwd()
    #     os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #     # print(f"Switched to project dir: {os.getcwd()}")
    #
    # @classmethod
    # def tearDownClass(cls) -> None:
    #     os.chdir(cls.previous_working_dir)
    #     # print(f"Switched back to original dir: {os.getcwd()}")

    def test_parse_normal(self):
        with open("test_cases/catalog_normal.html", "r") as f:
            page_html = f.read()

        parser.parse_catalog_page(page_html)

    def test_parse_last_page(self):
        with open("test_cases/catalog_last_page.html", "r") as f:
            page_html = f.read()

        parser.parse_catalog_page(page_html)


if __name__ == '__main__':
    unittest.main()
