from __future__ import annotations

import math

from src.ui.clock_widget.model.data_types import ClockHands


class ClockAngles:
    clock_hands_angles: ClockHands

    def __init__(self, pid_second: float, pid_minute: float, pid_hour: float) -> None:
        self.clock_hands_angles = ClockHands(float(pid_second), float(pid_minute), float(pid_hour))

    def clock_angles_reset(self) -> None:
        self.clock_hands_angles.second = 0.0
        self.clock_hands_angles.minute = 0.0
        self.clock_hands_angles.hour = 0.0

    def angles_in_radians(self) -> tuple[float, float, float]:
        second_angle = (self.clock_hands_angles.second / 60.0) * 2.0 * math.pi
        minute_angle = (self.clock_hands_angles.minute / 60.0) * 2.0 * math.pi
        hour_angle = (self.clock_hands_angles.hour / 12.0) * 2.0 * math.pi
        return second_angle, minute_angle, hour_angle
