import sys
import threading
from pathlib import Path

import uvicorn
from litestar import Litestar
from litestar.static_files import StaticFilesConfig

from src import STATIC_CATALGUE_NAME
from src.config.config import Config

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    STATIC_DIR = Path(sys._MEIPASS) / STATIC_CATALGUE_NAME
else:
    STATIC_DIR = Path(__file__).parent / STATIC_CATALGUE_NAME

app = Litestar(
    static_files_config=[
        StaticFilesConfig(
            path="/",
            directories=[STATIC_DIR],
            html_mode=True,
        )
    ]
)


def run_react_ui(host: str, port: int) -> None:
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )


def start_react_ui_in_background() -> None:
    config = Config.from_env()

    thread = threading.Thread(
        target=run_react_ui,
        args=(config.panel_host, config.react_port),
        daemon=True,
    )
    thread.start()
