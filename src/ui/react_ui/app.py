import os
from pathlib import Path

import uvicorn
from litestar import Litestar
from litestar.static_files import StaticFilesConfig


def create_app() -> Litestar:
    dist_dir = Path(__file__).parent / "dist"

    return Litestar(
        static_files_config=[
            StaticFilesConfig(
                path="/",
                directories=[dist_dir],
                html_mode=True,
            )
        ]
    )


def run() -> None:

    host = os.getenv("REACT_HOST", "127.0.0.1")
    port = int(os.getenv("REACT_PORT", "8000"))

    uvicorn.run(create_app(), host=host, port=port, log_level="info")
