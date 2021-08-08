import os
import argparse
import threading
from queue import Queue    # `Queue` has all the locking semantics for a multi-threaded environment.

from catalog_page_worker import catalog_page_worker
from detail_page_worker import detail_page_worker, PAGE_RETRIEVAL_COMPLETE_PLACEHOLDER_URL


# MARK: - Main
def main(images_dir: str, start_url: str):
    # Verify parameters
    if os.path.exists(images_dir):
        if os.path.isdir(images_dir):
            print(f"Using images dir `{images_dir}`.")
        else:
            raise FileExistsError(f"Images dir `{images_dir}` is a file or link.")
    else:
        os.makedirs(images_dir)
        print(f"Created images dir `{images_dir}`.")

    # Create threads.
    image_detail_page_urls_queue = Queue()

    catalog_page_thread = threading.Thread(target=catalog_page_worker, args=(image_detail_page_urls_queue, start_url))
    detail_page_thread = threading.Thread(target=detail_page_worker, args=(image_detail_page_urls_queue, images_dir))

    catalog_page_thread.start()
    detail_page_thread.start()

    catalog_page_thread.join()
    image_detail_page_urls_queue.put((PAGE_RETRIEVAL_COMPLETE_PLACEHOLDER_URL, None))

    detail_page_thread.join()


if __name__ == '__main__':
    print(f"Working directory: {os.getcwd()}")

    parser = argparse.ArgumentParser()
    parser.add_argument("--images_dir", "-d", type=str, default="images/")
    parser.add_argument("start_url", type=str)
    args = parser.parse_args()

    main(args.images_dir, args.start_url)
