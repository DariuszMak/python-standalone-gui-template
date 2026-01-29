from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget

from src.ui.pyside_ui.clock_widget.controller.clock_controller import ClockController
from src.ui.pyside_ui.clock_widget.view.helpers import convert_clock_pid_to_cartesian
from src.ui.pyside_ui.clock_widget.view.painter import Painter
from src.ui.pyside_ui.clock_widget.view.tick_events import TickEventSubject

if TYPE_CHECKING:
    from PySide6.QtGui import QPaintEvent


class ClockWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.duration = 15

        self._tick_subject = TickEventSubject()
        self._tick_subject.subscribe(self)

        self._timer: QTimer = QTimer(self)
        self._timer.timeout.connect(self._tick_subject.notify)
        self._timer.start(self.duration)

        self.current_datetime = datetime(1970, 1, 1, tzinfo=UTC)
        self.controller = ClockController(self.current_datetime)

    def on_tick(self) -> None:
        self.current_datetime = self.current_datetime + timedelta(milliseconds=self.duration)

        self.controller.update(self.current_datetime)
        self.update()

    def set_current_datetime(self, datetime: datetime) -> None:
        self.current_datetime = datetime
        self.reset()

    def reset(self) -> None:
        self.controller.reset(self.current_datetime)
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802, ARG002
        painter = Painter(self)

        center, radius, font_size = painter.paint_clock_face(self.rect, self.palette)
        hands_position = convert_clock_pid_to_cartesian(self.controller.clock_angles, center, radius)

        painter.paint_hands(center, hands_position)
        painter.paint_current_time(self.current_datetime, center, radius, font_size)
