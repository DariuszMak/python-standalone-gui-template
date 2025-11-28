from __future__ import annotations

from src.ui.clock_widget.model.pid import PID
from src.ui.clock_widget.model.strategies.movement_strategy import MovementStrategy


class PIDMovementStrategy(MovementStrategy):
    def __init__(self, kp: float, ki: float, kd: float) -> None:
        self.pid = PID(kp=kp, ki=ki, kd=kd)

    def update(self, current_value: float, target_value: float) -> float:
        error = target_value - current_value
        return current_value + self.pid.update(error)

    def reset(self) -> None:
        self.pid.reset()
