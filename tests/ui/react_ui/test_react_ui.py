import threading
from collections.abc import Callable
from typing import Any

import pytest
import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.ui.react_ui.app import app, create_app, run_react_ui, start_react_ui_in_background
from starlette.staticfiles import StaticFiles
from unittest.mock import Mock

def test_create_app_static_files_configured(monkeypatch):
    monkeypatch.setattr("starlette.staticfiles.StaticFiles", Mock)
    from src.ui.react_ui.app import create_app
    app = create_app()
    
    mounts = [route.path for route in app.routes if hasattr(route, "path")]
    assert "/assets" in mounts


def test_run_react_ui_calls_uvicorn(monkeypatch: pytest.MonkeyPatch) -> None:
    called = {}

    def fake_run(app_instance: Any, host: str, port: int, log_level: str) -> None:
        called["app"] = app_instance
        called["host"] = host
        called["port"] = port
        called["log_level"] = log_level

    monkeypatch.setattr(uvicorn, "run", fake_run)

    run_react_ui("127.0.0.1", 8080)

    assert called["app"] is app
    assert called["host"] == "127.0.0.1"
    assert called["port"] == 8080
    assert called["log_level"] == "info"


def test_start_react_ui_in_background(monkeypatch: pytest.MonkeyPatch) -> None:
    class DummyConfig:
        panel_host = "localhost"
        react_port = 7777

    started: dict[str, Any] = {}

    class DummyThread:
        def __init__(self, target: Callable[..., Any], args: tuple[Any, ...], daemon: bool) -> None:
            started["target"] = target
            started["args"] = args
            started["daemon"] = daemon

        def start(self) -> None:
            started["started"] = True

    monkeypatch.setattr("src.ui.react_ui.app.Config.from_env", lambda: DummyConfig())
    monkeypatch.setattr(threading, "Thread", DummyThread)

    start_react_ui_in_background()

    assert started["args"] == ("localhost", 7777)
    assert started["daemon"] is True
    assert started["started"] is True
