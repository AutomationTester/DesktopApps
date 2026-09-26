"""
Example 14 - Print-based Debugging
===================================
Day 1 | Topic: Print-based debugging

How to run:
    python 14_print_debugging.py

Idea: add temporary print() lines to SEE what the program is doing -
values of variables, which branch was taken, how many times a loop ran.

Good habits:
    * Print the variable NAME with its value:  print(f"{total=}")
    * Print the TYPE when you suspect type problems: type(x)
    * Use repr (!r) to see hidden spaces:  'PASS ' vs 'PASS'
    * Use a DEBUG switch so you can turn prints off without deleting them
    * Graduate to the logging module for real frameworks
"""
import logging

DEBUG = True        # change to False to hide all debug prints


def debug(message):
    """Print only when DEBUG is switched on."""
    if DEBUG:
        print(f"  [DEBUG] {message}")


# ---------------------------------------------------------------
# A function with a hidden problem: some results have extra spaces
# or lower-case letters (very common when reading from files/screens)
# ---------------------------------------------------------------
def count_passed(results):
    passed = 0
    for index, status in enumerate(results):
        debug(f"index={index} status={status!r} type={type(status).__name__}")
        if status == "PASS":
            passed += 1
        else:
            debug(f"  -> not counted as PASS: {status!r}")
    debug(f"final {passed=}")
    return passed


results_from_file = ["PASS", "PASS ", "pass", "FAIL", "PASS"]

print("=== Step 1: run with debug prints ===")
count = count_passed(results_from_file)
print(f"Passed count reported: {count}  (we expected 4!)")

print("\nThe debug output shows 'PASS ' (trailing space) and 'pass' (lower case).")
print("Fix: clean the value before comparing -> status.strip().upper()")


def count_passed_fixed(results):
    passed = 0
    for status in results:
        clean = status.strip().upper()
        debug(f"raw={status!r:8} clean={clean!r}")
        if clean == "PASS":
            passed += 1
    return passed


print("\n=== Step 2: run the fixed version ===")
print(f"Passed count reported: {count_passed_fixed(results_from_file)}")

# ---------------------------------------------------------------
# The f-string "=" trick (Python 3.8+) prints name AND value
# ---------------------------------------------------------------
print("\n=== f-string = trick ===")
window_title = "Untitled - Notepad"
retry_count = 2
print(f"{window_title=}")
print(f"{retry_count=}, {retry_count * 5=}")

# ---------------------------------------------------------------
# Next level: logging (keeps levels and timestamps; can write to a file)
# ---------------------------------------------------------------
print("\n=== logging module (preferred in frameworks) ===")
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)-7s %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger("demo")
log.debug("Clicking 'Save' button")            # detailed info for debugging
log.info("File saved")                          # normal progress
log.warning("Save took 4.2s (SLA 3s)")          # something odd
log.error("Confirmation dialog not found")      # a failure

print("\nRemember: remove or switch off debug prints before committing code.")
