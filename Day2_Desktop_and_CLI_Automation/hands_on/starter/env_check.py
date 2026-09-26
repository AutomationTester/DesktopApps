"""
Lab 5 (extra) - STARTER: env_check.py - pre-test environment check with subprocess

Target usage:
    python env_check.py
    python env_check.py --tools python git notepad.exe
    python env_check.py --report env_report.txt

Expected output (example):
    [PASS] python version         Python 3.14.7 (need >= 3.10)
    [PASS] tool: notepad.exe      C:\\Windows\\System32\\notepad.exe
    [FAIL] tool: nosuchtool       not found on PATH
    OVERALL: FAIL
Exit code 0 when everything passes, otherwise 1.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list, timeout: int = 30) -> subprocess.CompletedProcess:
    # TODO 1: return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    raise NotImplementedError("run")


def check_python(min_version: str) -> tuple:
    # TODO 2: run [sys.executable, "--version"], parse 'Python 3.14.7',
    #         compare (3, 14) >= (3, 10); return (ok, detail_text)
    raise NotImplementedError("check_python")


def check_tool(tool: str) -> tuple:
    # TODO 3: run ["where", tool]; returncode 0 -> (True, first line of stdout)
    #         otherwise (False, "not found on PATH")
    raise NotImplementedError("check_tool")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check that this machine is ready for testing.")
    parser.add_argument("--min-python", default="3.10")
    parser.add_argument("--tools", nargs="+", default=["python", "notepad.exe", "calc.exe"])
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)

    lines = []
    all_ok = True
    # TODO 4: call check_python and check_tool for every tool,
    #         append "[PASS] ..." / "[FAIL] ..." lines, track all_ok
    # TODO 5: stretch - check packages with [sys.executable, "-c", "import pywinauto"]
    # TODO 6: print the lines + OVERALL; if --report, write them to the file
    print("\n".join(lines) or "TODO: implement the checks")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
