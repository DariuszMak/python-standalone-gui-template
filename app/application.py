# -*- coding: utf-8 -*-
"""Application module."""
import sys


from PySide6.QtWidgets import QApplication, QMainWindow
from app.ui.auto_generated.main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    """MainWindow class."""

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


def run():
    """Main function that runs application."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


def hello_world():
    """Function just for test."""
    return "Hello World!"
