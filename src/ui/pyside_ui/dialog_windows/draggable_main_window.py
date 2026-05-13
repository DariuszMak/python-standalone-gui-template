from PySide6.QtWidgets import QMainWindow, QWidget

from src.ui.pyside_ui.dialog_windows.draggable_mixin import DraggableMixin


class DraggableMainWindow(DraggableMixin, QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        QMainWindow.__init__(self, parent)
        DraggableMixin.__init__(self)

        self._is_maximized = False

    def _can_drag(self) -> bool:
        return not self._is_maximized
