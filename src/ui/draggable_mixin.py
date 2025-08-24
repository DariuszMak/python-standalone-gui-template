from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QMouseEvent


class DraggableMixin:
    def __init__(self) -> None:
        self._drag_active: bool = False
        self._drag_position: QPoint = QPoint()

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton and not self._is_maximized:
            if self.windowHandle() is not None:
                self.windowHandle().startSystemMove()
                return

            self._drag_active = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if self._drag_active and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = False
            event.accept()
        super().mouseReleaseEvent(event)

