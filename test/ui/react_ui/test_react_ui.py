import os
import threading

import uvicorn
from litestar import Litestar
from litestar.static_files import StaticFilesConfig

from src.ui.react_ui.server import create_app, run
from src.ui.react_ui.background import run_react_ui, start_react_ui_in_background


def test_create_app_static_files_configured() -> None:
    app = create_app()

    assert isinstance(app, Litestar)
    assert app.static_files_config is not None
    assert len(app.static_files_config) == 1

    config: StaticFilesConfig = app.static_files_config[0]

    assert config.path == "/"
    assert config.html_mode is True
    assert len(config.directories) == 1


def test_run_calls_uvicorn(monkeypatch) -> None:
    called = {}

    def fake_run(app, host, port, log_level):
        called["app"] = app
        called["host"] = host
        called["port"] = port
        called["log_level"] = log_level

    monkeypatch.setattr(uvicorn, "run", fake_run)
    monkeypatch.setenv("REACT_HOST", "0.0.0.0")
    monkeypatch.setenv("REACT_PORT", "9000")

    run()

    assert called["host"] == "0.0.0.0"
    assert called["port"] == 9000
    assert called["log_level"] == "info"


def test_run_react_ui_calls_uvicorn(monkeypatch) -> None:
    called = {}

    def fake_run(app, host, port, log_level):
        called["app"] = app
        called["host"] = host
        called["port"] = port
        called["log_level"] = log_level

    monkeypatch.setattr(uvicorn, "run", fake_run)

    run_react_ui("127.0.0.1", 8080)

    assert called["host"] == "127.0.0.1"
    assert called["port"] == 8080
    assert called["log_level"] == "info"


def test_start_react_ui_in_background(monkeypatch) -> None:
    class DummyConfig:
        panel_host = "localhost"
        react_port = 7777

    started = {}

    class DummyThread:
        def __init__(self, target, args, daemon):
            started["target"] = target
            started["args"] = args
            started["daemon"] = daemon

        def start(self):
            started["started"] = True

    monkeypatch.setattr(
        "src.ui.react_ui.background.Config.from_env",
        lambda: DummyConfig(),
    )
    monkeypatch.setattr(threading, "Thread", DummyThread)

    start_react_ui_in_background()

    assert started["args"] == ("localhost", 7777)
    assert started["daemon"] is True
    assert started["started"] is True
