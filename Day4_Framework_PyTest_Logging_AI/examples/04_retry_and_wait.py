"""
Day 4 - Example 04: Smart retries and synchronization
=====================================================
Desktop/CLI automation is flaky mainly because of TIMING:
windows open slowly, files appear late, a process is still busy.

Bad fix  : time.sleep(10)      -> slow when app is fast, still fails when app is slower
Good fix : poll a CONDITION until it is true or a timeout expires (wait_until)
         : retry a FLAKY ACTION a few times with exponential backoff (@retry)

The same two helpers exist in automation_framework/core/waits.py.
Everything here is simulated, so it runs anywhere without a GUI.

Run:
    python 04_retry_and_wait.py
"""
import functools
import logging
import sys
import random
import time

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format="%(asctime)s | %(levelname)-7s | %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger("waits")


# ---------------------------------------------------------------------------
# 1. Polling wait
# ---------------------------------------------------------------------------
class WaitTimeoutError(Exception):
    pass


def wait_until(condition, timeout=5.0, interval=0.25, message="condition"):
    """Call condition() every `interval` seconds until it returns truthy or timeout expires.
    Returns the truthy value so callers can use it (e.g. the found window)."""
    end = time.monotonic() + timeout
    attempts = 0
    while True:
        attempts += 1
        try:
            result = condition()
            if result:
                log.info("'%s' satisfied after %d poll(s)", message, attempts)
                return result
        except Exception as exc:                      # e.g. element not found yet
            log.debug("poll %d raised %s", attempts, exc)
        if time.monotonic() >= end:
            raise WaitTimeoutError(f"Timed out after {timeout}s waiting for {message}")
        time.sleep(interval)


# ---------------------------------------------------------------------------
# 2. Retry decorator with exponential backoff
# ---------------------------------------------------------------------------
def retry(times=3, delay=0.2, backoff=2.0, exceptions=(Exception,)):
    """Retry the decorated function on the listed exceptions.
    Waits delay, delay*backoff, delay*backoff^2 ... between attempts."""
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
                    log.warning("%s attempt %d/%d failed (%s) - retrying in %.2fs",
                                func.__name__, attempt, times, exc, wait)
                    time.sleep(wait)
                    wait *= backoff
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# Simulated "application"
# ---------------------------------------------------------------------------
class FakeApp:
    """Window becomes visible ~1 second after start(); click fails randomly."""

    def __init__(self):
        self.started_at = None

    def start(self):
        self.started_at = time.monotonic()
        log.info("App launch requested")

    def is_window_visible(self):
        return self.started_at is not None and time.monotonic() - self.started_at > 1.0


_click_calls = {"n": 0}


@retry(times=4, delay=0.1, backoff=2, exceptions=(RuntimeError,))
def click_save_button():
    """Fails on the first 2 calls (simulates a busy UI), succeeds on the 3rd."""
    _click_calls["n"] += 1
    if _click_calls["n"] < 3:
        raise RuntimeError("button not clickable yet")
    log.info("Save button clicked")
    return True


@retry(times=3, delay=0.1, exceptions=(RuntimeError,))
def always_broken():
    raise RuntimeError("element does not exist")


if __name__ == "__main__":
    random.seed(1)
    print("\n=== 1. Polling wait instead of time.sleep ===")
    app = FakeApp()
    app.start()
    t0 = time.monotonic()
    wait_until(app.is_window_visible, timeout=5, interval=0.2, message="main window visible")
    print(f"Waited only {time.monotonic() - t0:.1f}s (a fixed sleep(5) would waste ~4s)")

    print("\n=== 2. Timeout when the condition never becomes true ===")
    try:
        wait_until(lambda: False, timeout=0.6, interval=0.2, message="dialog 'Saved'")
    except WaitTimeoutError as e:
        print("Caught:", e)

    print("\n=== 3. Retry with exponential backoff (succeeds on 3rd attempt) ===")
    click_save_button()

    print("\n=== 4. Retry gives up and re-raises the real error ===")
    try:
        always_broken()
    except RuntimeError as e:
        print("Caught after retries:", e)

    print("\nRule of thumb: WAIT for states, RETRY actions, never retry assertions to hide bugs.")
