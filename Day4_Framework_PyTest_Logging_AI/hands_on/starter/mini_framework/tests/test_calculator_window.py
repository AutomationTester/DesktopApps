"""Lab 2 - Calculator tests using the CalculatorWindow object (simulated app, no GUI)."""
import pytest

from core.waits import WaitTimeoutError
from utils.data_reader import read_csv

CASES = read_csv("calculator_data.csv")

# TODO (Lab 2, step 3): mark EVERY test in this module as desktop:  pytestmark = pytest.mark.desktop


# TODO (Lab 2, step 3): smoke test - calculator.calculate(7, "+", 8) must equal 15
def test_addition(calculator):
    pass


# TODO (Lab 2, step 4): data-driven test from test_data/calculator_data.csv
#   @pytest.mark.regression
#   @pytest.mark.parametrize("case", CASES, ids=[c["test_id"] for c in CASES])
#   compare with pytest.approx(float(case["expected"])) and add a helpful assert message


# TODO (Lab 2, step 4): negative test - 5 / 0 shows "Cannot divide by zero"
#   and reading calculator.result raises ValueError (use pytest.raises)


# TODO (Lab 2, step 4): press_operator("%") raises ValueError matching "Unsupported operator"


def test_wait_for_text_times_out(calculator):
    calculator.clear()
    with pytest.raises(WaitTimeoutError):
        calculator.wait_for_text("Display is 999", timeout=0.3, auto_id="CalculatorResults")


# TODO (Lab 2, step 5): a test marked @pytest.mark.demo_fail that asserts 2 + 2 == 5
