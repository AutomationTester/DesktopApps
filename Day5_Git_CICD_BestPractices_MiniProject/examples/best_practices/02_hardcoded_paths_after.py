"""
02_hardcoded_paths_after.py  -  GOOD: pathlib, relative to the project
======================================================================
Fixes:
  1. Paths are built relative to THIS FILE (Path(__file__)), so the script
     works from any working directory and on any machine.
  2. pathlib's "/" operator uses the correct separator on every OS.
  3. Output folders are created on demand (mkdir(parents=True, exist_ok=True)).
  4. Files are read/written with an explicit encoding.
  5. Temp data goes to the OS temp dir (tempfile) - no clutter, no clashes.

Run:
    python 02_hardcoded_paths_after.py
"""

import csv
import tempfile
from datetime import datetime
from pathlib import Path

# The folder that contains this script - the anchor for everything else.
HERE = Path(__file__).resolve().parent
# In the real framework this would be e.g.:  PROJECT_ROOT / "test_data"
REPORT_DIR = HERE / "output" / "reports"


def main() -> None:
    # Create a sample data file in a temp folder (so this demo is self-contained)
    with tempfile.TemporaryDirectory(prefix="day5_paths_") as tmp:
        data_file = Path(tmp) / "test_data" / "calculator_data.csv"
        data_file.parent.mkdir(parents=True, exist_ok=True)
        data_file.write_text("a,op,b,expected\n7,+,8,15\n9,*,6,54\n",
                             encoding="utf-8")

        with data_file.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        print("Data file  :", data_file)
        print("Rows read  :", rows)

        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = REPORT_DIR / f"run_{stamp}.txt"
        report_file.write_text(f"{len(rows)} rows processed\n", encoding="utf-8")
        print("Report file:", report_file)

        # Handy pathlib attributes
        print("  .name   =", report_file.name)
        print("  .stem   =", report_file.stem)
        print("  .suffix =", report_file.suffix)
        print("  .parent =", report_file.parent.name)
        print("  as_posix=", report_file.as_posix())

    # Clean up the demo output so re-runs leave no clutter
    report_file.unlink()
    for folder in (REPORT_DIR, REPORT_DIR.parent):
        if folder.exists() and not any(folder.iterdir()):
            folder.rmdir()
    print("[PASS] same code works on Windows, Linux and macOS")


if __name__ == "__main__":
    main()
