# -*- coding: utf-8 -*-
"""WarningDialog module."""
import typing as t

from PySide6 import QtCore, QtGui
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QWidget

from helpers.style_loader import StyleLoader
from ui.forms.moc_warning_dialog import Ui_Dialog  # type: ignore


class WarningDialog(QDialog):
    """WaringDialog class."""

    def __init__(self, parent: t.Optional[QWidget] = None) -> None:
        super().__init__()

        self.ui = Ui_Dialog()

        self.ui.setupUi(self)

        StyleLoader.setup_stylesheets(self)

        self.parent_obj: t.Optional[QWidget] = parent

        self.dragPos: QtCore.QPoint = QtCore.QPoint()

        self.setup_window_properties(parent)
        self.content_initialization()

    def setup_window_properties(self, parent: t.Optional[QWidget]) -> None:
        """Setup necessary window properties."""
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.ui.btn_close.clicked.connect(self.close)

        def moveWindow(event: QEvent) -> None:
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()

        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        StyleLoader.center_window(self, parent)

    def content_initialization(self) -> None:
        """Initialize content of window."""
        pixmap = QPixmap(":/logos/icons/images/warning.png")

        self.ui.label_warning.setPixmap(pixmap.scaled(40, 40, QtGui.Qt.AspectRatioMode.KeepAspectRatio))

    def mousePressEvent(self, event: QEvent) -> None:
        """Update position of mouse cursor."""
        self.dragPos = event.globalPosition().toPoint()

    def changeEvent(self, event: QEvent) -> None:
        """Event in case of language change."""
        if event.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)
        super().changeEvent(event)
