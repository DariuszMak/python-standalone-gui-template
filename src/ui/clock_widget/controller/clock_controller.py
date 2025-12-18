from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from src.ui.clock_widget.model.clock_pids import ClockAngles
from src.ui.clock_widget.model.strategies.pid_strategy import PIDMovementStrategy
from src.ui.clock_widget.view.helpers import calculate_clock_hands_angles

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from datetime import datetime

    from src.ui.clock_widget.model.data_types import ClockHands


class ClockController:
    def __init__(
        self,
        start_time: datetime,
    ) -> None:
        self.start_time = start_time

        self.second_strategy = PIDMovementStrategy(0.15, 0.005, 0.005)
        self.minute_strategy = PIDMovementStrategy(0.08, 0.004, 0.004)
        self.hour_strategy = PIDMovementStrategy(0.08, 0.002, 0.002)

        self.clock_pids = ClockAngles(0.0, 0.0, 0.0)

    def update(self, now: datetime) -> None:
        duration = now - self.start_time
        calculated_clock_hands_angles: ClockHands = calculate_clock_hands_angles(self.start_time, duration)

        self.clock_pids.clock_hands_angles.second = self.second_strategy.update(
            self.clock_pids.clock_hands_angles.second, calculated_clock_hands_angles.second
        )
        self.clock_pids.clock_hands_angles.minute = self.minute_strategy.update(
            self.clock_pids.clock_hands_angles.minute, calculated_clock_hands_angles.minute
        )
        self.clock_pids.clock_hands_angles.hour = self.hour_strategy.update(
            self.clock_pids.clock_hands_angles.hour, calculated_clock_hands_angles.hour
        )

    def clock_controller_reset(self, new_start_time: datetime) -> None:
        self.start_time = new_start_time
        self.clock_pids.clock_pids_reset()
        for strategy in (
            self.second_strategy,
            self.minute_strategy,
            self.hour_strategy,
        ):
            try:
                strategy.movement_strategy_reset()
            except Exception as e:
                logger.warning("Strategy reset failed: %s", e)
