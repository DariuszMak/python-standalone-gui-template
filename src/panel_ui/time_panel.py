import asyncio
import panel as pn
import httpx

pn.extension()

API_BASE_URL = "http://127.0.0.1:8001"


async def fetch_time() -> str:
    async with httpx.AsyncClient(timeout=2.0) as client:
        resp = await client.get(f"{API_BASE_URL}/time")
        resp.raise_for_status()
        return resp.json()["datetime"]


time_display = pn.pane.Markdown("No data", sizing_mode="stretch_width")
button = pn.widgets.Button(name="Fetch time from API", button_type="primary")


def on_click(event):
    async def _update():
        try:
            time_display.object = "Loading..."
            dt = await fetch_time()
            time_display.object = f"Server time: `{dt}`"
        except Exception as exc:
            time_display.object = f"Error: `{exc}`"

    asyncio.create_task(_update())


button.on_click(on_click)

layout = pn.Column(
    "# Server Time",
    button,
    time_display,
    width=400,
)

layout.servable()
