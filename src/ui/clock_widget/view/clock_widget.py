from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget

from src.ui.clock_widget.controller.clock_controller import ClockController
from src.ui.clock_widget.view.helpers import convert_clock_pid_to_cartesian
from src.ui.clock_widget.view.painter import Painter
from src.ui.clock_widget.view.tick_events import TickEventSubject

if TYPE_CHECKING:
    from PySide6.QtGui import QPaintEvent


class ClockWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._tick_subject = TickEventSubject()
        self._tick_subject.subscribe(self)

        self._timer: QTimer = QTimer(self)
        self._timer.timeout.connect(self._tick_subject.notify)
        self._timer.start(15)

        self.controller = ClockController(self.get_current_time())
        self.painter = Painter()

    def on_tick(self) -> None:
        self.controller.update(self.get_current_time())
        self.update()

    def get_current_time(self) -> datetime:
        return datetime.now(UTC).astimezone()

    def reset(self) -> None:
        self.controller.reset(self.get_current_time())
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802, ARG002
        self.painter.init_painter(self)

        center, radius, font_size = self.painter.paint_clock_face(self.rect, self.palette)
        hands_position = convert_clock_pid_to_cartesian(self.controller.clock_angles, center, radius)

        self.painter.paint_hands(center, hands_position)
        self.painter.paint_current_time(self.get_current_time(), center, radius, font_size)

        self.painter.end_painter()
