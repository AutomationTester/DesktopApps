"""
Pure-Python "application under test" for the pytest demo.

It stands in for the desktop Calculator so every pytest concept can be taught
without launching a GUI. In the real framework the equivalent calls go through
pages/calculator_page.py (CalculatorPage.calculate(a, op, b)).
"""
import logging

log = logging.getLogger(__name__)

SUPPORTED_OPS = ("+", "-", "*", "/")


class Calculator:
    def __init__(self):
        self.history = []
        self.is_open = False

    # --- lifecycle (mimics open/close of a desktop app) -------------------
    def open(self):
        self.is_open = True
        log.info("Calculator opened")
        return self

    def close(self):
        self.is_open = False
        log.info("Calculator closed")

    def clear(self):
        self.history.clear()
        log.debug("History cleared")

    # --- business logic ----------------------------------------------------
    def calculate(self, a, op, b):
        if not self.is_open:
            raise RuntimeError("Calculator is not open")
        if op not in SUPPORTED_OPS:
            raise ValueError(f"Unsupported operator: {op!r}")
        a, b = float(a), float(b)
        log.debug("calculate(%s %s %s)", a, op, b)
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        else:
            if b == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            result = a / b
        self.history.append((a, op, b, result))
        log.info("%s %s %s = %s", a, op, b, result)
        return result

    def percentage(self, value, percent):
        """Known bug (for the xfail demo): uses integer division."""
        return value * percent // 100


def is_valid_username(name: str) -> bool:
    """5..12 characters, ASCII letters and digits only."""
    return isinstance(name, str) and 5 <= len(name) <= 12 and name.isascii() and name.isalnum()
