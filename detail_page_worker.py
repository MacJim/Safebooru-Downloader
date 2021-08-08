"""
Details page retrieval and image downloader thread.
"""

import typing
from queue import Queue
import urllib.parse
import os
import random
import time

import file_helper
import downloader
import html_parser


IMAGE_DETAIL_PAGE_RETRIEVAL_INTERVAL_RANGE: typing.Final = (10.0, 20.0)
"""
A random float number will be chosen between this range for the (sleep) interval between image detail page requests.
"""

PAGE_RETRIEVAL_COMPLETE_PLACEHOLDER_URL: typing.Final = "complete_placeholder_url"
"""
The main thread pushes this item into the queue once the catalog page thread has joined.

The image detail page thread exits once it encounters this item from the queue.
"""

IMAGE_ID_KEY: typing.Final = "id"
"""
Image ID key in the GET parameter.

Example: `https://safebooru.org/index.php?page=post&s=view&id=1348630`
"""


def details_page_worker(image_detail_page_urls_queue: Queue, images_dir: str):
    while True:
        page_url, referer = image_detail_page_urls_queue.get(block=True)    # Must block here until the catalog page thread adds more URLs.
        if page_url == PAGE_RETRIEVAL_COMPLETE_PLACEHOLDER_URL:
            # No more URLs.
            print("Finished parsing all image detail pages.")
            return

        # Get image ID from page URL.
        parsed_page_url = urllib.parse.urlparse(page_url)
        get_parameters = urllib.parse.parse_qs(parsed_page_url.query)
        image_id = get_parameters[IMAGE_ID_KEY]    # This is actually a list.
        image_id = image_id[0]

        if file_helper.image_exists(image_id, images_dir):
            # Image already downloaded.
            print(f"Image {image_id} exists and will be skipped.")
            continue

        # Request.
        html_str = downloader.request_html(page_url, referer)

        # Get image URL from page HTML.
        image_url = html_parser.parse_image_detail_page(html_str)
        image_url = urllib.parse.urljoin(page_url, image_url)    # Convert to absolute URL.

        # Get image extension (typically `.jpg` or `.png`) from image URL.
        parsed_image_url = urllib.parse.urlparse(image_url)
        extension = os.path.splitext(parsed_image_url.path)[1]

        image_filename = image_id + extension
        image_filename = os.path.join(images_dir, image_filename)

        downloader.download_file(image_filename, image_url)

        print(f"Downloaded image {image_id} to `{image_filename}`.")

        # Sleep between pages.
        sleep_duration = random.uniform(IMAGE_DETAIL_PAGE_RETRIEVAL_INTERVAL_RANGE[0], IMAGE_DETAIL_PAGE_RETRIEVAL_INTERVAL_RANGE[1])
        print(f"Sleeping for {sleep_duration:.2f} seconds before parsing the next details page.")
        time.sleep(sleep_duration)
