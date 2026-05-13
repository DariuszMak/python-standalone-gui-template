from PySide6.QtWidgets import QDialog, QWidget

from src.ui.pyside_ui.dialog_windows.draggable_mixin import DraggableMixin


class DraggableDialog(DraggableMixin, QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        QDialog.__init__(self, parent)
        DraggableMixin.__init__(self)
