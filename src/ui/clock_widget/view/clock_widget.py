from __future__ import annotations

from datetime import UTC, datetime

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter, QPaintEvent
from PySide6.QtWidgets import QWidget

from src.ui.clock_widget.controller.clock_controller import ClockController
from src.ui.clock_widget.model.clock_angles import ClockAngles
from src.ui.clock_widget.view.helpers import convert_clock_pid_to_cartesian
from src.ui.clock_widget.view.painter import paint_clock_face, paint_current_time, paint_hands
from src.ui.clock_widget.view.tick_events import TickEventSubject


class ClockWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._tick_subject = TickEventSubject()
        self._tick_subject.subscribe(self)

        self._timer: QTimer = QTimer(self)
        self._timer.timeout.connect(self._tick_subject.notify)
        self._timer.start(15)

        self.controller = ClockController(datetime.now(UTC))

    def on_tick(self) -> None:
        self.current_time = datetime.now(UTC).astimezone()
        self.controller.update(self.current_time)
        self.update()

    def reset(self) -> None:
        self.controller.reset(datetime.now(UTC).astimezone())
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802, ARG002
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center, radius, font_size = paint_clock_face(painter, self.rect, self.palette)
        self.controller.clock_angles = ClockAngles(
            self.controller.clock_angles.clock_hands_angles.second,
            self.controller.clock_angles.clock_hands_angles.minute,
            self.controller.clock_angles.clock_hands_angles.hour,
        )

        hands_position = convert_clock_pid_to_cartesian(self.controller.clock_angles, center, radius)

        paint_hands(painter, center, hands_position)

        paint_current_time(self.current_time, painter, center, radius, font_size)
