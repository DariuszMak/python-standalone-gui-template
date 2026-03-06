import threading
from collections.abc import Callable
from typing import Any
from unittest.mock import patch

import pytest
import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.ui.react_ui.app import create_app, run
from src.ui.react_ui.server import run_react_ui, start_react_ui_in_background


def test_create_app_static_files_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("starlette.staticfiles.StaticFiles.__init__", lambda _self, *_args, **_kwargs: None)

    app = create_app()

    assert isinstance(app, FastAPI)

    static_mounts = [route for route in app.routes if isinstance(getattr(route, "app", None), StaticFiles)]
    assert len(static_mounts) == 1


def test_run_calls_uvicorn(monkeypatch: pytest.MonkeyPatch) -> None:
    called = {}

    def fake_run(app, host, port, log_level):
        called["app"] = app
        called["host"] = host
        called["port"] = port
        called["log_level"] = log_level

    monkeypatch.setattr(uvicorn, "run", fake_run)
    monkeypatch.setenv("REACT_HOST", "0.0.0.1")
    monkeypatch.setenv("REACT_PORT", "9000")

    with patch("starlette.staticfiles.StaticFiles.__init__", lambda _self, *_args, **_kwargs: None):
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
