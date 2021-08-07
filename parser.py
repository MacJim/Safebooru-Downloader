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
->
`ParseResult(scheme='', netloc='', path='', params='', query='page=post&s=list&tags=coat&pid=50960', fragment='')`

Note: May not include the scheme, netloc, and path.
"""

CATALOG_PAGE_IMAGE_DETAIL_PAGES_XPATH: typing.Final = "//div[@class='content']/div[1]/span[@id]/a/@href"
"""
Example: `index.php?page=post&s=view&id=3578328`
->
`ParseResult(scheme='', netloc='', path='index.php', params='', query='page=post&s=view&id=3578328', fragment='')`

Note: May not include the scheme and netloc.
"""


def parse_catalog_page(page_html: str) -> typing.Tuple[typing.Optional[str], typing.List[str]]:
    """
    :param page_html: Web page HTML source code.
    :return: (next page URL, a list of image detail page URLs). URLs may be relative and don't include the scheme, netloc, and path: use `urljoin` to join with the previous URL.
    """
    root: lxml.html.HtmlElement = lxml.html.fromstring(page_html)

    # Next page URL.
    next_page_url = root.xpath(CATALOG_PAGE_NEXT_BUTTON_XPATH)
    if next_page_url:
        # We have a next page.
        next_page_url = next_page_url[0]
        next_page_url = str(next_page_url)    # Convert `_ElementUnicodeResult` to `str`
    else:
        # This is the last page.
        next_page_url = None

    # Image detail page URLs.
    image_detail_page_urls = root.xpath(CATALOG_PAGE_IMAGE_DETAIL_PAGES_XPATH)
    image_detail_page_urls = [str(s) for s in image_detail_page_urls]    # Convert `_ElementUnicodeResult` to `str`

    return (next_page_url, image_detail_page_urls)
