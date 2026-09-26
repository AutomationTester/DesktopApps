"""
06_data_driven_calculator.py
============================
Day 3 - Data-driven desktop automation: Windows 11 Calculator + CSV/JSON.

Idea
----
The TEST LOGIC is written once. The TEST DATA lives in a file
(data/calculator_tests.csv or data/calculator_tests.json). Adding a new
test case = adding a row, no code change.

Design (layers - keep them separate!)
------------------------------------
    load_test_cases()      data layer    : CSV / JSON  ->  list of dicts
    MockCalculator         "driver"      : computes in pure Python (runs anywhere)
    GuiCalculator          "driver"      : drives the real app with pywinauto
    run_suite()            test layer    : for each row -> calculate -> compare
    write_results()        report layer  : results -> CSV with PASS/FAIL

Both drivers expose the SAME method: calculate(num1, operator, num2) -> str
so run_suite() does not care which one it gets. (That is polymorphism -
Day 1 OOP in action.)

Run
---
    python 06_data_driven_calculator.py --dry-run                        (CSV, mock, safe anywhere)
    python 06_data_driven_calculator.py --dry-run --data data/calculator_tests.json
    python 06_data_driven_calculator.py                                  (REAL GUI - Windows 11 only,
                                                                          do not touch mouse/keyboard)
Results are written to  sandbox/calculator_results.csv  (or --output PATH).
"""

import argparse
import csv
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_DATA = HERE / "data" / "calculator_tests.csv"
DEFAULT_OUTPUT = HERE / "sandbox" / "calculator_results.csv"

SUPPORTED_OPERATORS = ("+", "-", "*", "/")
DIVIDE_BY_ZERO_MSG = "Cannot divide by zero"


