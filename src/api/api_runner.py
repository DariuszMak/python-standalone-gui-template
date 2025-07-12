import uvicorn
from litestar import Litestar

from src.api.routes import ping

app = Litestar(route_handlers=[ping])


def run_api() -> None:
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
