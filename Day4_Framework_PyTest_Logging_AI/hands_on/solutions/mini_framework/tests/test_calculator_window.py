"""Lab 2 - Calculator tests using the CalculatorWindow object (simulated app, no GUI)."""
import pytest

from core.waits import WaitTimeoutError
from utils.data_reader import read_csv

CASES = read_csv("calculator_data.csv")

pytestmark = pytest.mark.desktop          # every test in this module


@pytest.mark.smoke
def test_addition(calculator):
    assert calculator.calculate(7, "+", 8) == 15


@pytest.mark.regression
@pytest.mark.parametrize("case", CASES, ids=[c["test_id"] for c in CASES])
def test_calculator_from_csv(calculator, case):
    result = calculator.calculate(case["num1"], case["operator"], case["num2"])
    assert result == pytest.approx(float(case["expected"])), f"{case['test_id']}: got {result}"


@pytest.mark.regression
def test_divide_by_zero_shows_message(calculator):
    calculator.clear()
    calculator.enter_number(5)
    calculator.press_operator("/")
    calculator.enter_number(0)
    calculator.press_equals()
    assert "Cannot divide by zero" in calculator.display_text()
    with pytest.raises(ValueError):
        _ = calculator.result


@pytest.mark.regression
def test_unsupported_operator_is_rejected(calculator):
    with pytest.raises(ValueError, match="Unsupported operator"):
        calculator.press_operator("%")


@pytest.mark.regression
def test_wait_for_text_times_out(calculator):
    calculator.clear()
    with pytest.raises(WaitTimeoutError):
        calculator.wait_for_text("Display is 999", timeout=0.3, auto_id="CalculatorResults")


@pytest.mark.demo_fail
def test_deliberate_failure_takes_screenshot(calculator):
    assert calculator.calculate(2, "+", 2) == 5, "wrong on purpose - check screenshots/ and the report"
