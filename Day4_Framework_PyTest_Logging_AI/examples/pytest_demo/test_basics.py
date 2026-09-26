"""
test_basics.py - test structure, discovery and assertions.

Discovery rules (see pytest.ini):
  * files named test_*.py (or *_test.py by default)
  * functions named test_*
  * classes named Test* (no __init__ method) containing test_* methods

Run only this file:          pytest test_basics.py
Run one test:                pytest test_basics.py::test_addition
Run tests matching a name:   pytest -k "divide"
"""
import pytest

from calculator import Calculator, is_valid_username


# ---------------------------------------------------------------------------
# Plain assert - pytest rewrites it to show both sides when it fails
# ---------------------------------------------------------------------------
def test_addition():
    calc = Calculator().open()
    assert calc.calculate(2, "+", 3) == 5


def test_assert_with_message():
    calc = Calculator().open()
    result = calc.calculate(10, "-", 4)
    assert result == 6, f"Expected 6 but calculator showed {result}"


# ---------------------------------------------------------------------------
# Floats: never compare with == directly -> pytest.approx
# ---------------------------------------------------------------------------
def test_float_result_with_approx():
    calc = Calculator().open()
    assert 0.1 + 0.2 != 0.3                           # classic float surprise
    assert calc.calculate(0.1, "+", 0.2) == pytest.approx(0.3)
    assert calc.calculate(10, "/", 3) == pytest.approx(3.333, rel=1e-3)


# ---------------------------------------------------------------------------
# Expected exceptions -> pytest.raises
# ---------------------------------------------------------------------------
def test_divide_by_zero_raises():
    calc = Calculator().open()
    with pytest.raises(ZeroDivisionError, match="divide by zero"):
        calc.calculate(5, "/", 0)


def test_unsupported_operator_raises():
    calc = Calculator().open()
    with pytest.raises(ValueError) as exc_info:
        calc.calculate(1, "%", 2)
    assert "%" in str(exc_info.value)


# ---------------------------------------------------------------------------
# Validating collections, strings, booleans, state
# ---------------------------------------------------------------------------
def test_history_is_recorded():
    calc = Calculator().open()
    calc.calculate(1, "+", 1)
    calc.calculate(3, "*", 3)
    assert len(calc.history) == 2
    assert calc.history[-1] == (3.0, "*", 3.0, 9.0)
    assert (1.0, "+", 1.0, 2.0) in calc.history


def test_username_rules():
    assert is_valid_username("tester01")
    assert not is_valid_username("abc")               # too short
    assert not is_valid_username("user_name")         # underscore not allowed


# ---------------------------------------------------------------------------
# Grouping related tests in a class (no __init__!)
# ---------------------------------------------------------------------------
class TestCalculatorState:
    def test_new_calculator_is_closed(self):
        assert Calculator().is_open is False

    def test_calculate_when_closed_fails(self):
        with pytest.raises(RuntimeError, match="not open"):
            Calculator().calculate(1, "+", 1)
