# -*- coding: utf-8 -*-
"""Style loader module."""

import os

from PySide6.QtWidgets import QMainWindow


class StyleLoader:
    """Loads style from files."""

    @staticmethod
    def get_project_absolute_path(relative_path: str) -> str:
        """Gets absolute path of project and concatenate with provided path."""
        base_path = os.path.abspath(".")
        joined_path = os.path.join(base_path, relative_path)
        real_path = os.path.realpath(joined_path)

        return real_path

    @staticmethod
    def get_qss_from_file() -> str:
        """Loads qss theme from file."""
        return StyleLoader.load_file_content("app/ui/themes/main_theme.qss")

    @staticmethod
    def load_file_content(path: str) -> str:
        """Loads text file content from specified file in path."""
        with open(StyleLoader.get_project_absolute_path(path), "r") as f:
            style = f.read()

        return style

    @staticmethod
    def setup_stylesheets(window: QMainWindow) -> None:
        """Sets new stylesheet to provided window."""
        stylesheet_from_file = StyleLoader.get_qss_from_file()

        window.setStyleSheet(stylesheet_from_file)
