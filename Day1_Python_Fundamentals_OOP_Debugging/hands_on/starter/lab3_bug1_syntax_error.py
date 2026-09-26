"""
Lab 3 - Faulty Script 1: SYNTAX ERRORS
=======================================
How to run:
    python lab3_bug1_syntax_error.py

Purpose of the script:
    Check which expected application windows are open and print a summary.

Expected output after you fix it:
    Window availability check
    Calculator: FOUND
    Notepad: FOUND
    Paint: MISSING
    Missing windows: 1
    Result: FAIL

This file has 4 SYNTAX errors. Python shows them ONE AT A TIME.
Fix one, run again, fix the next... until it runs.
Tip: read the line number and the "^" marker in the error message.
     Sometimes the real mistake is on the line ABOVE the one reported.
"""

expected_windows = ["Calculator", "Notepad", "Paint"]
open_windows = ["Notepad", "Calculator", "File Explorer"]
missing_count = 0

print("Window availability check"

for window in expected_windows
    if window in open_windows:
        print(f"{window}: FOUND")
    else:
        print(f"{window}: MISSING)
        missing_count += 1

print("Missing windows:", missing_count)
if missing_count = 0:
    print("Result: PASS")
else:
    print("Result: FAIL")
