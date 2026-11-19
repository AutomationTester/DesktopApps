"""
Lab 6 - STARTER - File permissions from Python
==============================================
  1. write octal_to_rwx() and rwx_to_octal()
  2. create sample files in sandbox/lab6/ and chmod them
  3. audit the files against the expected modes -> PASS/FAIL

NOTE: On Windows, os.chmod can only toggle the READ-ONLY flag. Run in WSL /
Linux to see full rwx behaviour.

Run:  python lab6_permissions_check.py
Search for "# TODO". See hands_on/Lab_Guide.md, Lab 6.
"""

import os
import platform
import stat
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE / "sandbox" / "lab6"
IS_WINDOWS = platform.system() == "Windows"


def octal_to_rwx(mode):
    """0o754 -> 'rwxr-xr--'"""
    # TODO 1: for shift in (6, 3, 0): digit = (mode >> shift) & 7
    #         build "r"/"-", "w"/"-", "x"/"-" using digit & 4, digit & 2, digit & 1
    raise NotImplementedError("TODO 1: octal_to_rwx")


def rwx_to_octal(text):
    """'rwxr-xr--' -> 0o754"""
    # TODO 2: process the text in chunks of 3; r=4, w=2, x=1; value = value * 8 + digit
    raise NotImplementedError("TODO 2: rwx_to_octal")


def main():
    try:
        for m in (0o755, 0o644, 0o600):
            print(f"{m:o} <-> {octal_to_rwx(m)}  back to octal: {rwx_to_octal(octal_to_rwx(m)):o}")
    except NotImplementedError as todo:
        print(f"Not finished yet -> {todo}")
        return

    ROOT.mkdir(parents=True, exist_ok=True)
    plan = {"deploy.sh": 0o755, "report.csv": 0o644, "secrets.env": 0o600, "golden.json": 0o444}
    # TODO 3: for each file in plan: (if it exists, chmod 0o644 first so you can rewrite it)
    #         write some text, os.chmod(file, mode), then print
    #         stat.filemode(file.stat().st_mode)
    # TODO 4: audit: compare stat.S_IMODE(st_mode) with the plan and print PASS/FAIL
    #         (on Windows only compare the owner-write bit stat.S_IWUSR)
    print("TODO 3/4: create, chmod and audit the files")


if __name__ == "__main__":
    main()
