from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, NamedTuple

from src.ui.clock_widget.model.clock_pid import ClockPIDs
from src.ui.clock_widget.view.helpers import calculate_clock_hands_angles

from src.ui.clock_widget.model.strategies.pid_strategy import PIDMovementStrategy
logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from datetime import datetime

    from src.ui.clock_widget.model.data_types import ClockHands


class Strategies(NamedTuple):
    second: PIDMovementStrategy
    minute: PIDMovementStrategy
    hour: PIDMovementStrategy


class ClockController:
    def __init__(self, start_time: datetime,  ) -> None:
        self.start_time = start_time

        self.strategies = Strategies(
            second= PIDMovementStrategy(0.15, 0.005, 0.005),
            minute= PIDMovementStrategy(0.08, 0.004, 0.004),
            hour= PIDMovementStrategy(0.08, 0.002, 0.002)
        )

        self.clock_pids = ClockPIDs(0.0, 0.0, 0.0)

    def update(self, now: datetime) -> None:
        duration = now - self.start_time
        calculated_clock_hands_angles: ClockHands = calculate_clock_hands_angles(self.start_time, duration)

        self.clock_pids.clock_hands_angles.second = self.strategies.second.update(
            self.clock_pids.clock_hands_angles.second, calculated_clock_hands_angles.second
        )
        self.clock_pids.clock_hands_angles.minute = self.strategies.minute.update(
            self.clock_pids.clock_hands_angles.minute, calculated_clock_hands_angles.minute
        )
        self.clock_pids.clock_hands_angles.hour = self.strategies.hour.update(
            self.clock_pids.clock_hands_angles.hour, calculated_clock_hands_angles.hour
        )

    def clock_controller_reset(self, new_start_time: datetime) -> None:
        self.start_time = new_start_time
        self.clock_pids.clock_pid_reset()
        for strategy in (
            self.strategies.second,
            self.strategies.minute,
            self.strategies.hour,
        ):
            try:
                strategy.movement_strategy_reset()
            except Exception as e:
                logger.warning("Strategy reset failed: %s", e)
