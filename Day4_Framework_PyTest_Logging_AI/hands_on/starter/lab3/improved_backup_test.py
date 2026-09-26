"""
Lab 3 - YOUR improved version of flaky_backup_test.py.

Fill it in AFTER you have
  1. listed the problems yourself (Lab_Guide.md, Lab 3 step 2)
  2. asked an AI assistant with a structured prompt (step 3)
  3. reviewed the answer with the checklist (step 4)

    python improved_backup_test.py        -> must print RESULT: PASS and exit with code 0, every time
"""
import argparse
import json
import logging
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "backup_tool.py"
WORK = HERE / "lab3_work"
SRC = WORK / "source_files"
DST = WORK / "backup"
LOG_FILE = HERE / "logs" / "improved_backup_test.log"
DEFAULT_TIMEOUT = 10.0

log = logging.getLogger("lab3.backup_test")


def setup_logging():
    # TODO: console handler (INFO, sys.stdout) + file handler LOG_FILE (DEBUG); create the logs folder
    pass


def wait_until(condition, timeout, interval=0.2, message="condition"):
    # TODO: poll condition() until truthy (return it) or raise TimeoutError after `timeout` seconds
    raise NotImplementedError


def prepare_source(file_count):
    """Delete WORK if it exists, create SRC with file0.txt.. files, return {name: content}."""
    # TODO: use shutil.rmtree, Path.mkdir(parents=True) and 'with open(...)'
    raise NotImplementedError


def read_status():
    """Return the dict from DST/status.json, or None if missing or half written."""
    # TODO: catch FileNotFoundError and json.JSONDecodeError (NOT a bare except)
    raise NotImplementedError


def run_backup_check(file_count=3, timeout=DEFAULT_TIMEOUT) -> bool:
    # TODO Arrange: expected = prepare_source(file_count)
    # TODO Act    : subprocess.run([sys.executable, str(TOOL), str(SRC), str(DST)],
    #               capture_output=True, text=True, timeout=timeout)  - handle TimeoutExpired, rc != 0
    # TODO Sync   : wait_until status.json says "done"
    # TODO Assert : status["files"] == file_count (int!), every file exists with the same content
    #               log every problem at ERROR level, return True/False
    raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(description="Improved backup_tool test")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--files", type=int, default=3)
    args = parser.parse_args()
    setup_logging()
    passed = run_backup_check(args.files, args.timeout)
    log.info("RESULT: %s", "PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
