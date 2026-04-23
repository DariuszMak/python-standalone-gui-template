from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

import panel as pn

from src.ui.panel_ui.settings import TICK_MS
from src.ui.panel_ui.time_panel.api import fetch_time
from src.ui.panel_ui.time_panel.clock_figure import build_clock_figure, hand_endpoint
from src.ui.shared.controller.clock_controller import ClockController
from src.ui.shared.helpers import format_datetime
from src.ui.shared.model.helpers import clock_hands_in_radians

if TYPE_CHECKING:
    from panel.io.callbacks import PeriodicCallback

logger = logging.getLogger(__name__)
pn.extension()


class ClockWidget:
    def __init__(self, size: int = 300) -> None:
        self._server_anchor: datetime = datetime.now().astimezone()
        self._wall_anchor_mono: float = time.monotonic()

        self._controller = ClockController(self._server_anchor)

        self._fig, self._sources = build_clock_figure(size)
        self._pane: pn.pane.Bokeh = pn.pane.Bokeh(self._fig, sizing_mode="fixed")  # type: ignore

        self._cb: PeriodicCallback = pn.state.add_periodic_callback(self._tick, period=TICK_MS)

        pn.state.on_session_destroyed(self._on_session_destroyed)

    def _on_session_destroyed(self, _session_context: object) -> None:
        self.stop()

    def panel(self) -> pn.pane.Bokeh:
        return self._pane

    def set_current_datetime(self, dt: datetime) -> None:
        self._server_anchor = dt
        self._wall_anchor_mono = time.monotonic()
        self._controller.reset(dt)

    def stop(self) -> None:
        if self._cb is not None:
            try:
                self._cb.stop()  # type: ignore[no-untyped-call]
            except Exception as exc:
                logger.debug("Failed to stop periodic callback", exc_info=exc)

    def _current_datetime(self) -> datetime:
        elapsed = time.monotonic() - self._wall_anchor_mono
        return self._server_anchor + timedelta(seconds=elapsed)

    def _tick(self) -> None:
        now = self._current_datetime()
        self._controller.update(now)

        sec_rad, min_rad, hour_rad = clock_hands_in_radians(self._controller._clock_hands)

        cx, cy, r = 0.0, 0.0, 1.0

        ex_h, ey_h = hand_endpoint(cx, cy, r * 0.5, hour_rad)
        ex_m, ey_m = hand_endpoint(cx, cy, r * 0.7, min_rad)
        ex_s, ey_s = hand_endpoint(cx, cy, r * 0.9, sec_rad)

        self._sources["hour"].data = {"x": [cx, ex_h], "y": [cy, ey_h]}
        self._sources["minute"].data = {"x": [cx, ex_m], "y": [cy, ey_m]}
        self._sources["second"].data = {"x": [cx, ex_s], "y": [cy, ey_s]}

        self._sources["time_text"].data = {
            "x": [0.0],
            "y": [-0.55],
            "text": [format_datetime(now)],
        }


def create_layout() -> pn.Column:
    clock = ClockWidget(size=300)

    time_display: pn.pane.Markdown = pn.pane.Markdown("No data", sizing_mode="stretch_width")  # type: ignore

    button: pn.widgets.Button = pn.widgets.Button(name="Fetch time from API", button_type="primary")  # type: ignore

    async def _fetch() -> None:
        try:
            time_display.object = "Loading..."
            dt_str = await fetch_time()
            dt = datetime.fromisoformat(dt_str)
            clock.set_current_datetime(dt)
            time_display.object = f"Server time: `{dt_str}`"
        except Exception as exc:
            time_display.object = f"Error: `{exc}`"

    def on_click(_: object) -> None:
        pn.state.execute(_fetch)

    def _on_load() -> None:
        pn.state.execute(_fetch)

    button.on_click(on_click)
    pn.state.onload(_on_load)

    return pn.Column(
        "# Server Time",
        clock.panel(),
        button,
        time_display,
        width=400,
    )
