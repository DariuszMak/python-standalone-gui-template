import asyncio
import logging
import os

from PySide6.QtCore import QEasingCurve, QEvent, QObject, QPropertyAnimation, Qt
from PySide6.QtGui import QCloseEvent, QGuiApplication, QKeyEvent, QResizeEvent

from src.api.models import ServerTimeResponse
from src.api.time_client import TimeClient
from src.helpers.style_loader import StyleLoader
from src.ui.clock_widget.view.clock_widget import ClockWidget
from src.ui.dialog_windows import ANIMATION_DURATION, MAINWINDOW_HEIGHT, MAINWINDOW_RESIZE_RANGE, MAINWINDOW_WIDTH
from src.ui.dialog_windows.draggable_main_window import DraggableMainWindow
from src.ui.dialog_windows.warning_dialog import WarningDialog
from src.ui.forms.moc_main_window import Ui_MainWindow

logger = logging.getLogger(__name__)


class MainWindow(DraggableMainWindow):
    def __init__(self, fetch_server_time: bool = True) -> None:
        super().__init__()

        self._supports_opacity = QGuiApplication.platformName().lower() not in ["wayland", "xcb"]
        self._is_closing = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # type: ignore[no-untyped-call]
        StyleLoader.style_window(self)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        self.setMinimumSize(MAINWINDOW_WIDTH - MAINWINDOW_RESIZE_RANGE, MAINWINDOW_HEIGHT - MAINWINDOW_RESIZE_RANGE)
        self.resize(MAINWINDOW_WIDTH, MAINWINDOW_HEIGHT)

        self.ui.pushButton.setText("Click to open dialog window")
        self.ui.pushButton.clicked.connect(self.show_warning_dialog)

        self.ui.btn_minimize.clicked.connect(self.showMinimized)
        self.ui.btn_maximize_restore.clicked.connect(self.toggle_maximize_restore)
        self.ui.btn_close.clicked.connect(self.close)

        self.clock_widget: ClockWidget = ClockWidget()
        layout = self.ui.frame_clock_widget.layout()
        if layout is not None:
            layout.addWidget(self.clock_widget)
        else:
            logger.warning("frame_clock_widget has no layout set.")

        if self._supports_opacity:
            self.fade_in_animation()

        self.installEventFilter(self)

        if fetch_server_time:
            self._server_time_task: asyncio.Task[None] | None = None

            api_host = os.getenv("API_HOST", "127.0.0.1")
            api_port = os.getenv("API_PORT", "8000")

            self._time_client = TimeClient(f"http://{api_host}:{api_port}")

            loop = asyncio.get_event_loop()
            loop.call_soon(self.fetch_server_time)

    def fetch_server_time(self) -> None:
        if self._server_time_task and not self._server_time_task.done():
            return

        self._server_time_task = asyncio.create_task(self._fetch_server_time())

    async def _fetch_server_time(self) -> None:
        try:
            result = await self._time_client.fetch_time()
            self._apply_server_time(result)
        except Exception as exc:
            logger.exception("Failed to fetch server time", exc_info=exc)

    def _apply_server_time(self, server_time: ServerTimeResponse) -> None:
        logger.info("Server datetime received: %s", server_time.datetime.isoformat())
        self.clock_widget.set_current_datetime(server_time.datetime)

    def fade_in_animation(self) -> None:
        if not self._supports_opacity:
            return
        self.setWindowOpacity(0.0)
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(600)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(0.9)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.start()

    def fade_out_animation(self) -> None:
        if not self._supports_opacity:
            self._final_close()
            return
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(ANIMATION_DURATION)
        self.anim.setStartValue(0.9)
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

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802
        min_width, min_height = MAINWINDOW_WIDTH - MAINWINDOW_RESIZE_RANGE, MAINWINDOW_HEIGHT - MAINWINDOW_RESIZE_RANGE
        new_width = max(event.size().width(), min_width)
        new_height = max(event.size().height(), min_height)

        if new_width != event.size().width() or new_height != event.size().height():
            self.resize(new_width, new_height)

        super().resizeEvent(event)

    def changeEvent(self, event: QEvent) -> None:  # noqa: N802
        if event.type() == QEvent.Type.LanguageChange:
            self.ui.retranslateUi(self)  # type: ignore[no-untyped-call]
        super().changeEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        if self._supports_opacity and not self._is_closing:
            logger.info("Closing main window...")
            event.ignore()
            self.clock_widget.reset()
            self.fade_out_animation()
        else:
            super().closeEvent(event)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:  # noqa: N802
        if event.type() == QEvent.Type.KeyPress and isinstance(event, QKeyEvent) and event.key() == Qt.Key.Key_R:
            self.fetch_server_time()
            return True
        return super().eventFilter(obj, event)

    def _final_close(self) -> None:
        self._is_closing = True
        super().close()
