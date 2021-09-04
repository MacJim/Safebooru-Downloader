"""
Catalog page retrieval thread.
"""

import typing
import time
import random
from queue import Queue
import urllib.parse

import downloader
import html_parser


SERVER_OVERLOADED_WAIT_INTERVAL_RANGE: typing.Final = (60.0, 120.0)
"""
If the catalog page thread encounters a server overload event, a random float number will be chosen between this range for the catalog page thread to sleep.
"""

PAGE_RETRIEVAL_INTERVAL_RANGE: typing.Final = (30.0, 60.0)
"""
A random float number will be chosen between this range for the (sleep) interval between catalog page requests.
"""


def catalog_page_worker(image_detail_page_urls_queue: Queue, catalog_page_urls: typing.List[str]):
    current_urls_and_referers: typing.List[typing.Tuple[str, typing.Optional[str]]] = [(url, None) for url in reversed(catalog_page_urls)]
    """
    A list of catalog page URLs and corresponding referers.
    
    Highest priority items are on the back (to ease `list.pop` behavior).
    """

    while current_urls_and_referers:
        current_url, referer = current_urls_and_referers[-1]

        print(f"Parsing catalog page `{current_url}` with referer `{referer}`.")

        html_str = downloader.request_html(current_url, referer)

        if html_parser.is_server_overloaded(html_str):
            # Server overloaded -> Sleep for a long time.
            sleep_duration = random.uniform(SERVER_OVERLOADED_WAIT_INTERVAL_RANGE[0], SERVER_OVERLOADED_WAIT_INTERVAL_RANGE[1])
            print(f"Server is overloaded. Sleeping for {sleep_duration:.2f} seconds before trying again.")
            time.sleep(sleep_duration)
            continue
        else:
            # Remove the current URL if the server isn't overloaded.
            current_urls_and_referers.pop()

        # Parse the current catalog page.
        next_page_url, image_detail_page_urls = html_parser.parse_catalog_page(html_str)

        # Add parsed detail page URLs and current URL (used as referer) to queue.
        for image_detail_page_url in image_detail_page_urls:
            image_detail_page_url = urllib.parse.urljoin(current_url, image_detail_page_url)
            image_detail_page_urls_queue.put((image_detail_page_url, current_url))

        print(f"Parsed {len(image_detail_page_urls)} URLs from `{current_url}`.")

        # Add next catalog page URL to `current_urls_and_referers` if this is not the last page.
        if next_page_url:
            # This is not the last page.
            next_url = urllib.parse.urljoin(current_url, next_page_url)    # `next_page_url` is usually relative: Need to join with current URL.
            next_referer = current_url

            current_urls_and_referers.append((next_url, next_referer))

        # Sleep between pages (if there are still pages remaining).
        if current_urls_and_referers:
            sleep_duration = random.uniform(PAGE_RETRIEVAL_INTERVAL_RANGE[0], PAGE_RETRIEVAL_INTERVAL_RANGE[1])
            print(f"Sleeping for {sleep_duration:.2f} seconds before parsing the next catalog page.")
            time.sleep(sleep_duration)

    print(f"Finished parsing all catalog pages!")
