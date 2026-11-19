"""
Lab 3 - Faulty Script 1: SYNTAX ERRORS (FIXED)
===============================================
How to run:
    python lab3_bug1_syntax_error.py

Bugs fixed (in the order Python reports them):
  1. print("Window availability check"      -> missing ")"
     Python reported "invalid syntax" on a LATER line (the 'if' line),
     because it was still looking for the closing bracket.
  2. for window in expected_windows         -> missing ":" at the end
     Message: SyntaxError: expected ':'
  3. print(f"{window}: MISSING)             -> missing closing quote
     Message: SyntaxError: unterminated f-string literal
  4. if missing_count = 0:                  -> "=" assigns, "==" compares
     Message: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
"""

expected_windows = ["Calculator", "Notepad", "Paint"]
open_windows = ["Notepad", "Calculator", "File Explorer"]
missing_count = 0

print("Window availability check")              # FIX 1: closed the bracket

for window in expected_windows:                 # FIX 2: added the colon
    if window in open_windows:
        print(f"{window}: FOUND")
    else:
        print(f"{window}: MISSING")             # FIX 3: closed the string
        missing_count += 1

print("Missing windows:", missing_count)
if missing_count == 0:                          # FIX 4: == for comparison
    print("Result: PASS")
else:
    print("Result: FAIL")
