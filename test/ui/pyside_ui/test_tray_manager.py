import sys
import pytest
from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QSystemTrayIcon
from pytestqt.qtbot import QtBot

from src.ui.pyside_ui.dialog_windows.main_window import MainWindow

def test_minimize_hides_window_to_tray(qtbot: QtBot, monkeypatch) -> None:
    # Patch window.tray to a dummy object if system tray unavailable
    class DummyTray:
        def notify_hidden(self) -> None:
            called["notify"] = True

    called = {"notify": False}

    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    if getattr(window, "tray", None) is None:
        monkeypatch.setattr(window, "tray", DummyTray())
    else:
        monkeypatch.setattr(window.tray, "notify_hidden", lambda: called.update({"notify": True}))

    # Minimize and trigger event
    window.setWindowState(Qt.WindowState.WindowMinimized)
    event = QEvent(QEvent.Type.WindowStateChange)
    window.changeEvent(event)

    qtbot.wait(10)

    assert window.isVisible() is False
    assert called["notify"] is True