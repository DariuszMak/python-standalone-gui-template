from __future__ import annotations

import math
from datetime import datetime, time, timedelta
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF

from src.ui.pyside_ui.clock_widget.model.data_types import ClockHands, HandsPosition

if TYPE_CHECKING:
    from src.ui.pyside_ui.clock_widget.model.clock_angles import ClockAngles


def polar_to_cartesian(center: QPointF, length: float, angle_radians: float) -> QPointF:
    x = center.x() + math.sin(angle_radians) * length
    y = center.y() - math.cos(angle_radians) * length
    return QPointF(x, y)


def convert_clock_pid_to_cartesian(clock_pid: ClockAngles, center: QPointF, radius: float) -> HandsPosition:
    second_polar, minute_polar, hour_polar = clock_pid.angles_in_radians()

    second_hand_cartesian = polar_to_cartesian(center, radius * 0.9, second_polar)
    minute_hand_cartesian = polar_to_cartesian(center, radius * 0.7, minute_polar)
    hour_hand_cartesian = polar_to_cartesian(center, radius * 0.5, hour_polar)

    return HandsPosition(second_hand_cartesian, minute_hand_cartesian, hour_hand_cartesian)


def calculate_clock_hands_angles(start_dt: datetime, duration: timedelta) -> ClockHands:
    midnight = datetime.combine(start_dt.date(), time(0, 0, 0), tzinfo=start_dt.tzinfo)
    start_ms = int((start_dt - midnight).total_seconds() * 1000)
    elapsed_ms = int(duration.total_seconds() * 1000)

    start_s = start_ms / 1000.0
    elapsed_s = elapsed_ms / 1000.0

    seconds_angle = start_s % 60.0 + elapsed_s
    minutes_angle = (start_s / 60.0) % 60.0 + elapsed_s / 60.0
    hours_angle = (start_s / 3600.0) % 12.0 + elapsed_s / 3600.0

    return ClockHands(second=float(seconds_angle), minute=float(minutes_angle), hour=float(hours_angle))


def format_datetime(datetime: datetime) -> str:
    formatted = f"{datetime.hour:02}:{datetime.minute:02}:{datetime.second:02}."
    formatted += f"{int(datetime.microsecond / 1000):03}"
    return formatted
