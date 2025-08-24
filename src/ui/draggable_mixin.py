from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QMouseEvent


class DraggableMixin:
    def __init__(self) -> None:
        self._drag_active: bool = False
        self._drag_position: QPoint = QPoint()

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            is_maximized = getattr(self, "_is_maximized", False)  # fallback for dialogs
            if not is_maximized and self.windowHandle() is not None:
                # try native drag first
                if self.windowHandle().startSystemMove():
                    return

            # fallback manual drag
            self._drag_active = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

        try:
            super().mousePressEvent(event)
        except AttributeError:
            pass  # ignore if no parent implementation

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if self._drag_active and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

        try:
            super().mouseMoveEvent(event)
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = False
            event.accept()

        try:
            super().mouseReleaseEvent(event)
        except AttributeError:
            pass
