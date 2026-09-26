"""
Lab 3 - Faulty Script 2: RUNTIME ERROR (KeyError)
==================================================
How to run:
    python lab3_bug2_key_error.py

Purpose of the script:
    Data-driven login test. For each row of test data, "log in" to a
    simulated application and compare the actual result with the expected one.

Expected output after you fix it:
    admin    -> actual=success  expected=success  PASS
    tester1  -> actual=success  expected=success  PASS
    guest    -> actual=failure  expected=failure  PASS
    Login tests passed: 3/3

This file has 2 bugs, both raise KeyError (one after the other).
Read the traceback: which KEY is missing, and on which line?
Decide: is the problem in the TEST DATA or in the CODE?
"""

# Users that exist in the (simulated) application
registered_users = {
    "admin": "Admin@123",
    "tester1": "Test@123",
}

# Test data - normally this would come from a CSV/Excel file
login_test_data = [
    {"username": "admin", "password": "Admin@123", "expected": "success"},
    {"username": "tester1", "password": "Test@123", "expected": "success"},
    {"username": "guest", "pasword": "Guest@1", "expected": "failure"},
]


def login(username, password):
    """Return 'success' if the username exists and the password matches."""
    if registered_users[username] == password:
        return "success"
    return "failure"


passed = 0
for row in login_test_data:
    actual = login(row["username"], row["password"])
    status = "PASS" if actual == row["expected"] else "FAIL"
    if status == "PASS":
        passed += 1
    print(f"{row['username']:8} -> actual={actual:8} expected={row['expected']:8} {status}")

print(f"Login tests passed: {passed}/{len(login_test_data)}")
