import os
import argparse
import threading
import typing
from queue import Queue    # `Queue` has all the locking semantics for a multi-threaded environment.

from catalog_page_worker import catalog_page_worker
from detail_page_worker import detail_page_worker, PAGE_RETRIEVAL_COMPLETE_PLACEHOLDER_URL


# MARK: - Main
def main(images_dir: str, catalog_page_urls: typing.List[str], detail_page_urls: typing.List[str]):
    # Verify parameters
    if os.path.exists(images_dir):
        if os.path.isdir(images_dir):
            print(f"Using images dir `{images_dir}`.")
        else:
            raise FileExistsError(f"Images dir `{images_dir}` is a file or link.")
    else:
        os.makedirs(images_dir)
        print(f"Created images dir `{images_dir}`.")

    if (not catalog_page_urls) and (not detail_page_urls):
        print("No URLs provided.")
        exit(1)

    # TODO: Add individual images to queue.
    image_detail_page_urls_queue = Queue()
    # for url in detail_page_urls:
    #     image_detail_page_urls_queue.put(url)

    # Create threads.
    catalog_page_thread = threading.Thread(target=catalog_page_worker, args=(image_detail_page_urls_queue, catalog_page_urls))
    detail_page_thread = threading.Thread(target=detail_page_worker, args=(image_detail_page_urls_queue, images_dir))

    catalog_page_thread.start()
    detail_page_thread.start()

    catalog_page_thread.join()
    image_detail_page_urls_queue.put((PAGE_RETRIEVAL_COMPLETE_PLACEHOLDER_URL, None))

    detail_page_thread.join()


# MARK: - Argument parser
def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--images_dir", "-d", type=str, default="images/")
    parser.add_argument("--catalog_page_urls", nargs="*", default=[])
    parser.add_argument("--detail_page_urls", nargs="*", default=[])

    return parser


# MARK: -
if __name__ == "__main__":
    print(f"Working directory: {os.getcwd()}")

    parser = get_argument_parser()
    args = parser.parse_args()

    main(args.images_dir, args.catalog_page_urls, args.detail_page_urls)
