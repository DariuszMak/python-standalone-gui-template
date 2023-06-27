# -*- coding: utf-8 -*-
"""Application module."""
import sys
from PySide6.QtWidgets import QApplication, QWidget


def run():
    """Main function that runs application."""
    app = QApplication(sys.argv)

    window = QWidget()
    window.show()

    app.exec_()


def hello_world():
    """Function just for test."""
    return "Hello World!"
