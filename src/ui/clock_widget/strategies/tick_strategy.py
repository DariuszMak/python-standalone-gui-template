from __future__ import annotations

from src.ui.clock_widget.strategies.movement_strategy import MovementStrategy


class TickMovementStrategy(MovementStrategy):
    def update(self, target_value: float) -> float:
        return float(target_value)
