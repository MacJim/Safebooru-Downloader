import unittest
from queue import Queue

from catalog_page_worker import catalog_page_worker


class CatalogPageWorkerTestCase (unittest.TestCase):
    def test_disguise_shirt(self):
        """
        This particular search has just 2 pages and should be fast to perform.
        """
        start_url = "https://safebooru.org/index.php?page=post&s=list&tags=disguise+shirt"

        image_detail_page_urls_queue = Queue()
        catalog_page_worker(image_detail_page_urls_queue, start_url)

        self.assertGreater(image_detail_page_urls_queue.qsize(), 40)
        self.assertLess(image_detail_page_urls_queue.qsize(), 80)    # NOTE: At the time of writing this test, this particular search has 47 results in total. As images get added over time, please re-perform the search to check if an increase in numbers is needed.

        while not image_detail_page_urls_queue.empty():
            image_detail_page_url, referer_url = image_detail_page_urls_queue.get()

            self.assertIsInstance(image_detail_page_url, str)
            # Example: index.php?page=post&s=view&id=3579606
            self.assertIn("?", image_detail_page_url)
            self.assertIn("id=", image_detail_page_url)

            self.assertIsInstance(referer_url, str)
            self.assertIn("https://safebooru.org/index.php", referer_url)


if __name__ == "__main__":
    unittest.main()
