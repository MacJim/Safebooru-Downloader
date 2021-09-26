"""
Generate random test cases for unit tests.
"""

import random
import string


def get_random_catalog_page_url() -> str:
    url_prefix = "https://safebooru.org/index.php?page=post&s=list&tags="
    url_suffix_len_range = (1, 100)

    random_tag_name = "".join(random.choices(string.ascii_lowercase + "+" + "-", k=random.randint(url_suffix_len_range[0], url_suffix_len_range[1])))

    return url_prefix + random_tag_name


def get_random_detail_page_url() -> str:
    url_prefix = "https://safebooru.org/index.php?page=post&s=view&id="

    random_image_id = random.randint(1, 9999999)

    return f"{url_prefix}{random_image_id}"
