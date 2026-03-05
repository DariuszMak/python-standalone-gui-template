from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.ui.pyside_ui.clock_widget.controller.update_logic import update_clock_hands
from src.ui.pyside_ui.clock_widget.model.data_types import ClockHands
from src.ui.pyside_ui.clock_widget.model.strategies.pid_strategy import PIDMovementStrategy
from src.ui.pyside_ui.clock_widget.view.helpers import calculate_clock_hands_angles

if TYPE_CHECKING:
    from datetime import datetime

logger = logging.getLogger(__name__)


class ClockController:
    def __init__(self, start_time: datetime) -> None:
        self.start_time = start_time

        self.strategies = (
            PIDMovementStrategy(0.15, 0.005, 0.005),
            PIDMovementStrategy(0.08, 0.004, 0.004),
            PIDMovementStrategy(0.08, 0.002, 0.002),
        )

        self.clock_hands = ClockHands(0.0, 0.0, 0.0)

    def update(self, now: datetime) -> None:
        duration = now - self.start_time
        target = calculate_clock_hands_angles(self.start_time, duration)

        self.clock_hands = update_clock_hands(self.clock_hands, target, self.strategies)

    def reset(self, new_start_time: datetime) -> None:
        self.start_time = new_start_time
        self.clock_hands = ClockHands(0.0, 0.0, 0.0)

        for strategy in self.strategies:
            try:
                strategy.reset()
            except Exception as e:
                logger.warning("Strategy reset failed: %s", e)
