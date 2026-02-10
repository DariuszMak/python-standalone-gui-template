import os

import uvicorn
from litestar import Litestar
from litestar.static_files import StaticFilesConfig

from src import STATIC_CATALGUE_NAME
from src.ui.react_ui.routes import now


def create_app() -> Litestar:
    return Litestar(
        route_handlers=[
            now,
        ],
        static_files_config=[
            StaticFilesConfig(
                path="/",
                directories=[os.path.join(os.path.dirname(__file__), STATIC_CATALGUE_NAME)],
                html_mode=True,
            )
        ],
    )


def run() -> None:
    uvicorn.run(
        create_app(),
        host=os.getenv("REACT_HOST", "127.0.0.1"),
        port=int(os.getenv("REACT_PORT", 8002)),
        log_level="info",
    )


if __name__ == "__main__":
    run()
