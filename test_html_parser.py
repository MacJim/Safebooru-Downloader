import os
import unittest

import html_parser


class ServerOverloadTestCase (unittest.TestCase):
    def test_parse_normal(self):
        with open("test_cases/catalog_normal.html", "r") as f:
            page_html = f.read()

        self.assertFalse(html_parser.is_server_overloaded(page_html))

    def test_parse_last_page(self):
        with open("test_cases/catalog_last_page.html", "r") as f:
            page_html = f.read()

        self.assertFalse(html_parser.is_server_overloaded(page_html))

    def test_parse_overload_page(self):
        with open("test_cases/catalog_overload.html", "r") as f:
            page_html = f.read()

        self.assertTrue(html_parser.is_server_overloaded(page_html))


class CatalogPageTestCase (unittest.TestCase):
    def test_parse_normal(self):
        with open("test_cases/catalog_normal.html", "r") as f:
            page_html = f.read()

        next_page_url, image_detail_page_urls = html_parser.parse_catalog_page(page_html)

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

        next_page_url, image_detail_page_urls = html_parser.parse_catalog_page(page_html)

        self.assertIsNone(next_page_url)

        self.assertIsNotNone(image_detail_page_urls)
        self.assertIsInstance(image_detail_page_urls, list)
        self.assertGreater(len(image_detail_page_urls), 0)
        for image_detail_page_url in image_detail_page_urls:
            self.assertIsInstance(image_detail_page_url, str)


class ImageDetailPageTestCase (unittest.TestCase):
    def test_parse(self):
        with open("test_cases/image_detail.html", "r") as f:
            page_html = f.read()

        original_image_url = html_parser.parse_image_detail_page(page_html)

        self.assertIsInstance(original_image_url, str)
        self.assertEqual(original_image_url, "https://safebooru.org//images/3439/7ec73c4962fcaf745a2585b4922c745615324bf9.jpg")


if __name__ == '__main__':
    unittest.main()
