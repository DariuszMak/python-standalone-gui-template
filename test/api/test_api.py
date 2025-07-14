from litestar.testing import TestClient

from src.api.app import app


def test_ping_route():
    with TestClient(app) as client:
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"message": "pong"}


def test_swagger_ui_available():
    with TestClient(app) as client:
        resp = client.get("/schema/swagger")
        assert resp.status_code == 200
        assert "html" in resp.headers["content-type"]
