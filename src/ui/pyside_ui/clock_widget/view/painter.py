from __future__ import annotations

import math
import typing
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QRect, QRectF
from PySide6.QtGui import QColor, QFont, QPaintDevice, QPainter, QPalette, QPen

from src.ui.pyside_ui.clock_widget.view.helpers import format_datetime, polar_to_cartesian

if TYPE_CHECKING:
    from datetime import datetime

    from src.ui.pyside_ui.clock_widget.model.data_types import HandsPosition


class Painter:
    def __init__(self, obj: QPaintDevice) -> None:
        self.painter = QPainter(obj)
        self.painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    def __del__(self) -> None:
        self.painter.end()

    def paint_clock_face(
        self,
        rect: typing.Callable[[], QRect | QRectF],
        palette: typing.Callable[[], QPalette],
    ) -> tuple[QPointF, float, int]:
        size = min(rect().width(), rect().height())
        center = QPointF(rect().center())
        radius = size * 0.4

        self.painter.fillRect(rect(), palette().window())

        pen = QPen(palette().text().color())
        pen.setWidthF(2.0)
        self.painter.setPen(pen)
        self.painter.drawEllipse(center, radius, radius)

        for hour in range(60):
            angle = (hour / 60.0) * 2.0 * math.pi
            outer = polar_to_cartesian(center, radius, angle)
            inner = polar_to_cartesian(center, radius - (10.0 if hour % 5 == 0 else 5.0), angle)
            pen = QPen(QColor(200, 200, 200))
            pen.setWidthF(3.0 if hour % 5 == 0 else 1.5)
            self.painter.setPen(pen)
            self.painter.drawLine(inner, outer)

        font_size = max(8, int(radius * 0.09))

        self.painter.setFont(QFont("Arial", font_size))
        for hour in range(12):
            angle = (hour / 12.0) * 2.0 * math.pi
            text_position = polar_to_cartesian(center, radius - float(font_size) * 2, angle)
            self.painter.setPen(QPen(QColor(255, 255, 255)))
            friendly_presented_hour = ((hour + 11) % 12) + 1
            font_metrics = self.painter.fontMetrics()
            width = font_metrics.horizontalAdvance(str(friendly_presented_hour))
            height = font_metrics.height()
            self.painter.drawText(
                QPointF(text_position.x() - width / 2, text_position.y() + height / 4), str(friendly_presented_hour)
            )
        return center, radius, font_size

    def paint_hands(self, center: QPointF, hands_position: HandsPosition) -> None:
        self.painter.setPen(QPen(QColor(255, 255, 255), 8.0))
        self.painter.drawLine(center, hands_position.hour)

        self.painter.setPen(QPen(QColor(200, 200, 200), 6.0))
        self.painter.drawLine(center, hands_position.minute)

        self.painter.setPen(QPen(QColor(255, 0, 0), 2.0))
        self.painter.drawLine(center, hands_position.second)

    def paint_current_time(self, current_time: datetime, center: QPointF, radius: float, font_size: int) -> None:
        formatted = format_datetime(current_time)
        self.painter.setPen(QPen(QColor(150, 255, 190)))
        self.painter.setFont(QFont("Consolas", font_size))
        font_metrics = self.painter.fontMetrics()
        width = font_metrics.horizontalAdvance(formatted)
        self.painter.drawText(QPointF(center.x() - width / 2, center.y() + radius / 2), formatted)
