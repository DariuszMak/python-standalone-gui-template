from datetime import UTC, datetime

import httpx
import pytest
from litestar.testing import TestClient

from src.api.app import app
from src.api.models import ServerTimeResponse
from src.api.time_client import TimeClient


def test_redoc_available() -> None:
    with TestClient(app) as client:
        resp = client.get("/schema/redoc")
        assert resp.status_code == 200
        assert "html" in resp.headers["content-type"]


def test_swagger_ui_available() -> None:
    with TestClient(app) as client:
        resp = client.get("/schema/swagger")
        assert resp.status_code == 200
        assert "html" in resp.headers["content-type"]


def test_ping_route() -> None:
    with TestClient(app) as client:
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"message": "pong"}


def test_time_route() -> None:
    with TestClient(app) as client:
        response = client.get("/time")
        assert response.status_code == 200
        data = response.json()
        assert "datetime" in data

        dt = datetime.fromisoformat(data["datetime"])
        assert dt.tzinfo == UTC


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                "error",
                request=None,
                response=None,
            )


@pytest.mark.asyncio
async def test_fetch_time(monkeypatch):
    iso_time = "2025-01-01T10:15:30"

    async def mock_get(self, url):
        return MockResponse({"datetime": iso_time})

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    client = TimeClient(base_url="http://testserver")
    result = await client.fetch_time()

    assert isinstance(result, ServerTimeResponse)
    assert result.datetime == datetime.fromisoformat(iso_time)
