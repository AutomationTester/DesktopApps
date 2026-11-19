"""
Lab 5 (Extra practice) - Safe Test Data Loader (SOLUTION)
==========================================================
How to run:
    python lab5_safe_test_data_loader.py

Practises: exception handling (try / except / else / finally / raise),
custom exceptions, functions, loops, working with files.

Scenario:
    Automation scripts read test data from files. Real files are messy:
    missing columns, text where numbers should be, blank lines, or the file
    is missing completely. A good framework must NOT crash on one bad row -
    it should skip it, report it clearly and continue.

Row format:  test_id,username,password,wait_seconds
The script writes a sample CSV into your system TEMP folder, reads it back,
and deletes it at the end (in 'finally').
"""
import os
import tempfile

SAMPLE_CSV = """test_id,username,password,wait_seconds
TC_301,admin,Admin@123,5
TC_302,tester1,Test@123,ten
TC_303,guest
TC_304,,NoUser@1,3

TC_305,manager,Mgr@2026,-2
TC_306,viewer,View@123,8
"""


class InvalidTestDataError(Exception):
    """Raised when a row of test data breaks a business rule."""


def parse_row(line, line_no):
    """Convert one CSV line to a dict. Raise an error for bad data."""
    parts = [part.strip() for part in line.split(",")]
    if len(parts) != 4:
        raise InvalidTestDataError(f"line {line_no}: expected 4 columns, got {len(parts)}")

    test_id, username, password, wait_text = parts
    if not username:
        raise InvalidTestDataError(f"line {line_no}: username is empty")

    wait_seconds = int(wait_text)          # may raise ValueError ("ten")
    if wait_seconds <= 0:
        raise InvalidTestDataError(f"line {line_no}: wait_seconds must be positive, got {wait_seconds}")

    return {"test_id": test_id, "username": username,
            "password": password, "wait_seconds": wait_seconds}


def load_test_data(path):
    """Return (valid_rows, errors). Never crashes because of one bad row."""
    valid_rows, errors = [], []
    try:
        with open(path, encoding="utf-8") as data_file:
            lines = data_file.read().splitlines()
    except FileNotFoundError:
        errors.append(f"File not found: {path}")
        return valid_rows, errors

    for line_no, line in enumerate(lines[1:], start=2):   # skip header row
        if not line.strip():
            continue                                        # ignore blank lines
        try:
            row = parse_row(line, line_no)
        except ValueError as error:
            errors.append(f"line {line_no}: not a number -> {error}")
        except InvalidTestDataError as error:
            errors.append(str(error))
        else:
            valid_rows.append(row)                          # only when no error
    return valid_rows, errors


def main():
    temp_path = os.path.join(tempfile.gettempdir(), "day1_lab5_login_data.csv")
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(SAMPLE_CSV)

        rows, errors = load_test_data(temp_path)
        print("VALID ROWS:")
        for row in rows:
            print(f"  {row['test_id']}  user={row['username']:8} wait={row['wait_seconds']}s")
        print("\nREJECTED ROWS:")
        for message in errors:
            print("  -", message)
        print(f"\nLoaded {len(rows)} valid rows, rejected {len(errors)}.")

        print("\nMissing file check:")
        _, missing_errors = load_test_data("no_such_file.csv")
        print("  -", missing_errors[0])
    finally:
        # cleanup ALWAYS runs - even if something above crashed
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print("\nCleanup: temporary data file deleted.")


if __name__ == "__main__":
    main()
