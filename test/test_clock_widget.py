import math
from datetime import UTC, datetime, timedelta

import pytest
from PySide6.QtCore import QPointF

from src.ui.clock_widget import PID, ClockPID, calculate_clock_angles, polar_to_cartesian


def approx_eq(a: float, b: float, epsilon: float = 1e-10) -> bool:
    return abs(a - b) < epsilon


# ---------------- Clock angle tests ----------------


def test_midnight_clock_angles():
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(0)
    angles = calculate_clock_angles(dt, duration)
    assert angles.seconds == 0.0
    assert angles.minutes == 0.0
    assert angles.hours == 0.0


def test_noon_clock_angles():
    dt = datetime(2025, 4, 27, 12, 0, 0, tzinfo=UTC)
    duration = timedelta(0)
    angles = calculate_clock_angles(dt, duration)
    assert angles.seconds == 0.0
    assert angles.minutes == 0.0
    assert angles.hours == 0.0


def test_noon_clock_angles_from_milliseconds():
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=12 * 60 * 60 * 1000)
    angles = calculate_clock_angles(dt, duration)
    assert angles.seconds == pytest.approx(43200.0)
    assert angles.minutes == pytest.approx(720.0)
    assert angles.hours == pytest.approx(12.0)


def test_maximum_clock_angles():
    dt = datetime(2025, 4, 27, 23, 59, 59, tzinfo=UTC)
    duration = timedelta(0)
    angles = calculate_clock_angles(dt, duration)
    assert angles.seconds == pytest.approx(59.0)
    assert angles.minutes == pytest.approx(59.983334, rel=1e-6)
    assert angles.hours == pytest.approx(11.9997225, rel=1e-6)


def test_maximum_clock_angles_from_milliseconds():
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=(23 * 60 * 60 * 1000 + 59 * 60 * 1000 + 59 * 1000 + 999))
    angles = calculate_clock_angles(dt, duration)
    assert angles.seconds == pytest.approx(86400.0)
    assert angles.minutes == pytest.approx(1440.0)
    assert angles.hours == pytest.approx(24.0)


def test_half_past_three_clock_angles():
    dt = datetime(2025, 4, 27, 3, 30, 0, tzinfo=UTC)
    duration = timedelta(0)
    angles = calculate_clock_angles(dt, duration)
    assert angles.seconds == pytest.approx(0.0)
    assert angles.minutes == pytest.approx(30.0)
    assert angles.hours == pytest.approx(3.5)


def test_half_past_three_clock_angles_from_milliseconds():
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=(3 * 60 * 60 * 1000 + 30 * 60 * 1000))
    angles = calculate_clock_angles(dt, duration)
    assert angles.seconds == pytest.approx(12600.0)
    assert angles.minutes == pytest.approx(210.0)
    assert angles.hours == pytest.approx(3.5)


def test_circled_clock_angles():
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=(33 * 60 * 60 * 1000 + 65 * 60 * 1000 + 61 * 1000 + 2))
    angles = calculate_clock_angles(dt, duration)
    assert angles.seconds == pytest.approx(122761.0)
    assert angles.minutes == pytest.approx(2046.0167, rel=1e-5)
    assert angles.hours == pytest.approx(34.100277, rel=1e-5)


def test_circled_clock_angles_after_month():
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=(37 * 24 * 60 * 60 * 1000 + 65 * 60 * 1000 + 61 * 1000 + 2))
    angles = calculate_clock_angles(dt, duration)
    assert angles.seconds == pytest.approx(3200761.0)
    assert angles.minutes == pytest.approx(53346.016, rel=1e-5)
    assert angles.hours == pytest.approx(889.1003, rel=1e-5)


# ---------------- PID tests ----------------


def test_pid_update():
    pid = PID(kp=1.0, ki=0.1, kd=0.5)
    output1 = pid.update(1.0)
    assert output1 == pytest.approx(1.0 + 0.1 + 0.5)

    output2 = pid.update(0.5)
    expected = 0.5 * pid.kp + (1.0 + 0.5) * pid.ki + (0.5 - 1.0) * pid.kd
    assert output2 == pytest.approx(expected)


def test_pid_reset():
    pid = PID(kp=1.0, ki=0.1, kd=0.5)
    pid.update(1.0)
    pid.update(0.5)
    assert pid.integral != 0.0
    assert pid.prev_error != 0.0

    pid.reset()
    assert pid.integral == 0.0
    assert pid.prev_error == 0.0


# ---------------- ClockPID tests ----------------


def test_clock_pid_angles_in_radians():
    c = ClockPID(pid_second=15.0, pid_minute=30.0, pid_hour=6.0)
    s_rad, m_rad, h_rad = c.angles_in_radians()
    assert approx_eq(s_rad, math.pi / 2.0)
    assert approx_eq(m_rad, math.pi)
    assert approx_eq(h_rad, math.pi)


def test_angles_at_zero():
    c = ClockPID(0.0, 0.0, 0.0)
    s, m, h = c.angles_in_radians()
    assert approx_eq(s, 0.0)
    assert approx_eq(m, 0.0)
    assert approx_eq(h, 0.0)


def test_angles_at_halfway():
    c = ClockPID(30.0, 30.0, 6.0)
    s, m, h = c.angles_in_radians()
    assert approx_eq(s, math.pi)
    assert approx_eq(m, math.pi)
    assert approx_eq(h, math.pi)


def test_angles_at_full():
    c = ClockPID(60.0, 60.0, 12.0)
    s, m, h = c.angles_in_radians()
    assert approx_eq(s, 2.0 * math.pi)
    assert approx_eq(m, 2.0 * math.pi)
    assert approx_eq(h, 2.0 * math.pi)


def test_quarter_angles():
    c = ClockPID(15.0, 15.0, 3.0)
    s, m, h = c.angles_in_radians()
    assert approx_eq(s, 0.25 * 2.0 * math.pi)
    assert approx_eq(m, 0.25 * 2.0 * math.pi)
    assert approx_eq(h, 0.25 * 2.0 * math.pi)


# ---------------- polar_to_cartesian tests ----------------


def test_polar_to_cartesian_zero_angle():
    center = QPointF(100.0, 100.0)
    res = polar_to_cartesian(center, 50.0, 0.0)
    assert abs(res.x() - center.x()) < 1e-10
    assert abs(res.y() - (center.y() - 50.0)) < 1e-10


def test_polar_to_cartesian_quarter_angle():
    center = QPointF(0.0, 0.0)
    res = polar_to_cartesian(center, 1.0, math.pi / 2.0)
    assert abs(res.x() - 1.0) < 1e-10
    assert abs(res.y() - 0.0) < 1e-10


def test_polar_to_cartesian_90_degrees():
    length = 10.0
    angle = math.pi / 2.0
    res = polar_to_cartesian(QPointF(0.0, 0.0), length, angle)
    assert abs(res.x() - 10.0) < 1e-5
    assert abs(res.y() - 0.0) < 1e-5


def test_polar_to_cartesian_180_degrees():
    length = 10.0
    angle = math.pi
    res = polar_to_cartesian(QPointF(0.0, 0.0), length, angle)
    assert abs(res.x() - 0.0) < 1e-5
    assert abs(res.y() - 10.0) < 1e-5
