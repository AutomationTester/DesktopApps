"""
STARTER - End-to-end desktop workflow (mini project part A)

    test_data/expressions.csv  ->  Calculator  ->  Notepad temp file  ->  verify file on disk

Implement every function marked TODO. Run the unit tests while you work:
    pytest tests/test_workflow_helpers.py -v
They are already written (test-first!) and turn green as you finish each helper.

RULES
  * Use ONLY page objects: CalculatorPage.calculate(a, op, b) -> float and the
    ReportNotepadPage methods. No raw pywinauto in this file.
  * Keep the pure helpers free of GUI code so they can run on the Linux CI runner.
"""
import operator
import re
from dataclasses import dataclass

from core.logger import get_logger
from core.waits import WaitTimeoutError, retry  # noqa: F401  (you will need retry)

log = get_logger("workflows.calc_to_notepad")

_OPERATORS = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
# Hint: a number is  -?\d+(?:\.\d+)?   and an operator is one of  + - * /
_EXPRESSION = re.compile(r"TODO")


@dataclass
class ExpressionResult:
    case_id: str
    expression: str
    expected: float
    actual: float

    @property
    def passed(self):
        # TODO: True when actual and expected are equal (use a small tolerance for floats)
        raise NotImplementedError

    def as_line(self):
        # TODO: return e.g. "EXP_01 | 7 + 8 = 15 | expected 15 | PASS"
        #       (use format_number for both numbers; "FAIL" when not passed)
        raise NotImplementedError


# ---------------------------------------------------------------- pure helpers
def parse_expression(text):
    """'7 + 8' -> ('7', '+', '8'). Raise ValueError for anything that is not 'a op b'."""
    # TODO: use _EXPRESSION.match(text); numbers stay STRINGS
    raise NotImplementedError


def expected_value(a, op, b):
    """Independent oracle: compute the answer with Python (use _OPERATORS)."""
    # TODO
    raise NotImplementedError


def format_number(value):
    """15.0 -> '15', 2.5 -> '2.5', 1/3 -> '0.333333' (max 6 decimals, no trailing zeros)."""
    # TODO
    raise NotImplementedError


def build_report_lines(results, title="Calculator report"):
    """[title, one line per result, 'TOTAL n | PASSED p | FAILED f']"""
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------- GUI steps
# TODO: decorate with @retry(times=2, delay=1.0, exceptions=(ValueError, WaitTimeoutError))
#       Why is it safe to retry calculate()?  (hint: what does it do first?)
def _calculate_with_retry(calculator, a, op, b):
    return calculator.calculate(a, op, b)


def compute_all(calculator, rows):
    """rows: dicts with keys id, expression, expected (from utils.data_reader.read_csv).
    Return a list of ExpressionResult. Log one line per result."""
    # TODO
    raise NotImplementedError


def write_report(notepad, lines):
    """Type the lines into OUR Notepad tab, save, and return the expected file text ("\\n".join)."""
    # TODO
    raise NotImplementedError
