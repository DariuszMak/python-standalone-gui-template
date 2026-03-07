import sys

import pytest
from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QSystemTrayIcon
from pytestqt.qtbot import QtBot

from src.ui.pyside_ui.dialog_windows.main_window import MainWindow


def test_minimize_hides_window_to_tray(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    if not QSystemTrayIcon.isSystemTrayAvailable() or sys.platform.startswith("linux"):
        pytest.skip("System tray not available on this platform, skipping hide-to-tray test")

    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    called = {"notify": False}

    def fake_notify() -> None:
        called["notify"] = True

    if getattr(window, "tray", None) is None:
        dummy_tray = type("DummyTray", (), {"notify_hidden": fake_notify})
        monkeypatch.setattr(window, "tray", dummy_tray())
    else:
        monkeypatch.setattr(window.tray, "notify_hidden", fake_notify)

    # Minimize the window and trigger the changeEvent
    window.setWindowState(Qt.WindowState.WindowMinimized)
    event = QEvent(QEvent.Type.WindowStateChange)
    window.changeEvent(event)

    qtbot.wait(10)

    assert window.isVisible() is False
    assert called["notify"] is True
