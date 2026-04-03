from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.ui.shared.controller.update_logic import update_clock_hands
from src.ui.shared.helpers import calculate_clock_hands_angles
from src.ui.shared.model.data_types import ClockHands
from src.ui.shared.model.strategies.pid_strategy import PIDMovementStrategy

if TYPE_CHECKING:
    from datetime import datetime

logger = logging.getLogger(__name__)


class ClockController:
    def __init__(self, start_time: datetime) -> None:
        self._start_time = start_time

        self._strategies = (
            PIDMovementStrategy(0.15, 0.005, 0.005),
            PIDMovementStrategy(0.08, 0.004, 0.004),
            PIDMovementStrategy(0.08, 0.002, 0.002),
        )

        self._clock_hands = ClockHands(0.0, 0.0, 0.0)

    def update(self, now: datetime) -> None:
        duration = now - self._start_time
        target = calculate_clock_hands_angles(self._start_time, duration)

        self._clock_hands = update_clock_hands(self._clock_hands, target, self._strategies)

    def reset(self, new_start_time: datetime) -> None:
        self._start_time = new_start_time
        self._clock_hands = ClockHands(0.0, 0.0, 0.0)

        for strategy in self._strategies:
            try:
                strategy.reset()
            except Exception as e:
                logger.warning("Strategy reset failed: %s", e)
