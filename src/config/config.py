from dataclasses import dataclass
from src.config.env import EnvLoaderMixin


@dataclass(frozen=True)
class Config(EnvLoaderMixin):
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    @property
    def api_base_url(self) -> str:
        return f"http://{self.api_host}:{self.api_port}"
