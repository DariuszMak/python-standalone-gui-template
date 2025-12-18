from __future__ import annotations

import math
import typing
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QRect, QRectF
from PySide6.QtGui import QColor, QFont, QPainter, QPalette, QPen

from src.ui.clock_widget.view.helpers import format_datetime, polar_to_cartesian

if TYPE_CHECKING:
    from datetime import datetime

    from src.ui.clock_widget.model.data_types import HandsPosition


def paint_clock_face(
    painter: QPainter,
    rect: typing.Callable[[], QRect | QRectF],
    palette: typing.Callable[[], QPalette],
) -> tuple[QPointF, float, int]:
    size = min(rect().width(), rect().height())
    center = QPointF(rect().center())
    radius = size * 0.4

    painter.fillRect(rect(), palette().window())

    pen = QPen(palette().text().color())
    pen.setWidthF(2.0)
    painter.setPen(pen)
    painter.drawEllipse(center, radius, radius)

    for hour in range(60):
        angle = (hour / 60.0) * 2.0 * math.pi
        outer = polar_to_cartesian(center, radius, angle)
        inner = polar_to_cartesian(center, radius - (10.0 if hour % 5 == 0 else 5.0), angle)
        pen = QPen(QColor(200, 200, 200))
        pen.setWidthF(3.0 if hour % 5 == 0 else 1.5)
        painter.setPen(pen)
        painter.drawLine(inner, outer)

    font_size = max(8, int(radius * 0.09))

    painter.setFont(QFont("Arial", font_size))
    for hour in range(12):
        angle = (hour / 12.0) * 2.0 * math.pi
        text_position = polar_to_cartesian(center, radius - float(font_size) * 2, angle)
        painter.setPen(QPen(QColor(255, 255, 255)))
        friendly_presented_hour = ((hour + 11) % 12) + 1
        font_metrics = painter.fontMetrics()
        width = font_metrics.horizontalAdvance(str(friendly_presented_hour))
        height = font_metrics.height()
        painter.drawText(
            QPointF(text_position.x() - width / 2, text_position.y() + height / 4), str(friendly_presented_hour)
        )
    return center, radius, font_size


def paint_hands(painter: QPainter, center: QPointF, hands_position: HandsPosition) -> None:
    painter.setPen(QPen(QColor(255, 255, 255), 8.0))
    painter.drawLine(center, hands_position.hour)

    painter.setPen(QPen(QColor(200, 200, 200), 6.0))
    painter.drawLine(center, hands_position.minute)

    painter.setPen(QPen(QColor(255, 0, 0), 2.0))
    painter.drawLine(center, hands_position.second)


def paint_current_time(
    current_time: datetime, painter: QPainter, center: QPointF, radius: float, font_size: int
) -> None:
    formatted = format_datetime(current_time)
    painter.setPen(QPen(QColor(150, 255, 190)))
    painter.setFont(QFont("Consolas", font_size))
    font_metrics = painter.fontMetrics()
    width = font_metrics.horizontalAdvance(formatted)
    painter.drawText(QPointF(center.x() - width / 2, center.y() + radius / 2), formatted)
