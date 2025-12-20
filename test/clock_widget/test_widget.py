from datetime import UTC, datetime, timedelta

from src.ui.clock_widget.view.helpers import calculate_clock_hands_angles


def test_clock_hands_progress_consistently() -> None:
    start = datetime(2025, 4, 27, 12, 0, 0, tzinfo=UTC)

    angles_t0 = calculate_clock_hands_angles(start, timedelta(0))
    angles_t1 = calculate_clock_hands_angles(start, timedelta(seconds=60))

    assert angles_t1.second > angles_t0.second
    assert angles_t1.minute > angles_t0.minute
    assert angles_t1.hour > angles_t0.hour
