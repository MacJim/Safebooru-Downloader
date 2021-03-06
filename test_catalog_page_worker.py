import unittest
from queue import Queue

from catalog_page_worker import catalog_page_worker


class CatalogPageWorkerTestCase (unittest.TestCase):
    def test_disguise_shirt(self):
        """
        This particular search has just 2 pages and should be fast to perform.
        """
        start_urls = ["https://safebooru.org/index.php?page=post&s=list&tags=disguise+shirt"]

        image_detail_page_urls_queue = Queue()
        catalog_page_worker(image_detail_page_urls_queue, start_urls)

        self.assertGreater(image_detail_page_urls_queue.qsize(), 40)
        self.assertLess(image_detail_page_urls_queue.qsize(), 80)    # NOTE: At the time of writing this test, this particular search has 47 results in total. As images get added over time, please re-perform the search to check if an increase in numbers is needed.

        while not image_detail_page_urls_queue.empty():
            # They are both absolute URLs.
            image_detail_page_url, referer_url = image_detail_page_urls_queue.get()

            self.assertIsInstance(image_detail_page_url, str)
            self.assertTrue(image_detail_page_url.startswith("https://safebooru.org/index.php"))
            self.assertIn("?", image_detail_page_url)
            self.assertIn("id=", image_detail_page_url)

            self.assertIsInstance(referer_url, str)
            self.assertTrue(referer_url.startswith("https://safebooru.org/index.php"))

    def test_multiple_start_urls(self):
        start_urls = [
            "https://safebooru.org/index.php?page=post&s=list&tags=mizushima_mitsuyoshi",    # 4 results
            "https://safebooru.org/index.php?page=post&s=list&tags=yukiman",    # 66 results
            "https://safebooru.org/index.php?page=post&s=list&tags=boo_%28mario%29",    # 6 results
        ]

        image_detail_page_urls_queue = Queue()
        catalog_page_worker(image_detail_page_urls_queue, start_urls)

        self.assertGreater(image_detail_page_urls_queue.qsize(), 75)
        self.assertLess(image_detail_page_urls_queue.qsize(), 120)    # NOTE: At the time of writing this test, this particular search has 76 results in total. As images get added over time, please re-perform the search to check if an increase in numbers is needed.

        while not image_detail_page_urls_queue.empty():
            # They are both absolute URLs.
            image_detail_page_url, referer_url = image_detail_page_urls_queue.get()

            self.assertIsInstance(image_detail_page_url, str)
            self.assertTrue(image_detail_page_url.startswith("https://safebooru.org/index.php"))
            self.assertIn("?", image_detail_page_url)
            self.assertIn("id=", image_detail_page_url)

            self.assertIsInstance(referer_url, str)
            self.assertTrue(referer_url.startswith("https://safebooru.org/index.php"))


if __name__ == "__main__":
    unittest.main()
