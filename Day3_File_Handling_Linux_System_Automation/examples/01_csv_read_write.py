"""
01_csv_read_write.py
====================
Day 3 - File Handling: reading and writing CSV files with the standard
library ``csv`` module.

What this example shows
-----------------------
1. Writing rows with csv.writer        (list-of-lists)
2. Reading rows with csv.reader        (every value comes back as a STRING)
3. Appending a row (mode="a")
4. Handling a header row and converting types
5. Why we always pass newline="" and encoding="utf-8"

Testing angle: CSV is the most common format for test data handed to you by
business analysts (it opens in Excel). You must be able to read it, convert
types, and write result reports back.

All files are created inside  examples/sandbox/  (created automatically).

Run:  python 01_csv_read_write.py
"""

import csv
from pathlib import Path

# Always build paths relative to THIS file, not the current working directory.
# That way the script works no matter where you run it from.
HERE = Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox"
SANDBOX.mkdir(exist_ok=True)

CSV_FILE = SANDBOX / "login_tests.csv"


def write_csv():
    """Write a small test-data table using csv.writer (rows = lists)."""
    rows = [
        ["test_id", "username", "password", "expected"],   # header row
        ["TC001", "admin", "admin123", "success"],
        ["TC002", "admin", "wrongpass", "failure"],
        ["TC003", "", "admin123", "failure"],               # empty username
        ["TC004", "o'brien, john", "pa$$", "failure"],     # comma inside value!
    ]
    # newline=""  -> stops Windows from writing blank lines between rows
    # encoding    -> be explicit; default encoding differs between OSes
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)          # write many rows at once
    print(f"[WRITE] Wrote {len(rows) - 1} data rows to {CSV_FILE.name}")


def read_csv():
    """Read the CSV back using csv.reader (each row is a list of strings)."""
    print("\n[READ] Raw rows from csv.reader:")
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)           # first row is the header
        print(f"  header  -> {header}")
        for row in reader:
            print(f"  row     -> {row}")
    # Note: the value "o'brien, john" was quoted automatically by csv.writer
    # and un-quoted correctly by csv.reader. Never split CSV lines with
    # line.split(",") - it breaks on commas inside values.


def append_row():
    """Append one more test case without rewriting the whole file."""
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["TC005", "guest", "guest", "success"])
    print("\n[APPEND] Added TC005")


def type_conversion_demo():
    """Everything read from CSV is a string - convert explicitly."""
    numbers_file = SANDBOX / "timings.csv"
    with open(numbers_file, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["test_id", "duration_sec", "retries"])
        w.writerow(["TC001", "1.25", "0"])
        w.writerow(["TC002", "3.50", "2"])

    total = 0.0
    with open(numbers_file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for test_id, duration, retries in reader:
            # "1.25" + "3.50" would be string concatenation -> convert first!
            total += float(duration)
            print(f"  {test_id}: duration={float(duration):.2f}s retries={int(retries)}")
    print(f"[TYPES] Total duration = {total:.2f}s")


def count_rows():
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        data_rows = list(csv.reader(f))[1:]
    print(f"\n[COUNT] {CSV_FILE.name} now has {len(data_rows)} test cases")


if __name__ == "__main__":
    write_csv()
    read_csv()
    append_row()
    count_rows()
    print("\n[TYPES] Converting string values to numbers:")
    type_conversion_demo()
    print("\nDone. Open the sandbox folder to inspect the generated CSV files.")
