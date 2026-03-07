from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QWidget


class TrayManager:
    def __init__(self, window: QWidget) -> None:
        self.window = window
        self.tray_icon = QSystemTrayIcon(window)

        icon = QIcon(":/logos/icons/images/program_icon.ico")
        self.tray_icon.setIcon(icon)

        self.menu = QMenu()

        self.restore_action = QAction("Restore")
        self.restore_action.triggered.connect(self.restore)

        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.quit)

        self.menu.addAction(self.restore_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self.icon_activated)

        self.tray_icon.show()

    def restore(self) -> None:
        self.window.show()
        self.window.setWindowState(Qt.WindowState.WindowNoState)
        self.window.activateWindow()

    def hide(self) -> None:
        self.window.hide()

    def quit(self) -> None:
        self.tray_icon.hide()
        QApplication.quit()

    def icon_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.window.isVisible():
                self.hide()
            else:
                self.restore()

    def notify_hidden(self) -> None:
        self.tray_icon.showMessage(
            "Application",
            "Application minimized to tray",
            QSystemTrayIcon.MessageIcon.Information,
            2000,
        )