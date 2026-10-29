from datetime import UTC, datetime

import httpx
import respx


async def test_index_is_available(client):
    response = await client.get("/")

    assert response.status_code == 200


async def test_index_shows_url_form(client):
    response = await client.get("/")

    assert 'name="url"' in response.text


async def test_create_url_saves_normalized_name(client):
    response = await client.post("/urls", data={"url": "https://WWW.Google.com/search?q=1"})

    assert response.status_code == 302
    assert response.headers["location"].endswith("/urls/1")

    page = await client.get("/urls/1")
    assert "Страница успешно добавлена" in page.text
    assert "https://www.google.com" in page.text
    assert 'data-test="url"' in page.text


async def test_create_existing_url_reports_duplicate(client):
    first = await client.post("/urls", data={"url": "https://ru.hexlet.io"})
    await client.get(first.headers["location"])

    response = await client.post("/urls", data={"url": "https://ru.hexlet.io/courses"})
    page = await client.get(response.headers["location"])

    assert response.status_code == 302
    assert "Страница уже существует" in page.text


async def test_create_invalid_url_is_rejected(client):
    response = await client.post("/urls", data={"url": "hexlet"})

    assert response.status_code == 422
    assert "Некорректный URL" in response.text


async def test_create_too_long_url_is_rejected(client):
    response = await client.post("/urls", data={"url": f"https://{'a' * 250}.com"})

    assert response.status_code == 422
    assert "URL превышает 255 символов" in response.text


async def test_create_empty_url_is_rejected(client):
    response = await client.post("/urls", data={"url": ""})

    assert response.status_code == 422
    assert "URL обязателен" in response.text


async def test_urls_index_shows_newest_first(client):
    await client.post("/urls", data={"url": "https://ru.hexlet.io"})
    await client.post("/urls", data={"url": "https://www.google.com"})

    response = await client.get("/urls")

    assert 'data-test="urls"' in response.text
    assert response.text.index("google.com") < response.text.index("ru.hexlet.io")


async def test_unknown_url_returns_404(client):
    response = await client.get("/urls/999")

    assert response.status_code == 404


async def test_create_check_adds_record(client):
    await client.post("/urls", data={"url": "https://ru.hexlet.io"})

    with respx.mock:
        respx.get("https://ru.hexlet.io").mock(return_value=httpx.Response(200))
        response = await client.post("/urls/1/checks")

    page = await client.get("/urls/1")

    assert response.status_code == 302
    assert "Страница успешно проверена" in page.text
    assert 'data-test="checks"' in page.text


async def test_urls_index_shows_last_check_date(client):
    await client.post("/urls", data={"url": "https://ru.hexlet.io"})

    with respx.mock:
        respx.get("https://ru.hexlet.io").mock(return_value=httpx.Response(200))
        await client.post("/urls/1/checks")

    response = await client.get("/urls")

    assert datetime.now(UTC).strftime("%Y-%m-%d") in response.text


async def test_check_for_unknown_url_returns_404(client):
    response = await client.post("/urls/999/checks")

    assert response.status_code == 404


async def test_check_saves_status_code(client):
    await client.post("/urls", data={"url": "https://ru.hexlet.io"})

    with respx.mock:
        respx.get("https://ru.hexlet.io").mock(return_value=httpx.Response(200))
        await client.post("/urls/1/checks")

    page = await client.get("/urls/1")
    assert "Страница успешно проверена" in page.text
    assert "200" in page.text


async def test_server_error_does_not_create_check(client, count_checks):
    await client.post("/urls", data={"url": "https://ru.hexlet.io"})

    with respx.mock:
        respx.get("https://ru.hexlet.io").mock(return_value=httpx.Response(500))
        await client.post("/urls/1/checks")

    page = await client.get("/urls/1")
    assert "Произошла ошибка при проверке" in page.text
    assert await count_checks() == 0


async def test_network_failure_does_not_create_check(client, count_checks):
    await client.post("/urls", data={"url": "https://ru.hexlet.io"})

    with respx.mock:
        respx.get("https://ru.hexlet.io").mock(side_effect=httpx.ConnectError("boom"))
        await client.post("/urls/1/checks")

    page = await client.get("/urls/1")
    assert "Произошла ошибка при проверке" in page.text
    assert await count_checks() == 0


async def test_check_stores_seo_tags(client):
    await client.post("/urls", data={"url": "https://ru.hexlet.io"})
    html = (
        "<html><head><title>Хекслет</title>"
        '<meta name="description" content="Практические курсы"></head>'
        "<body><h1>Школа программирования</h1></body></html>"
    )

    with respx.mock:
        respx.get("https://ru.hexlet.io").mock(return_value=httpx.Response(200, html=html))
        await client.post("/urls/1/checks")

    page = await client.get("/urls/1")
    assert "Школа программирования" in page.text
    assert "Хекслет" in page.text
    assert "Практические курсы" in page.text
