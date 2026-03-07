import sys
import pytest
from _pytest.monkeypatch import MonkeyPatch
from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QSystemTrayIcon
from pytestqt.qtbot import QtBot

from src.ui.pyside_ui.dialog_windows.main_window import MainWindow


def test_minimize_hides_window_to_tray(qtbot: QtBot, monkeypatch: MonkeyPatch) -> None:
    if not QSystemTrayIcon.isSystemTrayAvailable() or sys.platform.startswith("linux"):
        pytest.skip("System tray not available on this platform, skipping hide-to-tray test")

    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    # Ensure tray exists
    if getattr(window, "tray", None) is None:
        if hasattr(window, "init_tray"):
            window.init_tray()
        else:
            # fallback: create a dummy tray so test can patch it
            class DummyTray:
                def notify_hidden(self):  # type: ignore
                    pass
            window.tray = DummyTray()

    called = {"notify": False}

    def fake_notify() -> None:
        called["notify"] = True

    # Patch the tray notify_hidden method
    monkeypatch.setattr(window.tray, "notify_hidden", fake_notify)

    # Minimize the window and trigger changeEvent
    window.setWindowState(Qt.WindowState.WindowMinimized)
    event = QEvent(QEvent.Type.WindowStateChange)
    window.changeEvent(event)

    qtbot.wait(10)

    assert window.isVisible() is False
    assert called["notify"] is True