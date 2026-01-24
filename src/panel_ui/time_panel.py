import os

import httpx
import panel as pn

pn.extension()

API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = os.getenv("API_PORT", "8000")
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"


async def fetch_time() -> str:
    async with httpx.AsyncClient(timeout=2.0) as client:
        response = await client.get(f"{API_BASE_URL}/time")
        response.raise_for_status()
        return response.json()["datetime"]


time_display = pn.pane.Markdown("No data", sizing_mode="stretch_width")
button = pn.widgets.Button(name="Fetch server time", button_type="primary")


async def on_click_async() -> None:
    try:
        time_display.object = "Loading..."
        server_time = await fetch_time()
        time_display.object = f"Server time: `{server_time}`"
    except Exception as exc:
        time_display.object = f"Error: `{exc}`"


def on_click(_: object) -> None:
    pn.state.run_async(on_click_async())


button.on_click(on_click)

layout = pn.Column(
    pn.pane.Markdown("## Server Time"),
    button,
    time_display,
    width=400,
)

layout.servable()
