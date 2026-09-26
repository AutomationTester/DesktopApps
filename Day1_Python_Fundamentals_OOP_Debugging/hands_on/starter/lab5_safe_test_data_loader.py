"""
Lab 5 (Extra practice) - Safe Test Data Loader (STARTER)
=========================================================
How to run:
    python lab5_safe_test_data_loader.py

Practises: exception handling (try / except / else / finally / raise),
custom exceptions, functions, loops, working with files.

Row format:  test_id,username,password,wait_seconds
The script writes a sample CSV into your system TEMP folder, reads it back,
and should delete it at the end.

RIGHT NOW the script CRASHES on the first bad row. Your job: complete the
TODOs so that bad rows are REPORTED and SKIPPED, and the script finishes.
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
    # TODO 1: if len(parts) != 4 -> raise InvalidTestDataError(f"line {line_no}: expected 4 columns, got {len(parts)}")

    test_id, username, password, wait_text = parts
    # TODO 2: if username is empty -> raise InvalidTestDataError(f"line {line_no}: username is empty")

    wait_seconds = int(wait_text)          # may raise ValueError ("ten")
    # TODO 3: if wait_seconds <= 0 -> raise InvalidTestDataError(... must be positive ...)

    return {"test_id": test_id, "username": username,
            "password": password, "wait_seconds": wait_seconds}


def load_test_data(path):
    """Return (valid_rows, errors). Should never crash because of one bad row."""
    valid_rows, errors = [], []

    # TODO 4: wrap the open() in try / except FileNotFoundError.
    #         On error: errors.append(f"File not found: {path}") and return valid_rows, errors
    with open(path, encoding="utf-8") as data_file:
        lines = data_file.read().splitlines()

    for line_no, line in enumerate(lines[1:], start=2):   # skip header row
        if not line.strip():
            continue                                        # ignore blank lines
        # TODO 5: wrap the next two lines in try / except ValueError / except InvalidTestDataError / else
        #   except ValueError as error        -> errors.append(f"line {line_no}: not a number -> {error}")
        #   except InvalidTestDataError as e  -> errors.append(str(e))
        #   else                              -> valid_rows.append(row)
        row = parse_row(line, line_no)
        valid_rows.append(row)
    return valid_rows, errors


def main():
    temp_path = os.path.join(tempfile.gettempdir(), "day1_lab5_login_data.csv")
    # TODO 6: put everything below in try: ... finally: so the temp file is
    #         ALWAYS deleted (os.remove(temp_path) if os.path.exists(temp_path))
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


if __name__ == "__main__":
    main()
