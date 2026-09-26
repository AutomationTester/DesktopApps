"""
Day 4 - Example 06: Test data generation (no AI, no Faker - pure Python)
========================================================================
AI tools can suggest test data, but you must understand the classic
techniques they are (hopefully) applying:

  * Equivalence Class Partitioning (ECP): one representative per class
  * Boundary Value Analysis (BVA): min-1, min, min+1, max-1, max, max+1
  * Random-but-reproducible data: random.Random(seed)

Field spec used here (a typical desktop "Add Employee" form):
    age       : integer 18..60
    username  : 5..12 chars, letters/digits only
    salary    : 10000.00 .. 99999.99

The data is written to generated_test_data.csv so pytest can parametrize from it.

Run:
    python 06_test_data_generation.py
"""
import csv
import random
import string
from pathlib import Path

OUT_FILE = Path(__file__).parent / "generated_test_data.csv"


def boundary_values(minimum, maximum, step=1):
    """Classic 6-point BVA; returns (value, expected_valid) tuples."""
    return [
        (minimum - step, False), (minimum, True), (minimum + step, True),
        (maximum - step, True), (maximum, True), (maximum + step, False),
    ]


def equivalence_classes_age():
    return [
        (35, True, "valid middle value"),
        (-5, False, "negative"),
        (150, False, "far above max"),
        ("abc", False, "non-numeric"),
        ("", False, "empty"),
    ]


def username_cases(rng, min_len=5, max_len=12):
    letters = string.ascii_letters + string.digits
    rand = lambda n: "".join(rng.choice(letters) for _ in range(n))
    return [
        (rand(min_len - 1), False, "too short (min-1)"),
        (rand(min_len), True, "exact min length"),
        (rand(max_len), True, "exact max length"),
        (rand(max_len + 1), False, "too long (max+1)"),
        ("user_01", False, "contains underscore"),
        ("  ", False, "whitespace only"),
        ("tester" + "é", False, "non-ASCII character"),
    ]


def generate(seed=42):
    rng = random.Random(seed)            # same seed -> same data -> reproducible failures
    rows = []
    for value, valid in boundary_values(18, 60):
        rows.append(("age", value, valid, "BVA"))
    for value, valid, note in equivalence_classes_age():
        rows.append(("age", value, valid, f"ECP: {note}"))
    for value, valid, note in username_cases(rng):
        rows.append(("username", value, valid, note))
    for value, valid in boundary_values(10000.00, 99999.99, step=0.01):
        rows.append(("salary", round(value, 2), valid, "BVA"))
    for _ in range(3):
        rows.append(("salary", round(rng.uniform(10000, 99999.99), 2), True, "random valid"))
    return rows


if __name__ == "__main__":
    rows = generate()
    with open(OUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["field", "value", "expected_valid", "technique"])
        writer.writerows(rows)

    print(f"{'field':<9} {'value':<16} {'valid':<6} technique")
    print("-" * 60)
    for field, value, valid, tech in rows:
        shown = repr(value).encode("ascii", "backslashreplace").decode()
        print(f"{field:<9} {shown:<16} {str(valid):<6} {tech}")
    print(f"\n{len(rows)} rows written to {OUT_FILE.name}")
    print("Run again: identical output thanks to random.Random(42).")
