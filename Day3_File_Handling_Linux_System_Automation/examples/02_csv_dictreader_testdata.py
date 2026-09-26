"""
02_csv_dictreader_testdata.py
=============================
Day 3 - Managing test data with csv.DictReader / csv.DictWriter.

DictReader gives you each row as a dictionary keyed by the header, so your
code says row["username"] instead of row[1]. If a BA inserts a new column
in the middle of the sheet, your script still works.

What this example shows
-----------------------
1. Creating a test-data CSV (data/login_testdata.csv inside the sandbox)
2. Loading it with DictReader and validating required columns
3. Running a (fake) "system under test" for every row -> data-driven testing
4. Writing a results report with DictWriter (PASS/FAIL column added)

Run:  python 02_csv_dictreader_testdata.py
"""

import csv
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox"
SANDBOX.mkdir(exist_ok=True)

TESTDATA = SANDBOX / "login_testdata.csv"
RESULTS = SANDBOX / "login_results.csv"

REQUIRED_COLUMNS = {"test_id", "username", "password", "expected"}


def create_sample_data():
    """Create sample test data (in real life a BA/tester would supply this)."""
    rows = [
        {"test_id": "TC001", "username": "admin", "password": "admin123", "expected": "success"},
        {"test_id": "TC002", "username": "admin", "password": "wrong", "expected": "failure"},
        {"test_id": "TC003", "username": "", "password": "admin123", "expected": "failure"},
        {"test_id": "TC004", "username": "tester", "password": "test@123", "expected": "success"},
        # Deliberately wrong expectation, so we see a FAIL in the report:
        {"test_id": "TC005", "username": "guest", "password": "guest", "expected": "success"},
    ]
    with open(TESTDATA, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["test_id", "username", "password", "expected"])
        writer.writeheader()
        writer.writerows(rows)


def load_test_data(path):
    """Load test data and fail fast if the file is malformed."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Test data file is missing columns: {sorted(missing)}")
        # strip() protects against stray spaces typed in Excel
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


# ---------------------------------------------------------------------------
# A fake "application under test". In the real course this would be a
# pywinauto login window or a CLI tool; the data handling is identical.
# ---------------------------------------------------------------------------
VALID_USERS = {"admin": "admin123", "tester": "test@123"}


def fake_login(username, password):
    if username and VALID_USERS.get(username) == password:
        return "success"
    return "failure"


def run_tests(test_rows):
    results = []
    for row in test_rows:
        actual = fake_login(row["username"], row["password"])
        status = "PASS" if actual == row["expected"] else "FAIL"
        results.append({
            "test_id": row["test_id"],
            "username": row["username"] or "<empty>",
            "expected": row["expected"],
            "actual": actual,
            "status": status,
            "executed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        print(f"  {row['test_id']}: expected={row['expected']:<8} actual={actual:<8} -> {status}")
    return results


def write_results(results, path):
    fieldnames = ["test_id", "username", "expected", "actual", "status", "executed_at"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    create_sample_data()
    rows = load_test_data(TESTDATA)
    print(f"Loaded {len(rows)} test cases from {TESTDATA.name}\n")
    results = run_tests(rows)
    write_results(results, RESULTS)
    passed = sum(r["status"] == "PASS" for r in results)
    print(f"\nSummary: {passed}/{len(results)} passed. Report -> sandbox/{RESULTS.name}")
