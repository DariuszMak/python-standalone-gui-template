"""Tests for view/helpers.py.

All calls to ``calculate_clock_hands_angles`` that care about a specific
wall-clock time now pass ``display_tz=timezone.utc`` so that the results are
deterministic regardless of the machine's local timezone.

The new tests at the bottom (``test_timezone_*``) specifically exercise the
bug that caused the clock to run 1 hour behind on UTC+N systems.
"""

import math
from datetime import UTC, datetime, timedelta, timezone

import pytest
from PySide6.QtCore import QPointF

from src.ui.pyside_ui.clock_widget.model.data_types import ClockHands
from src.ui.pyside_ui.clock_widget.view.helpers import (
    calculate_clock_hands_angles,
    convert_clock_pid_to_cartesian,
    format_datetime,
    polar_to_cartesian,
)

# ---------------------------------------------------------------------------
# polar_to_cartesian
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# calculate_clock_hands_angles — existing behaviour (display_tz=UTC keeps
# these deterministic on every machine)
# ---------------------------------------------------------------------------


def test_midnight_clock_hands_angles() -> None:
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(0)
    angles = calculate_clock_hands_angles(dt, duration, display_tz=UTC)
    assert angles.second == 0.0
    assert angles.minute == 0.0
    assert angles.hour == 0.0


def test_noon_clock_hands_angles() -> None:
    dt = datetime(2025, 4, 27, 12, 0, 0, tzinfo=UTC)
    duration = timedelta(0)
    angles = calculate_clock_hands_angles(dt, duration, display_tz=UTC)
    assert angles.second == 0.0
    assert angles.minute == 0.0
    assert angles.hour == 0.0


def test_noon_clock_hands_angles_from_milliseconds() -> None:
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=12 * 60 * 60 * 1000)
    angles = calculate_clock_hands_angles(dt, duration, display_tz=UTC)
    assert angles.second == pytest.approx(43200.0)
    assert angles.minute == pytest.approx(720.0)
    assert angles.hour == pytest.approx(12.0)


def test_maximum_clock_hands_angles() -> None:
    dt = datetime(2025, 4, 27, 23, 59, 59, tzinfo=UTC)
    duration = timedelta(0)
    angles = calculate_clock_hands_angles(dt, duration, display_tz=UTC)
    assert angles.second == pytest.approx(59.0)
    assert angles.minute == pytest.approx(59.983334, rel=1e-6)
    assert angles.hour == pytest.approx(11.9997225, rel=1e-6)


def test_maximum_clock_hands_angles_from_milliseconds() -> None:
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=(23 * 60 * 60 * 1000 + 59 * 60 * 1000 + 59 * 1000 + 999))
    angles = calculate_clock_hands_angles(dt, duration, display_tz=UTC)
    assert angles.second == pytest.approx(86400.0)
    assert angles.minute == pytest.approx(1440.0)
    assert angles.hour == pytest.approx(24.0)


def test_half_past_three_clock_hands_angles() -> None:
    dt = datetime(2025, 4, 27, 3, 30, 0, tzinfo=UTC)
    duration = timedelta(0)
    angles = calculate_clock_hands_angles(dt, duration, display_tz=UTC)
    assert angles.second == pytest.approx(0.0)
    assert angles.minute == pytest.approx(30.0)
    assert angles.hour == pytest.approx(3.5)


def test_half_past_three_clock_hands_angles_from_milliseconds() -> None:
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=(3 * 60 * 60 * 1000 + 30 * 60 * 1000))
    angles = calculate_clock_hands_angles(dt, duration, display_tz=UTC)
    assert angles.second == pytest.approx(12600.0)
    assert angles.minute == pytest.approx(210.0)
    assert angles.hour == pytest.approx(3.5)


def test_circled_clock_hands_angles() -> None:
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=(33 * 60 * 60 * 1000 + 65 * 60 * 1000 + 61 * 1000 + 2))
    angles = calculate_clock_hands_angles(dt, duration, display_tz=UTC)
    assert angles.second == pytest.approx(122761.0)
    assert angles.minute == pytest.approx(2046.0167, rel=1e-5)
    assert angles.hour == pytest.approx(34.100277, rel=1e-5)


