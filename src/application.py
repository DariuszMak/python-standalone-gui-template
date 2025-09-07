import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen

from src.helpers.style_loader import StyleLoader
from src.ui.main_window import MainWindow


def run() -> None:
    app = QApplication(sys.argv)

    pixmap = QPixmap(":/logos/icons/images/program_icon.ico").scaled(
        64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
    )

    splash = QSplashScreen(pixmap)
    StyleLoader.center_window(splash)
    splash.show()
    app.processEvents()

    window = MainWindow()

    window.setMinimumSize(500, 400)
    window.resize(500, 400)

    window.show()

    splash.finish(window)

    sys.exit(app.exec())
