"""
Lab 3 - Faulty Script 2: RUNTIME ERROR (KeyError) (FIXED)
==========================================================
How to run:
    python lab3_bug2_key_error.py

Bugs fixed:
  1. KeyError: 'password'  -> a TEST DATA bug. The third row had the key
     "pasword" (typo). Dictionary keys must match exactly (and are
     case-sensitive). Fixed the data.
  2. KeyError: 'guest'     -> a CODE bug. registered_users[username] crashes
     when the user does not exist. A negative test (unknown user) is a
     valid scenario, so the code must handle it. Fixed with
     dict.get(username), which returns None instead of raising KeyError.
"""

registered_users = {
    "admin": "Admin@123",
    "tester1": "Test@123",
}

login_test_data = [
    {"username": "admin", "password": "Admin@123", "expected": "success"},
    {"username": "tester1", "password": "Test@123", "expected": "success"},
    {"username": "guest", "password": "Guest@1", "expected": "failure"},   # FIX 1: key spelling
]


def login(username, password):
    """Return 'success' if the username exists and the password matches."""
    stored_password = registered_users.get(username)      # FIX 2: None if user is unknown
    if stored_password is not None and stored_password == password:
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
