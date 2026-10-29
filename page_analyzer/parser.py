from typing import NamedTuple

from bs4 import BeautifulSoup, Tag

MAX_TEXT_LENGTH = 200
ELLIPSIS = "..."


class PageContent(NamedTuple):
    h1: str | None
    title: str | None
    description: str | None


def parse_page(html: str) -> PageContent:
    soup = BeautifulSoup(html, "html.parser")
    description = soup.find("meta", attrs={"name": "description"})
    return PageContent(
        h1=_shorten(_text(soup.h1)),
        title=_shorten(_text(soup.title)),
        description=_shorten(_attribute(description, "content")),
    )


def _text(tag: Tag | None) -> str | None:
    return tag.get_text(strip=True) if tag else None


def _attribute(tag: Tag | None, name: str) -> str | None:
    if not isinstance(tag, Tag):
        return None
    value = tag.get(name)
    return value.strip() if isinstance(value, str) else None


def _shorten(text: str | None) -> str | None:
    if text is None or len(text) <= MAX_TEXT_LENGTH:
        return text
    return text[:MAX_TEXT_LENGTH] + ELLIPSIS
