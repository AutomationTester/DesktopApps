"""
Lab 3 - Faulty Script 3: RUNTIME ERROR (TypeError)
===================================================
How to run:
    python lab3_bug3_type_error.py

Purpose of the script:
    Print one summary line per test suite.

Expected output after you fix it:
    Suite Login: 5/6 passed (83.3%)
    Suite Billing: 7/9 passed (77.8%)
    Suite Reports: 4/4 passed (100.0%)

This file has 3 bugs. Each one raises a TypeError - but for a
DIFFERENT reason. Read each error message carefully.
Hint: numbers read from files often arrive as TEXT (str).
"""


def build_summary(suite_name, passed, failed):
    """Return a one-line summary for a suite."""
    total = passed + failed
    percent = passed / total * 100
    return "Suite " + suite_name + ": " + passed + "/" + str(total) + f" passed ({percent:.1f}%)"


print(build_summary("Login", 5, 1))

# the Billing numbers were read from a CSV file, so they arrived as text
billing_passed = "7"
billing_failed = "2"
print(build_summary("Billing", billing_passed, billing_failed))

print(build_summary("Reports", 4))
