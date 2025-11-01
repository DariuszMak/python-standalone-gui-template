from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, datetime, time, timedelta

from PySide6.QtCore import QPointF, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget


@dataclass
class HandAngles:
    seconds: float
    minutes: float
    hours: float


def polar_to_cartesian(center: QPointF, length: float, angle_radians: float) -> QPointF:
    x = center.x() + math.sin(angle_radians) * length
    y = center.y() - math.cos(angle_radians) * length
    return QPointF(x, y)


def calculate_clock_angles(start_dt: datetime, duration: timedelta) -> HandAngles:
    midnight = datetime.combine(start_dt.date(), time(0, 0, 0), tzinfo=start_dt.tzinfo)
    start_ms = int((start_dt - midnight).total_seconds() * 1000)
    elapsed_ms = int(duration.total_seconds() * 1000)

    start_s = start_ms / 1000.0
    elapsed_s = elapsed_ms / 1000.0

    seconds_angle = start_s % 60.0 + elapsed_s
    minutes_angle = (start_s / 60.0) % 60.0 + elapsed_s / 60.0
    hours_angle = (start_s / 3600.0) % 12.0 + elapsed_s / 3600.0

    return HandAngles(seconds=float(seconds_angle), minutes=float(minutes_angle), hours=float(hours_angle))


class PID:
    def __init__(self, kp: float = 0.0, ki: float = 0.0, kd: float = 0.0) -> None:
        self.kp = float(kp)
        self.ki = float(ki)
        self.kd = float(kd)
        self.prev_error = 0.0
        self.integral = 0.0

    def update(self, error: float) -> float:
        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative

    def reset(self) -> None:
        self.prev_error = 0.0
        self.integral = 0.0


class ClockPID:
    def __init__(self, pid_second: float, pid_minute: float, pid_hour: float) -> None:
        self.pid_second = float(pid_second)
        self.pid_minute = float(pid_minute)
        self.pid_hour = float(pid_hour)

    def angles_in_radians(self) -> tuple[float, float, float]:
        second_angle = (self.pid_second / 60.0) * 2.0 * math.pi
        minute_angle = (self.pid_minute / 60.0) * 2.0 * math.pi
        hour_angle = (self.pid_hour / 12.0) * 2.0 * math.pi
        return second_angle, minute_angle, hour_angle


class ClockWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.start_time = datetime.now(UTC).astimezone()
        self.current_time = self.start_time
        self.pid_second = 0.0
        self.pid_minute = 0.0
        self.pid_hour = 0.0

        self.second_pid = PID(kp=0.15, ki=0.005, kd=0.005)
        self.minute_pid = PID(kp=0.08, ki=0.004, kd=0.004)
        self.hour_pid = PID(kp=0.08, ki=0.002, kd=0.002)

        self.setMinimumSize(300, 300)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_tick)
        self._timer.start(15)

    def _on_tick(self) -> None:
        self.current_time = datetime.now(UTC).astimezone()
        self.update_pid()
        self.update()

    def reset(self) -> None:
        self.start_time = datetime.now(UTC).astimezone()
        self.current_time = self.start_time
        self.pid_second = 0.0
        self.pid_minute = 0.0
        self.pid_hour = 0.0
        self.second_pid.reset()
        self.minute_pid.reset()
        self.hour_pid.reset()

    def update_pid(self) -> None:
        duration = self.current_time - self.start_time
        calculated = calculate_clock_angles(self.start_time, duration)

        pid_second_error = calculated.seconds - self.pid_second
        pid_minute_error = calculated.minutes - self.pid_minute
        pid_hour_error = calculated.hours - self.pid_hour

        self.pid_second += self.second_pid.update(pid_second_error)
        self.pid_minute += self.minute_pid.update(pid_minute_error)
        self.pid_hour += self.hour_pid.update(pid_hour_error)

    def paintEvent(self, event) -> None:  # noqa: N802, ARG002
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

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
            text_pos = polar_to_cartesian(center, radius - float(font_size)*2, angle)
            painter.setPen(QPen(QColor(255, 255, 255)))
            number = ((i + 11) % 12) + 1
            fm = painter.fontMetrics()
            w = fm.horizontalAdvance(str(number))
            h = fm.height()
            painter.drawText(QPointF(text_pos.x() - w / 2, text_pos.y() + h / 4), str(number))

        clock = ClockPID(self.pid_second, self.pid_minute, self.pid_hour)
        s_ang, m_ang, h_ang = clock.angles_in_radians()

        second_hand = polar_to_cartesian(center, radius * 0.9, s_ang)
        minute_hand = polar_to_cartesian(center, radius * 0.7, m_ang)
        hour_hand = polar_to_cartesian(center, radius * 0.5, h_ang)

        painter.setPen(QPen(QColor(255, 255, 255), 8.0))
        painter.drawLine(center, hour_hand)

        painter.setPen(QPen(QColor(200, 200, 200), 6.0))
        painter.drawLine(center, minute_hand)

        painter.setPen(QPen(QColor(255, 0, 0), 2.0))
        painter.drawLine(center, second_hand)

        dt = self.current_time
        formatted = f"{dt.hour:02}:{dt.minute:02}:{dt.second:02}.{int(dt.microsecond / 1000):03}"
        painter.setPen(QPen(QColor(150, 255, 190)))
        painter.setFont(QFont("Consolas", font_size))
        fm = painter.fontMetrics()
        w = fm.horizontalAdvance(formatted)
        painter.drawText(QPointF(center.x() - w / 2, center.y() + radius / 2), formatted)
