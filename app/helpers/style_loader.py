# -*- coding: utf-8 -*-
"""Style loader module."""

import os

from PySide6.QtWidgets import QMainWindow


class StyleLoader:
    """Loads style from files."""

    @staticmethod
    def get_real_path_from_relative_path(relative_path: str) -> str:
        """Gets absolute path of project and concatenate with provided path."""
        return os.path.realpath(relative_path)

    @staticmethod
    def load_file_content(path: str) -> str:
        """Loads text file content from specified file in path."""
        with open(StyleLoader.get_real_path_from_relative_path(path), "r") as f:
            content = f.read()

        return content

    @staticmethod
    def get_qss_from_file() -> str:
        """Loads qss theme from file."""
        return StyleLoader.load_file_content("app/ui/themes/main_theme.qss")

    @staticmethod
    def setup_stylesheets(window: QMainWindow) -> None:
        """Sets new stylesheet to provided window."""
        stylesheet_content = StyleLoader.get_qss_from_file()

        window.setStyleSheet(stylesheet_content)
