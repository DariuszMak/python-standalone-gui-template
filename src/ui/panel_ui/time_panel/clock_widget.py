import time
from datetime import datetime, timedelta
import panel as pn

from src.ui.panel_ui.settings import TICK_MS
from src.ui.panel_ui.time_panel.clock_figure import build_clock_figure, _hand_endpoint
from src.ui.shared.controller.clock_controller import ClockController
from src.ui.shared.helpers import format_datetime
from src.ui.shared.model.helpers import clock_hands_in_radians


class ClockWidget:
    def __init__(self, size: int = 300) -> None:
        self._server_anchor = datetime.now().astimezone()
        self._wall_anchor_mono = time.monotonic()

        self._controller = ClockController(self._server_anchor)

        self._fig, self._sources = build_clock_figure(size)
        self._pane = pn.pane.Bokeh(self._fig)

        self._cb = pn.state.add_periodic_callback(self._tick, period=TICK_MS)

    def panel(self):
        return self._pane

    def set_current_datetime(self, dt: datetime) -> None:
        self._server_anchor = dt
        self._wall_anchor_mono = time.monotonic()
        self._controller.reset(dt)

    def _current_datetime(self) -> datetime:
        elapsed = time.monotonic() - self._wall_anchor_mono
        return self._server_anchor + timedelta(seconds=elapsed)

    def _tick(self) -> None:
        now = self._current_datetime()
        self._controller.update(now)

        sec, min_, hour = clock_hands_in_radians(self._controller._clock_hands)

        cx, cy, r = 0.0, 0.0, 1.0

        self._sources["hour"].data = {"x": [cx, _hand_endpoint(cx, cy, r * 0.5, hour)[0]],
                                      "y": [cy, _hand_endpoint(cx, cy, r * 0.5, hour)[1]]}

        self._sources["minute"].data = {"x": [cx, _hand_endpoint(cx, cy, r * 0.7, min_)[0]],
                                        "y": [cy, _hand_endpoint(cx, cy, r * 0.7, min_)[1]]}

        self._sources["second"].data = {"x": [cx, _hand_endpoint(cx, cy, r * 0.9, sec)[0]],
                                        "y": [cy, _hand_endpoint(cx, cy, r * 0.9, sec)[1]]}

        self._sources["time_text"].data = {
            "x": [0.0],
            "y": [-0.55],
            "text": [format_datetime(now)],
        }