import math

from src.ui.shared.model.data_types import ClockHands


def clock_hands_in_radians(hands: ClockHands) -> tuple[float, float, float]:
    second_angle = (hands.second / 60.0) * 2.0 * math.pi
    minute_angle = (hands.minute / 60.0) * 2.0 * math.pi
    hour_angle = (hands.hour / 12.0) * 2.0 * math.pi
    return second_angle, minute_angle, hour_angle
