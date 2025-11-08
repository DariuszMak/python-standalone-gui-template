from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, datetime, time, timedelta

from PySide6.QtCore import QPointF, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import QWidget

from src.ui.clock_widget.data_types import ClockHands



class ClockPID:
    clock_hands: ClockHands

    def __init__(self, pid_second: float, pid_minute: float, pid_hour: float) -> None:
        self.clock_hands = ClockHands(float(pid_second), float(pid_minute), float(pid_hour))

    def reset(self) -> None:
        self.clock_hands.second = 0.0
        self.clock_hands.minute = 0.0
        self.clock_hands.hour = 0.0

    def angles_in_radians(self) -> tuple[float, float, float]:
        second_angle = (self.clock_hands.second / 60.0) * 2.0 * math.pi
        minute_angle = (self.clock_hands.minute / 60.0) * 2.0 * math.pi
        hour_angle = (self.clock_hands.hour / 12.0) * 2.0 * math.pi
        return second_angle, minute_angle, hour_angle