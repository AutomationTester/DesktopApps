"""
Day 4 - Example 08: AI-assisted debugging - the AFTER script (reviewed + improved)
=================================================================================
Same scenario as 07_ai_debugging_before.py, rewritten after:
  1. asking an AI coding assistant to review the script (prompt in ai_prompt_examples.md)
  2. a HUMAN reviewing and correcting the AI suggestions (review checklist in the same file)

What changed and why:
  * stale report deleted before the run           -> no false PASS/FAIL from old data
  * sys.executable + argument list, no shell=True -> portable, no quoting bugs
  * proc.wait(timeout) + wait_until(file exists)  -> synchronisation instead of sleep
  * 'with open' + .strip()                        -> handle closed, newline ignored
  * specific exceptions, logged with traceback     -> real error visible
  * logging to console + file                     -> evidence for debugging
  * return code 0/1                               -> CI/pytest can detect failure
  * constants / argparse for timeout              -> no magic numbers

Run:
    python 08_ai_debugging_after.py
    python 08_ai_debugging_after.py --timeout 10
"""
import argparse
import logging
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
REPORT = HERE / "report_after.txt"
LOG_FILE = HERE / "logs" / "ai_debugging_after.log"
EXPECTED_TOTAL = "TOTAL=42"
DEFAULT_TIMEOUT = 5.0
POLL_INTERVAL = 0.2

JOB_CODE = (
    "import sys, time, random; "
    "time.sleep(random.uniform(0.5, 2.0)); "
    "open(sys.argv[1], 'w', encoding='utf-8').write('TOTAL=42\\n')"
)


def build_logger():
    LOG_FILE.parent.mkdir(exist_ok=True)
    logger = logging.getLogger("export_test")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s", "%H:%M:%S")
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)
    file_h = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
    file_h.setFormatter(fmt)
    logger.addHandler(console)
    logger.addHandler(file_h)
    return logger


log = build_logger()


def wait_until(condition, timeout, interval=POLL_INTERVAL, message="condition"):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        if condition():
            return True
        time.sleep(interval)
    raise TimeoutError(f"Timed out after {timeout}s waiting for {message}")


def run_export_test(timeout=DEFAULT_TIMEOUT) -> bool:
    # 1. Arrange - clean state
    if REPORT.exists():
        REPORT.unlink()
        log.debug("Deleted stale report %s", REPORT.name)

    # 2. Act - start job safely and wait for it
    cmd = [sys.executable, "-c", JOB_CODE, str(REPORT)]
    log.info("Starting export job")
    log.debug("Command: %s", cmd)
    started = time.monotonic()
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        _, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        log.error("Export job did not finish within %.1fs", timeout)
        return False
    if proc.returncode != 0:
        log.error("Export job failed with rc=%s, stderr=%s", proc.returncode, stderr.strip())
        return False
    wait_until(REPORT.exists, timeout=timeout, message=f"{REPORT.name} to exist")
    log.info("Job finished in %.2fs", time.monotonic() - started)

    # 3. Assert - read safely, normalise, compare, log evidence
    try:
        with open(REPORT, encoding="utf-8") as f:
            actual = f.read().strip()
    except OSError:
        log.exception("Could not read report")
        return False
    if actual != EXPECTED_TOTAL:
        log.error("Report mismatch: expected %r, got %r", EXPECTED_TOTAL, actual)
        return False
    log.info("Report content verified: %s", actual)
    return True


def main():
    parser = argparse.ArgumentParser(description="Export job test (improved)")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    args = parser.parse_args()
    passed = run_export_test(args.timeout)
    log.info("RESULT: %s", "PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
