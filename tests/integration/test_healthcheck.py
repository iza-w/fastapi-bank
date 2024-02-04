from starlette import status


async def test_healthcheck__returns_ok(app, async_client):
    response = await async_client.get(app.url_path_for("health"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
