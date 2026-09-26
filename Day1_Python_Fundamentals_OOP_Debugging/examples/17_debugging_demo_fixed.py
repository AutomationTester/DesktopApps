"""
Example 17 - Debugging Demo (FIXED VERSION)
============================================
Day 1 | Topic: Debugging faulty scripts (live demo - answer)

How to run:
    python 17_debugging_demo_fixed.py

Expected output:
    Total: 6 | Passed: 3
    Failed: 2 | Skipped: 1 | Pass rate: 60.0%
    Total duration: 16.0 seconds

The 4 bugs that were in 17_debugging_demo_buggy.py:

BUG 1 (runtime - KeyError: 'Status')
    counts[result["Status"]]  -> dictionary keys are CASE-SENSITIVE.
    The key is "status". Found by: reading the last line of the traceback.

BUG 2 (runtime - TypeError: can only concatenate str (not "int") to str)
    "Total: " + len(test_run)  -> cannot join text and a number with +.
    Fix: use an f-string (or str()). Found by: traceback, appears only
    AFTER bug 1 is fixed (errors show up one at a time!).

BUG 3 (logic - wrong pass rate 50.0% instead of 60.0%)
    executed included SKIP tests. Skipped tests were not executed.
    Found by: comparing actual vs expected output, then a breakpoint
    in pass_rate() and looking at 'executed' in the Variables panel.

BUG 4 (logic - total duration 1.3 instead of 16.0)
    total = result["duration"] REPLACES the value every loop.
    It must ADD: total += result["duration"].
    Found by: print(f"{total=}") inside the loop, or Step Over (F10)
    through the loop and watching 'total'.

Lesson: runtime errors shout (traceback); logic errors whisper (wrong
output, no error). Always compare ACTUAL with EXPECTED - like a tester!
"""

test_run = [
    {"id": "TC_101", "name": "Open app", "status": "PASS", "duration": 2.1},
    {"id": "TC_102", "name": "Login", "status": "PASS", "duration": 3.4},
    {"id": "TC_103", "name": "Create invoice", "status": "FAIL", "duration": 5.0},
    {"id": "TC_104", "name": "Print invoice", "status": "SKIP", "duration": 0},
    {"id": "TC_105", "name": "Export PDF", "status": "PASS", "duration": 4.2},
    {"id": "TC_106", "name": "Logout", "status": "FAIL", "duration": 1.3},
]


def count_by_status(results):
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    for result in results:
        counts[result["status"]] += 1          # FIX 1: correct key "status"
    return counts


def pass_rate(counts):
    executed = counts["PASS"] + counts["FAIL"]  # FIX 3: skipped tests are not executed
    if executed == 0:                           # bonus: protect against ZeroDivisionError
        return 0.0
    return counts["PASS"] / executed * 100


def total_duration(results):
    total = 0
    for result in results:
        total += result["duration"]             # FIX 4: add, do not replace
    return round(total, 2)                      # round to hide float noise (15.999999...)


counts = count_by_status(test_run)
rate = pass_rate(counts)
print(f"Total: {len(test_run)} | Passed: {counts['PASS']}")   # FIX 2: f-string
print(f"Failed: {counts['FAIL']} | Skipped: {counts['SKIP']} | Pass rate: {rate:.1f}%")
print(f"Total duration: {total_duration(test_run)} seconds")
