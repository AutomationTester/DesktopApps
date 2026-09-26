"""
Example 05 - Conditional Statements
====================================
Day 1 | Topic: Conditional statements (if, elif, else)

How to run:
    python 05_conditionals.py

Conditions let a script DECIDE - the heart of every test verification.
"""

# ---------------------------------------------------------------
# 1. Simple if / else - the basic "assert" of a manual tester
# ---------------------------------------------------------------
print("--- if / else ---")
expected_status = "Saved"
actual_status = "Saved"

if actual_status == expected_status:
    print("PASS: status bar shows 'Saved'")
else:
    print(f"FAIL: expected '{expected_status}' but got '{actual_status}'")

# ---------------------------------------------------------------
# 2. if / elif / else - choose one of many paths
# ---------------------------------------------------------------
print("\n--- if / elif / else : defect severity ---")
crash_count = 2

if crash_count == 0:
    severity = "None"
elif crash_count <= 2:
    severity = "Medium"
elif crash_count <= 5:
    severity = "High"
else:
    severity = "Critical"
print(f"Crashes: {crash_count} -> Severity: {severity}")

# ---------------------------------------------------------------
# 3. Combining conditions with and / or / not
# ---------------------------------------------------------------
print("\n--- Login validation with combined conditions ---")
username = "admin"
password = "Admin@123"
account_locked = False

if not username or not password:
    print("Error: username and password are required")
elif account_locked:
    print("Error: account is locked")
elif username == "admin" and password == "Admin@123":
    print("Login successful - dashboard opened")
else:
    print("Error: invalid credentials")

# ---------------------------------------------------------------
# 4. Nested if - a condition inside a condition
# ---------------------------------------------------------------
print("\n--- Nested if : window checks ---")
window_found = True
window_title = "Calculator"

if window_found:
    if window_title == "Calculator":
        print("Correct window found - continue test")
    else:
        print("Wrong window in focus - take screenshot")
else:
    print("Window not found - mark test as BLOCKED")

# ---------------------------------------------------------------
# 5. Conditional expression (one-line if)
# ---------------------------------------------------------------
print("\n--- One-line if (ternary) ---")
response_time = 3.8
result = "PASS" if response_time <= 3 else "FAIL"
print(f"Response time {response_time}s against SLA 3s -> {result}")

# ---------------------------------------------------------------
# 6. Truthy / falsy values
#    Empty string "", 0, empty list [], None  -> behave like False
# ---------------------------------------------------------------
print("\n--- Truthy / falsy ---")
error_message = ""          # no error text on screen
if error_message:
    print("Error shown:", error_message)
else:
    print("No error message displayed - good")

# ---------------------------------------------------------------
# 7. match / case (Python 3.10+) - neat for fixed choices
# ---------------------------------------------------------------
print("\n--- match / case : test environment ---")
environment = "QA"
match environment:
    case "DEV":
        base_path = r"C:\apps\dev\billing.exe"
    case "QA":
        base_path = r"C:\apps\qa\billing.exe"
    case "PROD":
        base_path = r"C:\apps\prod\billing.exe"
    case _:                      # _ means "anything else"
        base_path = "unknown"
print(f"Environment {environment} -> app path {base_path}")
