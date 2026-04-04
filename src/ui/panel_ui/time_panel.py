from __future__ import annotations

import math
import time
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

import httpx
import panel as pn
from bokeh.models import ColumnDataSource, Range1d
from bokeh.plotting import figure

from src.config.config import Config
from src.ui.shared.controller.clock_controller import ClockController
from src.ui.shared.helpers import format_datetime
from src.ui.shared.model.helpers import clock_hands_in_radians

if TYPE_CHECKING:
    from panel.io.callbacks import PeriodicCallback

pn.extension()


def _hand_endpoint(cx: float, cy: float, radius: float, angle_rad: float) -> tuple[float, float]:
    return (
        cx + math.sin(angle_rad) * radius,
        cy + math.cos(angle_rad) * radius,
    )


def _build_clock_figure(size: int = 300) -> tuple[figure, dict[str, ColumnDataSource]]:
    cx, cy, r = 0.0, 0.0, 1.0

    p = figure(
        width=size,
        height=size,
        x_range=Range1d(start=-1.25, end=1.25),
        y_range=Range1d(start=-1.25, end=1.25),
        toolbar_location=None,
        background_fill_color="#1a1a1a",
        border_fill_color="#1a1a1a",
        outline_line_color=None,
    )
    p.axis.visible = False
    p.grid.visible = False

    p.circle(
        x=0,
        y=0,
        radius=r,
        fill_color="#1a1a1a",
        line_color="rgba(255,255,255,0.18)",
        line_width=2,
    )

    for i in range(60):
        ang = (i / 60.0) * 2.0 * math.pi
        is_maj = i % 5 == 0
        outer = (math.sin(ang) * r, math.cos(ang) * r)
        inner_r = r - (0.08 if is_maj else 0.04)
        inner = (math.sin(ang) * inner_r, math.cos(ang) * inner_r)
        p.line(
            x=[inner[0], outer[0]],
            y=[inner[1], outer[1]],
            line_color="rgba(180,180,180,0.65)",
            line_width=2.5 if is_maj else 1.2,
        )

    font_size = max(8, int(r * 300 * 0.036))
    for h in range(12):
        ang = (h / 12.0) * 2.0 * math.pi
        label_r = r - 0.22
        tx = math.sin(ang) * label_r
        ty = math.cos(ang) * label_r
        p.text(
            x=[tx],
            y=[ty],
            text=[str(((h + 11) % 12) + 1)],
            text_align="center",
            text_baseline="middle",
            text_color="rgba(255,255,255,0.85)",
            text_font_size=f"{font_size}px",
        )

    src_hour = ColumnDataSource({"x": [cx, cx], "y": [cy, cy]})
    src_min = ColumnDataSource({"x": [cx, cx], "y": [cy, cy]})
    src_sec = ColumnDataSource({"x": [cx, cx], "y": [cy, cy]})

    p.line("x", "y", source=src_hour, line_width=8, line_color="rgba(255,255,255,0.9)", line_cap="round")
    p.line("x", "y", source=src_min, line_width=6, line_color="rgba(200,200,200,0.75)", line_cap="round")
    p.line("x", "y", source=src_sec, line_width=2, line_color="#ff4444", line_cap="round")

    p.circle(x=0, y=0, radius=0.035, fill_color="#ff4444", line_color=None)

    src_text = ColumnDataSource({"x": [0.0], "y": [-0.55], "text": ["00:00:00.000"]})
    p.text(
        "x",
        "y",
        text="text",
        source=src_text,
        text_align="center",
        text_baseline="middle",
        text_color="#7af0a0",
        text_font="Consolas, monospace",
        text_font_size=f"{max(8, int(font_size * 0.95))}px",
    )

    sources = {"hour": src_hour, "minute": src_min, "second": src_sec, "time_text": src_text}
    return p, sources


class ClockWidget:
    TICK_MS = 15

    def __init__(self, size: int = 300) -> None:
        self._server_anchor: datetime = datetime.now().astimezone()
        self._wall_anchor_mono: float = time.monotonic()

        self._controller = ClockController(self._server_anchor)

        self._fig, self._sources = _build_clock_figure(size)
        self._pane: pn.pane.Bokeh = pn.pane.Bokeh(self._fig, sizing_mode="fixed")  # type: ignore

        self._cb: PeriodicCallback = pn.state.add_periodic_callback(self._tick, period=self.TICK_MS)

    def panel(self) -> pn.pane.Bokeh:
        return self._pane

    def set_current_datetime(self, dt: datetime) -> None:
        self._server_anchor = dt
        self._wall_anchor_mono = time.monotonic()
        self._controller.reset(dt)

    def stop(self) -> None:
        if self._cb is not None:
            self._cb.stop()  # type: ignore[no-untyped-call]

    def _current_datetime(self) -> datetime:
        elapsed = time.monotonic() - self._wall_anchor_mono
        return self._server_anchor + timedelta(seconds=elapsed)

    def _tick(self) -> None:
        now = self._current_datetime()
        self._controller.update(now)

        sec_rad, min_rad, hour_rad = clock_hands_in_radians(self._controller._clock_hands)

        cx, cy, r = 0.0, 0.0, 1.0

        ex_h, ey_h = _hand_endpoint(cx, cy, r * 0.5, hour_rad)
        ex_m, ey_m = _hand_endpoint(cx, cy, r * 0.7, min_rad)
        ex_s, ey_s = _hand_endpoint(cx, cy, r * 0.9, sec_rad)

        self._sources["hour"].data = {"x": [cx, ex_h], "y": [cy, ey_h]}
        self._sources["minute"].data = {"x": [cx, ex_m], "y": [cy, ey_m]}
        self._sources["second"].data = {"x": [cx, ex_s], "y": [cy, ey_s]}

        self._sources["time_text"].data = {
            "x": [0.0],
            "y": [-0.55],
            "text": [format_datetime(now)],
        }


async def fetch_time() -> str:
    config = Config.from_env()
    async with httpx.AsyncClient(timeout=2.0) as client:
        resp = await client.get(f"{config.api_base_url}/time")
        resp.raise_for_status()
        data: Any = resp.json()
        return str(data["datetime"])


def create_layout() -> pn.Column:
    clock = ClockWidget(size=300)

    time_display: pn.pane.Markdown = pn.pane.Markdown(  # type: ignore
        "No data", sizing_mode="stretch_width"
    )

    button: pn.widgets.Button = pn.widgets.Button(  # type: ignore
        name="Fetch time from API", button_type="primary"
    )

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
