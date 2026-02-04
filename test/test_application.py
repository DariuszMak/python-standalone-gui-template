from unittest.mock import MagicMock, patch

import pytest

from src.application import create_app


@pytest.mark.qt
def test_create_app_sets_up_main_window(qtbot):
    with (
        patch("src.ui.pyside_ui.dialog_windows.main_window.MainWindow") as MockWindow,
        patch("src.helpers.style_loader.StyleLoader.center_window") as center_window,
        patch("PySide6.QtWidgets.QSplashScreen") as MockSplash,
    ):
        mock_window = MagicMock()
        MockWindow.return_value = mock_window

        _app, _loop, _window = create_app()

        MockWindow.assert_called_once_with(fetch_server_time=False)
        mock_window.show.assert_called_once()

        MockSplash.return_value.show.assert_called_once()
        center_window.assert_called_once()
