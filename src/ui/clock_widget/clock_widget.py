from __future__ import annotations

import math
from datetime import UTC, datetime

from PySide6.QtCore import QPointF, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import QWidget

from src.ui.clock_widget.clock_pid import ClockPID
from src.ui.clock_widget.data_types import ClockHands, HandsPosition
from src.ui.clock_widget.helpers import calculate_clock_hands_angles, polar_to_cartesian
from src.ui.clock_widget.strategies.pid_strategy import PIDMovementStrategy


class ClockWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.start_time = datetime.now(UTC).astimezone()
        self.current_time = self.start_time
        self.clock_pid = ClockPID(0.0, 0.0, 0.0)

        self.second_strategy = PIDMovementStrategy(0.15, 0.005, 0.005)
        self.minute_strategy = PIDMovementStrategy(0.08, 0.004, 0.004)
        self.hour_strategy = PIDMovementStrategy(0.08, 0.002, 0.002)

        self.setMinimumSize(300, 300)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_tick)
        self._timer.start(15)

    def _on_tick(self) -> None:
        self.current_time = datetime.now(UTC).astimezone()
        self.update_clock_pid()
        self.update()

    def reset(self) -> None:
        self.start_time = datetime.now(UTC).astimezone()
        self.current_time = self.start_time
        self.clock_pid.reset()

        for strat in (self.second_strategy, self.minute_strategy, self.hour_strategy):
            strat.reset()

    def update_clock_pid(self) -> None:
        duration = self.current_time - self.start_time
        calculated_clock_hands_angles: ClockHands = calculate_clock_hands_angles(self.start_time, duration)

        self.clock_pid.clock_hands.second = self.second_strategy.update(
            self.clock_pid.clock_hands.second, calculated_clock_hands_angles.second
        )
        self.clock_pid.clock_hands.minute = self.minute_strategy.update(
            self.clock_pid.clock_hands.minute, calculated_clock_hands_angles.minute
        )
        self.clock_pid.clock_hands.hour = self.hour_strategy.update(
            self.clock_pid.clock_hands.hour, calculated_clock_hands_angles.hour
        )

    def convert_clock_pid_to_cartesian(self, clock_pid: ClockPID, center: QPointF, radius: float) -> HandsPosition:
        second_polar, minute_polar, hour_polar = clock_pid.angles_in_radians()

        second_hand_cartesian = polar_to_cartesian(center, radius * 0.9, second_polar)
        minute_hand_cartesian = polar_to_cartesian(center, radius * 0.7, minute_polar)
        hour_hand_cartesian = polar_to_cartesian(center, radius * 0.5, hour_polar)

        return HandsPosition(second_hand_cartesian, minute_hand_cartesian, hour_hand_cartesian)

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

        for i in range(60):
            angle = (i / 60.0) * 2.0 * math.pi
            outer = polar_to_cartesian(center, radius, angle)
            inner = polar_to_cartesian(center, radius - (10.0 if i % 5 == 0 else 5.0), angle)
            pen = QPen(QColor(200, 200, 200))
            pen.setWidthF(3.0 if i % 5 == 0 else 1.5)
            painter.setPen(pen)
            painter.drawLine(inner, outer)

        font_size = max(8, int(radius * 0.09))

        painter.setFont(QFont("Arial", font_size))
        for i in range(12):
            angle = (i / 12.0) * 2.0 * math.pi
            text_pos = polar_to_cartesian(center, radius - float(font_size) * 2, angle)
            painter.setPen(QPen(QColor(255, 255, 255)))
            number = ((i + 11) % 12) + 1
            fm = painter.fontMetrics()
            w = fm.horizontalAdvance(str(number))
            h = fm.height()
            painter.drawText(QPointF(text_pos.x() - w / 2, text_pos.y() + h / 4), str(number))
        return center, radius, font_size

    def paint_hands(self, painter: QPainter, center: QPointF, hands_position: HandsPosition) -> None:
        painter.setPen(QPen(QColor(255, 255, 255), 8.0))
        painter.drawLine(center, hands_position.hour)

        painter.setPen(QPen(QColor(200, 200, 200), 6.0))
        painter.drawLine(center, hands_position.minute)

        painter.setPen(QPen(QColor(255, 0, 0), 2.0))
        painter.drawLine(center, hands_position.second)

    def paint_current_time(self, painter: QPainter, center: QPointF, radius: float, font_size: int) -> None:
        dt = self.current_time
        formatted = f"{dt.hour:02}:{dt.minute:02}:{dt.second:02}.{int(dt.microsecond / 1000):03}"
        painter.setPen(QPen(QColor(150, 255, 190)))
        painter.setFont(QFont("Consolas", font_size))
        fm = painter.fontMetrics()
        w = fm.horizontalAdvance(formatted)
        painter.drawText(QPointF(center.x() - w / 2, center.y() + radius / 2), formatted)

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802, ARG002
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center, radius, font_size = self.paint_clock_face(painter)
        self.clock_pid = ClockPID(
            self.clock_pid.clock_hands.second, self.clock_pid.clock_hands.minute, self.clock_pid.clock_hands.hour
        )

        hands_position = self.convert_clock_pid_to_cartesian(self.clock_pid, center, radius)

        self.paint_hands(painter, center, hands_position)

        self.paint_current_time(painter, center, radius, font_size)
