import asyncio
from collections.abc import Callable, Coroutine
from typing import cast
from unittest.mock import MagicMock, patch

import panel as pn
import pytest
import respx
from httpx import HTTPStatusError, Response
from src.ui.panel_ui.time_panel import fetch_time

from src.ui.panel_ui import time_panel


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


def _make_layout(
    monkeypatch: pytest.MonkeyPatch,
    fake_fetch: Callable[[], Coroutine[None, None, str]],
) -> pn.Column:
    """
    Build a create_layout() Column with:
      - periodic callbacks suppressed (no live Bokeh server needed)
      - fetch_time replaced by fake_fetch
      - pn.state.execute runs the coroutine immediately and synchronously
      - pn.state.onload is a no-op
    """

    def immediate_execute(fn: Callable[[], Coroutine[None, None, None]]) -> None:
        asyncio.run(fn())

    monkeypatch.setattr(time_panel, "fetch_time", fake_fetch)
    monkeypatch.setattr(pn.state, "execute", immediate_execute)
    monkeypatch.setattr(pn.state, "onload", lambda _: None)

    # Suppress the periodic callback so no Bokeh server is required
    with patch.object(pn.state, "add_periodic_callback", return_value=MagicMock()):
        return time_panel.create_layout()


def test_on_click_success(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_fetch_time() -> str:
        return "2026-01-25T12:00:00Z"

    col = _make_layout(monkeypatch, fake_fetch_time)

    # col[0] = "# Server Time" heading
    # col[1] = ClockWidget pane  (pn.pane.Bokeh)
    # col[2] = Fetch button
    # col[3] = Markdown time display
    _button = cast("pn.widgets.Button", col[2])
    _time_display = cast("pn.pane.Markdown", col[3])

    assert _time_display.object == "No data"

    _button.clicks += 1

    assert _time_display.object == "Server time: `2026-01-25T12:00:00Z`"


def test_on_click_error(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_fetch_time() -> str:
        raise RuntimeError("boom")

    col = _make_layout(monkeypatch, fake_fetch_time)

    _button = cast("pn.widgets.Button", col[2])
    _time_display = cast("pn.pane.Markdown", col[3])

    _button.clicks += 1

    assert "Error:" in _time_display.object
    assert "boom" in _time_display.object


def test_on_click_sets_clock_datetime(monkeypatch: pytest.MonkeyPatch) -> None:
    """set_current_datetime is called with the parsed datetime on a successful fetch."""
    from datetime import UTC, datetime

    received: list[datetime] = []

    async def fake_fetch_time() -> str:
        return "2026-01-25T12:00:00+00:00"

    original_init = time_panel.ClockWidget.__init__

    def patched_init(self: time_panel.ClockWidget, size: int = 300) -> None:
        original_init(self, size)
        original_set = self.set_current_datetime

        def capturing_set(dt: datetime) -> None:
            received.append(dt)
            original_set(dt)

        self.set_current_datetime = capturing_set  # type: ignore[method-assign]

    monkeypatch.setattr(time_panel.ClockWidget, "__init__", patched_init)

    col = _make_layout(monkeypatch, fake_fetch_time)
    _button = cast("pn.widgets.Button", col[2])

    _button.clicks += 1

    assert len(received) == 1
    assert received[0] == datetime(2026, 1, 25, 12, 0, 0, tzinfo=UTC)


def test_layout_structure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Column has the expected four items in the right order."""

    async def fake_fetch_time() -> str:
        return "2026-01-25T12:00:00Z"

    col = _make_layout(monkeypatch, fake_fetch_time)

    assert len(col) == 4
    assert isinstance(col[1], pn.pane.Bokeh)
    assert isinstance(col[2], pn.widgets.Button)
    assert isinstance(col[3], pn.pane.Markdown)
