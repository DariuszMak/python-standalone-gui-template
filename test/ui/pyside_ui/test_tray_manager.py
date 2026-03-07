from _pytest.monkeypatch import MonkeyPatch
from PySide6.QtCore import QEvent, Qt
from pytestqt.qtbot import QtBot
import sys
import pytest
from src.ui.pyside_ui.dialog_windows.main_window import MainWindow
from PySide6.QtWidgets import QSystemTrayIcon

pytestmark = pytest.mark.skipif(
    not QSystemTrayIcon.isSystemTrayAvailable(),
    reason="System tray not supported in Linux/WSL test environment",
)
def test_minimize_hides_window_to_tray(qtbot: QtBot, monkeypatch: MonkeyPatch) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    called = {"notify": False}

    def fake_notify() -> None:
        called["notify"] = True

    monkeypatch.setattr(window.tray, "notify_hidden", fake_notify)

    window.setWindowState(Qt.WindowState.WindowMinimized)

    event = QEvent(QEvent.Type.WindowStateChange)
    window.changeEvent(event)

    qtbot.wait(10)

    assert window.isVisible() is False
    assert called["notify"] is True