def test_circled_clock_hands_angles_after_month() -> None:
    dt = datetime(2025, 4, 27, 0, 0, 0, tzinfo=UTC)
    duration = timedelta(milliseconds=(37 * 24 * 60 * 60 * 1000 + 65 * 60 * 1000 + 61 * 1000 + 2))
    angles = calculate_clock_hands_angles(dt, duration, display_tz=UTC)
    assert angles.second == pytest.approx(3200761.0)
    assert angles.minute == pytest.approx(53346.016, rel=1e-5)
    assert angles.hour == pytest.approx(889.1003, rel=1e-5)


def test_clock_hands_angles_from_epoch_to_recent_date() -> None:
    epoch = datetime(1970, 1, 1, 0, 0, 0, tzinfo=UTC)
    recent = datetime(2025, 4, 27, 15, 30, 45, tzinfo=UTC)

    duration = recent - epoch

    angles = calculate_clock_hands_angles(epoch, duration, display_tz=UTC)

    total_seconds = duration.total_seconds()
    total_minutes = total_seconds / 60.0
    total_hours = total_seconds / 3600.0

    assert angles.second == pytest.approx(total_seconds, rel=1e-9)
    assert angles.minute == pytest.approx(total_minutes, rel=1e-9)
    assert angles.hour == pytest.approx(total_hours, rel=1e-9)

    assert angles.second > 60.0 * 1_000_000
    assert angles.minute > 60.0 * 10_000
    assert angles.hour > 12.0 * 1_000


# ---------------------------------------------------------------------------
# calculate_clock_hands_angles — timezone bug regression tests
#
# These tests guard against the bug where the clock displayed UTC time
# instead of local wall-clock time, causing it to appear N hours behind on
# UTC+N systems (e.g. 1 hour behind on Polish machines, UTC+1).
# ---------------------------------------------------------------------------


def test_timezone_utc_plus1_shows_local_hour() -> None:
    """UTC 14:30 in UTC+1 should display as 15:30 (hour angle ≈ 3.5)."""
    tz_plus1 = timezone(timedelta(hours=1))
    # Express the same instant as UTC+1 local time
    local_dt = datetime(2025, 4, 27, 15, 30, 0, tzinfo=tz_plus1)

    angles = calculate_clock_hands_angles(local_dt, timedelta(0), display_tz=tz_plus1)

    assert angles.second == pytest.approx(0.0)
    assert angles.minute == pytest.approx(30.0)
    assert angles.hour == pytest.approx(3.5)  # 15 % 12 = 3, plus 0.5 for 30 min


def test_timezone_utc_and_local_same_instant_differ_by_offset() -> None:
    """The same instant expressed in UTC vs UTC+1 should differ by exactly 1 h."""
    tz_plus1 = timezone(timedelta(hours=1))
    utc_dt = datetime(2025, 4, 27, 14, 30, 0, tzinfo=UTC)
    local_dt = utc_dt.astimezone(tz_plus1)

    angles_utc = calculate_clock_hands_angles(utc_dt, timedelta(0), display_tz=UTC)
    angles_local = calculate_clock_hands_angles(local_dt, timedelta(0), display_tz=tz_plus1)

    # UTC shows 14:30 → hour angle = 2.5 (14 % 12 = 2, plus 0.5)
    assert angles_utc.hour == pytest.approx(2.5)
    # Local (UTC+1) shows 15:30 → hour angle = 3.5
    assert angles_local.hour == pytest.approx(3.5)
    # Difference must equal the UTC offset (1 h)
    assert angles_local.hour - angles_utc.hour == pytest.approx(1.0)


