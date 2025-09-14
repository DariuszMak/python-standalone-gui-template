import logging

from PySide6.QtCore import QEasingCurve, QEvent, QPropertyAnimation
from PySide6.QtGui import QCloseEvent, QGuiApplication

from src.helpers.style_loader import StyleLoader
from src.ui.draggable_main_window import DraggableMainWindow
from src.ui.forms.moc_main_window import Ui_MainWindow
from src.ui.warning_dialog import WarningDialog

logger = logging.getLogger(__name__)


class MainWindow(DraggableMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self._supports_opacity = QGuiApplication.platformName().lower() not in ["wayland", "xcb"]
        self._is_closing = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        StyleLoader.style_window(self)

        self.ui.pushButton.setText("Click to open dialog window")
        self.ui.pushButton.clicked.connect(self.show_warning_dialog)

        self.ui.btn_minimize.clicked.connect(self.showMinimized)
        self.ui.btn_maximize_restore.clicked.connect(self.toggle_maximize_restore)
        self.ui.btn_close.clicked.connect(self.close)
        if self._supports_opacity:
            self.fade_in_animation()

    def fade_in_animation(self) -> None:
        if not self._supports_opacity:
            return
        self.setWindowOpacity(0.0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(600)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.start()

    def fade_out_animation(self) -> None:
        if not self._supports_opacity:
            self._final_close()
            return
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(600)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.anim.finished.connect(self._final_close)
        self.anim.start()

    def show_warning_dialog(self) -> None:
        dlg = WarningDialog(self)
        dlg.ui.label_title_bar_top.setText("Warning title")
        dlg.ui.label_info.setText("Warning message")

        if dlg.exec_():
            logger.info("Accepted")
        else:
            logger.info("Cancelled")

    def toggle_maximize_restore(self) -> None:
        if self._is_maximized:
            self.showNormal()
        else:
            self.showMaximized()
        self._is_maximized = not self._is_maximized

    def resizeEvent(self, event):  # noqa: N802
        min_width, min_height = 500, 400
        new_width = max(event.size().width(), min_width)
        new_height = max(event.size().height(), min_height)

        if new_width != event.size().width() or new_height != event.size().height():
            self.resize(new_width, new_height)

        super().resizeEvent(event)

    def changeEvent(self, event: QEvent) -> None:  # noqa: N802
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)
        super().changeEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        logger.info("Closing main window...")

        if self._supports_opacity and not self._is_closing:
            event.ignore()
            self.fade_out_animation()
        else:
            super().closeEvent(event)

    def _final_close(self) -> None:
        self._is_closing = True
        super().close()
