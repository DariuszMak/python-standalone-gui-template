from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, datetime, time, timedelta

from PySide6.QtCore import QPointF, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import QWidget
@dataclass
class ClockHands:
    second: float
    minute: float
    hour: float


@dataclass
class HandsPosition:
    second: QPointF
    minute: QPointF
    hour: QPointF
