"""Style loader module."""

import os

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget

from src.helpers.io_file import IOFile


class StyleLoader:
    """Load style from files."""

    MAIN_THEME_PATH = os.path.join("src", "ui", "themes", "main_theme.qss")

    @staticmethod
    def style_window(window: QWidget) -> None:
        StyleLoader.setup_stylesheets(window)
        StyleLoader.set_main_program_icon(window)

    @staticmethod
    def set_main_program_icon(window: QWidget) -> None:
        icon = QIcon()
        icon.addFile(":/logos/icons/images/program_icon.ico", QSize(64, 64), QIcon.Normal, QIcon.Off)
        window.setWindowIcon(icon)

    @staticmethod
    def setup_stylesheets(window: QWidget) -> None:
        """Set new stylesheet to provided window."""
        stylesheet_content = StyleLoader.get_qss_from_file()

        window.setStyleSheet(stylesheet_content)

    @staticmethod
    def get_qss_from_file(path: str = MAIN_THEME_PATH) -> str:
        """Load qss theme from file."""
        return IOFile.load_file_content(path)

    @staticmethod
    def center_window(current_window: QWidget, parent_obj: QWidget | None = None) -> None:
        """Center window according to provided widget."""
        if parent_obj is not None:
            current_window.move(parent_obj.geometry().center() - current_window.rect().center())
        else:
            mouse_pointer_position = current_window.cursor().pos()

            screen = QApplication.screenAt(mouse_pointer_position)

            position = screen.geometry().center() - current_window.rect().center()

            current_window.move(position.x(), position.y())
