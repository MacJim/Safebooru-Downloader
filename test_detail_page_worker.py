import unittest
from queue import Queue
import tempfile
import os
import hashlib
import typing

import detail_page_worker
import file_helper


URL_KEY: typing.Final = "url"
REFERER_KEY: typing.Final = "referer"
IMAGE_ID_KEY: typing.Final = "image_id"
FILENAME_KEY: typing.Final = "filename"
SHA_SUM_KEY: typing.Final = "sha_sum"


class DetailPageWorkerTestCase (unittest.TestCase):
    def test_2_urls(self):
        test_cases = [
            # With referer.
            {
                URL_KEY: "https://safebooru.org/index.php?page=post&s=view&id=3579893",
                REFERER_KEY: "https://safebooru.org/index.php?page=post&s=list&tags=shirt",
                IMAGE_ID_KEY: "3579893",
                FILENAME_KEY: "3579893.png",
                SHA_SUM_KEY: "dc805946d3740d973fb17bf4229238621f33fbcc390f1d6a423a935fe2103dfe",
            },
            {
                URL_KEY: "https://safebooru.org/index.php?page=post&s=view&id=3579822",
                REFERER_KEY: "https://safebooru.org/index.php?page=post&s=list&tags=shirt&pid=40",
                IMAGE_ID_KEY: "3579822",
                FILENAME_KEY: "3579822.jpg",
                SHA_SUM_KEY: "98922798774893dafc0c121874abcaf7d5106108fe871ae18edc07b8e15ac98b",
            },

            # Without referer (`--detail_page_urls` option).
            {
                URL_KEY: "https://safebooru.org/index.php?page=post&s=view&id=3630363",
                REFERER_KEY: None,
                IMAGE_ID_KEY: "3630363",
                FILENAME_KEY: "3630363.png",
                SHA_SUM_KEY: "47ca593d32f68b050109e02b837f69d2a4c82928654f2a64b6cb2b9cef0c6b40",
            },
            {
                URL_KEY: "https://safebooru.org/index.php?page=post&s=view&id=3629944",
                REFERER_KEY: None,
                IMAGE_ID_KEY: "3629944",
                FILENAME_KEY: "3629944.jpg",
                SHA_SUM_KEY: "eccfe4068ce8440f445e830bff9a0a9bc06e676952136c4312f3570166573928",
            }
        ]

        image_detail_page_urls_queue = Queue()
        for test_case in test_cases:
            image_detail_page_urls_queue.put((test_case[URL_KEY], test_case[REFERER_KEY]))

        # Completion placeholder.
        image_detail_page_urls_queue.put((detail_page_worker.PAGE_RETRIEVAL_COMPLETE_PLACEHOLDER_URL, None))

        with tempfile.TemporaryDirectory() as dir_name:
            detail_page_worker.detail_page_worker(image_detail_page_urls_queue, dir_name)

            for test_case in test_cases:
                with self.subTest(url=test_case[URL_KEY]):
                    self.assertTrue(file_helper.image_exists(test_case[IMAGE_ID_KEY], dir_name))

                    filename = os.path.join(dir_name, test_case[FILENAME_KEY])
                    self.assertTrue(os.path.isfile(filename))

                    with open(filename, "rb") as f:
                        content = f.read()
                        hasher = hashlib.sha256()
                        hasher.update(content)
                        self.assertEqual(hasher.hexdigest(), test_case[SHA_SUM_KEY])


if __name__ == "__main__":
    unittest.main()
