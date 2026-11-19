"""Synchronisation helpers: poll for a condition instead of time.sleep(), retry flaky actions."""
import functools
import time

from core.logger import get_logger

log = get_logger("waits")


class WaitTimeoutError(Exception):
    pass


def wait_until(condition, timeout=10, interval=0.1, message="condition"):
    """Call condition() until it returns a truthy value or `timeout` seconds pass.
    Exceptions raised by condition() count as 'not yet'. Returns the truthy value."""
    end = time.monotonic() + timeout
    last_error = None
    while True:
        try:
            result = condition()
            if result:
                return result
        except Exception as exc:
            last_error = exc
        if time.monotonic() >= end:
            detail = f" (last error: {last_error})" if last_error else ""
            raise WaitTimeoutError(f"Timed out after {timeout}s waiting for {message}{detail}")
        time.sleep(interval)


def retry(times=3, delay=0.5, backoff=2.0, exceptions=(Exception,)):
    """Decorator with exponential backoff: waits delay, delay*backoff, ... between attempts."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == times:
                        log.error("%s failed after %d attempts: %s", func.__name__, times, exc)
                        raise
                    log.warning("%s attempt %d/%d failed: %s - retrying in %.2fs",
                                func.__name__, attempt, times, exc, wait)
                    time.sleep(wait)
                    wait *= backoff
        return wrapper
    return decorator
