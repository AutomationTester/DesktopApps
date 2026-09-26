"""
02_calculator_pywinauto.py
==========================
Day 2 - Element-based automation of Windows 11 Calculator with pywinauto

WHY THIS EXAMPLE
    Calculator is a Store (UWP/WinUI) app. It exposes every button in the
    UI Automation tree with a stable AutomationId (auto_id), e.g. 'num7Button'.
    That makes it the perfect "hello world" for element-based automation.

KEY LESSONS
    1. Store apps need backend="uia".
    2. 'calc.exe' is only a LAUNCHER - it starts the real app and exits.
       So we do NOT keep the Application().start() handle; instead we
       launch with subprocess and CONNECT to the window through Desktop().
    3. Always WAIT for the window before touching it (.wait("visible")).
    4. Prefer invoke() (UIA pattern) over click_input() (real mouse click):
       invoke() works even if the window is partly covered.
    5. A test is not a test without VERIFICATION: read the result and assert.

HOW TO RUN
    python 02_calculator_pywinauto.py
"""

import re
import subprocess
import time

from pywinauto import Desktop

# Mapping from a character to the Calculator button's AutomationId.
# Found with Accessibility Insights / Inspect.exe / print_control_identifiers().
BUTTONS = {
    "0": "num0Button", "1": "num1Button", "2": "num2Button", "3": "num3Button",
    "4": "num4Button", "5": "num5Button", "6": "num6Button", "7": "num7Button",
    "8": "num8Button", "9": "num9Button",
    "+": "plusButton", "-": "minusButton", "*": "multiplyButton",
    "/": "divideButton", "=": "equalButton", "C": "clearButton",
}


def open_calculator(timeout: int = 10):
    """Launch Calculator and return a WindowSpecification connected to it."""
    calc = Desktop(backend="uia").window(title="Calculator")
    if not calc.exists(timeout=1):   # reuse an open Calculator: every calc.exe
        subprocess.Popen("calc.exe")   # launch opens ANOTHER window -> "2 elements match"
    calc.wait("visible", timeout=timeout)   # explicit wait - never time.sleep()
    return calc


def press(calc, key: str) -> None:
    """Press one Calculator button identified by its AutomationId."""
    auto_id = BUTTONS[key]
    calc.child_window(auto_id=auto_id, control_type="Button").invoke()


def enter(calc, expression: str) -> None:
    """Type a whole expression such as '12+30=' button by button."""
    for ch in expression.replace(" ", ""):
        press(calc, ch)


def read_result(calc) -> str:
    """Return the number shown in the display, e.g. '15' or '-3.5'."""
    # The display element's text is like: 'Display is 15'
    raw = calc.child_window(auto_id="CalculatorResults").window_text()
    number = raw.replace("Display is", "").strip()
    # Calculator formats large numbers with thousand separators: '1,234'
    return number.replace(",", "")


def check(calc, expression: str, expected: str) -> bool:
    """Run one test case, print PASS/FAIL and return True on pass."""
    press(calc, "C")                        # start from a known state!
    enter(calc, expression + "=")
    actual = read_result(calc)
    status = "PASS" if actual == expected else "FAIL"
    print(f"[{status}] {expression:<10} expected={expected:<6} actual={actual}")
    return actual == expected


def main() -> None:
    calc = open_calculator()
    calc.set_focus()
    print("Connected to:", calc.window_text())

    # Make sure we are in Standard mode (the header text shows the mode).
    # Not asserting strictly - just informative.
    try:
        header = calc.child_window(auto_id="Header").window_text()
        print("Calculator mode:", header)
    except Exception:
        pass

    # Data-driven test cases: (expression, expected display)
    test_cases = [
        ("7+8", "15"),
        ("9*6", "54"),
        ("50-80", "-30"),
        ("100/4", "25"),
    ]

    results = [check(calc, expr, exp) for expr, exp in test_cases]
    passed = sum(results)
    print(f"\nSummary: {passed}/{len(results)} passed")

    time.sleep(1)       # only so the audience can see the final state
    calc.close()        # safe here: Calculator holds no user data


if __name__ == "__main__":
    main()
