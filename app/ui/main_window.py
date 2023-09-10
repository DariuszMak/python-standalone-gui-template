# -*- coding: utf-8 -*-
"""MainWindow module."""
from PySide6.QtWidgets import QMainWindow

from app.helpers.style_loader import StyleLoader
from app.ui.forms.moc_main_window import Ui_MainWindow
from app.ui.warning_dialog import WarningDialog


class MainWindow(QMainWindow):
    """MainWindow class."""

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        StyleLoader.setup_stylesheets(self)
        self.ui.pushButton.setText("Click to open dialog window")
        self.ui.pushButton.clicked.connect(self.show_warning_dialog)

    def show_warning_dialog(self) -> None:
        """Show warning dialog."""
        dlg = WarningDialog(self)
        dlg.ui.label_title_bar_top.setText("Warning title")
        dlg.ui.label_info.setText("Warning message")

        if dlg.exec_():
            print("Accepted")
        else:
            print("Cancelled")
