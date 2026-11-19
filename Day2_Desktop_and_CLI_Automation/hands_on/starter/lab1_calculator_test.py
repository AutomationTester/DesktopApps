"""
Lab 1 - STARTER: Automate Windows 11 Calculator and verify results

Complete every TODO. Run:  python lab1_calculator_test.py
Hints are in hands_on/Lab_Guide.md. Use Accessibility Insights / Inspect.exe
or calc.print_control_identifiers() to discover the AutomationIds.
"""

import subprocess
import sys
import time

from pywinauto import Desktop

# TODO 1: complete the mapping from key -> AutomationId
#         digits are 'num0Button' .. 'num9Button'
BUTTON_IDS = {
    "0": "num0Button",
    # "1": ...,
    "+": "plusButton",
    # "-": ..., "*": ..., "/": ..., "=": ..., "C": ...,
}

TEST_CASES = [
    # (expression, expected display text)
    ("2+3", "5"),
    # TODO 2: add at least 4 more cases: subtraction with a negative result,
    #         multiplication, division with a decimal result, a result >= 1000
]


def open_calculator(timeout: int = 10):
    """Start Calculator and return a window spec connected to it."""
    # TODO 3: start calc.exe with subprocess.Popen (it is only a launcher!)
    # TODO 4: connect: Desktop(backend="uia").window(title="Calculator")
    # TODO 5: wait until it is visible (timeout=timeout), then set_focus()
    raise NotImplementedError("open_calculator")


def click_button(calc, key: str) -> None:
    # TODO 6: find the child_window by auto_id AND control_type="Button", then invoke()
    raise NotImplementedError("click_button")


def get_display(calc) -> str:
    # TODO 7: read child_window(auto_id="CalculatorResults").window_text()
    #         It looks like 'Display is 1,000' -> return '1000'
    raise NotImplementedError("get_display")


def calculate(calc, expression: str) -> str:
    # TODO 8: press C first (known start state), press each key, press '=',
    #         then return get_display(calc)
    raise NotImplementedError("calculate")


def main() -> int:
    calc = open_calculator()
    passed = 0
    try:
        for expression, expected in TEST_CASES:
            actual = calculate(calc, expression)
            # TODO 9: compare, count passes and print a PASS/FAIL line
            pass
    finally:
        time.sleep(0.5)
        # TODO 10: close Calculator (safe - it holds no user data)
    total = len(TEST_CASES)
    print(f"\nResult: {passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
