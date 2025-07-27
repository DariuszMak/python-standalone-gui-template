import os

import uvicorn
from litestar import Litestar
from litestar.openapi.config import OpenAPIConfig

from src.api.routes import ping

openapi_config = OpenAPIConfig(title="My API", version="0.1.0", description="API documentation for my service")

app = Litestar(route_handlers=[ping], openapi_config=openapi_config)


def run_api() -> None:
    port = int(os.getenv("API_PORT", "8000"))
    host = os.getenv("API_HOST", "127.0.0.1")

    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    run_api()