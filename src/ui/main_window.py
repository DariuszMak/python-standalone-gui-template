import logging

from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QMainWindow

from src.helpers.style_loader import StyleLoader
from src.ui.forms.moc_main_window import Ui_MainWindow
from src.ui.warning_dialog import WarningDialog

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        StyleLoader.style_window(self)
        self.ui.pushButton.setText("Click to open dialog window")
        self.ui.pushButton.clicked.connect(self.show_warning_dialog)

        self.ui.btn_minimize.clicked.connect(self.minimize_window)
        self.ui.btn_maximize_restore.clicked.connect(self.maximize_restore_window)
        self.ui.btn_close.clicked.connect(self.close_window)

        self._drag_active: bool = False
        self._drag_position: QPoint = QPoint()
        self._is_maximized: bool = False

    def show_warning_dialog(self) -> None:
        dlg = WarningDialog(self)
        dlg.ui.label_title_bar_top.setText("Warning title")
        dlg.ui.label_info.setText("Warning message")

        if dlg.exec_():
            logger.info("Accepted")
        else:
            logger.info("Cancelled")

    def minimize_window(self) -> None:
        self.showMinimized()

    def maximize_restore_window(self) -> None:
        if self._is_maximized:
            self.showNormal()
            self._is_maximized = False
        else:
            self.showMaximized()
            self._is_maximized = True

    def close_window(self) -> None:
        self.close()

def mousePressEvent(self, event) -> None:  # noqa: N802
    if event.button() == Qt.MouseButton.LeftButton and not self._is_maximized:
        if self.windowHandle() is not None and self.windowHandle().startSystemMove(event):
            return

        self._drag_active = True
        self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        event.accept()

def mouseMoveEvent(self, event) -> None:  # noqa: N802
    if self._drag_active and event.buttons() & Qt.MouseButton.LeftButton:
        self.move(event.globalPosition().toPoint() - self._drag_position)
        event.accept()

def mouseReleaseEvent(self, event) -> None:  # noqa: N802
    if event.button() == Qt.MouseButton.LeftButton:
        self._drag_active = False
        event.accept()

