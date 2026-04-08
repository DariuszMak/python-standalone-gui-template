from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.ui.shared.controller.update_logic import update_clock_hands
from src.ui.shared.model.data_types import ClockHands


def make_passthrough_strategy(multiplier: float = 1.0):
    """Returns a mock strategy where update returns target_value * multiplier."""
    strategy = MagicMock()
    strategy.update.side_effect = lambda current, target: target * multiplier
    return strategy


def make_fixed_strategy(value: float):
    """Returns a mock strategy that always returns a fixed value."""
    strategy = MagicMock()
    strategy.update.return_value = value
    return strategy


def test_returns_clock_hands_instance() -> bool:
    strategies = [make_passthrough_strategy() for _ in range(3)]
    current = ClockHands(0.0, 0.0, 0.0)
    target = ClockHands(10.0, 20.0, 5.0)

    result = update_clock_hands(current, target, strategies)

    assert isinstance(result, ClockHands)


def test_each_strategy_receives_correct_current_and_target() -> None:
    strategies = [MagicMock() for _ in range(3)]
    for s in strategies:
        s.update.return_value = 0.0

    current = ClockHands(second=1.0, minute=2.0, hour=3.0)
    target = ClockHands(second=4.0, minute=5.0, hour=6.0)

    update_clock_hands(current, target, strategies)

    strategies[0].update.assert_called_once_with(1.0, 4.0)
    strategies[1].update.assert_called_once_with(2.0, 5.0)
    strategies[2].update.assert_called_once_with(3.0, 6.0)


def test_result_uses_strategy_output() -> None:
    strategies = [
        make_fixed_strategy(11.0),
        make_fixed_strategy(22.0),
        make_fixed_strategy(33.0),
    ]
    current = ClockHands(0.0, 0.0, 0.0)
    target = ClockHands(1.0, 1.0, 1.0)

    result = update_clock_hands(current, target, strategies)

    assert result.second == pytest.approx(11.0)
    assert result.minute == pytest.approx(22.0)
    assert result.hour == pytest.approx(33.0)


def test_passthrough_strategies_return_target_values() -> None:
    strategies = [make_passthrough_strategy() for _ in range(3)]
    current = ClockHands(0.0, 0.0, 0.0)
    target = ClockHands(15.0, 30.0, 6.0)

    result = update_clock_hands(current, target, strategies)

    assert result.second == pytest.approx(15.0)
    assert result.minute == pytest.approx(30.0)
    assert result.hour == pytest.approx(6.0)


def test_raises_value_error_on_strategy_count_mismatch() -> None:
    strategies = [make_passthrough_strategy(), make_passthrough_strategy()]
    current = ClockHands(0.0, 0.0, 0.0)
    target = ClockHands(1.0, 2.0, 3.0)

    with pytest.raises(ValueError):
        update_clock_hands(current, target, strategies)


def test_zero_current_and_target() -> None:
    strategies = [make_passthrough_strategy() for _ in range(3)]
    current = ClockHands(0.0, 0.0, 0.0)
    target = ClockHands(0.0, 0.0, 0.0)

    result = update_clock_hands(current, target, strategies)

    assert result.second == pytest.approx(0.0)
    assert result.minute == pytest.approx(0.0)
    assert result.hour == pytest.approx(0.0)


def test_strategies_called_exactly_once_each() -> None:
    strategies = [MagicMock() for _ in range(3)]
    for s in strategies:
        s.update.return_value = 0.0

    current = ClockHands(1.0, 2.0, 3.0)
    target = ClockHands(4.0, 5.0, 6.0)

    update_clock_hands(current, target, strategies)

    for s in strategies:
        assert s.update.call_count == 1
