"""
Lab 1 - SOLUTION: Automate Windows 11 Calculator and verify results

Run:  python lab1_calculator_test.py
Exit code: 0 if all test cases pass, 1 otherwise.
"""

import subprocess
import sys
import time

from pywinauto import Desktop

BUTTON_IDS = {
    **{str(d): f"num{d}Button" for d in range(10)},
    "+": "plusButton",
    "-": "minusButton",
    "*": "multiplyButton",
    "/": "divideButton",
    "=": "equalButton",
    "C": "clearButton",
}

TEST_CASES = [
    # (expression, expected display text)
    ("2+3", "5"),
    ("7*8", "56"),
    ("15-20", "-5"),
    ("144/12", "12"),
    ("10/4", "2.5"),
    ("999+1", "1000"),      # display shows '1,000' -> we strip the comma
]


def open_calculator(timeout: int = 10):
    """Start Calculator and connect to its window (calc.exe is a launcher)."""
    calc = Desktop(backend="uia").window(title="Calculator")
    if not calc.exists(timeout=1):   # reuse an open Calculator: every calc.exe
        subprocess.Popen("calc.exe")   # launch opens ANOTHER window -> "2 elements match"
    calc.wait("visible", timeout=timeout)
    calc.set_focus()
    return calc


def click_button(calc, key: str) -> None:
    calc.child_window(auto_id=BUTTON_IDS[key], control_type="Button").invoke()


def get_display(calc) -> str:
    text = calc.child_window(auto_id="CalculatorResults").window_text()
    return text.replace("Display is", "").strip().replace(",", "")


def calculate(calc, expression: str) -> str:
    click_button(calc, "C")                 # known start state
    for key in expression:
        click_button(calc, key)
    click_button(calc, "=")
    return get_display(calc)


def main() -> int:
    calc = open_calculator()
    passed = 0
    try:
        for expression, expected in TEST_CASES:
            actual = calculate(calc, expression)
            ok = actual == expected
            passed += ok
            print(f"[{'PASS' if ok else 'FAIL'}] {expression:<8} = {actual:<8} (expected {expected})")
    finally:
        time.sleep(0.5)
        calc.close()                        # Calculator holds no user data
    total = len(TEST_CASES)
    print(f"\nResult: {passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
