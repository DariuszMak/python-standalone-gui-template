from dataclasses import dataclass

from src.config.env import EnvLoaderMixin


@dataclass(frozen=True)
class Config(EnvLoaderMixin):
    host: str = "127.0.0.1"
    panel_port: int = 8001
    api_port: int = 8000
    react_port: int = 8002

    @property
    def panel_api_base_url(self) -> str:
        return f"http://{self.host}:{self.panel_port}"

    @property
    def api_base_url(self) -> str:
        return f"http://{self.host}:{self.api_port}"

    @property
    def react_base_url(self) -> str:
        return f"http://{self.host}:{self.react_port}"
