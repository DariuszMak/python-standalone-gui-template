import asyncio
from collections.abc import Callable, Coroutine

import panel as pn
import pytest
import respx
from httpx import HTTPStatusError, Response

from src.panel_ui import time_panel
from src.panel_ui.time_panel import fetch_time, time_display


@pytest.mark.asyncio
async def test_fetch_time_success(monkeypatch: pytest.MonkeyPatch) -> None:
    class DummyConfig:
        api_base_url = "http://testserver"

    monkeypatch.setattr(
        "src.panel_ui.time_panel.Config.from_env",
        lambda: DummyConfig(),
    )

    with respx.mock:
        respx.get("http://testserver/time").mock(
            return_value=Response(
                200,
                json={"datetime": "2026-01-25T12:00:00Z"},
            )
        )

        result = await fetch_time()

    assert result == "2026-01-25T12:00:00Z"


@pytest.mark.asyncio
async def test_fetch_time_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    class DummyConfig:
        api_base_url = "http://testserver"

    monkeypatch.setattr(
        "src.panel_ui.time_panel.Config.from_env",
        lambda: DummyConfig(),
    )

    with respx.mock:
        respx.get("http://testserver/time").mock(return_value=Response(500))

        with pytest.raises(HTTPStatusError):
            await fetch_time()


def test_on_click_success(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_fetch_time() -> str:
        return "2026-01-25T12:00:00Z"

    def immediate_execute(fn: Callable[[], Coroutine[None, None, None]]) -> None:
        asyncio.run(fn())

    monkeypatch.setattr(time_panel, "fetch_time", fake_fetch_time)
    monkeypatch.setattr(pn.state, "execute", immediate_execute)

    assert time_display.object == "No data"

    time_panel.on_click(object())

    assert time_display.object == "Server time: `2026-01-25T12:00:00Z`"


def test_on_click_error(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_fetch_time() -> str:
        raise RuntimeError("boom")

    def immediate_execute(fn: Callable[[], Coroutine[None, None, None]]) -> None:
        asyncio.run(fn())

    monkeypatch.setattr(time_panel, "fetch_time", fake_fetch_time)
    monkeypatch.setattr(pn.state, "execute", immediate_execute)

    time_panel.on_click(object())

    assert "Error:" in time_display.object
    assert "boom" in time_display.object
