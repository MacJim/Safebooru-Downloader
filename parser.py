import typing

import lxml.html


# MARK: - Server overload
SERVER_OVERLOAD_XPATH: typing.Final = "//div[@class='content']//h1/text()"
SERVER_OVERLOAD_KEYWORD: typing.Final = "overload"


def is_server_overloaded(page_html: str) -> bool:
    """
    :param page_html: Page HTML string
    :return: `True` if the server is overloaded; `False` if normal.
    """
    root: lxml.html.HtmlElement = lxml.html.fromstring(page_html)

    server_overload_message = root.xpath(SERVER_OVERLOAD_XPATH)
    if server_overload_message:
        return True
    else:
        return False


# MARK: - Catalog page
CATALOG_PAGE_NEXT_BUTTON_XPATH: typing.Final = "//div[@class='pagination']/a[@alt='next']/@href"
"""
Example: `?page=post&s=list&tags=coat&pid=50960`

Note: Doesn't include the scheme, netloc, and path.
"""

CATALOG_PAGE_IMAGES_XPATH: typing.Final = ""


def parse_catalog_page(page_html: str):
    root: lxml.html.HtmlElement = lxml.html.fromstring(page_html)

    # TODO:
    # Next page URL.
    next_page_url = root.xpath(CATALOG_PAGE_NEXT_BUTTON_XPATH)
    print(next_page_url)
    if next_page_url:
        # We have a next page.
        next_page_url = next_page_url[0]
    else:
        # This is the last page.
        next_page_url = None
