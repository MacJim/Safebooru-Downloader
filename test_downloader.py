import unittest
import tempfile
import hashlib
import os

import downloader


class HeaderTestCase (unittest.TestCase):
    def test_no_referer(self):
        url = "https://www.google.com/search?q=hello"
        referer = None

        header_dict = downloader._get_header_for_url(url, referer)

        self.assertNotIn(downloader.HEADER_REFERER_KEY, header_dict)

        self.assertIn(downloader.HEADER_HOST_KEY, header_dict)
        self.assertEqual("www.google.com", header_dict[downloader.HEADER_HOST_KEY])

        self.assertEqual(downloader.HEADER_SEC_FETCH_SITE_VALUE_NONE, header_dict[downloader.HEADER_SEC_FETCH_SITE_KEY])

    def test_has_referer(self):
        url = "https://en.wikipedia.org/wiki/Hello"
        referer = "https://www.google.com/search?q=hello"

        header_dict = downloader._get_header_for_url(url, referer)

        self.assertIn(downloader.HEADER_REFERER_KEY, header_dict)
        self.assertEqual(referer, header_dict[downloader.HEADER_REFERER_KEY])

        self.assertIn(downloader.HEADER_HOST_KEY, header_dict)
        self.assertEqual("en.wikipedia.org", header_dict[downloader.HEADER_HOST_KEY])

        self.assertEqual(downloader.HEADER_SEC_FETCH_SITE_VALUE_SAME_ORIGIN, header_dict[downloader.HEADER_SEC_FETCH_SITE_KEY])


class RequestHTMLTestCase (unittest.TestCase):
    def test_google(self):
        url = "https://www.google.com"
        request_result = downloader.request_html(url)

        print("Google request result:")
        print(request_result[:100] + " ...")
        self.assertIsInstance(request_result, str)
        self.assertGreater(len(request_result), 0)

    def test_safebooru(self):
        url = "https://safebooru.org/index.php?page=post&s=list"
        request_result = downloader.request_html(url)

        print("Safebooru request result:")
        print(request_result[:100] + " ...")
        self.assertIsInstance(request_result, str)
        self.assertGreater(len(request_result), 0)


class DownloadFileTestCase (unittest.TestCase):
    def test_safebooru(self):
        test_files = [
            ("1.jpg", "https://safebooru.org//images/3439/f6214b519d1ae7295b1754e5a1cd80bccb9bdb4d.jpg", "2f75ffdb1393c1444ff930d0a4847df2ba75cee85cd370d5d59bcd706f3bb862"),
            ("2.jpg", "https://safebooru.org//images/3439/fe2aa73a8b208223d1f38078471eaf989347a7dc.jpg", "c3d1c5dfd189b1b9a5e664ffe32fe4e2d8c77eed7e8d2953ec37161ecd7efd14"),
        ]

        with tempfile.TemporaryDirectory() as dir_name:
            # print(f"Temporary dir name: {dir_name}")

            for filename, url, checksum in test_files:
                abs_filename = os.path.join(dir_name, filename)

                with self.subTest(abs_filename=abs_filename, url=url, checksum=checksum):
                    downloader.download_file(abs_filename, url)

                    with open(abs_filename, "rb") as f:
                        content = f.read()
                        hasher = hashlib.sha256()
                        hasher.update(content)
                        self.assertEqual(hasher.hexdigest(), checksum)

                    with self.assertRaises(FileExistsError):
                        downloader.download_file(abs_filename, url)


if __name__ == "__main__":
    unittest.main()
