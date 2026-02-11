import uvicorn
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi.config import OpenAPIConfig

from src.api.routes import current_time, ping
from src.config.config import Config

cors_config = CORSConfig(
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

openapi_config = OpenAPIConfig(
    title="My API",
    version="0.1.0",
    description="API documentation for my service",
)

app = Litestar(
    route_handlers=[ping, current_time],
    openapi_config=openapi_config,
    cors_config=cors_config,
)


def run_api() -> None:
    config = Config.from_env()

    uvicorn_config = uvicorn.Config(
        app,
        host=config.api_host,
        port=config.api_port,
        log_level="info",
    )
    uvicorn.Server(uvicorn_config).run()


if __name__ == "__main__":
    run_api()
