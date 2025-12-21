import time

from PySide6.QtWidgets import QApplication

from src.ui.clock_widget.view.clock_widget import ClockWidget


def test_clock_widget_runs() -> None:
    app = QApplication.instance() or QApplication([])

    widget = ClockWidget()
    widget.show()

    before = (
        widget.controller.clock_angles.clock_hands_angles.second,
        widget.controller.clock_angles.clock_hands_angles.minute,
        widget.controller.clock_angles.clock_hands_angles.hour,
    )

    end_time = time.time() + 0.1
    while time.time() < end_time:
        app.processEvents()

    after = (
        widget.controller.clock_angles.clock_hands_angles.second,
        widget.controller.clock_angles.clock_hands_angles.minute,
        widget.controller.clock_angles.clock_hands_angles.hour,
    )

    assert before != after

    widget._timer.stop()
    widget.hide()
    widget.deleteLater()
    app.processEvents()
