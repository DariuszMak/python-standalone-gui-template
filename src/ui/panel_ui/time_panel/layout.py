import panel as pn
from datetime import datetime

from src.ui.panel_ui.time_panel.clock_widget import ClockWidget
from src.ui.panel_ui.time_panel.api import fetch_time


def create_layout() -> pn.Column:
    clock = ClockWidget()

    time_display = pn.pane.Markdown("No data")
    button = pn.widgets.Button(name="Fetch time from API", button_type="primary")

    async def _fetch() -> None:
        try:
            time_display.object = "Loading..."
            dt_str = await fetch_time()
            dt = datetime.fromisoformat(dt_str)
            clock.set_current_datetime(dt)
            time_display.object = f"Server time: `{dt_str}`"
        except Exception as exc:
            time_display.object = f"Error: `{exc}`"

    def on_click(_):
        pn.state.execute(_fetch)

    button.on_click(on_click)

    return pn.Column("# Server Time", clock.panel(), button, time_display)