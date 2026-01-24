import threading
import panel as pn
from panel.io.server import serve

from src.panel_ui.time_panel import layout


def run_panel() -> None:
    serve(
        {
            "/": layout,
        },
        address="127.0.0.1",
        port=5007,
        show=False,
        autoreload=False,
    )


def start_panel_in_background() -> None:
    thread = threading.Thread(target=run_panel, daemon=True)
    thread.start()
