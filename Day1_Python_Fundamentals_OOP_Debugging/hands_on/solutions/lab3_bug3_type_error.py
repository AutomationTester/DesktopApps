"""
Lab 3 - Faulty Script 3: RUNTIME ERROR (TypeError) (FIXED)
===========================================================
How to run:
    python lab3_bug3_type_error.py

Bugs fixed:
  1. TypeError: can only concatenate str (not "int") to str
     "Suite " + ... + passed  -> cannot join text and a number with "+".
     Fix: build the text with an f-string.
  2. TypeError: unsupported operand type(s) for /: 'str' and 'str'
     The Billing values were TEXT ("7", "2"). "7" + "2" gave "72" (joined,
     not added!) and then dividing text failed. Fix: convert with int()
     when the data is read.
  3. TypeError: build_summary() missing 1 required positional argument: 'failed'
     The Reports call passed only 2 of the 3 arguments. Fix: pass failed=0.
"""


def build_summary(suite_name, passed, failed):
    """Return a one-line summary for a suite."""
    total = passed + failed
    percent = passed / total * 100
    return f"Suite {suite_name}: {passed}/{total} passed ({percent:.1f}%)"   # FIX 1


print(build_summary("Login", 5, 1))

# the Billing numbers were read from a CSV file, so they arrived as text
billing_passed = int("7")          # FIX 2: convert text to numbers
billing_failed = int("2")
print(build_summary("Billing", billing_passed, billing_failed))

print(build_summary("Reports", 4, 0))    # FIX 3: pass all three arguments
