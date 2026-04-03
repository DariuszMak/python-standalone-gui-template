from __future__ import annotations

from src.ui.shared.model.strategies.movement_strategy import MovementStrategy


class TickMovementStrategy(MovementStrategy):
    def update(self, _: float, target_value: float) -> float:
        return float(target_value)
