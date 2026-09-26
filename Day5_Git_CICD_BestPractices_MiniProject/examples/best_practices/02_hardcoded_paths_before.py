"""
02_hardcoded_paths_before.py  -  BAD: hard-coded, OS-specific paths
===================================================================
Problems in this script (count them!):
  1. Absolute path to ONE person's machine (C:\\Users\\ravi\\...)
  2. Windows-only backslashes glued with "+"
  3. Depends on the CURRENT WORKING DIRECTORY ("reports\\" is relative
     to wherever you launched python from, not to this file)
  4. Crashes if the folder does not exist
  5. Will never work on the Linux CI runner

Run it to see it fail gracefully (we catch the error for the demo):
    python 02_hardcoded_paths_before.py
"""

DATA_FILE = "C:\\Users\\ravi\\Desktop\\automation\\test_data\\calculator_data.csv"
REPORT_DIR = "reports\\"


def main() -> None:
    report_file = REPORT_DIR + "run_" + "001" + ".txt"
    print("Data file  :", DATA_FILE)
    print("Report file:", report_file)
    try:
        with open(DATA_FILE) as f:          # no encoding either!
            print(f.read())
    except OSError as exc:
        print("[FAIL] ", type(exc).__name__, "-", exc)
        print("        -> works only on Ravi's laptop, never on CI")


if __name__ == "__main__":
    main()
