import asyncio
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen
from qasync import QEventLoop  # type: ignore

from src.helpers.style_loader import StyleLoader
from src.ui.dialog_windows.main_window import MainWindow


def run() -> None:
    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    pixmap = QPixmap(":/logos/icons/images/program_icon.ico").scaled(
        64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
    )

    splash = QSplashScreen(pixmap)
    StyleLoader.center_window(splash)
    splash.show()
    app.processEvents()

    window = MainWindow(fetch_server_time=False)
    window.show()

    splash.finish(window)

    QTimer.singleShot(0, window.fetch_server_time)

    with loop:
        sys.exit(loop.run_forever())
