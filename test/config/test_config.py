import pytest

from src.config.config import Config


def test_config_defaults() -> None:
    config = Config()
    assert config.api_host == "127.0.0.1"
    assert config.api_port == 8000
    assert config.api_base_url == "http://127.0.0.1:8000"


def test_config_custom_values() -> None:
    config = Config(api_host="api.example.com", api_port=9000)
    assert config.api_host == "api.example.com"
    assert config.api_port == 9000
    assert config.api_base_url == "http://api.example.com:9000"


def test_config_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_HOST", "env.example.com")
    monkeypatch.setenv("API_PORT", "8080")

    config = Config.from_env()

    assert config.api_host == "env.example.com"
    assert config.api_port == 8080
    assert config.api_base_url == "http://env.example.com:8080"


def test_config_from_env_partial(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_PORT", "9090")
    monkeypatch.delenv("API_HOST", raising=False)

    config = Config.from_env()

    assert config.api_host == "127.0.0.1"  # default used
    assert config.api_port == 9090
    assert config.api_base_url == "http://127.0.0.1:9090"
