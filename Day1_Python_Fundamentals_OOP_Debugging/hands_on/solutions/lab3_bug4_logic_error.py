"""
Lab 3 - Faulty Script 4: LOGIC ERRORS (FIXED)
==============================================
How to run:
    python lab3_bug4_logic_error.py

Bugs fixed:
  1. classify_response: conditions were in the wrong ORDER. 4.5 > 1 is
     True, so "SLOW" was returned before "> 3" was ever checked.
     Fix: check the biggest limit first.
  2. count_failures: range(1, len(results)) starts at index 1, so the
     FIRST result was never checked ("off-by-one" error).
     Fix: loop over the list directly (no index needed).
  3. all_passed: returned True as soon as it saw ONE "PASS".
     Fix: return False as soon as a non-PASS is found; return True only
     after the whole loop finishes. (Or simply: all(r == "PASS" for r in results))
"""


def classify_response(seconds):
    """FAST if <= 1s, SLOW if more than 1s up to 3s, VERY SLOW if more than 3s."""
    if seconds > 3:                 # FIX 1: biggest limit first
        return "VERY SLOW"
    elif seconds > 1:
        return "SLOW"
    else:
        return "FAST"


def count_failures(results):
    """Return how many items in results are 'FAIL'."""
    failures = 0
    for result in results:          # FIX 2: check every item (no off-by-one)
        if result == "FAIL":
            failures += 1
    return failures


def all_passed(results):
    """Return True only if EVERY result is 'PASS'."""
    for result in results:
        if result != "PASS":        # FIX 3: stop at the first NON-pass
            return False
    return True                     # every item was PASS


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
