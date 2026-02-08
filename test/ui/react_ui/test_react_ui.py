import threading
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import pytest
import uvicorn
from litestar import Litestar

from src.ui.react_ui.app import create_app, run
from src.ui.react_ui.server import run_react_ui, start_react_ui_in_background

if TYPE_CHECKING:
    from litestar.static_files import StaticFilesConfig


def test_create_app_static_files_configured() -> None:
    app = create_app()

    assert isinstance(app, Litestar)
    assert app.static_files_config is not None
    assert len(app.static_files_config) == 1

    config: StaticFilesConfig = app.static_files_config[0]

    assert config.path == "/"
    assert config.html_mode is True
    assert len(config.directories) == 1


def test_run_calls_uvicorn(monkeypatch: pytest.MonkeyPatch) -> None:
    called = {}

    def fake_run(app: Any, host: str, port: int, log_level: str) -> None:
        called["app"] = app
        called["host"] = host
        called["port"] = port
        called["log_level"] = log_level

    monkeypatch.setattr(uvicorn, "run", fake_run)
    monkeypatch.setenv("REACT_HOST", "0.0.0.1")
    monkeypatch.setenv("REACT_PORT", "9000")

    run()

    assert called["host"] == "0.0.0.1"
    assert called["port"] == 9000
    assert called["log_level"] == "info"


def test_run_react_ui_calls_uvicorn(monkeypatch: pytest.MonkeyPatch) -> None:
    called = {}

    def fake_run(app: Any, host: str, port: int, log_level: str) -> None:
        called["app"] = app
        called["host"] = host
        called["port"] = port
        called["log_level"] = log_level

    monkeypatch.setattr(uvicorn, "run", fake_run)

    run_react_ui("127.0.0.1", 8080)

    assert called["host"] == "127.0.0.1"
    assert called["port"] == 8080
    assert called["log_level"] == "info"


def test_start_react_ui_in_background(monkeypatch: pytest.MonkeyPatch) -> None:
    class DummyConfig:
        panel_host = "localhost"
        react_port = 7777

    started: dict[str, Any] = {}

    class DummyThread:
        def __init__(
            self,
            target: Callable[..., Any],
            args: tuple[Any, ...],
            daemon: bool,
        ) -> None:
            started["target"] = target
            started["args"] = args
            started["daemon"] = daemon

        def start(self) -> None:
            started["started"] = True

    monkeypatch.setattr(
        "src.ui.react_ui.server.Config.from_env",
        lambda: DummyConfig(),
    )
    monkeypatch.setattr(threading, "Thread", DummyThread)

    start_react_ui_in_background()

    assert started["args"] == ("localhost", 7777)
    assert started["daemon"] is True
    assert started["started"] is True