# =============================================================================
# 1. DATA LAYER - no GUI code here
# =============================================================================
def load_test_cases(path):
    """Return a list of dicts: test_id, num1, operator, num2, expected, description."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Test data file not found: {path}")

    if path.suffix.lower() == ".csv":
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    elif path.suffix.lower() == ".json":
        with open(path, encoding="utf-8") as f:
            rows = json.load(f)["tests"]
    else:
        raise ValueError(f"Unsupported data file type: {path.suffix} (use .csv or .json)")

    cases = []
    for row in rows:
        op = str(row["operator"]).strip()
        if op not in SUPPORTED_OPERATORS:
            raise ValueError(f"{row['test_id']}: unsupported operator '{op}'")
        cases.append({
            "test_id": str(row["test_id"]).strip(),
            # CSV gives strings, JSON may give ints -> normalise to str
            "num1": str(row["num1"]).strip(),
            "operator": op,
            "num2": str(row["num2"]).strip(),
            "expected": str(row["expected"]).strip(),
            "description": str(row.get("description", "")).strip(),
        })
    return cases


def results_match(expected, actual):
    """Compare numerically when possible (so '15' == '15.0'), else as text."""
    try:
        return abs(float(expected) - float(actual)) < 1e-9
    except ValueError:
        return expected.strip().lower() == actual.strip().lower()


# =============================================================================
# 2. DRIVERS - same interface, different implementation
# =============================================================================
class MockCalculator:
    """Pure-Python stand-in for the GUI. Used with --dry-run."""

    name = "MOCK"

    def start(self):
        print("[MOCK] No GUI launched - computing results in Python")

    def calculate(self, num1, operator, num2):
        a, b = float(num1), float(num2)
        if operator == "/" and b == 0:
            return DIVIDE_BY_ZERO_MSG
        result = {"+": a + b, "-": a - b, "*": a * b, "/": a / b if b else 0}[operator]
        # Format like the Calculator display: 15 not 15.0, 2.25 stays 2.25
        return str(int(result)) if result == int(result) else f"{result:.10g}"

    def stop(self):
        pass


class GuiCalculator:
    """Drives the real Windows 11 Calculator using pywinauto (UIA backend)."""

    name = "GUI"
    OPERATOR_BUTTONS = {"+": "plusButton", "-": "minusButton",
                        "*": "multiplyButton", "/": "divideButton"}

    def __init__(self, timeout=10):
        self.timeout = timeout
        self.window = None

    def start(self):
        # Import here so --dry-run works on machines without pywinauto (e.g. Linux)
        from pywinauto import Desktop

        # On Windows 11 calc.exe is only a launcher, so we find the window
        # from the Desktop instead of from the Popen process.
        self.window = Desktop(backend="uia").window(title="Calculator")
        if not self.window.exists(timeout=1):   # reuse an open Calculator: every calc.exe
            subprocess.Popen("calc.exe")   # launch opens ANOTHER window -> "2 elements match"
        self.window.wait("visible", timeout=self.timeout)
        print("[GUI] Calculator window found")

    def _click(self, auto_id):
        self.window.child_window(auto_id=auto_id, control_type="Button").invoke()

    def _enter_number(self, number):
        negative = number.startswith("-")
        for ch in number.lstrip("-"):
            if ch.isdigit():
                self._click(f"num{ch}Button")
            elif ch == ".":
                self._click("decimalSeparatorButton")
        if negative:
            self._click("negateButton")

    def _read_display(self):
        text = self.window.child_window(auto_id="CalculatorResults").window_text()
        # "Display is 1,234" -> "1234"
        return text.replace("Display is", "").replace(",", "").strip()

    def calculate(self, num1, operator, num2):
        self._click("clearButton")
        self._enter_number(num1)
        self._click(self.OPERATOR_BUTTONS[operator])
        self._enter_number(num2)
        self._click("equalButton")
        time.sleep(0.3)   # tiny pause for the display to refresh
        return self._read_display()

    def stop(self):
        if self.window is not None:
            self.window.close()
            print("[GUI] Calculator closed")


# =============================================================================
# 3. TEST LAYER - knows nothing about files or GUI details
# =============================================================================
def run_suite(cases, calculator):
    results = []
    calculator.start()
    try:
        for case in cases:
            try:
                actual = calculator.calculate(case["num1"], case["operator"], case["num2"])
                status = "PASS" if results_match(case["expected"], actual) else "FAIL"
                error = ""
            except Exception as exc:          # one broken row must not stop the suite
                actual, status, error = "", "ERROR", f"{type(exc).__name__}: {exc}"
            results.append({**case, "actual": actual, "status": status, "error": error,
                            "mode": calculator.name,
                            "executed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            expr = f"{case['num1']} {case['operator']} {case['num2']}"
            print(f"  {case['test_id']:<9} {expr:<14} expected={case['expected']:<22} "
                  f"actual={actual:<22} {status}")
    finally:
        calculator.stop()                     # always clean up the app
    return results


# =============================================================================
# 4. REPORT LAYER
# =============================================================================
def write_results(results, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["test_id", "num1", "operator", "num2", "expected", "actual",
              "status", "error", "mode", "executed_at", "description"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)


def main():
    parser = argparse.ArgumentParser(description="Data-driven Windows Calculator tests")
    parser.add_argument("--data", default=str(DEFAULT_DATA), help="CSV or JSON test data file")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="results CSV path")
    parser.add_argument("--dry-run", "--mock", dest="dry_run", action="store_true",
                        help="use MockCalculator (no GUI) - safe on any OS")
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.is_absolute():
        data_path = HERE / data_path

    cases = load_test_cases(data_path)
    print(f"Loaded {len(cases)} test cases from {data_path.name}")

    if args.dry_run:
        calculator = MockCalculator()
    else:
        if sys.platform != "win32":
            sys.exit("GUI mode needs Windows. Use --dry-run on this OS.")
        calculator = GuiCalculator()

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = HERE / output_path       # relative paths are relative to this script

    results = run_suite(cases, calculator)
    write_results(results, output_path)

    counts = {s: sum(r["status"] == s for r in results) for s in ("PASS", "FAIL", "ERROR")}
    print(f"\nTotal={len(results)}  PASS={counts['PASS']}  FAIL={counts['FAIL']}  ERROR={counts['ERROR']}")
    print(f"Results written to {output_path}")
    # Non-zero exit code when anything failed -> CI pipelines notice
    sys.exit(0 if counts["FAIL"] == counts["ERROR"] == 0 else 1)


if __name__ == "__main__":
    main()
