import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen

from src.helpers.style_loader import StyleLoader
from src.ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QSizePolicy



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

    window.show()

    splash.finish(window)

    sys.exit(app.exec())
