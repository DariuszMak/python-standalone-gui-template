from PySide6 import QtCore, QtGui
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QWidget
from PySide6.QtGui import QMouseEvent


from src.helpers.style_loader import StyleLoader
from src.ui.forms.moc_warning_dialog import Ui_Dialog  # type: ignore


class WarningDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__()

        self.ui = Ui_Dialog()

        self.ui.setupUi(self)

        StyleLoader.style_window(self)

        self.parent_obj: QWidget | None = parent

        self.dragPos: QtCore.QPoint = QtCore.QPoint()

        self.setup_window_properties(parent)
        self.content_initialization()

    def setup_window_properties(self, parent: QWidget | None) -> None:
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.ui.btn_close.clicked.connect(self.close)

        def move_window(event: QMouseEvent) -> None:
            if event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                self.dragPos = event.globalPosition().toPoint()
                event.accept()

        self.ui.frame_label_top_btns.mouseMoveEvent = move_window
        StyleLoader.center_window(self, parent)

    def content_initialization(self) -> None:
        pixmap = QPixmap(":/logos/icons/images/warning.png")

        self.ui.label_warning.setPixmap(pixmap.scaled(40, 40, QtGui.Qt.AspectRatioMode.KeepAspectRatio))

    def mousePressEvent(self, event: QEvent) -> None:  # noqa: N802
        self.dragPos = event.globalPosition().toPoint()

    def changeEvent(self, event: QEvent) -> None:  # noqa: N802
        if event.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)
        super().changeEvent(event)
