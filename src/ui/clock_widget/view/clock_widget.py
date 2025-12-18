from __future__ import annotations

import math
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import QWidget

from src.ui.clock_widget.controller.clock_controller import ClockController
from src.ui.clock_widget.model.clock_angles import ClockAngles
from src.ui.clock_widget.view.helpers import convert_clock_pid_to_cartesian, format_datetime, polar_to_cartesian
from src.ui.clock_widget.view.tick_events import TickEventSubject

if TYPE_CHECKING:
    from src.ui.clock_widget.model.data_types import HandsPosition


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

    def paint_clock_face(self, painter: QPainter) -> tuple[QPointF, float, int]:
        rect = self.rect()
        size = min(rect.width(), rect.height())
        center = QPointF(rect.center())
        radius = size * 0.4

        painter.fillRect(rect, self.palette().window())

        pen = QPen(self.palette().text().color())
        pen.setWidthF(2.0)
        painter.setPen(pen)
        painter.drawEllipse(center, radius, radius)

        for hour in range(60):
            angle = (hour / 60.0) * 2.0 * math.pi
            outer = polar_to_cartesian(center, radius, angle)
            inner = polar_to_cartesian(center, radius - (10.0 if hour % 5 == 0 else 5.0), angle)
            pen = QPen(QColor(200, 200, 200))
            pen.setWidthF(3.0 if hour % 5 == 0 else 1.5)
            painter.setPen(pen)
            painter.drawLine(inner, outer)

        font_size = max(8, int(radius * 0.09))

        painter.setFont(QFont("Arial", font_size))
        for hour in range(12):
            angle = (hour / 12.0) * 2.0 * math.pi
            text_position = polar_to_cartesian(center, radius - float(font_size) * 2, angle)
            painter.setPen(QPen(QColor(255, 255, 255)))
            friendly_presented_hour = ((hour + 11) % 12) + 1
            font_metrics = painter.fontMetrics()
            width = font_metrics.horizontalAdvance(str(friendly_presented_hour))
            height = font_metrics.height()
            painter.drawText(
                QPointF(text_position.x() - width / 2, text_position.y() + height / 4), str(friendly_presented_hour)
            )
        return center, radius, font_size

    def paint_hands(self, painter: QPainter, center: QPointF, hands_position: HandsPosition) -> None:
        painter.setPen(QPen(QColor(255, 255, 255), 8.0))
        painter.drawLine(center, hands_position.hour)

        painter.setPen(QPen(QColor(200, 200, 200), 6.0))
        painter.drawLine(center, hands_position.minute)

        painter.setPen(QPen(QColor(255, 0, 0), 2.0))
        painter.drawLine(center, hands_position.second)

    def paint_current_time(self, painter: QPainter, center: QPointF, radius: float, font_size: int) -> None:
        formatted = format_datetime(self.current_time)
        painter.setPen(QPen(QColor(150, 255, 190)))
        painter.setFont(QFont("Consolas", font_size))
        font_metrics = painter.fontMetrics()
        width = font_metrics.horizontalAdvance(formatted)
        painter.drawText(QPointF(center.x() - width / 2, center.y() + radius / 2), formatted)

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802, ARG002
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center, radius, font_size = self.paint_clock_face(painter)
        self.controller.clock_angles = ClockAngles(
            self.controller.clock_angles.clock_hands_angles.second,
            self.controller.clock_angles.clock_hands_angles.minute,
            self.controller.clock_angles.clock_hands_angles.hour,
        )

        hands_position = convert_clock_pid_to_cartesian(self.controller.clock_angles, center, radius)

        self.paint_hands(painter, center, hands_position)

        self.paint_current_time(painter, center, radius, font_size)
