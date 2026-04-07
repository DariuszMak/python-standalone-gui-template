import threading
from collections.abc import Callable
from typing import Any

import pytest
import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.ui.react_ui.app import create_app, run_react_ui, start_react_ui_in_background


def test_create_app_static_files_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("starlette.staticfiles.StaticFiles.__init__", lambda _self, *_args, **_kwargs: None)

    test_app = create_app()

    assert isinstance(test_app, FastAPI)

    static_mounts = [route for route in test_app.routes if isinstance(getattr(route, "app", None), StaticFiles)]
    assert len(static_mounts) == 1


def test_run_react_ui_calls_uvicorn(monkeypatch: pytest.MonkeyPatch) -> None:
    called: dict[str, Any] = {}
    captured_app: list[FastAPI] = []

    def fake_create_app(config: Any = None) -> FastAPI:  # noqa: ANN401
        fa = FastAPI()
        captured_app.append(fa)
        return fa

    def fake_run(app_instance: Any, host: str, port: int, log_level: str) -> None:
        called["app"] = app_instance
        called["host"] = host
        called["port"] = port
        called["log_level"] = log_level

    monkeypatch.setattr("src.ui.react_ui.app.create_app", fake_create_app)
    monkeypatch.setattr(uvicorn, "run", fake_run)

    run_react_ui("127.0.0.1", 8080)

    assert len(captured_app) == 1
    assert called["app"] is captured_app[0]
    assert called["host"] == "127.0.0.1"
    assert called["port"] == 8080
    assert called["log_level"] == "info"


def test_start_react_ui_in_background(monkeypatch: pytest.MonkeyPatch) -> None:
    class DummyConfig:
        panel_host = "localhost"
        react_port = 7777

    dummy_config = DummyConfig()
    started: dict[str, Any] = {}

    class DummyThread:
        def __init__(self, target: Callable[..., Any], args: tuple[Any, ...], daemon: bool) -> None:
            started["target"] = target
            started["args"] = args
            started["daemon"] = daemon

        def start(self) -> None:
            started["started"] = True

    monkeypatch.setattr("src.ui.react_ui.app.Config.from_env", lambda: dummy_config)
    monkeypatch.setattr(threading, "Thread", DummyThread)

    start_react_ui_in_background()

    assert started["args"] == ("localhost", 7777, dummy_config)
    assert started["daemon"] is True
    assert started["started"] is True