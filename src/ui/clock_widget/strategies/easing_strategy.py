from __future__ import annotations

from src.ui.clock_widget.strategies.movement_strategy import MovementStrategy


class EasingMovementStrategy(MovementStrategy):
    """Simple linear easing toward the target.

    factor: 0.0 .. 1.0 - how quickly to approach the target each update.
    """

    def __init__(self, factor: float = 0.1) -> None:
        self.factor = float(factor)

    def update(self, current_value: float, target_value: float) -> float:
        return current_value + (target_value - current_value) * self.factor
