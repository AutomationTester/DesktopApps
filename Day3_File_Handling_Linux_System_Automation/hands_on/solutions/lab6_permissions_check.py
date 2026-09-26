"""
Lab 6 - SOLUTION - File permissions from Python
===============================================
Automation scripts often need to CHECK permissions (e.g. "is the deploy
script executable?", "is the secrets file readable by everyone?").

This script:
  1. creates sample files in sandbox/lab6/
  2. applies chmod with octal modes (0o755, 0o644, 0o600, 0o444)
  3. prints the permission string (like ls -l) and the octal value
  4. converts octal <-> rwx with a helper you write yourself
  5. audits the files against expected modes -> PASS/FAIL

NOTE: On Windows, os.chmod can only toggle the READ-ONLY flag, so the
reported modes will differ from Linux. Run it in WSL / Linux to see the
full rwx behaviour. The script prints which behaviour applies.

Run:  python lab6_permissions_check.py
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
    out = ""
    for shift in (6, 3, 0):                  # owner, group, others
        digit = (mode >> shift) & 7
        out += ("r" if digit & 4 else "-") + ("w" if digit & 2 else "-") + ("x" if digit & 1 else "-")
    return out


def rwx_to_octal(text):
    """'rwxr-xr--' -> 0o754"""
    value = 0
    for i in range(0, 9, 3):
        chunk = text[i:i + 3]
        digit = (4 if chunk[0] == "r" else 0) + (2 if chunk[1] == "w" else 0) + (1 if chunk[2] == "x" else 0)
        value = value * 8 + digit
    return value


def main():
    print(f"OS: {platform.system()} "
          f"({'only read-only flag is supported by chmod' if IS_WINDOWS else 'full POSIX permissions'})\n")

    print("Octal <-> rwx conversion table:")
    for m in (0o777, 0o755, 0o750, 0o700, 0o644, 0o640, 0o600, 0o444):
        rwx = octal_to_rwx(m)
        assert rwx_to_octal(rwx) == m
        print(f"  {m:o}  <->  {rwx}")

    ROOT.mkdir(parents=True, exist_ok=True)
    plan = {
        "deploy.sh": 0o755,       # script: everyone can run, only owner edits
        "report.csv": 0o644,      # normal data file
        "secrets.env": 0o600,     # only the owner may read
        "golden.json": 0o444,     # read-only baseline data
    }
    print("\nApplying chmod:")
    for name, mode in plan.items():
        f = ROOT / name
        if f.exists():
            os.chmod(f, 0o644)    # make writable again so we can rewrite it
        f.write_text("#!/usr/bin/env bash\necho deploy\n" if name.endswith(".sh") else "data\n",
                     encoding="utf-8")
        os.chmod(f, mode)
        actual = stat.S_IMODE(f.stat().st_mode)
        print(f"  {name:<12} requested {mode:o} ({octal_to_rwx(mode)})  "
              f"actual {actual:o} {stat.filemode(f.stat().st_mode)}")

    print("\nAudit:")
    for name, mode in plan.items():
        actual = stat.S_IMODE((ROOT / name).stat().st_mode)
        if IS_WINDOWS:
            # Windows can only tell us "writable or not"
            ok = bool(actual & stat.S_IWUSR) == bool(mode & stat.S_IWUSR)
        else:
            ok = actual == mode
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    # Is the script executable for the current user?
    print(f"\nos.access(deploy.sh, X_OK) = {os.access(ROOT / 'deploy.sh', os.X_OK)}")
    print(f"os.access(golden.json, W_OK) = {os.access(ROOT / 'golden.json', os.W_OK)}  (read-only -> False)")


if __name__ == "__main__":
    main()
