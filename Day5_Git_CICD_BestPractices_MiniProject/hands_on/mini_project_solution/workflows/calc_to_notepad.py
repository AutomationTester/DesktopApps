"""
End-to-end desktop workflow (mini project part A)

    test_data/expressions.csv  ->  Calculator  ->  Notepad temp file  ->  verify file on disk

The module is split in two layers:
  * PURE helpers (parse_expression, expected_value, format_number, build_report_lines)
    -> no GUI, unit-tested on any OS, including the Linux CI runner.
  * GUI steps (compute_all, write_report) -> use ONLY the framework's page objects
    (CalculatorPage.calculate, ReportNotepadPage.write_lines/save/close_tab),
    never raw pywinauto.
"""
import operator
import re
from dataclasses import dataclass

from core.logger import get_logger
from core.waits import WaitTimeoutError, retry

log = get_logger("workflows.calc_to_notepad")

_OPERATORS = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
_NUMBER = r"-?\d+(?:\.\d+)?"
_EXPRESSION = re.compile(rf"^\s*({_NUMBER})\s*([+\-*/])\s*({_NUMBER})\s*$")


@dataclass
class ExpressionResult:
    case_id: str
    expression: str
    expected: float
    actual: float

    @property
    def passed(self):
        return abs(self.actual - self.expected) < 1e-9

    def as_line(self):
        status = "PASS" if self.passed else "FAIL"
        return (f"{self.case_id} | {self.expression} = {format_number(self.actual)}"
                f" | expected {format_number(self.expected)} | {status}")


# ---------------------------------------------------------------- pure helpers
def parse_expression(text):
    """'7 + 8' -> ('7', '+', '8'). Numbers stay strings (CalculatorPage types them digit by digit)."""
    match = _EXPRESSION.match(text)
    if not match:
        raise ValueError(f"Not a simple 'a op b' expression: {text!r}")
    return match.group(1), match.group(2), match.group(3)


def expected_value(a, op, b):
    """Independent oracle: what Python says the answer is."""
    return _OPERATORS[op](float(a), float(b))


def format_number(value):
    """15.0 -> '15', 2.5 -> '2.5', 1/3 -> '0.333333'."""
    value = float(value)
    if value.is_integer():
        return str(int(value))
    return f"{value:.6f}".rstrip("0").rstrip(".")


def build_report_lines(results, title="Calculator report"):
    passed = sum(r.passed for r in results)
    lines = [title]
    lines += [r.as_line() for r in results]
    lines.append(f"TOTAL {len(results)} | PASSED {passed} | FAILED {len(results) - passed}")
    return lines


# ---------------------------------------------------------------- GUI steps
@retry(times=2, delay=1.0, exceptions=(ValueError, WaitTimeoutError))
def _calculate_with_retry(calculator, a, op, b):
    # calculate() starts with clear(), so repeating it is safe (idempotent step)
    return calculator.calculate(a, op, b)


def compute_all(calculator, rows):
    """rows: dicts with keys id, expression, expected (from utils.data_reader.read_csv)."""
    results = []
    for row in rows:
        a, op, b = parse_expression(row["expression"])
        actual = _calculate_with_retry(calculator, a, op, b)
        result = ExpressionResult(row["id"], row["expression"].strip(), float(row["expected"]), actual)
        log.info(result.as_line())
        results.append(result)
    return results


def write_report(notepad, lines):
    """Type the report into OUR Notepad tab and save it. The caller closes the tab (in finally)."""
    notepad.write_lines(lines)
    notepad.save()
    return "\n".join(lines)
