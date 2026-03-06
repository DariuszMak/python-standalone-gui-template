import os
import sys
import threading
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles

from src import STATIC_CATALGUE_NAME
from src.config.config import Config


def create_app() -> FastAPI:
    # Determine static directory
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        static_dir = Path(sys._MEIPASS) / STATIC_CATALGUE_NAME
    else:
        static_dir = Path(__file__).parent / STATIC_CATALGUE_NAME

    app = FastAPI()

    # Mount React static files
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

    # Middleware to silence noisy requests
    @app.middleware("http")
    async def ignore_noise_requests(request: Request, call_next):
        path = request.url.path
        if path.startswith("/.well-known") or path.endswith(".map"):
            return Response(status_code=204)
        return await call_next(request)

    return app


# Single FastAPI app instance
app = create_app()


def run_react_ui(host: str | None = None, port: int | None = None) -> None:
    host = host or os.getenv("REACT_HOST", "127.0.0.1")
    port = port or int(os.getenv("REACT_PORT", "8000"))

    uvicorn.run(app, host=host, port=port, log_level="info")


def start_react_ui_in_background() -> None:
    config = Config.from_env()
    thread = threading.Thread(
        target=run_react_ui,
        args=(config.panel_host, config.react_port),
        daemon=True,
    )
    thread.start()
