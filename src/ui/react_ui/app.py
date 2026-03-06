import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def create_app() -> FastAPI:
    dist_dir = Path(__file__).parent / "dist"

    app = FastAPI()

    app.mount(
        "/",
        StaticFiles(directory=dist_dir, html=True),
        name="static",
    )

    return app


def run() -> None:
    host = os.getenv("REACT_HOST", "127.0.0.1")
    port = int(os.getenv("REACT_PORT", "8000"))

    uvicorn.run(create_app(), host=host, port=port, log_level="info")
