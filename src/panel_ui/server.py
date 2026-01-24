import threading

from panel.io.server import serve

from src.config.config import Config
from src.panel_ui.time_panel import layout


def run_panel() -> None:
    config = Config.from_env()

    serve(
        {
            "/": layout,
        },
        address=config.panel_host,
        port=config.panel_port,
        show=False,
        autoreload=False,
    )


def start_panel_in_background() -> None:
    thread = threading.Thread(target=run_panel, daemon=True)
    thread.start()
