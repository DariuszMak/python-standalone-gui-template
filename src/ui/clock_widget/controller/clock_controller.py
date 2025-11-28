from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, NamedTuple

from src.ui.clock_widget.model.clock_pid import ClockPID
from src.ui.clock_widget.model.helpers import calculate_clock_hands_angles

if TYPE_CHECKING:
    from datetime import datetime

    from src.ui.clock_widget.model.data_types import ClockHands


class Strategies(NamedTuple):
    second: object
    minute: object
    hour: object


class ClockController:
    """Controller that advances the model state (ClockPID) using provided strategies.

    - `start_time` is the wall clock moment from which the target positions are calculated.
    - `strategies` is a NamedTuple with movement strategy instances for second, minute, hour.
    """

    def __init__(self, start_time: datetime, strategies: Strategies) -> None:
        self.start_time = start_time
        self.strategies = strategies
        # keep model state here
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

    def reset(self, new_start_time: datetime) -> None:
        self.start_time = new_start_time
        self.current_pid.reset()
        # reset strategies if they implement reset()
        for s in (self.strategies.second, self.strategies.minute, self.strategies.hour):
            with contextlib.suppress(Exception):
                s.reset()
