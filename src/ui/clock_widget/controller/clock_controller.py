from __future__ import annotations

import contextlib
from datetime import datetime
from typing import TYPE_CHECKING, NamedTuple

from src.ui.clock_widget.model.clock_pid import ClockPID
from src.ui.clock_widget.view.helpers import calculate_clock_hands_angles

if TYPE_CHECKING:
    from datetime import datetime

    from src.ui.clock_widget.model.data_types import ClockHands
    from src.ui.clock_widget.model.strategies.pid_strategy import PIDMovementStrategy


class Strategies(NamedTuple):
    second: PIDMovementStrategy
    minute: PIDMovementStrategy
    hour: PIDMovementStrategy


class ClockController:
    def __init__(self, start_time: datetime, strategies: Strategies) -> None:
        self.start_time = start_time
        self.strategies = strategies
        self.current_pid = ClockPID(0.0, 0.0, 0.0)

    def update(self, now: datetime) -> None:
        duration = now - self.start_time
        calculated_clock_hands_angles: ClockHands = calculate_clock_hands_angles(self.start_time, duration)

        self.current_pid.clock_hands_angles.second = self.strategies.second.update(
            self.current_pid.clock_hands_angles.second, calculated_clock_hands_angles.second
        )
        self.current_pid.clock_hands_angles.minute = self.strategies.minute.update(
            self.current_pid.clock_hands_angles.minute, calculated_clock_hands_angles.minute
        )
        self.current_pid.clock_hands_angles.hour = self.strategies.hour.update(
            self.current_pid.clock_hands_angles.hour, calculated_clock_hands_angles.hour
        )

    def clock_controller_reset(self, new_start_time: datetime) -> None:
        self.start_time = new_start_time
        self.current_pid.clock_pid_reset()
        for strategy in (
            self.strategies.second,
            self.strategies.minute,
            self.strategies.hour,
        ):
            with contextlib.suppress(Exception):
                strategy.movement_strategy_reset()
