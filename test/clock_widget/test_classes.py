import math

import pytest

from src.pyside_ui.clock_widget.model.clock_angles import ClockAngles
from src.pyside_ui.clock_widget.model.pid import PID


def approx_eq(a: float, b: float, epsilon: float = 1e-10) -> bool:
    return abs(a - b) < epsilon


def test_pid_update() -> None:
    pid = PID(kp=1.0, ki=0.1, kd=0.5)
    output1 = pid.update(1.0)
    assert output1 == pytest.approx(1.0 + 0.1 + 0.5)

    output2 = pid.update(0.5)
    expected = 0.5 * pid.kp + (1.0 + 0.5) * pid.ki + (0.5 - 1.0) * pid.kd
    assert output2 == pytest.approx(expected)


def test_pid_reset() -> None:
    pid = PID(kp=1.0, ki=0.1, kd=0.5)
    pid.update(1.0)
    pid.update(0.5)
    assert pid.integral != 0.0
    assert pid.prev_error != 0.0

    pid.reset()
    assert pid.integral == 0.0
    assert pid.prev_error == 0.0


def test_clock_angles_reset() -> None:
    pid = ClockAngles(10.5, 20.3, 5.7)
    assert pid.clock_hands_angles.second == 10.5
    assert pid.clock_hands_angles.minute == 20.3
    assert pid.clock_hands_angles.hour == 5.7

    pid.reset()

    assert pid.clock_hands_angles.second == 0.0
    assert pid.clock_hands_angles.minute == 0.0
    assert pid.clock_hands_angles.hour == 0.0


def test_clock_angles_angles_in_radians() -> None:
    c = ClockAngles(pid_second=15.0, pid_minute=30.0, pid_hour=6.0)
    s_rad, m_rad, h_rad = c.angles_in_radians()
    assert approx_eq(s_rad, math.pi / 2.0)
    assert approx_eq(m_rad, math.pi)
    assert approx_eq(h_rad, math.pi)


def test_clock_angles_angles_at_zero() -> None:
    c = ClockAngles(0.0, 0.0, 0.0)
    s, m, h = c.angles_in_radians()
    assert approx_eq(s, 0.0)
    assert approx_eq(m, 0.0)
    assert approx_eq(h, 0.0)


def test_clock_angles_angles_at_halfway() -> None:
    c = ClockAngles(30.0, 30.0, 6.0)
    s, m, h = c.angles_in_radians()
    assert approx_eq(s, math.pi)
    assert approx_eq(m, math.pi)
    assert approx_eq(h, math.pi)


def test_clock_angles_angles_at_full() -> None:
    c = ClockAngles(60.0, 60.0, 12.0)
    s, m, h = c.angles_in_radians()
    assert approx_eq(s, 2.0 * math.pi)
    assert approx_eq(m, 2.0 * math.pi)
    assert approx_eq(h, 2.0 * math.pi)


def test_clock_angles_quarter_angles() -> None:
    c = ClockAngles(15.0, 15.0, 3.0)
    s, m, h = c.angles_in_radians()
    assert approx_eq(s, 0.25 * 2.0 * math.pi)
    assert approx_eq(m, 0.25 * 2.0 * math.pi)
    assert approx_eq(h, 0.25 * 2.0 * math.pi)
