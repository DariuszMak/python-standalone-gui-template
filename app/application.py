# -*- coding: utf-8 -*-
"""Application module."""
import sys
import os

from PySide6.QtWidgets import QApplication, QMainWindow
from app.ui.auto_generated.main_window import Ui_MainWindow  # type: ignore


class StylesLoader:
    """Loads style from files."""

    @staticmethod
    def resource_path(relative_path: str) -> str:
        """Gets absolute path of project and concatenate with provided path."""
        base_path = os.path.abspath(".")

        return os.path.realpath(os.path.join(base_path, relative_path))

    @staticmethod
    def get_qss_from_file() -> str:
        """Loads qss theme from file."""
        theme_file_path = StylesLoader.resource_path("app/ui/themes/main_theme.qss")

        with open(theme_file_path, "r") as f:
            style = f.read()

        return style

    @staticmethod
    def setup_stylesheets(window: QMainWindow) -> None:
        """Sets new stylesheet to provided window."""
        stylesheet_from_file = StylesLoader.get_qss_from_file()

        window.setStyleSheet(stylesheet_from_file)


class MainWindow(QMainWindow):
    """MainWindow class."""

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        StylesLoader.setup_stylesheets(self)


def run() -> None:
    """Main function that runs application."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


def hello_world() -> str:
    """Function just for test."""
    return "Hello World!"
