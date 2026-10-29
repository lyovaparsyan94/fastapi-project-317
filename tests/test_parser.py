from page_analyzer.parser import parse_page

PAGE = """
<html>
  <head>
    <title>Newest Questions - Stack Overflow</title>
    <meta name="description" content="  Q&amp;A for programmers  ">
  </head>
  <body><h1> Newest Questions </h1></body>
</html>
"""


def test_parse_page_extracts_seo_tags():
    page = parse_page(PAGE)

    assert page.h1 == "Newest Questions"
    assert page.title == "Newest Questions - Stack Overflow"
    assert page.description == "Q&A for programmers"


def test_parse_page_without_tags_returns_nothing():
    page = parse_page("<html><body><p>ничего</p></body></html>")

    assert page == (None, None, None)


def test_parse_page_ignores_foreign_meta():
    page = parse_page('<html><head><meta name="keywords" content="python"></head></html>')

    assert page.description is None


def test_parse_page_shortens_long_values():
    long_text = "H1 Lorem ipsum " + "dolor sit amet " * 40
    page = parse_page(f"<html><body><h1>{long_text}</h1></body></html>")

    assert page.h1.startswith("H1 Lorem ipsum")
    assert page.h1.endswith("...")
    assert len(page.h1) == 203


def test_parse_page_keeps_short_values_intact():
    page = parse_page("<html><body><h1>Короткий заголовок</h1></body></html>")

    assert page.h1 == "Короткий заголовок"
