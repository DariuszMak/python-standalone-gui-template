import pytest

from src.config.config import Config


def test_config_defaults() -> None:
    config = Config()

    assert config.api_host == "127.0.0.1"
    assert config.api_port == 8000
    assert config.api_base_url == "http://127.0.0.1:8000"

    assert config.panel_host == "127.0.0.1"
    assert config.panel_port == 8001
    assert config.panel_api_base_url == "http://127.0.0.1:8001"


def test_config_custom_values() -> None:
    config = Config(
        api_host="api.example.com",
        api_port=9000,
        panel_host="panel.example.com",
        panel_port=7000,
    )

    assert config.api_host == "api.example.com"
    assert config.api_port == 9000
    assert config.api_base_url == "http://api.example.com:9000"

    assert config.panel_host == "panel.example.com"
    assert config.panel_port == 7000
    assert config.panel_api_base_url == "http://panel.example.com:7000"


def test_config_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_HOST", "env.example.com")
    monkeypatch.setenv("API_PORT", "8080")
    monkeypatch.setenv("PANEL_HOST", "panel.env.example.com")
    monkeypatch.setenv("PANEL_PORT", "9090")

    config = Config.from_env()

    assert config.api_host == "env.example.com"
    assert config.api_port == 8080
    assert config.api_base_url == "http://env.example.com:8080"

    assert config.panel_host == "panel.env.example.com"
    assert config.panel_port == 9090
    assert config.panel_api_base_url == "http://panel.env.example.com:9090"


def test_config_from_env_partial(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("API_HOST", raising=False)
    monkeypatch.setenv("API_PORT", "9090")
    monkeypatch.setenv("PANEL_HOST", "panel.only.env")
    monkeypatch.delenv("PANEL_PORT", raising=False)

    config = Config.from_env()

    assert config.api_host == "127.0.0.1"
    assert config.api_port == 9090
    assert config.api_base_url == "http://127.0.0.1:9090"

    assert config.panel_host == "panel.only.env"
    assert config.panel_port == 8001
    assert config.panel_api_base_url == "http://panel.only.env:8001"
