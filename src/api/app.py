import platform
import os
import uvicorn
from litestar import Litestar
from litestar.openapi.config import OpenAPIConfig

from src.api.routes import ping

openapi_config = OpenAPIConfig(
    title="My API",
    version="0.1.0",
    description="API documentation for my service"
)

app = Litestar(route_handlers=[ping], openapi_config=openapi_config)




def run_api() -> None:
    if os.name == "nt":
        port = 8000
    else:
        port = 8001


    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    run_api()
