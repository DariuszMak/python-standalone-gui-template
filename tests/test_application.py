from unittest.mock import MagicMock, patch

from PySide6.QtWidgets import QApplication
from pytestqt.qtbot import QtBot

from src.application import create_app


def test_create_app_wires_everything(qtbot: QtBot) -> None:  # noqa: ARG001
    app = QApplication.instance()
    assert app is not None

    with (
        patch("src.application.QSplashScreen") as mock_splash_cls,
        patch("src.application.StyleLoader.center_window") as center_window,
        patch("src.application.MainWindow") as mock_main_window_cls,
        patch("src.application.QTimer.singleShot") as single_shot,
    ):
        splash = MagicMock()
        mock_splash_cls.return_value = splash

        window = MagicMock()
        mock_main_window_cls.return_value = window

        returned_app, loop, returned_window = create_app()

        assert returned_app is app

        try:
            mock_splash_cls.assert_called_once()
            splash.show.assert_called_once()
            splash.finish.assert_called_once_with(window)
            center_window.assert_called_once_with(splash)

            mock_main_window_cls.assert_called_once_with(fetch_server_time=False)
            window.show.assert_called_once()

            single_shot.assert_called_once_with(0, window.fetch_server_time)

            assert returned_window is window

        finally:
            loop.close()
