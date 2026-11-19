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
    """Log folder cleanup: delete the oldest run_*.log files so that, together with the
    new file about to be created, only `keep_last` remain. Return how many were deleted."""
    # TODO (Lab 1, step 4):
    #   old_logs = sorted(LOG_DIR.glob("run_*.log"))   (names contain a timestamp -> sorted = oldest first)
    #   delete old_logs[:max(0, len(old_logs) - (keep_last - 1))]
    raise NotImplementedError


def setup_logging(level="INFO", keep_last=5, console=True):
    """Configure the 'minifw' logger ONCE per run and return the log file path."""
    global _log_file
    if _log_file is not None:              # already configured -> no duplicate handlers
        return _log_file

    LOG_DIR.mkdir(exist_ok=True)
    deleted = cleanup_old_logs(keep_last)
    _log_file = LOG_DIR / f"run_{datetime.now():%Y%m%d_%H%M%S_%f}.log"

    root = logging.getLogger(ROOT_LOGGER)
    root.setLevel(logging.DEBUG)

    # TODO (Lab 1, step 4):
    #   1. FileHandler(_log_file, encoding="utf-8"), level = `level`, formatter FILE_FORMAT
    #   2. if console: StreamHandler(sys.stdout), level INFO, formatter CONSOLE_FORMAT
    #   3. add both handlers to `root`

    root.info("Log file: %s (deleted %d old log(s))", _log_file.name, deleted)
    return _log_file


def get_logger(name):
    """Child logger, e.g. get_logger('pages.calculator') -> 'minifw.pages.calculator'."""
    # TODO (Lab 1, step 4): return logging.getLogger(f"{ROOT_LOGGER}.{name}")
    raise NotImplementedError
