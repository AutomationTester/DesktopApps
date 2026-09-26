"""
Lab 4 - STARTER: calc_cli.py - pass arguments to a GUI automation script

Target usage:
    python calc_cli.py 12 + 30          -> 12 + 30: expected='42' actual='42' -> PASS
    python calc_cli.py 9 x 6            ('x' also means multiply)
    python calc_cli.py 12 + 30 --expected 43      (deliberate FAIL, exit code 1)

Exit codes: 0 = PASS, 1 = FAIL, 2 = bad arguments (argparse does this for you)
Tip: reuse your code from Lab 1!
"""

import argparse
import subprocess
import sys
import time

from pywinauto import Desktop

OPERATORS = {"+": "plusButton", "-": "minusButton", "*": "multiplyButton",
             "x": "multiplyButton", "/": "divideButton"}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="calc_cli",
                                description="Verify Windows Calculator from the command line.")
    # TODO 1: positional 'a'  (type=int)
    # TODO 2: positional 'op' (choices=list(OPERATORS))
    # TODO 3: positional 'b'  (type=int)
    # TODO 4: optional --expected (string) to override the expected value
    return p


def expected_result(a: int, op: str, b: int) -> str:
    # TODO 5: compute the expected display text in Python (the test ORACLE)
    #         return '42' for 12 + 30, '2.5' for 10 / 4
    #         stretch: 'Cannot divide by zero' for x / 0
    raise NotImplementedError("expected_result")


def run_in_calculator(a: int, op: str, b: int) -> str:
    # TODO 6: Popen("calc.exe"), connect via Desktop(backend="uia"), wait visible
    # TODO 7: press clearButton, digits of a, operator, digits of b, equalButton
    # TODO 8: read CalculatorResults, strip 'Display is' and commas
    # TODO 9: close Calculator, return the text
    raise NotImplementedError("run_in_calculator")


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    # TODO 10: expected = args.expected or expected_result(...)
    #          actual = run_in_calculator(...)
    #          print one line with expected, actual and PASS/FAIL
    #          return 0 for PASS, 1 for FAIL
    return 1


if __name__ == "__main__":
    sys.exit(main())
