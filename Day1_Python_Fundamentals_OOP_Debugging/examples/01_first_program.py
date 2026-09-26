"""
Example 01 - Your First Python Program
=======================================
Day 1 | Topic: Python syntax and first program

How to run (from the examples folder):
    python 01_first_program.py

What this shows:
    * print() - the most used function for showing output
    * comments  - lines starting with # are ignored by Python
    * indentation - Python uses spaces (not { }) to group code
    * a tiny "test step" style output, like a tester would write
"""

# ---------------------------------------------------------------
# 1. The classic first program
# ---------------------------------------------------------------
print("Hello, Automation World!")

# ---------------------------------------------------------------
# 2. print() can take many values separated by commas.
#    Python adds a space between them automatically.
# ---------------------------------------------------------------
print("Course:", "Python Desktop Application Automation Testing")
print("Day:", 1)

# ---------------------------------------------------------------
# 3. Strings can use single quotes or double quotes - both are fine.
# ---------------------------------------------------------------
print('Single quotes work')
print("Double quotes work too")

# ---------------------------------------------------------------
# 4. Indentation matters!
#    The lines "inside" the if statement are indented by 4 spaces.
#    (We will learn "if" properly later - just notice the spacing.)
# ---------------------------------------------------------------
app_is_open = True
if app_is_open:
    print("Step 1: Application window is open")   # indented -> inside the if
    print("Step 2: Ready to start testing")        # indented -> inside the if
print("This line is NOT indented, so it always runs")

# ---------------------------------------------------------------
# 5. A very small "test script" style output
# ---------------------------------------------------------------
print()                      # an empty print() prints a blank line
print("=" * 40)              # "=" repeated 40 times -> a separator line
print("TEST CASE: TC_001 - Verify application title")
print("=" * 40)
expected_title = "Notepad"
actual_title = "Notepad"
print("Expected title :", expected_title)
print("Actual title   :", actual_title)
print("Result         :", "PASS" if expected_title == actual_title else "FAIL")
