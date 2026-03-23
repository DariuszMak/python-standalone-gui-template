import pytest

from src.ui.pyside_ui.clock_widget.model.strategies.easing_strategy import EasingMovementStrategy
from src.ui.pyside_ui.clock_widget.model.strategies.movement_strategy import MovementStrategy
from src.ui.pyside_ui.clock_widget.model.strategies.pid_strategy import PIDMovementStrategy
from src.ui.pyside_ui.clock_widget.model.strategies.tick_strategy import TickMovementStrategy


def test_movement_strategy_is_abstract() -> None:
    with pytest.raises(TypeError):
        MovementStrategy()  # type: ignore[abstract]


def test_easing_strategy_moves_fractionally() -> None:
    strat = EasingMovementStrategy(factor=0.2)
    assert strat.update(0.0, 10.0) == pytest.approx(2.0)
    assert strat.update(5.0, 15.0) == pytest.approx(7.0)


def test_easing_strategy_factor_1_moves_directly() -> None:
    strat = EasingMovementStrategy(factor=1.0)
    assert strat.update(3.0, 10.0) == pytest.approx(10.0)


def test_easing_strategy_factor_0_stays_same() -> None:
    strat = EasingMovementStrategy(factor=0.0)
    assert strat.update(3.0, 10.0) == 3.0


def test_tick_strategy_snaps_to_target() -> None:
    strat = TickMovementStrategy()
    assert strat.update(5.0, 20.0) == 20.0
    assert strat.update(-10.0, -3.5) == -3.5


def test_pid_strategy_moves_toward_target() -> None:
    strat = PIDMovementStrategy(0.1, 0.0, 0.0)
    v1 = strat.update(0.0, 10.0)
    assert v1 > 0.0
    v2 = strat.update(v1, 10.0)
    assert v2 > v1


def test_pid_strategy_reset() -> None:
    strat = PIDMovementStrategy(0.1, 0.1, 0.0)
    v1 = strat.update(0.0, 10.0)
    strat.reset()
    v2 = strat.update(0.0, 10.0)
    assert v2 == pytest.approx(v1)
