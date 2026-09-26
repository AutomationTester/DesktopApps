"""
Example 17 - Debugging Demo (BUGGY VERSION - fails on purpose!)
================================================================
Day 1 | Topic: Debugging faulty scripts (live demo)

How to run:
    python 17_debugging_demo_buggy.py

This script is SUPPOSED to print a test execution summary:
    Total: 6 | Passed: 3
    Failed: 2 | Skipped: 1 | Pass rate: 60.0%
    Total duration: 16.0 seconds
    (pass rate = passed / executed, where executed = passed + failed)

It contains 4 intentional bugs (2 crash the script,
2 give WRONG output). Find them using:
    1. The traceback (read the LAST line first)
    2. print-based debugging
    3. VS Code breakpoints + step over / step into

DO NOT look at 17_debugging_demo_fixed.py until you have tried!
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
        counts[result["Status"]] += 1
    return counts


def pass_rate(counts):
    executed = counts["PASS"] + counts["FAIL"] + counts["SKIP"]
    return counts["PASS"] / executed * 100


def total_duration(results):
    total = 0
    for result in results:
        total = result["duration"]
    return total


counts = count_by_status(test_run)
rate = pass_rate(counts)
print("Total: " + len(test_run) + " | Passed: " + str(counts["PASS"]))
print(f"Failed: {counts['FAIL']} | Skipped: {counts['SKIP']} | Pass rate: {rate:.1f}%")
print(f"Total duration: {total_duration(test_run)} seconds")
