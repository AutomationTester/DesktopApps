"""
Lab 1 - STARTER - Data-driven desktop automation using CSV/JSON
===============================================================
Your job: implement the DATA, TEST and REPORT layers. The calculator
drivers (MockCalculator and GuiCalculator) are already written for you.

Goal output files:
    sandbox/lab1_results.csv    one row per test with PASS/FAIL/ERROR
    sandbox/lab1_summary.json   totals + pass rate + list of failed ids

Run (safe anywhere):
    python lab1_data_driven_calculator.py --dry-run
    python lab1_data_driven_calculator.py --dry-run --data data/calc_lab_tests.json

Search for "# TODO" - there are 6 of them. See hands_on/Lab_Guide.md, Lab 1.
"""

import argparse
import csv
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox"
OPERATORS = ("+", "-", "*", "/")
DIV_ZERO = "Cannot divide by zero"


# ----------------------------------------------------------------- data layer
def load_rows(path):
    """Return raw rows (list of dicts) from a .csv or .json file."""
    path = Path(path)
    # TODO 1: if the suffix is .csv  -> open with newline="" and use csv.DictReader
    #         if the suffix is .json -> json.load(f) and return the "tests" list
    #         otherwise raise ValueError("Unsupported file type")
    raise NotImplementedError("TODO 1: load_rows")


def validate_row(row):
    """Return an error message for a bad row, or '' if the row is valid."""
    # TODO 2: return a message when
    #   - any of test_id, num1, operator, num2, expected is empty
    #   - operator is not in OPERATORS
    #   - num1 or num2 cannot be converted with float()
    # otherwise return ""
    raise NotImplementedError("TODO 2: validate_row")


def is_match(expected, actual):
    # TODO 3: compare as numbers when both convert to float (tolerance 1e-6),
    #         otherwise compare as lower-case strings. Return True/False.
    raise NotImplementedError("TODO 3: is_match")


# -------------------------------------------------------------------- drivers (DONE)
class MockCalculator:
    name = "MOCK"

    def start(self):
        pass

    def stop(self):
        pass

    def calculate(self, num1, op, num2):
        a, b = float(num1), float(num2)
        if op == "/" and b == 0:
            return DIV_ZERO
        value = {"+": a + b, "-": a - b, "*": a * b, "/": a / b if b else 0}[op]
        return str(int(value)) if value == int(value) else repr(value)


class GuiCalculator:
    """Real Windows 11 Calculator (pywinauto, UIA backend)."""
    name = "GUI"
    OPS = {"+": "plusButton", "-": "minusButton", "*": "multiplyButton", "/": "divideButton"}

    def start(self):
        from pywinauto import Desktop
        self.win = Desktop(backend="uia").window(title="Calculator")
        if not self.win.exists(timeout=1):   # reuse an open Calculator: every calc.exe
            subprocess.Popen("calc.exe")   # launch opens ANOTHER window -> "2 elements match"
        self.win.wait("visible", timeout=10)

    def _press(self, auto_id):
        self.win.child_window(auto_id=auto_id, control_type="Button").invoke()

    def _type_number(self, text):
        for ch in str(text):
            self._press("decimalSeparatorButton" if ch == "." else f"num{ch}Button")

    def calculate(self, num1, op, num2):
        self._press("clearButton")
        self._type_number(num1)
        self._press(self.OPS[op])
        self._type_number(num2)
        self._press("equalButton")
        time.sleep(0.3)
        text = self.win.child_window(auto_id="CalculatorResults").window_text()
        return text.replace("Display is", "").replace(",", "").strip()

    def stop(self):
        self.win.close()


# ----------------------------------------------------------------- test layer
def run_tests(rows, calc):
    results = []
    calc.start()
    try:
        for row in rows:
            row = {k: str(v).strip() for k, v in row.items()}
            # TODO 4: - call validate_row(row); if it returns a message -> status "ERROR"
            #         - else call calc.calculate(...) and set status PASS/FAIL using is_match
            #         - wrap calculate in try/except so one bad row does not stop the run
            #         - append a dict with: test_id, num1, operator, num2, expected,
            #           actual, status, notes   and print one line per test
            raise NotImplementedError("TODO 4: run_tests loop")
    finally:
        calc.stop()
    return results


# --------------------------------------------------------------- report layer
def write_reports(results, data_file, mode):
    SANDBOX.mkdir(exist_ok=True)
    # TODO 5: write results to SANDBOX / "lab1_results.csv" using csv.DictWriter
    # TODO 6: build a summary dict (data_file, mode, total, PASS, FAIL, ERROR,
    #         pass_rate, failed_ids) and json.dump it to SANDBOX / "lab1_summary.json"
    #         Return (csv_path, json_path, summary)
    raise NotImplementedError("TODO 5/6: write_reports")


def main():
    parser = argparse.ArgumentParser(description="Lab 1 - data-driven Calculator tests")
    parser.add_argument("--data", default="data/calc_lab_tests.csv")
    parser.add_argument("--dry-run", action="store_true", help="use the mock calculator")
    args = parser.parse_args()

    data_file = Path(args.data) if Path(args.data).is_absolute() else HERE / args.data
    try:
        rows = load_rows(data_file)
        print(f"Running {len(rows)} tests from {data_file.name}")
        calc = MockCalculator() if args.dry_run else GuiCalculator()
        results = run_tests(rows, calc)
        csv_path, json_path, summary = write_reports(results, data_file, calc.name)
    except NotImplementedError as todo:
        print(f"Not finished yet -> {todo}")
        return 2
    print(f"\nSummary: {summary}")
    return 0 if summary["FAIL"] == summary["ERROR"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
