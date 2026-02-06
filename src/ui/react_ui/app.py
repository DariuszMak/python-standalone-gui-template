import os
import uvicorn
from litestar import Litestar
from litestar.static_files import StaticFiles

def create_app() -> Litestar:
    return Litestar(
        route_handlers=[
            StaticFiles(
                path="/",
                directories=[os.path.join(os.path.dirname(__file__), "static")],
                html_mode=True,
            )
        ]
    )

def run() -> None:
    uvicorn.run(
        create_app(),
        host=os.getenv("REACT_HOST", "127.0.0.1"),
        port=int(os.getenv("REACT_PORT", 8005)),
        log_level="info",
    )

if __name__ == "__main__":
    run()
