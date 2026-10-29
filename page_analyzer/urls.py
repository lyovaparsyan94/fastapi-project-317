from urllib.parse import urlparse

from pydantic import HttpUrl, TypeAdapter, ValidationError

MAX_URL_LENGTH = 255

_http_url = TypeAdapter(HttpUrl)


def is_valid_url(url: str) -> bool:
    if not url or len(url) > MAX_URL_LENGTH:
        return False
    try:
        _http_url.validate_python(url)
    except ValidationError:
        return False
    return True


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}".lower()
