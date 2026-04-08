from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest

from src.ui.shared.controller.clock_controller import ClockController
from src.ui.shared.model.data_types import ClockHands


def make_dt(hour: int = 12, minute: int = 0, second: int = 0, tz: timezone = timezone.utc) -> datetime:
    return datetime(2024, 1, 1, hour, minute, second, tzinfo=tz)


class TestClockControllerInit:
    def test_initial_clock_hands_are_zero(self):
        controller = ClockController(start_time=make_dt())
        assert controller._clock_hands == ClockHands(0.0, 0.0, 0.0)

    def test_three_pid_strategies_created(self):
        controller = ClockController(start_time=make_dt())
        assert len(controller._strategies) == 3

    def test_start_time_stored(self):
        start = make_dt(10, 30, 0)
        controller = ClockController(start_time=start)
        assert controller._start_time == start


class TestClockControllerUpdate:
    def test_update_changes_clock_hands_from_zero(self):
        start = make_dt(12, 0, 0)
        controller = ClockController(start_time=start)
        now = start + timedelta(seconds=5)

        controller.update(now)

        # Hands should have moved from their initial zero state
        hands = controller._clock_hands
        assert hands.second != 0.0 or hands.minute != 0.0 or hands.hour != 0.0

    def test_update_called_multiple_times_advances_hands(self):
        start = make_dt(12, 0, 0)
        controller = ClockController(start_time=start)

        controller.update(start + timedelta(seconds=1))
        hands_after_first = ClockHands(
            controller._clock_hands.second,
            controller._clock_hands.minute,
            controller._clock_hands.hour,
        )

        controller.update(start + timedelta(seconds=10))
        hands_after_second = controller._clock_hands

        # Hands should progress forward
        assert hands_after_second.second >= hands_after_first.second

    def test_update_with_zero_elapsed_time(self):
        start = make_dt(12, 0, 0)
        controller = ClockController(start_time=start)

        # now == start_time → duration is zero
        controller.update(start)

        # PID with zero error from zero start should remain at (or near) zero
        hands = controller._clock_hands
        assert abs(hands.second) < 1.0
        assert abs(hands.minute) < 1.0
        assert abs(hands.hour) < 1.0

    @patch("src.ui.shared.controller.clock_controller.update_clock_hands")
    @patch("src.ui.shared.controller.clock_controller.calculate_clock_hands_angles")
    def test_update_delegates_to_helpers(self, mock_calc, mock_update):
        target = ClockHands(10.0, 5.0, 1.0)
        new_hands = ClockHands(9.0, 4.5, 0.9)
        mock_calc.return_value = target
        mock_update.return_value = new_hands

        start = make_dt()
        controller = ClockController(start_time=start)
        now = start + timedelta(seconds=30)

        controller.update(now)

        mock_calc.assert_called_once_with(start, now - start)
        mock_update.assert_called_once_with(ClockHands(0.0, 0.0, 0.0), target, controller._strategies)
        assert controller._clock_hands == new_hands


class TestClockControllerReset:
    def test_reset_updates_start_time(self):
        original_start = make_dt(8, 0, 0)
        controller = ClockController(start_time=original_start)

        new_start = make_dt(10, 0, 0)
        controller.reset(new_start)

        assert controller._start_time == new_start

    def test_reset_zeroes_clock_hands(self):
        start = make_dt()
        controller = ClockController(start_time=start)
        controller.update(start + timedelta(seconds=30))

        controller.reset(make_dt(9, 0, 0))

        assert controller._clock_hands == ClockHands(0.0, 0.0, 0.0)

    def test_reset_calls_strategy_reset(self):
        controller = ClockController(start_time=make_dt())
        mock_strategies = [MagicMock() for _ in range(3)]
        controller._strategies = tuple(mock_strategies)

        controller.reset(make_dt(11, 0, 0))

        for strategy in mock_strategies:
            strategy.reset.assert_called_once()

    def test_reset_logs_warning_when_strategy_reset_raises(self, caplog):
        import logging

        controller = ClockController(start_time=make_dt())

        failing_strategy = MagicMock()
        failing_strategy.reset.side_effect = RuntimeError("boom")
        controller._strategies = (failing_strategy,)

        with caplog.at_level(logging.WARNING, logger="src.ui.shared.controller.clock_controller"):
            controller.reset(make_dt(11, 0, 0))  # should not raise

        assert any("boom" in record.message for record in caplog.records)

    def test_after_reset_update_uses_new_start_time(self):
        start = make_dt(12, 0, 0)
        controller = ClockController(start_time=start)
        controller.update(start + timedelta(minutes=5))

        new_start = make_dt(6, 0, 0)
        controller.reset(new_start)
        controller.update(new_start + timedelta(seconds=5))

        # After reset the controller should be tracking from new_start
        assert controller._start_time == new_start
        # Hands should reflect a small elapsed duration, not the prior 5-minute state
        hands = controller._clock_hands
        assert abs(hands.second) < 60.0