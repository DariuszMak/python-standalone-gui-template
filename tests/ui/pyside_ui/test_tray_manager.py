import pytest
from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QApplication, QWidget
from pytestqt.qtbot import QtBot

from src.ui.pyside_ui.dialog_windows.main_window import MainWindow
from src.ui.pyside_ui.tray_manager import TrayManager


class DummySignal:
    def connect(self, *_args, **_kwargs) -> None:
        pass


class DummyActivationReason:
    Trigger = 1


class DummyMessageIcon:
    Information = 1


class DummyTrayIcon:
    ActivationReason = DummyActivationReason
    MessageIcon = DummyMessageIcon

    def __init__(self, *_args, **_kwargs) -> None:
        self.context_menu = None
        self.icon = None
        self.visible = False
        self.hidden = False
        self.messages = []
        self.activated = DummySignal()

    def setIcon(self, icon) -> None:
        self.icon = icon

    def setContextMenu(self, menu) -> None:
        self.context_menu = menu

    def show(self) -> None:
        self.visible = True

    def hide(self) -> None:
        self.hidden = True

    def showMessage(self, title, message, icon, timeout) -> None:
        self.messages.append({
            "title": title,
            "message": message,
            "icon": icon,
            "timeout": timeout,
        })


@pytest.fixture
def tray_manager(
    monkeypatch: pytest.MonkeyPatch,
    qtbot: QtBot,
) -> TrayManager:
    monkeypatch.setattr(
        "src.ui.pyside_ui.tray_manager.QSystemTrayIcon",
        DummyTrayIcon,
    )

    window = QWidget()

    qtbot.addWidget(window)

    manager = TrayManager(window)

    return manager


def test_minimize_hides_window_to_tray(
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    window = MainWindow(fetch_server_time=False)

    qtbot.addWidget(window)

    window.show()

    called = {"notify": False}

    if window._tray is None:

        class DummyTray:
            def notify_hidden(self) -> None:
                called["notify"] = True

        monkeypatch.setattr(window, "_tray", DummyTray())

    else:
        monkeypatch.setattr(
            window._tray,
            "notify_hidden",
            lambda: called.update({"notify": True}),
        )

    window.setWindowState(Qt.WindowState.WindowMinimized)

    event = QEvent(QEvent.Type.WindowStateChange)

    window.changeEvent(event)

    qtbot.wait(20)

    assert window.isVisible() is False
    assert called["notify"] is True


def test_restore_shows_window(
    tray_manager: TrayManager,
    qtbot: QtBot,
) -> None:
    tray_manager._window.hide()

    tray_manager.restore()

    qtbot.wait(20)

    assert tray_manager._window.isVisible() is True

    assert tray_manager._window.windowState() == Qt.WindowState.WindowNoState


def test_hide_hides_window(
    tray_manager: TrayManager,
    qtbot: QtBot,
) -> None:
    tray_manager._window.show()

    tray_manager.hide()

    qtbot.wait(20)

    assert tray_manager._window.isVisible() is False


def test_quit_hides_tray_and_quits(
    tray_manager: TrayManager,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called = {"quit": False}

    monkeypatch.setattr(
        QApplication,
        "quit",
        lambda: called.update({"quit": True}),
    )

    tray_manager.quit()

    assert tray_manager._tray_icon.hidden is True
    assert called["quit"] is True


def test_icon_activated_hides_window(
    tray_manager: TrayManager,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called = {"hide": False}

    tray_manager._window.show()

    monkeypatch.setattr(
        tray_manager,
        "hide",
        lambda: called.update({"hide": True}),
    )

    tray_manager.icon_activated(DummyTrayIcon.ActivationReason.Trigger)

    assert called["hide"] is True


def test_icon_activated_restores_window(
    tray_manager: TrayManager,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    called = {"restore": False}

    tray_manager._window.hide()

    monkeypatch.setattr(
        tray_manager,
        "restore",
        lambda: called.update({"restore": True}),
    )

    tray_manager.icon_activated(DummyTrayIcon.ActivationReason.Trigger)

    assert called["restore"] is True


def test_notify_hidden_shows_message(
    tray_manager: TrayManager,
) -> None:
    tray_manager.notify_hidden()

    assert len(tray_manager._tray_icon.messages) == 1

    message = tray_manager._tray_icon.messages[0]

    assert message["title"] == "Application"

    assert message["message"] == "Application minimized to tray"

    assert message["icon"] == DummyMessageIcon.Information

    assert message["timeout"] == 2000


def test_tray_manager_initialization(
    tray_manager: TrayManager,
) -> None:
    assert tray_manager._tray_icon.visible is True

    assert tray_manager._tray_icon.context_menu is not None
