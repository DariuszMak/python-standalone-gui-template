from __future__ import annotations

from typing import TYPE_CHECKING

from src.ui.shared.model.data_types import ClockHands

if TYPE_CHECKING:
    from collections.abc import Iterable

    from src.ui.shared.model.strategies.movement_strategy import MovementStrategy


def update_clock_hands(
    current: ClockHands,
    target: ClockHands,
    strategies: Iterable[MovementStrategy],
) -> ClockHands:
    current_values = (current.second, current.minute, current.hour)
    target_values = (target.second, target.minute, target.hour)

    updated = [strategy.update(c, t) for c, t, strategy in zip(current_values, target_values, strategies, strict=True)]

    return ClockHands(*updated)
