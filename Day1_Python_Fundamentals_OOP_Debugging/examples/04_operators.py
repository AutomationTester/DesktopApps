"""
Example 04 - Operators
=======================
Day 1 | Topic: Operators (arithmetic, comparison, logical)

How to run:
    python 04_operators.py
"""

# ---------------------------------------------------------------
# 1. Arithmetic operators
# ---------------------------------------------------------------
total_tests = 17
passed = 14

print("--- Arithmetic ---")
print("Addition       10 + 3  =", 10 + 3)
print("Subtraction    10 - 3  =", 10 - 3)
print("Multiplication 10 * 3  =", 10 * 3)
print("Division       10 / 3  =", 10 / 3)     # always gives a float
print("Floor division 10 // 3 =", 10 // 3)    # whole part only
print("Modulus        10 % 3  =", 10 % 3)     # remainder
print("Power          2 ** 5  =", 2 ** 5)

failed = total_tests - passed
pass_percentage = passed / total_tests * 100
print(f"\nFailed tests    : {failed}")
print(f"Pass percentage : {pass_percentage:.2f}%")  # :.2f -> 2 decimal places

# Modulus is handy: take a screenshot on every 5th step
print("\nSteps where a screenshot is taken:", [s for s in range(1, 16) if s % 5 == 0])

# ---------------------------------------------------------------
# 2. Assignment operators
# ---------------------------------------------------------------
print("\n--- Assignment ---")
retry = 0
retry += 1     # same as retry = retry + 1
retry += 1
print("Retry count after two attempts:", retry)

# ---------------------------------------------------------------
# 3. Comparison operators -> always give True or False
# ---------------------------------------------------------------
expected_title = "Calculator"
actual_title = "Calculator"
response_time = 2.4
sla_seconds = 3

print("\n--- Comparison ---")
print("expected == actual :", expected_title == actual_title)
print("expected != actual :", expected_title != actual_title)
print("response < SLA     :", response_time < sla_seconds)
print("response > SLA     :", response_time > sla_seconds)
print("passed >= 14       :", passed >= 14)
print("failed <= 2        :", failed <= 2)

# ---------------------------------------------------------------
# 4. Logical operators: and, or, not
# ---------------------------------------------------------------
username_ok = True
password_ok = False
is_admin = True

print("\n--- Logical ---")
print("Login allowed (user AND password):", username_ok and password_ok)
print("Show warning  (user OR password)  :", username_ok or password_ok)
print("Not admin                         :", not is_admin)

# Combine comparison + logical in one test check
build_ok = pass_percentage >= 80 and failed < 5
print(f"Build accepted? (>=80% pass AND <5 failures): {build_ok}")

# ---------------------------------------------------------------
# 5. Membership and identity operators (very common in checks)
# ---------------------------------------------------------------
print("\n--- Membership (in / not in) ---")
menu_items = ["File", "Edit", "View", "Help"]
print("'Edit' in menu     :", "Edit" in menu_items)
print("'Tools' not in menu:", "Tools" not in menu_items)
print("'Error' in log line:", "Error" in "2026-09-26 10:01 Error: window not found")

print("\n--- Identity (is / is not) - use mainly with None ---")
defect_id = None
print("defect_id is None  :", defect_id is None)
