import pytest
import respx
from httpx import Response

from src.panel_ui.time_panel import fetch_time
import pytest

from src.panel_ui import time_panel


@pytest.mark.asyncio
async def test_fetch_time_success(monkeypatch):
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
async def test_fetch_time_http_error(monkeypatch):
    class DummyConfig:
        api_base_url = "http://testserver"

    monkeypatch.setattr(
        "src.panel_ui.time_panel.Config.from_env",
        lambda: DummyConfig(),
    )

    with respx.mock:
        respx.get("http://testserver/time").mock(
            return_value=Response(500)
        )

        with pytest.raises(Exception):
            await fetch_time()




def test_on_click_success(monkeypatch):
    async def fake_fetch_time():
        return "2026-01-25T12:00:00Z"

    async def immediate_execute(coro):
        await coro()

    monkeypatch.setattr(time_panel, "fetch_time", fake_fetch_time)
    monkeypatch.setattr(time_panel.pn.state, "execute", immediate_execute)

    # initial state
    assert time_panel.time_display.object == "No data"

    # simulate click
    time_panel.on_click(object())

    assert time_panel.time_display.object == (
        "Server time: `2026-01-25T12:00:00Z`"
    )


def test_on_click_error(monkeypatch):
    async def fake_fetch_time():
        raise RuntimeError("boom")

    async def immediate_execute(coro):
        await coro()

    monkeypatch.setattr(time_panel, "fetch_time", fake_fetch_time)
    monkeypatch.setattr(time_panel.pn.state, "execute", immediate_execute)

    time_panel.on_click(object())

    assert "Error:" in time_panel.time_display.object
    assert "boom" in time_panel.time_display.object
