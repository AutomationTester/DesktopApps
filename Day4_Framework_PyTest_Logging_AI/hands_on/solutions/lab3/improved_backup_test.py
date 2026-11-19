"""
Lab 3 - SOLUTION: the backup test after AI-assisted review + human review.

    python improved_backup_test.py
    python improved_backup_test.py --timeout 15 --files 5

Fixes (numbers match the issue list in lab3_prompt_and_review.md):
  1  paths built from __file__ with pathlib   -> works from any working directory
  2  clean work folder before every run        -> no crash on 2nd run, no stale data
  3  'with open' everywhere                    -> no leaked/locked file handles
  4  sys.executable + list args, no shell=True -> right interpreter, no quoting bugs
  5  process wait with timeout + polling for status 'done' -> no fixed sleep
  6  JSON read tolerant to 'file half written' -> no random JSONDecodeError
  7  files compared as int                     -> 3 == 3, not 3 == "3"
  8  verifies names AND contents of copied files
  9  specific exceptions, logged with traceback
 10  logging to console + file, exit code 0/1  -> debuggable, CI friendly
 11  magic numbers -> constants / argparse
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
POLL_INTERVAL = 0.2

log = logging.getLogger("lab3.backup_test")


def setup_logging():
    if log.handlers:
        return
    LOG_FILE.parent.mkdir(exist_ok=True)
    log.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s", "%H:%M:%S")
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)
    file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
    file_handler.setFormatter(fmt)
    log.addHandler(console)
    log.addHandler(file_handler)


def wait_until(condition, timeout, interval=POLL_INTERVAL, message="condition"):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        value = condition()
        if value:
            return value
        time.sleep(interval)
    raise TimeoutError(f"Timed out after {timeout}s waiting for {message}")


def prepare_source(file_count):
    """Arrange: fresh work folder with `file_count` small files. Returns {name: content}."""
    if WORK.exists():
        shutil.rmtree(WORK)
    SRC.mkdir(parents=True)
    expected = {}
    for i in range(file_count):
        name, content = f"file{i}.txt", f"data {i}"
        with open(SRC / name, "w", encoding="utf-8") as f:
            f.write(content)
        expected[name] = content
    log.debug("Created %d source files in %s", file_count, SRC)
    return expected


def read_status():
    """Return the status dict, or None if the file is missing or half written."""
    try:
        with open(DST / "status.json", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return None


def run_backup_check(file_count=3, timeout=DEFAULT_TIMEOUT) -> bool:
    expected = prepare_source(file_count)

    # Act
    cmd = [sys.executable, str(TOOL), str(SRC), str(DST)]
    log.info("Starting backup of %d file(s)", file_count)
    log.debug("Command: %s", cmd)
    started = time.monotonic()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        log.error("backup_tool did not finish within %.1fs", timeout)
        return False
    log.debug("rc=%s stdout=%r stderr=%r", proc.returncode, proc.stdout, proc.stderr)
    if proc.returncode != 0:
        log.error("backup_tool failed rc=%s: %s", proc.returncode, proc.stderr.strip())
        return False

    # Synchronise on the application's own 'done' signal (still needed if the tool
    # ever becomes asynchronous; costs nothing when it is already done)
    try:
        status = wait_until(lambda: (s := read_status()) and s.get("status") == "done" and s,
                            timeout=timeout, message="status.json to report 'done'")
    except TimeoutError as exc:
        log.error("%s - last status: %s", exc, read_status())
        return False
    log.info("Backup finished in %.2fs, status=%s", time.monotonic() - started, status)

    # Assert
    ok = True
    if status["files"] != file_count:
        log.error("status.json files=%r, expected %d", status["files"], file_count)
        ok = False
    for name, content in expected.items():
        copy = DST / name
        if not copy.exists():
            log.error("Missing in backup: %s", name)
            ok = False
            continue
        actual = copy.read_text(encoding="utf-8")
        if actual != content:
            log.error("Content mismatch in %s: expected %r, got %r", name, content, actual)
            ok = False
    if ok:
        log.info("All %d file(s) present with correct content", file_count)
    return ok


def main():
    parser = argparse.ArgumentParser(description="Improved backup_tool test")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--files", type=int, default=3)
    args = parser.parse_args()
    setup_logging()
    try:
        passed = run_backup_check(args.files, args.timeout)
    except Exception:
        log.exception("Unexpected error")
        passed = False
    log.info("RESULT: %s", "PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
