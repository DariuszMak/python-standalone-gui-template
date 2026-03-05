from __future__ import annotations

from typing import Iterable

from src.ui.pyside_ui.clock_widget.model.data_types import ClockHands
from src.ui.pyside_ui.clock_widget.model.strategies.movement_strategy import MovementStrategy


def update_clock_hands(
    current: ClockHands,
    target: ClockHands,
    strategies: Iterable[MovementStrategy],
) -> ClockHands:
    current_values = (current.second, current.minute, current.hour)
    target_values = (target.second, target.minute, target.hour)

    updated = [
        strategy.update(c, t)
        for c, t, strategy in zip(current_values, target_values, strategies)
    ]

    return ClockHands(*updated)