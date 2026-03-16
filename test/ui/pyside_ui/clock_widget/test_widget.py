import time

from PySide6.QtWidgets import QApplication

from src.ui.pyside_ui.clock_widget.view.clock_widget import ClockWidget


def test_clock_widget_runs() -> None:
    app = QApplication.instance() or QApplication([])

    widget = ClockWidget()
    widget.show()

    before = (
        widget._controller.clock_hands.second,
        widget._controller.clock_hands.minute,
        widget._controller.clock_hands.hour,
    )

    end_time = time.time() + 0.1
    while time.time() < end_time:
        app.processEvents()

    after = (
        widget._controller.clock_hands.second,
        widget._controller.clock_hands.minute,
        widget._controller.clock_hands.hour,
    )

    assert before != after

    widget._timer.stop()
    widget.hide()
    widget.deleteLater()
    app.processEvents()
