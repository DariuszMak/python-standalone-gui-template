import asyncio
from collections.abc import Callable, Coroutine
from typing import cast

import panel as pn
import pytest
import respx
from httpx import HTTPStatusError, Response

from src.ui.panel_ui import time_panel
from src.ui.panel_ui.time_panel import fetch_time


@pytest.mark.asyncio
async def test_fetch_time_success(monkeypatch: pytest.MonkeyPatch) -> None:
    class DummyConfig:
        api_base_url = "http://testserver"

    monkeypatch.setattr(
        "src.ui.panel_ui.time_panel.Config.from_env",
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
        "src.ui.panel_ui.time_panel.Config.from_env",
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
    monkeypatch.setattr(pn.state, "onload", lambda _: None)

    col = time_panel.create_layout()
    _button = cast("pn.widgets.Button", col[1])
    _time_display = cast("pn.pane.Markdown", col[2])

    assert _time_display.object == "No data"

    _button.clicks += 1

    assert _time_display.object == "Server time: `2026-01-25T12:00:00Z`"


def test_on_click_error(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_fetch_time() -> str:
        raise RuntimeError("boom")

    def immediate_execute(fn: Callable[[], Coroutine[None, None, None]]) -> None:
        asyncio.run(fn())

    monkeypatch.setattr(time_panel, "fetch_time", fake_fetch_time)
    monkeypatch.setattr(pn.state, "execute", immediate_execute)
    monkeypatch.setattr(pn.state, "onload", lambda _: None)

    col = time_panel.create_layout()
    _button = cast("pn.widgets.Button", col[1])
    _time_display = cast("pn.pane.Markdown", col[2])

    _button.clicks += 1

    assert "Error:" in _time_display.object
    assert "boom" in _time_display.object
