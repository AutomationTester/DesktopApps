"""
Lab 3 - Faulty Script 4: LOGIC ERRORS (no crash, wrong answers!)
=================================================================
How to run:
    python lab3_bug4_logic_error.py

Purpose of the script:
    Helper functions used in a test report. The bottom of the file checks
    each function against the EXPECTED value.

This script runs WITHOUT any error message - but some answers are wrong.
Logic errors are the hardest to find. Use:
    * print-based debugging (print variables inside loops)
    * VS Code breakpoints + Step Over (F10) / Step Into (F11)

There are 3 logic bugs (one in each function). Target: all checks PASS.
"""


def classify_response(seconds):
    """FAST if <= 1s, SLOW if more than 1s up to 3s, VERY SLOW if more than 3s."""
    if seconds > 1:
        return "SLOW"
    elif seconds > 3:
        return "VERY SLOW"
    else:
        return "FAST"


def count_failures(results):
    """Return how many items in results are 'FAIL'."""
    failures = 0
    for i in range(1, len(results)):
        if results[i] == "FAIL":
            failures += 1
    return failures


def all_passed(results):
    """Return True only if EVERY result is 'PASS'."""
    for result in results:
        if result == "PASS":
            return True
    return False


# ---------------- checks (do not change) ----------------
checks = [
    ("classify_response(0.5)", classify_response(0.5), "FAST"),
    ("classify_response(2.0)", classify_response(2.0), "SLOW"),
    ("classify_response(4.5)", classify_response(4.5), "VERY SLOW"),
    ("count_failures([FAIL, PASS, FAIL])", count_failures(["FAIL", "PASS", "FAIL"]), 2),
    ("count_failures([PASS, PASS])", count_failures(["PASS", "PASS"]), 0),
    ("all_passed([PASS, PASS])", all_passed(["PASS", "PASS"]), True),
    ("all_passed([PASS, FAIL])", all_passed(["PASS", "FAIL"]), False),
]

passed = 0
for name, actual, expected in checks:
    status = "PASS" if actual == expected else "FAIL"
    passed += status == "PASS"
    print(f"{name:38} expected={expected!s:10} actual={actual!s:10} {status}")
print(f"\nChecks passed: {passed}/{len(checks)}")
