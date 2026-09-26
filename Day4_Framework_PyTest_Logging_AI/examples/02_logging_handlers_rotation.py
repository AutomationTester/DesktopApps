"""
Day 4 - Example 02: Handlers, formatters and log file management
================================================================
A logger can send the SAME message to several destinations (handlers),
each with its own level and format.

Covers:
  * StreamHandler (console)       - INFO and above, short format
  * FileHandler (per-run file)    - DEBUG and above, detailed format
  * RotatingFileHandler           - size based rotation (maxBytes, backupCount)
  * TimedRotatingFileHandler      - time based rotation (when='midnight', 'S', 'H'...)
  * Log folder cleanup            - delete per-run logs older than N days / keep last N

All files are written into ./logs next to this script.

Run:
    python 02_logging_handlers_rotation.py
"""
import logging
import os
import sys
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

DETAILED = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
)
SHORT = logging.Formatter("%(levelname)-8s %(message)s")


def close_handlers(logger):
    """Always close handlers you added - otherwise files stay locked on Windows."""
    for h in list(logger.handlers):
        h.close()
        logger.removeHandler(h)


# ---------------------------------------------------------------------------
# 1. Console + per-run FileHandler
# ---------------------------------------------------------------------------
def demo_console_and_per_run_file():
    print("\n=== 1. Console (INFO+) + per-run file (DEBUG+) ===")
    logger = logging.getLogger("demo.per_run")
    logger.setLevel(logging.DEBUG)       # logger lets everything through...
    logger.propagate = False             # ...and does not duplicate to root

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)       # ...console filters to INFO+
    console.setFormatter(SHORT)

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"run_{run_id}.log"
    file_h = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_h.setLevel(logging.DEBUG)       # ...file keeps everything
    file_h.setFormatter(DETAILED)

    logger.addHandler(console)
    logger.addHandler(file_h)

    logger.debug("Locator used: auto_id='CalculatorResults'  (file only)")
    logger.info("Test started (console + file)")
    logger.warning("Window slow to appear, waited 3s (console + file)")

    close_handlers(logger)
    print(f"Per-run log written to: {log_file.relative_to(LOG_DIR.parent)}")
    print("File contents:")
    print(log_file.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 2. RotatingFileHandler - size based
# ---------------------------------------------------------------------------
def demo_rotating_file_handler():
    print("=== 2. RotatingFileHandler (maxBytes=1000, backupCount=3) ===")
    logger = logging.getLogger("demo.rotating")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    path = LOG_DIR / "rotating.log"
    handler = RotatingFileHandler(path, maxBytes=1000, backupCount=3, encoding="utf-8")
    handler.setFormatter(DETAILED)
    logger.addHandler(handler)

    for i in range(1, 41):
        logger.info("Test step %02d executed successfully", i)

    close_handlers(logger)
    files = sorted(p.name for p in LOG_DIR.glob("rotating.log*"))
    print("Files after 40 messages:", files)
    print("rotating.log = newest, rotating.log.3 = oldest; older data is discarded.\n")


# ---------------------------------------------------------------------------
# 3. TimedRotatingFileHandler - time based
# ---------------------------------------------------------------------------
def demo_timed_rotating_file_handler():
    print("=== 3. TimedRotatingFileHandler (when='S', interval=1 for demo) ===")
    print("In real projects use when='midnight', backupCount=7 -> one file per day, keep a week.")
    logger = logging.getLogger("demo.timed")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    path = LOG_DIR / "timed.log"
    handler = TimedRotatingFileHandler(path, when="S", interval=1, backupCount=2, encoding="utf-8")
    handler.setFormatter(DETAILED)
    logger.addHandler(handler)

    for i in range(3):
        logger.info("Message in second %d", i)
        time.sleep(1.1)
    close_handlers(logger)
    files = sorted(p.name for p in LOG_DIR.glob("timed.log*"))
    print("Files:", files)
    print("Rotated files get a timestamp suffix, e.g. timed.log.2026-09-26_10-15-01\n")


# ---------------------------------------------------------------------------
# 4. Log folder cleanup
# ---------------------------------------------------------------------------
def cleanup_logs(folder: Path, pattern="run_*.log", keep_last=5, max_age_days=7):
    """Keep only the newest `keep_last` files AND delete anything older than max_age_days."""
    files = sorted(folder.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    cutoff = time.time() - max_age_days * 86400
    deleted = []
    for index, f in enumerate(files):
        if index >= keep_last or f.stat().st_mtime < cutoff:
            f.unlink()
            deleted.append(f.name)
    return deleted


def demo_cleanup():
    print("=== 4. Log folder cleanup ===")
    # Create some fake old run logs
    for n in range(8):
        fake = LOG_DIR / f"run_fake_{n:02d}.log"
        fake.write_text("old run\n", encoding="utf-8")
        old = time.time() - (n * 2) * 86400          # 0, 2, 4 ... 14 days old
        os.utime(fake, (old, old))
    before = len(list(LOG_DIR.glob("run_*.log")))
    deleted = cleanup_logs(LOG_DIR, keep_last=5, max_age_days=7)
    after = len(list(LOG_DIR.glob("run_*.log")))
    print(f"run_*.log files before: {before}, deleted: {len(deleted)}, after: {after}")
    print("Rule: keep newest 5 AND nothing older than 7 days.")


if __name__ == "__main__":
    demo_console_and_per_run_file()
    demo_rotating_file_handler()
    demo_timed_rotating_file_handler()
    demo_cleanup()
    print("\nDone. Open the examples/logs folder to inspect the files.")
