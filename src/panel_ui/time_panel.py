import asyncio
from typing import Any

import httpx
import panel as pn

pn.extension()

API_BASE_URL = "http://127.0.0.1:8001"


async def fetch_time() -> str:
    async with httpx.AsyncClient(timeout=2.0) as client:
        resp = await client.get(f"{API_BASE_URL}/time")
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

    task = asyncio.create_task(_update())
    pn.state._tasks.add(task)
    task.add_done_callback(pn.state._tasks.discard)


button.on_click(on_click)

layout = pn.Column(
    "# Server Time",
    button,
    time_display,
    width=400,
)

layout.servable()
