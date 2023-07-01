# -*- coding: utf-8 -*-
"""Style loader module."""
import os
from app.helpers.io_file import IOFile
from PySide6.QtWidgets import QMainWindow


class StyleLoader:
    """Loads style from files."""

    MAIN_THEME_PATH = os.path.join("app", "ui", "themes", "main_theme.qss")

    @staticmethod
    def setup_stylesheets(window: QMainWindow) -> None:
        """Sets new stylesheet to provided window."""
        stylesheet_content = StyleLoader.get_qss_from_file()

        window.setStyleSheet(stylesheet_content)

    @staticmethod
    def get_qss_from_file(path: str = MAIN_THEME_PATH) -> str:
        """Loads qss theme from file."""
        return IOFile.load_file_content(path)
