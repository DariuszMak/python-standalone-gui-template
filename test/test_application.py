import pytest
from unittest.mock import MagicMock, patch

from PySide6.QtWidgets import QApplication

from src.application import create_app


@pytest.mark.qt
def test_create_app_wires_everything(qtbot):
    """
    Smoke-test the Qt bootstrap:
    - reuses existing QApplication
    - shows splash + main window
    - schedules fetch_server_time
    """

    # pytest-qt already created the QApplication
    app = QApplication.instance()
    assert app is not None

    with patch("src.application.QSplashScreen") as MockSplash, \
         patch("src.application.StyleLoader.center_window") as center_window, \
         patch("src.application.MainWindow") as MockMainWindow, \
         patch("src.application.QTimer.singleShot") as single_shot:

        # Arrange
        splash = MagicMock()
        MockSplash.return_value = splash

        window = MagicMock()
        MockMainWindow.return_value = window

        # Act
        returned_app, loop, returned_window = create_app()

        # Assert QApplication
        assert returned_app is app

        # Splash screen
        MockSplash.assert_called_once()
        splash.show.assert_called_once()
        splash.finish.assert_called_once_with(window)
        center_window.assert_called_once_with(splash)

        # Main window
        MockMainWindow.assert_called_once_with(fetch_server_time=False)
        window.show.assert_called_once()

        # Timer setup
        single_shot.assert_called_once_with(0, window.fetch_server_time)

        # Sanity
        assert returned_window is window
