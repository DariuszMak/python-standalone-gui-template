import os
import sys
import threading
from collections.abc import Awaitable, Callable
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src import STATIC_CATALGUE_NAME
from src.config.config import Config
from routes.time import router 



def create_app() -> FastAPI:

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        static_dir = Path(sys._MEIPASS) / STATIC_CATALGUE_NAME
    else:
        static_dir = Path(__file__).parent / STATIC_CATALGUE_NAME

    app = FastAPI()

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon() -> FileResponse:
        return FileResponse(Path("src/ui/pyside_ui/forms/icons/images/program_icon.ico"))

    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

    app.include_router(router)


    @app.middleware("http")
    async def ignore_noise_requests(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        path = request.url.path
        if path.startswith("/.well-known") or path.endswith(".map"):
            return Response(status_code=204)
        return await call_next(request)

    return app


app = create_app()


def run_react_ui(host: str | None = None, port: int | None = None) -> None:
    host_str: str = str(host or os.getenv("REACT_HOST") or "127.0.0.1")
    port_int: int = port or int(os.getenv("REACT_PORT", "8000"))
    uvicorn.run(app, host=host_str, port=port_int, log_level="info")


def start_react_ui_in_background() -> None:
    config: Config = Config.from_env()
    host: str = config.panel_host or "127.0.0.1"
    port: int = config.react_port or 8000

    thread = threading.Thread(
        target=run_react_ui,
        args=(host, port),
        daemon=True,
    )
    thread.start()
