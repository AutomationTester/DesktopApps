"""
A tiny SIMULATED desktop with a Calculator window.

It copies the parts of the pywinauto API our framework uses, so the framework
code is the same as for the real app:

    desktop.window(title="Calculator")          -> WindowSpec
    window.wait("visible", timeout=5)
    window.child_window(auto_id="num7Button")   -> ElementSpec
    element.wait("exists", timeout=3)
    element.invoke() / element.click_input()
    element.window_text()

auto_ids are the real Windows 11 Calculator ones (num0Button..num9Button,
plusButton, equalButton, clearButton, CalculatorResults ...).

The window appears only after `startup_delay` seconds and clicks fail randomly
with probability `flaky_click_rate` (never twice in a row) - so waits and retries are really needed.
"""
import random
import time


class ElementNotFoundError(Exception):
    pass


class FlakyClickError(Exception):
    pass


class _CalculatorEngine:
    OPS = {"plusButton": "+", "minusButton": "-", "multiplyButton": "*", "divideButton": "/"}

    def __init__(self):
        self.clear()

    def clear(self):
        self.entry = "0"
        self.stored = None
        self.op = None
        self.fresh = True
        self.error = None

    def press(self, auto_id):
        if auto_id == "clearButton":
            self.clear()
        elif auto_id.startswith("num") and auto_id.endswith("Button"):
            digit = auto_id[3]
            self.entry = digit if self.fresh or self.entry == "0" else self.entry + digit
            self.fresh = False
        elif auto_id == "negateButton":
            self.entry = self.entry[1:] if self.entry.startswith("-") else "-" + self.entry
        elif auto_id in self.OPS:
            self.stored, self.op, self.fresh = float(self.entry), self.OPS[auto_id], True
        elif auto_id == "equalButton" and self.op:
            a, b = self.stored, float(self.entry)
            if self.op == "/" and b == 0:
                self.error = "Cannot divide by zero"
                return
            value = {"+": a + b, "-": a - b, "*": a * b, "/": a / b if b else 0}[self.op]
            self.entry = f"{value:g}"
            self.op, self.fresh = None, True

    def display(self):
        return self.error or f"Display is {self.entry}"


class ElementSpec:
    def __init__(self, window, criteria):
        self.window, self.criteria = window, criteria

    def _resolve(self):
        for element in self.window.elements:
            if all(element.get(k) == v for k, v in self.criteria.items()):
                return element
        raise ElementNotFoundError(f"No element matches {self.criteria}")

    def exists(self, timeout=0):
        try:
            return self.window.is_visible() and bool(self._resolve())
        except ElementNotFoundError:
            return False

    def wait(self, state, timeout=5):
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            if self.exists():
                return self
            time.sleep(0.05)
        raise ElementNotFoundError(f"{self.criteria} not '{state}' after {timeout}s")

    def invoke(self):
        element = self._resolve()
        # Fail randomly, but never twice in a row -> a retry of 2+ attempts always recovers
        if not self.window.last_click_failed and self.window.rng.random() < self.window.flaky_click_rate:
            self.window.last_click_failed = True
            raise FlakyClickError(f"{element['auto_id']} did not respond (simulated flakiness)")
        self.window.last_click_failed = False
        self.window.engine.press(element["auto_id"])

    click_input = invoke

    def window_text(self):
        element = self._resolve()
        if element["auto_id"] == "CalculatorResults":
            return self.window.engine.display()
        return element["title"]


class WindowSpec:
    def __init__(self, title, startup_delay, flaky_click_rate, seed):
        self.title = title
        self.opened_at = time.monotonic()
        self.startup_delay = startup_delay
        self.flaky_click_rate = flaky_click_rate
        self.rng = random.Random(seed)
        self.engine = _CalculatorEngine()
        self.closed = False
        self.last_click_failed = False
        names = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        self.elements = [{"auto_id": f"num{d}Button", "title": names[d], "control_type": "Button"}
                         for d in range(10)]
        self.elements += [
            {"auto_id": "plusButton", "title": "Plus", "control_type": "Button"},
            {"auto_id": "minusButton", "title": "Minus", "control_type": "Button"},
            {"auto_id": "multiplyButton", "title": "Multiply by", "control_type": "Button"},
            {"auto_id": "divideButton", "title": "Divide by", "control_type": "Button"},
            {"auto_id": "equalButton", "title": "Equals", "control_type": "Button"},
            {"auto_id": "clearButton", "title": "Clear", "control_type": "Button"},
            {"auto_id": "negateButton", "title": "Positive negative", "control_type": "Button"},
            {"auto_id": "CalculatorResults", "title": "Display", "control_type": "Text"},
        ]

    def is_visible(self):
        return not self.closed and time.monotonic() - self.opened_at >= self.startup_delay

    def exists(self, timeout=0):
        return self.is_visible()

    def wait(self, state, timeout=5):
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            if self.is_visible():
                return self
            time.sleep(0.05)
        raise ElementNotFoundError(f"Window '{self.title}' not '{state}' after {timeout}s")

    def window_text(self):
        return self.title

    def child_window(self, **criteria):
        return ElementSpec(self, criteria)

    def close(self):
        self.closed = True


class SimulatedDesktop:
    """Stand-in for pywinauto.Desktop(backend='uia')."""

    def __init__(self):
        self._windows = {}

    def launch(self, title, startup_delay=0.5, flaky_click_rate=0.0, seed=7):
        """Like subprocess.Popen('calc.exe'): the window shows up a bit later."""
        self._windows[title] = WindowSpec(title, startup_delay, flaky_click_rate, seed)

    def window(self, title):
        if title not in self._windows:
            raise ElementNotFoundError(f"No window titled '{title}' (was the app launched?)")
        return self._windows[title]
