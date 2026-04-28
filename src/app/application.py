import asyncio
import sys
from typing import Any

import structlog
from PySide6.QtCore import QCoreApplication, Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen
from qasync import QEventLoop  # type: ignore

from src.helpers.style_loader import StyleLoader
from src.ui.pyside_ui.dialog_windows.main_window import MainWindow

logger = structlog.get_logger(__name__)


def create_app() -> tuple[QCoreApplication, Any, MainWindow]:
    logger.info("initializing_application")

    app = QApplication.instance()
    if app is None:
        logger.debug("creating_new_qapplication_instance")
        app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    logger.debug("displaying_splash_screen")
    pixmap = QPixmap(":/logos/icons/images/program_icon.ico").scaled(
        64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
    )

    splash = QSplashScreen(pixmap)
    StyleLoader.center_window(splash)
    splash.show()
    app.processEvents()

    logger.info("loading_main_window")
    window = MainWindow(fetch_server_time=False)
    window.show()

    splash.finish(window)

    logger.debug("scheduling_server_time_fetch")
    QTimer.singleShot(0, window.fetch_server_time)

    return app, loop, window


def run() -> None:
    try:
        _app, loop, _ = create_app()
        logger.info("application_started", loop_type="QEventLoop")
        with loop:
            sys.exit(loop.run_forever())
    except Exception as e:
        logger.exception("application_failed_to_start", error=str(e))
        sys.exit(1)
