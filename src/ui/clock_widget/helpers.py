from __future__ import annotations

import math
from datetime import datetime, time, timedelta

from PySide6.QtCore import QPointF

from src.ui.clock_widget.data_types import ClockHands


def polar_to_cartesian(center: QPointF, length: float, angle_radians: float) -> QPointF:
    x = center.x() + math.sin(angle_radians) * length
    y = center.y() - math.cos(angle_radians) * length
    return QPointF(x, y)


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
