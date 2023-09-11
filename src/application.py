# -*- coding: utf-8 -*-
"""Application module."""
import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def run() -> None:
    """Main function that runs application."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
