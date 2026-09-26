"""
Day 4 - Example 01: Logging basics
==================================
Shows WHY print() is not enough and HOW the Python logging module works:
  * the 5 standard log levels
  * basicConfig() with a format string
  * named loggers (one per module)
  * logging exceptions with a full traceback (logger.exception)

Run:
    python 01_logging_basics.py
"""
import logging
import sys

# ---------------------------------------------------------------------------
# 1. print() vs logging
# ---------------------------------------------------------------------------
print("print(): no time, no level, no source, cannot be switched off or sent to a file")

# ---------------------------------------------------------------------------
# 2. Configure the ROOT logger once, at program start.
#    level=DEBUG  -> show everything from DEBUG upwards
#    format       -> what each line looks like
# ---------------------------------------------------------------------------
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt="%H:%M:%S",
                    stream=sys.stdout)  # stdout keeps print() and log lines in order

# ---------------------------------------------------------------------------
# 3. Get a NAMED logger. Convention: logging.getLogger(__name__)
# ---------------------------------------------------------------------------
log = logging.getLogger("demo.calculator_test")


def demo_levels():
    """The 5 standard levels, lowest to highest severity."""
    log.debug("DEBUG    (10): locator details, raw values -> developers only")
    log.info("INFO     (20): normal milestones - 'Calculator opened'")
    log.warning("WARNING  (30): unexpected but test continues - 'retrying click'")
    log.error("ERROR    (40): a step failed - 'Result field not found'")
    log.critical("CRITICAL (50): cannot continue - 'Application crashed'")


def demo_lazy_formatting():
    """Use %s placeholders: the string is only built if the level is enabled."""
    a, b = 7, 5
    log.info("Calculating %s + %s", a, b)          # recommended
    log.info(f"Calculating {a} + {b} (f-string also works, slightly less efficient)")


def demo_exception_logging():
    """logger.exception() = ERROR level + full traceback. Use inside except."""
    try:
        result = 10 / 0
        log.info("Result %s", result)
    except ZeroDivisionError:
        log.exception("Division step failed")


def demo_changing_level():
    """Raise the threshold: DEBUG and INFO disappear, WARNING+ remain."""
    print("\n--- Setting logger level to WARNING ---")
    log.setLevel(logging.WARNING)
    log.debug("You will NOT see this")
    log.info("You will NOT see this either")
    log.warning("You WILL see this warning")
    log.setLevel(logging.DEBUG)


if __name__ == "__main__":
    print("\n--- The 5 log levels ---")
    demo_levels()
    print("\n--- Lazy formatting ---")
    demo_lazy_formatting()
    print("\n--- Logging an exception ---")
    demo_exception_logging()
    demo_changing_level()
    print("\nDone. Notice every line carries time, level, logger name, function and line number.")
