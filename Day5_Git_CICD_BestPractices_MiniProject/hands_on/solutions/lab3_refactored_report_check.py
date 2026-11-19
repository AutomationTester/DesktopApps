"""
lab3_refactored_report_check.py - Lab 3 SOLUTION (refactored, reliable version)

Fixes compared to lab3_starter/flaky_report_check.py
  1. Paths via pathlib, relative to this file - no cwd dependency, works on Linux CI.
  2. Each run writes into its OWN temporary folder (isolated test data, no stale report).
  3. Command is a LIST, no shell=True, uses sys.executable (the same Python/venv).
  4. We keep the Popen handle and WAIT for the process with a TIMEOUT (no fixed sleep).
  5. A hung process started by us is killed in `finally` - nothing is left behind.
  6. Transient failure (exit code 75 "busy") is RETRIED with exponential backoff.
  7. Real errors are NOT swallowed: specific exceptions with clear messages.
  8. logging instead of print (timestamps, levels, goes to a file in the framework).
  9. Files opened with explicit encoding (pathlib read_text).
 10. Settings (timeouts, retries) in one config dict - easy to move to config.yaml.
 11. Meaningful exit code (0 pass / 1 fail) so CI can see the result.

Run:
    python lab3_refactored_report_check.py              # random behaviour, 5 runs
    python lab3_refactored_report_check.py --mode hang  # watch the timeout + kill
"""
import argparse
import logging
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
GENERATOR = HERE.parent / "lab3_starter" / "report_generator.py"

CONFIG = {
    "process_timeout": 5.0,     # seconds - generator needs max 3 s when healthy
    "retries": 3,               # attempts for transient "busy" errors
    "retry_delay": 0.5,         # first backoff delay, doubled each time
}
EXIT_BUSY = 75

log = logging.getLogger("lab3")


class TransientError(Exception):
    """The tool said 'busy' - worth trying again."""


class GeneratorTimeout(Exception):
    """The tool did not finish in time (hung)."""


def run_generator_once(out_file: Path, mode: str = "random", timeout: float = None) -> None:
    timeout = timeout or CONFIG["process_timeout"]
    cmd = [sys.executable, str(GENERATOR), "--out", str(out_file), "--mode", mode]
    log.debug("Starting: %s", cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        raise GeneratorTimeout(f"generator did not finish within {timeout}s") from None
    finally:
        if proc.poll() is None:              # still running -> it is OUR child, kill it
            log.warning("Killing hung generator PID %s", proc.pid)
            proc.kill()
            proc.communicate()               # reap it and close the pipes
    if proc.returncode == EXIT_BUSY:
        raise TransientError(stderr.strip() or "busy")
    if proc.returncode != 0:
        raise RuntimeError(f"generator failed rc={proc.returncode}: {stderr.strip()}")
    log.debug("Generator said: %s", stdout.strip())


def run_with_retry(out_file: Path, mode: str = "random", retries: int = None,
                   delay: float = None) -> None:
    retries = retries or CONFIG["retries"]
    wait = delay if delay is not None else CONFIG["retry_delay"]
    for attempt in range(1, retries + 1):
        try:
            run_generator_once(out_file, mode)
            return
        except TransientError as exc:
            if attempt == retries:
                raise
            log.warning("Attempt %d/%d: %s - retrying in %.1fs", attempt, retries, exc, wait)
            time.sleep(wait)
            wait *= 2


def check_report(mode: str = "random") -> bool:
    with tempfile.TemporaryDirectory(prefix="lab3_") as tmp:   # auto-deleted, even on error
        out_file = Path(tmp) / "report.txt"
        try:
            run_with_retry(out_file, mode)
        except (TransientError, GeneratorTimeout, RuntimeError) as exc:
            log.error("FAIL - %s: %s", type(exc).__name__, exc)
            return False
        if not out_file.is_file():
            log.error("FAIL - generator exited 0 but wrote no report at %s", out_file)
            return False
        content = out_file.read_text(encoding="utf-8")
        if "REPORT OK" not in content:
            log.error("FAIL - unexpected report content: %r", content)
            return False
        log.info("PASS - report OK")
        return True


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="random", choices=["random", "ok", "busy", "hang"])
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s | %(levelname)-7s | %(message)s")
    results = [check_report(args.mode) for _ in range(args.runs)]
    log.info("Summary: %d/%d passed", sum(results), len(results))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
