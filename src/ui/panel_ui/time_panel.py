from typing import Any

import httpx
import panel as pn

from src.config.config import Config

pn.extension()


async def fetch_time() -> str:
    config = Config.from_env()

    async with httpx.AsyncClient(timeout=2.0) as client:
        resp = await client.get(f"{config.api_base_url}/time")
        resp.raise_for_status()
        data: Any = resp.json()
        return str(data["datetime"])


time_display = pn.pane.Markdown(  # type: ignore[no-untyped-call]
    "No data",
    sizing_mode="stretch_width",
)

button = pn.widgets.Button(  # type: ignore[no-untyped-call]
    name="Fetch time from API",
    button_type="primary",
)


def on_click(_: object) -> None:
    async def _update() -> None:
        try:
            time_display.object = "Loading..."
            dt = await fetch_time()
            time_display.object = f"Server time: `{dt}`"
        except Exception as exc:
            time_display.object = f"Error: `{exc}`"

    pn.state.execute(_update)


button.on_click(on_click)

layout = pn.Column(
    "# Server Time",
    button,
    time_display,
    width=400,
)

layout.servable()
