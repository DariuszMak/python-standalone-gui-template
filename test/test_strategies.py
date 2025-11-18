import math
import pytest

from src.ui.clock_widget.strategies.movement_strategy import MovementStrategy
from src.ui.clock_widget.strategies.easing_strategy import EasingMovementStrategy
from src.ui.clock_widget.strategies.tick_strategy import TickMovementStrategy
from src.ui.clock_widget.strategies.pid_strategy import PIDMovementStrategy


def test_movement_strategy_is_abstract():
    with pytest.raises(TypeError):
        MovementStrategy()  # abstract


def test_easing_strategy_moves_fractionally():
    strat = EasingMovementStrategy(factor=0.2)
    assert strat.update(0.0, 10.0) == pytest.approx(2.0)
    assert strat.update(5.0, 15.0) == pytest.approx(7.0)


def test_easing_strategy_factor_1_moves_directly():
    strat = EasingMovementStrategy(factor=1.0)
    assert strat.update(3.0, 10.0) == pytest.approx(10.0)


def test_easing_strategy_factor_0_stays_same():
    strat = EasingMovementStrategy(factor=0.0)
    assert strat.update(3.0, 10.0) == 3.0


def test_tick_strategy_snaps_to_target():
    strat = TickMovementStrategy()
    assert strat.update(5.0, 20.0) == 20.0
    assert strat.update(-10.0, -3.5) == -3.5


def test_pid_strategy_moves_toward_target():
    strat = PIDMovementStrategy(0.1, 0.0, 0.0)
    v1 = strat.update(0.0, 10.0)
    assert v1 > 0.0
    v2 = strat.update(v1, 10.0)
    assert v2 > v1


def test_pid_strategy_reset():
    strat = PIDMovementStrategy(0.1, 0.1, 0.0)
    v1 = strat.update(0.0, 10.0)
    strat.reset()
    v2 = strat.update(0.0, 10.0)
    assert v2 == pytest.approx(v1)
