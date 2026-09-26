"""
Example 12 - Automation-oriented OOP Example
=============================================
Day 1 | Topic: Automation-oriented OOP examples

How to run:
    python 12_automation_oop_example.py

This script puts EVERYTHING from the OOP session together in a small,
simulated "framework" for a Calculator desktop app. No real GUI is used -
a FakeCalculatorApp class pretends to be the application. From Day 2 you
will replace it with real pywinauto code, but the STRUCTURE stays the same.

Framework pieces (just like real projects):
    FakeCalculatorApp -> the "application under test" (simulated)
    BaseScreen        -> common actions (parent class)
    CalculatorScreen  -> page/screen object with calculator actions (child)
    TestResult        -> stores the result of one test
    TestRunner        -> runs tests and prints a report
"""
from datetime import datetime


# ======================= Application (simulated) =======================
class FakeCalculatorApp:
    """Pretends to be Windows Calculator. Stores what is typed and computes."""

    def __init__(self):
        self.display = "0"
        self._expression = ""

    def press(self, key):
        if key == "C":
            self._expression, self.display = "", "0"
        elif key == "=":
            # eval is fine here because WE control the input (demo only)
            self.display = str(eval(self._expression))
            self._expression = self.display
        else:
            self._expression += key
            self.display = self._expression


# ======================= Framework layer =======================
class BaseScreen:
    """Parent class: behaviour every screen needs."""

    def __init__(self, app, name):
        self.app = app
        self.name = name

    def log(self, message):
        print(f"    [{self.name}] {message}")


class CalculatorScreen(BaseScreen):
    """Screen object: hides HOW we talk to the app behind simple methods."""

    def __init__(self, app):
        super().__init__(app, "Calculator")

    def clear(self):
        self.app.press("C")
        self.log("Pressed C")

    def enter(self, text):
        for key in text:                # press each character one by one
            self.app.press(key)
        self.log(f"Typed '{text}'")

    def equals(self):
        self.app.press("=")
        self.log("Pressed =")

    def read_display(self):
        return self.app.display


class TestResult:
    """Holds the outcome of one test case."""

    def __init__(self, test_id, expected, actual):
        self.test_id = test_id
        self.expected = expected
        self.actual = actual
        self.status = "PASS" if expected == actual else "FAIL"


class TestRunner:
    """Runs test data through the screen object and reports."""

    def __init__(self, screen):
        self.screen = screen
        self.results = []

    def run_calculation_test(self, test_id, expression, expected):
        print(f"  Running {test_id}: {expression} = {expected}?")
        self.screen.clear()
        self.screen.enter(expression)
        self.screen.equals()
        actual = self.screen.read_display()
        self.results.append(TestResult(test_id, expected, actual))

    def report(self):
        print("\n" + "=" * 50)
        print(f" TEST REPORT  ({datetime.now():%Y-%m-%d %H:%M})")
        print("=" * 50)
        for r in self.results:
            print(f" {r.test_id:8} expected={r.expected:>6} actual={r.actual:>6}  {r.status}")
        passed = sum(1 for r in self.results if r.status == "PASS")
        print("-" * 50)
        print(f" Total={len(self.results)}  Passed={passed}  Failed={len(self.results) - passed}")


# ======================= Test layer =======================
test_data = [
    ("CALC_01", "2+3", "5"),
    ("CALC_02", "9-4", "5"),
    ("CALC_03", "6*7", "42"),
    ("CALC_04", "8/2", "4"),        # real result is "4.0" -> intentional FAIL to discuss
]

app = FakeCalculatorApp()
screen = CalculatorScreen(app)
runner = TestRunner(screen)

print("Starting calculator test suite...\n")
for test_id, expression, expected in test_data:
    runner.run_calculation_test(test_id, expression, expected)
runner.report()

print("\nDiscussion: why did CALC_04 fail? Is it an app bug or a test bug?")
