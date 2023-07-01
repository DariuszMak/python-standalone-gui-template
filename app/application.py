# -*- coding: utf-8 -*-
"""Application module."""
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from app.helpers.style_loader import StyleLoader
from app.ui.auto_generated.main_window import Ui_MainWindow  # type: ignore


class MainWindow(QMainWindow):
    """MainWindow class."""

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        StyleLoader.setup_stylesheets(self)


def run() -> None:
    """Main function that runs application."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
