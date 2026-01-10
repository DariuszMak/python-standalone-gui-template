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
    def __init__(self, json_data: dict[str, str], status_code: int = 200) -> None:
        self._json_data = json_data
        self.status_code = status_code

    def json(self) -> dict[str, str]:
        return self._json_data

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            request = httpx.Request("GET", "http://testserver/time")
            response = httpx.Response(
                status_code=self.status_code,
                request=request,
            )
            raise httpx.HTTPStatusError(
                "error",
                request=request,
                response=response,
            )


@pytest.mark.asyncio
async def test_fetch_time(monkeypatch: pytest.MonkeyPatch) -> None:
    iso_time = "2025-01-01T10:15:30"

    async def mock_get(self: httpx.AsyncClient, url: str) -> MockResponse:  # noqa: ARG001
        return MockResponse({"datetime": iso_time})

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    client = TimeClient(base_url="http://testserver")
    result = await client.fetch_time()

    assert isinstance(result, ServerTimeResponse)
    assert result.datetime == datetime.fromisoformat(iso_time)



@pytest.mark.asyncio
async def test_time_route_remote(monkeypatch: pytest.MonkeyPatch) -> None:
    iso_time = "2025-01-01T12:00:00+00:00"

    class MockResponse:
        def json(self) -> dict[str, str]:
            return {"datetime": iso_time}

        def raise_for_status(self) -> None:
            return None

    async def mock_get(self: httpx.AsyncClient, url: str) -> MockResponse:  # noqa: ARG001
        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    with TestClient(app) as client:
        response = client.get("/time")

    assert response.status_code == 200
    data = response.json()
    assert data["datetime"] == iso_time

@pytest.mark.asyncio
async def test_time_route_fallback_to_local(monkeypatch: pytest.MonkeyPatch) -> None:
    async def mock_get(self: httpx.AsyncClient, url: str) -> None:  # noqa: ARG001
        raise httpx.ConnectError("no internet")

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    with TestClient(app) as client:
        response = client.get("/time")

    assert response.status_code == 200
    data = response.json()

    dt = datetime.fromisoformat(data["datetime"])
    assert dt.tzinfo == UTC
