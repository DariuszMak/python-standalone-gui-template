import sys
import threading
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles

from src import STATIC_CATALGUE_NAME
from src.config.config import Config

# Determine static dir
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    STATIC_DIR = Path(sys._MEIPASS) / STATIC_CATALGUE_NAME
else:
    STATIC_DIR = Path(__file__).parent / STATIC_CATALGUE_NAME

app = FastAPI()

# Mount React static files
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


@app.middleware("http")
async def ignore_noise_requests(request: Request, call_next):
    path = request.url.path
    if path.startswith("/.well-known") or path.endswith(".map"):
        return Response(status_code=204)
    response = await call_next(request)
    return response


def run_react_ui(host: str, port: int) -> None:
    uvicorn.run(app, host=host, port=port, log_level="info")


def start_react_ui_in_background() -> None:
    config = Config.from_env()
    thread = threading.Thread(
        target=run_react_ui,
        args=(config.panel_host, config.react_port),
        daemon=True,
    )
    thread.start()
