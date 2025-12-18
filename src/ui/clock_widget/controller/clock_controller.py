from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, NamedTuple, Protocol

from src.ui.clock_widget.model.clock_pid import ClockPID
from src.ui.clock_widget.view.helpers import calculate_clock_hands_angles

if TYPE_CHECKING:
    from datetime import datetime

    from src.ui.clock_widget.model.data_types import ClockHands


class ClockStrategy(Protocol):
    def update(self, current: float, target: float) -> float: ...
    def strategy_reset(self) -> None: ...


class Strategies(NamedTuple):
    second: ClockStrategy
    minute: ClockStrategy
    hour: ClockStrategy


class ClockController:
    def __init__(self, start_time: datetime, strategies: Strategies) -> None:
        self.start_time = start_time
        self.strategies = strategies
        self.current_pid = ClockPID(0.0, 0.0, 0.0)

    def update(self, now: datetime) -> ClockPID:
        duration = now - self.start_time
        calculated: ClockHands = calculate_clock_hands_angles(self.start_time, duration)

        self.current_pid.clock_hands_angles.second = self.strategies.second.update(
            self.current_pid.clock_hands_angles.second, calculated.second
        )
        self.current_pid.clock_hands_angles.minute = self.strategies.minute.update(
            self.current_pid.clock_hands_angles.minute, calculated.minute
        )
        self.current_pid.clock_hands_angles.hour = self.strategies.hour.update(
            self.current_pid.clock_hands_angles.hour, calculated.hour
        )

        return self.current_pid

    def clock_controller_reset(self, new_start_time: datetime) -> None:
        self.start_time = new_start_time
        self.current_pid.clock_pid_reset()
        for strategy in (
            self.strategies.second,
            self.strategies.minute,
            self.strategies.hour,
        ):
            with contextlib.suppress(Exception):
                strategy.strategy_reset()
