import typing
import os
import urllib.parse
import urllib.request


# MARK: - Config
DEFAULT_HEADERS: typing.Final = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    # "Accept-Encoding": "gzip, deflate, br",    # Don't add those compression options. Otherwise, I'll need to decode on my end.
    "Accept-Encoding": "identity",    # Force no compression.
    "Accept-Language": "en-US",
    "Connection": "keep-alive",
    "DNT": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",    # `navigate` for top level navigation requests, `no-cors` for loading an image.
    "Sec-Fetch-Site": "same-origin",    # `none` for user-initiated pages
    "Sec-Fetch-User": "?1",    # Value will always be `?1`.
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
}

HEADER_HOST_KEY: typing.Final = "Host"
HEADER_REFERER_KEY: typing.Final = "Referer"
HEADER_SEC_FETCH_SITE_KEY: typing.Final = "Sec-Fetch-Site"
HEADER_SEC_FETCH_SITE_VALUE_NONE: typing.Final = "none"
HEADER_SEC_FETCH_SITE_VALUE_SAME_ORIGIN: typing.Final = "same-origin"


# MARK: - Helper functions
def _get_header_for_url(url: str, referer: typing.Optional[str]) -> typing.Dict[str, str]:
    """
    Get the request header for a URL.

    :param url:
    :param referer: If `None`, also sets `Sec-Fetch-Site` to `none`.
    :return: Header dictionary.
    """
    return_value = DEFAULT_HEADERS.copy()  # IMO a shallow copy is enough here.

    parsed_url = urllib.parse.urlparse(url)
    return_value[HEADER_HOST_KEY] = parsed_url.netloc

    if referer:
        return_value[HEADER_REFERER_KEY] = referer
    else:
        return_value[HEADER_SEC_FETCH_SITE_KEY] = HEADER_SEC_FETCH_SITE_VALUE_NONE

    return_value = {key: return_value[key] for key in return_value}    # Sort according to key.
    return return_value


# MARK: - Requests
def request_html(url: str, referer=None) -> str:
    header_dict = _get_header_for_url(url, referer)

    # Create request.
    req = urllib.request.Request(url, headers=header_dict, method="GET")
    with urllib.request.urlopen(req) as response:
        charset = response.info().get_content_charset()
        # print(f"Charset: {charset}")    # Python: utf-8
        response_bytes = response.read()
        response_str = response_bytes.decode(charset)

    return response_str


def download_file(filename: str, url: str, referer=None):
    if os.path.exists(filename):
        raise FileExistsError(f"`{filename}` exists.")

    header_dict = _get_header_for_url(url, referer)

    # Create request.
    req = urllib.request.Request(url, headers=header_dict, method="GET")
    with urllib.request.urlopen(req) as response, open(filename, "wb") as f:
        data = response.read()
        f.write(data)
