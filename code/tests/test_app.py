async def test_index_is_available(client):
    response = await client.get("/")

    assert response.status_code == 200
