import unittest

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


if __name__ == "__main__":
    unittest.main()
