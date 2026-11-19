"""Logging for the whole run: console (INFO+) and one log file per run (level from config)."""
import logging
import sys
from datetime import datetime

from core.paths import LOG_DIR

ROOT_LOGGER = "minifw"
FILE_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"
CONSOLE_FORMAT = "%(levelname)-8s %(name)s | %(message)s"

_log_file = None


def cleanup_old_logs(keep_last):
    """Log folder cleanup: delete the oldest run logs so that, with the new one, keep_last remain."""
    old_logs = sorted(LOG_DIR.glob("run_*.log"))
    to_delete = old_logs[:max(0, len(old_logs) - (keep_last - 1))]
    for old in to_delete:
        old.unlink(missing_ok=True)
    return len(to_delete)


def setup_logging(level="INFO", keep_last=5, console=True):
    """Configure the root framework logger ONCE per run. Returns the log file path."""
    global _log_file
    if _log_file is not None:              # already configured -> no duplicate handlers
        return _log_file

    LOG_DIR.mkdir(exist_ok=True)
    deleted = cleanup_old_logs(keep_last)
    _log_file = LOG_DIR / f"run_{datetime.now():%Y%m%d_%H%M%S_%f}.log"

    root = logging.getLogger(ROOT_LOGGER)
    root.setLevel(logging.DEBUG)           # handlers decide what is actually written

    file_handler = logging.FileHandler(_log_file, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(FILE_FORMAT))
    root.addHandler(file_handler)

    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(CONSOLE_FORMAT))
        root.addHandler(console_handler)

    root.info("Log file: %s (deleted %d old log(s))", _log_file.name, deleted)
    return _log_file


def get_logger(name):
    """Child logger, e.g. get_logger('pages.calculator') -> 'minifw.pages.calculator'.
    Children send their records up to the 'minifw' handlers."""
    return logging.getLogger(f"{ROOT_LOGGER}.{name}")
