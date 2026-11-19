"""
Lab 4 - SOLUTION: calc_cli.py - pass arguments to a GUI automation script

    python calc_cli.py 12 + 30
    python calc_cli.py 9 x 6            ('x' also means multiply)
    python calc_cli.py 10 / 4
    python calc_cli.py 7 / 0            (Calculator: 'Cannot divide by zero')
    python calc_cli.py 12 + 30 --expected 43     (deliberate FAIL demo)
    python calc_cli.py 12 + 30 --keep-open

The script:
  1. validates the arguments with argparse
  2. computes the EXPECTED result in Python (the test oracle)
  3. drives the real Calculator with pywinauto
  4. prints PASS/FAIL and exits with 0 (pass) / 1 (fail) / 2 (bad usage)

Note: in PowerShell and cmd, '*' is passed as-is. In Git Bash it would be
expanded to file names - quote it ("*") or use 'x'.
"""

import argparse
import subprocess
import sys
import time

from pywinauto import Desktop

OPERATORS = {"+": "plusButton", "-": "minusButton", "*": "multiplyButton",
             "x": "multiplyButton", "/": "divideButton"}
DIVIDE_BY_ZERO_TEXT = "Cannot divide by zero"


def non_negative_int(value: str) -> int:
    """argparse 'type' function: accept only whole numbers >= 0."""
    if not value.isdigit():
        raise argparse.ArgumentTypeError(f"{value!r} is not a whole number >= 0")
    return int(value)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="calc_cli",
                                description="Verify Windows Calculator from the command line.")
    p.add_argument("a", type=non_negative_int, help="first number")
    p.add_argument("op", choices=list(OPERATORS), help="operator")
    p.add_argument("b", type=non_negative_int, help="second number")
    p.add_argument("--expected", help="override the expected display value")
    p.add_argument("--keep-open", action="store_true", help="do not close Calculator")
    return p


def expected_result(a: int, op: str, b: int) -> str:
    if op == "/" and b == 0:
        return DIVIDE_BY_ZERO_TEXT
    value = {"+": a + b, "-": a - b, "*": a * b, "x": a * b, "/": a / b if b else 0}[op]
    if float(value).is_integer():
        return str(int(value))
    return repr(float(value))


def same(expected: str, actual: str) -> bool:
    """Compare numbers with a small tolerance (Calculator rounds long decimals)."""
    try:
        return abs(float(expected) - float(actual)) < 1e-9
    except ValueError:
        return expected == actual


class CalculatorApp:
    """Tiny page-object style wrapper around the Calculator window."""

    def __init__(self, timeout: int = 10):
        self.win = Desktop(backend="uia").window(title="Calculator")
        if not self.win.exists(timeout=1):   # reuse an open Calculator: every calc.exe
            subprocess.Popen("calc.exe")   # launch opens ANOTHER window -> "2 elements match"
        self.win.wait("visible", timeout=timeout)
        self.win.set_focus()

    def press(self, auto_id: str) -> None:
        self.win.child_window(auto_id=auto_id, control_type="Button").invoke()

    def enter_number(self, number: int) -> None:
        for digit in str(number):
            self.press(f"num{digit}Button")

    def result(self) -> str:
        text = self.win.child_window(auto_id="CalculatorResults").window_text()
        return text.replace("Display is", "").strip().replace(",", "")

    def calculate(self, a: int, op: str, b: int) -> str:
        self.press("clearButton")
        self.enter_number(a)
        self.press(OPERATORS[op])
        self.enter_number(b)
        self.press("equalButton")
        return self.result()

    def close(self) -> None:
        self.win.close()


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    expected = args.expected or expected_result(args.a, args.op, args.b)

    app = CalculatorApp()
    try:
        actual = app.calculate(args.a, args.op, args.b)
    finally:
        if not args.keep_open:
            time.sleep(0.5)
            app.close()

    ok = same(expected, actual)
    print(f"{args.a} {args.op} {args.b}: expected={expected!r} actual={actual!r} "
          f"-> {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
