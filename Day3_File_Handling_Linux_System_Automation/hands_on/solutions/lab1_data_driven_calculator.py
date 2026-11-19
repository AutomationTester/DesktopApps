"""
Lab 1 - SOLUTION - Data-driven desktop automation using CSV/JSON
================================================================
Reads Calculator test cases from CSV or JSON, validates each row, runs it
through a calculator "driver" (mock or real GUI), and writes:

    sandbox/lab1_results.csv    one row per test with PASS/FAIL/ERROR
    sandbox/lab1_summary.json   totals + pass rate + list of failed ids

Run (safe anywhere):
    python lab1_data_driven_calculator.py --dry-run
    python lab1_data_driven_calculator.py --dry-run --data data/calc_lab_tests.json
    python lab1_data_driven_calculator.py --dry-run --priority high
Real GUI (Windows 11 only, hands off the mouse!):
    python lab1_data_driven_calculator.py
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
    if path.suffix.lower() == ".csv":
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    if path.suffix.lower() == ".json":
        with open(path, encoding="utf-8") as f:
            return json.load(f)["tests"]
    raise ValueError(f"Unsupported file type: {path.suffix}")


def validate_row(row):
    """Return an error message for a bad row, or '' if the row is valid."""
    for key in ("test_id", "num1", "operator", "num2", "expected"):
        if str(row.get(key, "")).strip() == "":
            return f"missing value for '{key}'"
    if str(row["operator"]).strip() not in OPERATORS:
        return f"unsupported operator '{row['operator']}'"
    for key in ("num1", "num2"):
        try:
            float(row[key])
        except (TypeError, ValueError):
            return f"{key} is not a number: '{row[key]}'"
    return ""


def is_match(expected, actual):
    try:
        return abs(float(expected) - float(actual)) < 1e-6
    except ValueError:
        return str(expected).strip().lower() == str(actual).strip().lower()


# -------------------------------------------------------------------- drivers
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
    """Real Windows 11 Calculator (pywinauto, UIA backend). Not run in class labs by default."""
    name = "GUI"
    OPS = {"+": "plusButton", "-": "minusButton", "*": "multiplyButton", "/": "divideButton"}

    def start(self):
        from pywinauto import Desktop           # lazy import: dry-run needs no pywinauto
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
            problem = validate_row(row)
            if problem:
                actual, status = "", "ERROR"
            else:
                try:
                    actual = calc.calculate(row["num1"], row["operator"], row["num2"])
                    status = "PASS" if is_match(row["expected"], actual) else "FAIL"
                except Exception as exc:
                    actual, status, problem = "", "ERROR", str(exc)
            results.append({"test_id": row["test_id"], "num1": row["num1"], "operator": row["operator"],
                            "num2": row["num2"], "expected": row["expected"], "actual": actual,
                            "status": status, "notes": problem})
            print(f"  {row['test_id']:<8} {row['num1']:>5} {row['operator']} {row['num2']:<5} "
                  f"expected={row['expected']:<22} actual={actual:<22} {status} {problem}")
    finally:
        calc.stop()
    return results


# --------------------------------------------------------------- report layer
def write_reports(results, data_file, mode):
    SANDBOX.mkdir(exist_ok=True)
    csv_path = SANDBOX / "lab1_results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    total = len(results)
    counts = {s: sum(r["status"] == s for r in results) for s in ("PASS", "FAIL", "ERROR")}
    summary = {
        "data_file": Path(data_file).name,
        "mode": mode,
        "total": total,
        **counts,
        "pass_rate": round(counts["PASS"] / total * 100, 1) if total else 0.0,
        "failed_ids": [r["test_id"] for r in results if r["status"] != "PASS"],
    }
    json_path = SANDBOX / "lab1_summary.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    return csv_path, json_path, summary


def main():
    parser = argparse.ArgumentParser(description="Lab 1 - data-driven Calculator tests")
    parser.add_argument("--data", default="data/calc_lab_tests.csv")
    parser.add_argument("--dry-run", action="store_true", help="use the mock calculator")
    parser.add_argument("--priority", help="only run rows with this priority (stretch goal)")
    args = parser.parse_args()

    data_file = Path(args.data) if Path(args.data).is_absolute() else HERE / args.data
    rows = load_rows(data_file)
    if args.priority:
        rows = [r for r in rows if str(r.get("priority", "")).lower() == args.priority.lower()]
    print(f"Running {len(rows)} tests from {data_file.name}")

    calc = MockCalculator() if args.dry_run else GuiCalculator()
    results = run_tests(rows, calc)
    if not results:
        print("No tests selected.")
        return 0
    csv_path, json_path, summary = write_reports(results, data_file, calc.name)
    print(f"\nSummary: total={summary['total']} PASS={summary['PASS']} FAIL={summary['FAIL']} "
          f"ERROR={summary['ERROR']} pass_rate={summary['pass_rate']}%")
    print(f"Reports: {csv_path.relative_to(HERE)} , {json_path.relative_to(HERE)}")
    return 0 if summary["FAIL"] == summary["ERROR"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
