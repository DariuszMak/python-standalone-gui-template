from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtWidgets import QApplication

from src.application import create_app


def test_create_app_wires_everything(qtbot):
    app = QApplication.instance()
    assert app is not None

    with (
        patch("src.application.QSplashScreen") as MockSplash,
        patch("src.application.StyleLoader.center_window") as center_window,
        patch("src.application.MainWindow") as MockMainWindow,
        patch("src.application.QTimer.singleShot") as single_shot,
    ):
        splash = MagicMock()
        MockSplash.return_value = splash

        window = MagicMock()
        MockMainWindow.return_value = window

        returned_app, _loop, returned_window = create_app()

        assert returned_app is app

        MockSplash.assert_called_once()
        splash.show.assert_called_once()
        splash.finish.assert_called_once_with(window)
        center_window.assert_called_once_with(splash)

        MockMainWindow.assert_called_once_with(fetch_server_time=False)
        window.show.assert_called_once()

        single_shot.assert_called_once_with(0, window.fetch_server_time)

        assert returned_window is window
