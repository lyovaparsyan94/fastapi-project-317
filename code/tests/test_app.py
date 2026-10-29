async def test_index_is_available(client):
    response = await client.get("/")

    assert response.status_code == 200


async def test_index_shows_url_form(client):
    response = await client.get("/")

    assert '<form action="/urls" method="post"' in response.text
    assert 'name="url"' in response.text
