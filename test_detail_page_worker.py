import unittest
from queue import Queue
import tempfile
import os
import hashlib

import detail_page_worker
import file_helper


class DetailPageWorkerTestCase (unittest.TestCase):
    def test_2_urls(self):
        image_detail_page_urls_queue = Queue()
        image_detail_page_urls_queue.put(("https://safebooru.org/index.php?page=post&s=view&id=3579893", "https://safebooru.org/index.php?page=post&s=list&tags=shirt"))
        image_detail_page_urls_queue.put(("https://safebooru.org/index.php?page=post&s=view&id=3579822", "https://safebooru.org/index.php?page=post&s=list&tags=shirt&pid=40"))
        image_detail_page_urls_queue.put((detail_page_worker.PAGE_RETRIEVAL_COMPLETE_PLACEHOLDER_URL, None))

        with tempfile.TemporaryDirectory() as dir_name:
            detail_page_worker.detail_page_worker(image_detail_page_urls_queue, dir_name)

            self.assertTrue(file_helper.image_exists("3579893", dir_name))
            filename1 = os.path.join(dir_name, "3579893.png")
            self.assertTrue(os.path.isfile(filename1))
            with open(filename1, "rb") as f:
                content = f.read()
                hasher = hashlib.sha256()
                hasher.update(content)
                self.assertEqual(hasher.hexdigest(), "dc805946d3740d973fb17bf4229238621f33fbcc390f1d6a423a935fe2103dfe")

            self.assertTrue(file_helper.image_exists("3579822", dir_name))
            filename2 = os.path.join(dir_name, "3579822.jpg")
            self.assertTrue(os.path.isfile(filename2))
            with open(filename2, "rb") as f:
                content = f.read()
                hasher = hashlib.sha256()
                hasher.update(content)
                self.assertEqual(hasher.hexdigest(), "98922798774893dafc0c121874abcaf7d5106108fe871ae18edc07b8e15ac98b")


if __name__ == "__main__":
    unittest.main()