def test_timezone_utc_minus5_shows_local_hour() -> None:
    """UTC 20:00 in UTC-5 should display as 15:00 (hour angle = 3.0)."""
    tz_minus5 = timezone(timedelta(hours=-5))
    local_dt = datetime(2025, 4, 27, 15, 0, 0, tzinfo=tz_minus5)

    angles = calculate_clock_hands_angles(local_dt, timedelta(0), display_tz=tz_minus5)

    assert angles.second == pytest.approx(0.0)
    assert angles.minute == pytest.approx(0.0)
    assert angles.hour == pytest.approx(3.0)


def test_timezone_utc_offset_does_not_bleed_into_elapsed() -> None:
    """Elapsed time should be unaffected by timezone; only the start offset shifts."""
    tz_plus2 = timezone(timedelta(hours=2))
    # Start at local midnight (00:00 UTC+2 = 22:00 UTC previous day)
    start_local = datetime(2025, 4, 27, 0, 0, 0, tzinfo=tz_plus2)
    # Elapsed: 1 hour
    duration = timedelta(hours=1)

    angles = calculate_clock_hands_angles(start_local, duration, display_tz=tz_plus2)

    # start_s = 0 (midnight), elapsed_s = 3600
    assert angles.second == pytest.approx(3600.0)
    assert angles.minute == pytest.approx(60.0)
    assert angles.hour == pytest.approx(1.0)


def test_timezone_noon_in_utc_plus1_is_not_midnight() -> None:
    """Ensure UTC 11:00 (= noon in UTC+1) does NOT produce zero angles (old bug)."""
    tz_plus1 = timezone(timedelta(hours=1))
    utc_dt = datetime(2025, 4, 27, 11, 0, 0, tzinfo=UTC)

    # With the old (broken) code this would give hour=11.0 (UTC), but the local
    # clock face should show 12:00 → hour angle = 0.0 after mod 12.
    angles = calculate_clock_hands_angles(utc_dt, timedelta(0), display_tz=tz_plus1)

    # 12:00 local → 12 % 12 = 0.0
    assert angles.hour == pytest.approx(0.0)
    assert angles.minute == pytest.approx(0.0)
    assert angles.second == pytest.approx(0.0)


def test_timezone_old_bug_utc_shows_wrong_hour_on_utc_plus1() -> None:
    """Regression: before the fix, UTC 14:30 on a UTC+1 machine showed 14:30
    instead of 15:30, i.e. exactly 1 hour behind.  Passing display_tz=UTC
    should still show 14:30 (the old broken behaviour), while display_tz=UTC+1
    shows the correct 15:30."""
    tz_plus1 = timezone(timedelta(hours=1))
    utc_dt = datetime(2025, 4, 27, 14, 30, 0, tzinfo=UTC)

    angles_wrong = calculate_clock_hands_angles(utc_dt, timedelta(0), display_tz=UTC)
    angles_correct = calculate_clock_hands_angles(utc_dt, timedelta(0), display_tz=tz_plus1)

    assert angles_wrong.hour == pytest.approx(2.5)   # 14:30 UTC → 2.5 (14 % 12)
    assert angles_correct.hour == pytest.approx(3.5)  # 15:30 local → 3.5


# ---------------------------------------------------------------------------
# format_datetime
# ---------------------------------------------------------------------------


def test_format_datetime() -> None:
    dt = datetime(2024, 1, 2, 3, 4, 5, 678901, tzinfo=UTC)
    result = format_datetime(dt)
    assert result == "03:04:05.678"


# ---------------------------------------------------------------------------
# convert_clock_pid_to_cartesian
# ---------------------------------------------------------------------------


def test_convert_clock_pid_to_cartesian() -> None:
    center = QPointF(100.0, 100.0)
    radius = 50.0

    clock_angles = ClockHands(
        second=0.0,
        minute=15.0,
        hour=6.0,
    )

    hands = convert_clock_pid_to_cartesian(clock_angles, center, radius)

    assert hands.second == QPointF(100.0, 100.0 - radius * 0.9)
    assert hands.minute == QPointF(100.0 + radius * 0.7, 100.0)
    assert hands.hour == QPointF(100.0, 100.0 + radius * 0.5)