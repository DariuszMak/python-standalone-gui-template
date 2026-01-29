import math
from datetime import UTC, datetime, timedelta

import pytest
from PySide6.QtCore import QPointF

from src.pyside_ui.clock_widget.model.clock_angles import ClockAngles
from src.pyside_ui.clock_widget.view.helpers import (
    calculate_clock_hands_angles,
    convert_clock_pid_to_cartesian,
    format_datetime,
    polar_to_cartesian,
)


def test_polar_to_cartesian_zero_angle() -> None:
    center = QPointF(100.0, 100.0)
    res = polar_to_cartesian(center, 50.0, 0.0)
    assert abs(res.x() - center.x()) < 1e-10
    assert abs(res.y() - (center.y() - 50.0)) < 1e-10


def test_polar_to_cartesian_quarter_angle() -> None:
    center = QPointF(0.0, 0.0)
    res = polar_to_cartesian(center, 1.0, math.pi / 2.0)
    assert abs(res.x() - 1.0) < 1e-10
    assert abs(res.y() - 0.0) < 1e-10


def test_polar_to_cartesian_90_degrees() -> None:
    length = 10.0
    angle = math.pi / 2.0
    res = polar_to_cartesian(QPointF(0.0, 0.0), length, angle)
    assert abs(res.x() - 10.0) < 1e-5
    assert abs(res.y() - 0.0) < 1e-5


def test_polar_to_cartesian_180_degrees() -> None:
    length = 10.0
    angle = math.pi
    res = polar_to_cartesian(QPointF(0.0, 0.0), length, angle)
    assert abs(res.x() - 0.0) < 1e-5
    assert abs(res.y() - 10.0) < 1e-5


def test_midnight_clock_hands_angles() -> None:
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(0)
    angles = calculate_clock_hands_angles(dt, duration)
    assert angles.second == 0.0
    assert angles.minute == 0.0
    assert angles.hour == 0.0


def test_noon_clock_hands_angles() -> None:
    dt = datetime(2025, 4, 27, 12, 0, 0, tzinfo=UTC)
    duration = timedelta(0)
    angles = calculate_clock_hands_angles(dt, duration)
    assert angles.second == 0.0
    assert angles.minute == 0.0
    assert angles.hour == 0.0


def test_noon_clock_hands_angles_from_milliseconds() -> None:
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=12 * 60 * 60 * 1000)
    angles = calculate_clock_hands_angles(dt, duration)
    assert angles.second == pytest.approx(43200.0)
    assert angles.minute == pytest.approx(720.0)
    assert angles.hour == pytest.approx(12.0)


def test_maximum_clock_hands_angles() -> None:
    dt = datetime(2025, 4, 27, 23, 59, 59, tzinfo=UTC)
    duration = timedelta(0)
    angles = calculate_clock_hands_angles(dt, duration)
    assert angles.second == pytest.approx(59.0)
    assert angles.minute == pytest.approx(59.983334, rel=1e-6)
    assert angles.hour == pytest.approx(11.9997225, rel=1e-6)


def test_maximum_clock_hands_angles_from_milliseconds() -> None:
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=(23 * 60 * 60 * 1000 + 59 * 60 * 1000 + 59 * 1000 + 999))
    angles = calculate_clock_hands_angles(dt, duration)
    assert angles.second == pytest.approx(86400.0)
    assert angles.minute == pytest.approx(1440.0)
    assert angles.hour == pytest.approx(24.0)


def test_half_past_three_clock_hands_angles() -> None:
    dt = datetime(2025, 4, 27, 3, 30, 0, tzinfo=UTC)
    duration = timedelta(0)
    angles = calculate_clock_hands_angles(dt, duration)
    assert angles.second == pytest.approx(0.0)
    assert angles.minute == pytest.approx(30.0)
    assert angles.hour == pytest.approx(3.5)


def test_half_past_three_clock_hands_angles_from_milliseconds() -> None:
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=(3 * 60 * 60 * 1000 + 30 * 60 * 1000))
    angles = calculate_clock_hands_angles(dt, duration)
    assert angles.second == pytest.approx(12600.0)
    assert angles.minute == pytest.approx(210.0)
    assert angles.hour == pytest.approx(3.5)


def test_circled_clock_hands_angles() -> None:
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=(33 * 60 * 60 * 1000 + 65 * 60 * 1000 + 61 * 1000 + 2))
    angles = calculate_clock_hands_angles(dt, duration)
    assert angles.second == pytest.approx(122761.0)
    assert angles.minute == pytest.approx(2046.0167, rel=1e-5)
    assert angles.hour == pytest.approx(34.100277, rel=1e-5)


def test_circled_clock_hands_angles_after_month() -> None:
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=(37 * 24 * 60 * 60 * 1000 + 65 * 60 * 1000 + 61 * 1000 + 2))
    angles = calculate_clock_hands_angles(dt, duration)
    assert angles.second == pytest.approx(3200761.0)
    assert angles.minute == pytest.approx(53346.016, rel=1e-5)
    assert angles.hour == pytest.approx(889.1003, rel=1e-5)


def test_format_datetime() -> None:
    dt = datetime(2024, 1, 2, 3, 4, 5, 678901, tzinfo=UTC)
    result = format_datetime(dt)
    assert result == "03:04:05.678"


def test_convert_clock_pid_to_cartesian() -> None:
    center = QPointF(100.0, 100.0)
    radius = 50.0

    clock_angles = ClockAngles(
        pid_second=0.0,
        pid_minute=15.0,
        pid_hour=6.0,
    )

    hands = convert_clock_pid_to_cartesian(clock_angles, center, radius)

    assert hands.second == QPointF(100.0, 100.0 - radius * 0.9)
    assert hands.minute == QPointF(100.0 + radius * 0.7, 100.0)
    assert hands.hour == QPointF(100.0, 100.0 + radius * 0.5)
