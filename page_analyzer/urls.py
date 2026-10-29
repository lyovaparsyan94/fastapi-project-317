from urllib.parse import urlparse

from pydantic import HttpUrl, TypeAdapter, ValidationError

MAX_URL_LENGTH = 255

_http_url = TypeAdapter(HttpUrl)


def url_error(url: str) -> str | None:
    if not url:
        return "URL обязателен"
    if len(url) > MAX_URL_LENGTH:
        return f"URL превышает {MAX_URL_LENGTH} символов"
    try:
        _http_url.validate_python(url)
    except ValidationError:
        return "Некорректный URL"
    return None


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}".lower()
