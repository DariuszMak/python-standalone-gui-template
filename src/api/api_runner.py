import uvicorn
from litestar import Litestar, get


@get("/ping")
def ping() -> dict:
    return {"message": "pong"}


app = Litestar(route_handlers=[ping])


def run_api() -> None:
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
