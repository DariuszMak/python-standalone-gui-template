from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget

from src.helpers.style_loader import StyleLoader
from src.ui.draggable_dialog import DraggableDialog
from src.ui.forms.moc_warning_dialog import Ui_Dialog

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QEvent
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget
import logging


logger = logging.getLogger(__name__)


class WarningDialog(DraggableDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        StyleLoader.style_window(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.ui.btn_close.clicked.connect(self.close)
        StyleLoader.center_window(self, parent)

        pixmap = QPixmap(":/logos/icons/images/warning.png")
        self.ui.label_warning.setPixmap(pixmap.scaled(40, 40, Qt.KeepAspectRatio))

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)
        super().changeEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        logger.info("Closing dialog window...")
        super().closeEvent(event)