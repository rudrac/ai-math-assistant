import pytest

from ai_math_assistant.math_tools import calculate_math, solve_equation


def test_calculate_math_simple():
    assert calculate_math('2 + 3 * 4') == '14'


def test_calculate_math_symbolic():
    assert calculate_math('sin(pi/2)') == '1'


def test_solve_equation_linear():
    assert solve_equation('2*x - 4 = 0') == '[2]'


def test_solve_equation_invalid():
    with pytest.raises(ValueError):
        solve_equation('bad expression')
