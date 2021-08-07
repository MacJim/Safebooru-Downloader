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
    def test_parse_normal(self):
        with open("test_cases/catalog_normal.html", "r") as f:
            page_html = f.read()

        next_page_url, image_detail_page_urls = parser.parse_catalog_page(page_html)

        self.assertIsNotNone(next_page_url)
        self.assertIsInstance(next_page_url, str)

        self.assertIsNotNone(image_detail_page_urls)
        self.assertIsInstance(image_detail_page_urls, list)
        self.assertGreater(len(image_detail_page_urls), 0)
        for image_detail_page_url in image_detail_page_urls:
            self.assertIsInstance(image_detail_page_url, str)

    def test_parse_last_page(self):
        with open("test_cases/catalog_last_page.html", "r") as f:
            page_html = f.read()

        next_page_url, image_detail_page_urls = parser.parse_catalog_page(page_html)

        self.assertIsNone(next_page_url)

        self.assertIsNotNone(image_detail_page_urls)
        self.assertIsInstance(image_detail_page_urls, list)
        self.assertGreater(len(image_detail_page_urls), 0)
        for image_detail_page_url in image_detail_page_urls:
            self.assertIsInstance(image_detail_page_url, str)


if __name__ == '__main__':
    unittest.main()
