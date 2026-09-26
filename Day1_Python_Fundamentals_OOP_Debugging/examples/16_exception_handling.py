"""
Example 16 - Exception Handling (try, except, else, finally, raise)
====================================================================
Day 1 | Topic: Exception handling

How to run:
    python 16_exception_handling.py

try     -> code that MIGHT fail
except  -> what to do IF it fails (catch specific errors first)
else    -> runs only if NO error happened
finally -> ALWAYS runs (error or not) - perfect for cleanup:
           close the app, close files, take a final screenshot
raise   -> create an error yourself when something is wrong
"""


# ---------------------------------------------------------------
# 1. Basic try / except
# ---------------------------------------------------------------
print("--- 1. Basic try / except ---")
text_from_screen = "12a"
try:
    value = int(text_from_screen)
    print("Converted:", value)
except ValueError:
    print(f"Could not convert {text_from_screen!r} to a number - test marked FAIL")

# ---------------------------------------------------------------
# 2. Multiple except blocks + capturing the error object
# ---------------------------------------------------------------
print("\n--- 2. Multiple except blocks ---")


def get_pass_rate(summary, key):
    try:
        passed = summary["passed"]
        total = summary[key]
        return passed / total * 100
    except KeyError as error:
        print(f"  Missing key in summary: {error}")
    except ZeroDivisionError:
        print("  No tests were executed - cannot calculate pass rate")
    except TypeError as error:
        print(f"  Wrong data type in summary: {error}")
    return None


print(get_pass_rate({"passed": 8, "total": 10}, "total"))
print(get_pass_rate({"passed": 8, "total": 10}, "executed"))
print(get_pass_rate({"passed": 0, "total": 0}, "total"))
print(get_pass_rate({"passed": "8", "total": 10}, "total"))

# ---------------------------------------------------------------
# 3. try / except / else / finally - the full structure
# ---------------------------------------------------------------
print("\n--- 3. try / except / else / finally ---")


def run_test(test_name, should_fail):
    print(f"Running {test_name}")
    try:
        print("  launching application (simulated)")
        if should_fail:
            raise RuntimeError("Save button not found")
        print("  steps executed")
    except RuntimeError as error:
        print(f"  FAIL - {error}")
    else:
        print("  PASS - no errors")
    finally:
        print("  closing application (always runs)")


run_test("TC_021 Save file", should_fail=False)
run_test("TC_022 Save file as", should_fail=True)

# ---------------------------------------------------------------
# 4. raise - validate input and fail loudly
# ---------------------------------------------------------------
print("\n--- 4. raise your own errors ---")


def set_timeout(seconds):
    if seconds <= 0:
        raise ValueError(f"Timeout must be positive, got {seconds}")
    return seconds


for value in (10, -1):
    try:
        print("Timeout set to", set_timeout(value))
    except ValueError as error:
        print("Error:", error)

# ---------------------------------------------------------------
# 5. Custom exception class (OOP + exceptions)
# ---------------------------------------------------------------
print("\n--- 5. Custom exception ---")


class WindowNotFoundError(Exception):
    """Raised when an expected application window is not present."""


def find_window(title, open_windows):
    if title not in open_windows:
        raise WindowNotFoundError(f"Window '{title}' not found. Open windows: {open_windows}")
    return title


open_windows = ["Notepad", "File Explorer"]
for wanted in ("Notepad", "Calculator"):
    try:
        print("Found:", find_window(wanted, open_windows))
    except WindowNotFoundError as error:
        print("WindowNotFoundError:", error)

# ---------------------------------------------------------------
# 6. Retry pattern - very common in desktop automation
# ---------------------------------------------------------------
print("\n--- 6. Retry pattern ---")
attempts_needed = 3          # pretend the window appears on the 3rd try


def click_ok(attempt):
    if attempt < attempts_needed:
        raise WindowNotFoundError("OK dialog not visible yet")
    return "clicked OK"


for attempt in range(1, 6):
    try:
        print(f"Attempt {attempt}:", click_ok(attempt))
        break
    except WindowNotFoundError as error:
        print(f"Attempt {attempt}: {error} - retrying")
else:
    # a for-loop "else" runs only if the loop did NOT break
    print("Gave up after 5 attempts")

# ---------------------------------------------------------------
# 7. finally with files - (a 'with' block does this cleanup for you)
# ---------------------------------------------------------------
print("\n--- 7. Cleanup with files ---")
try:
    with open("does_not_exist.csv") as data_file:
        rows = data_file.readlines()
except FileNotFoundError as error:
    print(f"Test data file missing: {error.filename} - test BLOCKED")

print("\nTips:")
print("  * Catch SPECIFIC errors (ValueError, KeyError) - not a bare 'except:'")
print("  * Never hide errors silently with 'except: pass' in test code")
print("  * In test scripts a failure should be VISIBLE in the report")
