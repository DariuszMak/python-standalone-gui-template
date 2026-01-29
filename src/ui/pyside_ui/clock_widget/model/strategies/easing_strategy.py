from __future__ import annotations

from src.ui.pyside_ui.clock_widget.model.strategies.movement_strategy import MovementStrategy


class EasingMovementStrategy(MovementStrategy):
    def __init__(self, factor: float = 0.1) -> None:
        self.factor = float(factor)

    def update(self, current_value: float, target_value: float) -> float:
        return current_value + (target_value - current_value) * self.factor
