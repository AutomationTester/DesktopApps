"""
Example 13 - Common Python and Automation Errors
=================================================
Day 1 | Topic: Common Python and automation errors

How to run:
    python 13_common_errors.py

Each small demo below CAUSES a common error on purpose and then CATCHES it,
so the script keeps running and you can see the error name and message.
Learn to READ the error name - it tells you what kind of problem it is.

Reading a traceback (when an error is NOT caught):
    Traceback (most recent call last):
      File "script.py", line 12, in <module>     <- WHERE (file + line)
        print(results["TC_09"])                   <- the failing line
    KeyError: 'TC_09'                             <- WHAT (type: message)
    -> Always read the LAST line first, then the line number above it.
"""


def show(error_title, func):
    """Run func(); if it raises an error, print its type and message."""
    print(f"\n--- {error_title} ---")
    try:
        func()
        print("No error")
    except Exception as error:               # catch any normal error
        print(f"{type(error).__name__}: {error}")


# 1. SyntaxError - Python cannot even understand the code (missing colon)
#    We use compile() so that THIS file itself still runs.
def syntax_error():
    compile("if status == 'PASS'\n    print('ok')", "<demo>", "exec")

# 2. IndentationError - wrong spacing (a type of SyntaxError)
def indentation_error():
    compile("def open_app():\nprint('opening')", "<demo>", "exec")

# 3. NameError - using a variable that does not exist (often a typo)
def name_error():
    window_title = "Notepad"
    print(window_titel)                      # noqa - typo on purpose

# 4. TypeError - wrong type for an operation
def type_error():
    passed = 8
    print("Passed tests: " + passed)         # cannot add str + int

# 5. ValueError - right type, bad value
def value_error():
    int("12a")                               # text read from screen is not a number

# 6. KeyError - dictionary key missing
def key_error():
    login_data = {"username": "admin", "password": "Admin@123"}
    print(login_data["user_name"])           # wrong key name

# 7. IndexError - list position does not exist
def index_error():
    results = ["PASS", "FAIL", "PASS"]
    print(results[3])                        # valid indexes are 0, 1, 2

# 8. AttributeError - object does not have that attribute/method
def attribute_error():
    title = "Calculator"
    title.click()                            # a str has no click() method

# 9. ZeroDivisionError - dividing by zero
def zero_division_error():
    executed = 0
    passed = 0
    print(passed / executed * 100)           # no tests executed yet!

# 10. FileNotFoundError - common in automation (test data / config files)
def file_not_found_error():
    open("missing_test_data.csv")

# 11. ModuleNotFoundError - package not installed or name misspelled
def module_not_found_error():
    import pywinautoo                        # noqa - misspelled on purpose

# 12. A typical AUTOMATION error - "element not found" (simulated)
class ElementNotFoundError(Exception):
    """Custom error similar to what GUI tools raise."""

def element_not_found():
    visible_buttons = ["OK", "Cancel"]
    wanted = "Save"
    if wanted not in visible_buttons:
        raise ElementNotFoundError(f"Button '{wanted}' not found on window 'Settings'")


show("1. SyntaxError", syntax_error)
show("2. IndentationError", indentation_error)
show("3. NameError", name_error)
show("4. TypeError", type_error)
show("5. ValueError", value_error)
show("6. KeyError", key_error)
show("7. IndexError", index_error)
show("8. AttributeError", attribute_error)
show("9. ZeroDivisionError", zero_division_error)
show("10. FileNotFoundError", file_not_found_error)
show("11. ModuleNotFoundError", module_not_found_error)
show("12. Automation: ElementNotFoundError (custom)", element_not_found)

print("\nOther automation errors you will meet from Day 2 onwards:")
print("  - Timeout / window not found (app slow to start)")
print("  - Element not found (wrong locator, control not visible yet)")
print("  - Stale state (window closed while script still uses it)")
print("  - Screen resolution / scaling differences (image-based tools)")
