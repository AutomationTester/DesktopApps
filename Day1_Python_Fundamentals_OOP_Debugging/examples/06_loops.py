"""
Example 06 - Loops (for, while)
================================
Day 1 | Topic: Loops

How to run:
    python 06_loops.py

Loops repeat work - run many test cases, retry a step, wait for a window.
"""
import time

# ---------------------------------------------------------------
# 1. for loop over a list
# ---------------------------------------------------------------
print("--- for loop over test cases ---")
test_cases = ["TC_001 Login", "TC_002 Logout", "TC_003 Search"]
for test in test_cases:
    print("Executing:", test)

# ---------------------------------------------------------------
# 2. range() - repeat a fixed number of times
#    range(start, stop) -> stop is NOT included
# ---------------------------------------------------------------
print("\n--- range() ---")
for step in range(1, 4):
    print(f"Step {step} of 3")

# ---------------------------------------------------------------
# 3. enumerate() - get position AND value
# ---------------------------------------------------------------
print("\n--- enumerate() ---")
for index, test in enumerate(test_cases, start=1):
    print(f"{index}. {test}")

# ---------------------------------------------------------------
# 4. Loop over a dictionary - count results
# ---------------------------------------------------------------
print("\n--- Loop over a dict : results summary ---")
results = {
    "TC_001": "PASS",
    "TC_002": "FAIL",
    "TC_003": "PASS",
    "TC_004": "SKIP",
    "TC_005": "PASS",
}
pass_count = 0
fail_count = 0
for test_id, status in results.items():
    print(f"{test_id}: {status}")
    if status == "PASS":
        pass_count += 1
    elif status == "FAIL":
        fail_count += 1
print(f"Passed={pass_count}  Failed={fail_count}  Total={len(results)}")

# ---------------------------------------------------------------
# 5. Data-driven testing - loop over a list of dictionaries
# ---------------------------------------------------------------
print("\n--- Data-driven login test ---")
login_data = [
    {"user": "admin", "pwd": "Admin@123", "expected": "success"},
    {"user": "admin", "pwd": "wrong", "expected": "failure"},
    {"user": "", "pwd": "Admin@123", "expected": "failure"},
]
for row in login_data:
    # a fake "application" rule for the demo
    actual = "success" if row["user"] == "admin" and row["pwd"] == "Admin@123" else "failure"
    verdict = "PASS" if actual == row["expected"] else "FAIL"
    print(f"user={row['user']!r:8} pwd={row['pwd']!r:12} -> {actual:8} {verdict}")

# ---------------------------------------------------------------
# 6. while loop - repeat UNTIL a condition changes
#    Typical use: wait/poll for a window to appear
# ---------------------------------------------------------------
print("\n--- while loop : wait for window (simulated) ---")
attempt = 0
max_attempts = 5
window_ready = False
while not window_ready and attempt < max_attempts:
    attempt += 1
    print(f"Attempt {attempt}: checking if window is ready...")
    time.sleep(0.2)                 # small wait (seconds)
    if attempt == 3:                # pretend it appears on the 3rd check
        window_ready = True
print("Window ready!" if window_ready else "Timed out waiting for window")

# ---------------------------------------------------------------
# 7. break and continue
# ---------------------------------------------------------------
print("\n--- break : stop at first critical failure ---")
statuses = ["PASS", "PASS", "CRITICAL", "PASS"]
for number, status in enumerate(statuses, start=1):
    if status == "CRITICAL":
        print(f"Test {number} CRITICAL - stopping the run")
        break
    print(f"Test {number} {status}")

print("\n--- continue : skip tests marked SKIP ---")
for test_id, status in results.items():
    if status == "SKIP":
        continue            # jump to next item
    print("Reporting", test_id)

# ---------------------------------------------------------------
# 8. List comprehension - a short way to build a list with a loop
# ---------------------------------------------------------------
failed_tests = [tid for tid, st in results.items() if st == "FAIL"]
print("\nFailed tests (list comprehension):", failed_tests)
