"""
01_sleep_vs_wait_after.py  -  GOOD: explicit wait (poll a condition)
====================================================================
Same random-start-up FakeApp as the "before" file, but we POLL the
condition until it is true or a TIMEOUT expires:

  * fast app -> we continue immediately (no wasted time)
  * slow app -> we keep waiting up to the timeout
  * broken app -> we fail with a CLEAR message after the timeout

This is exactly what pywinauto's  window.wait("visible", timeout=10)
and the framework's  core.waits.wait_until(...)  do for you.

Run:
    python 01_sleep_vs_wait_after.py
"""

import random
import threading
import time
from typing import Callable


class FakeApp:
    def __init__(self) -> None:
        self.ready = False

    def start(self) -> None:
        delay = random.uniform(0.2, 2.0)
        print(f"[app] starting... (will need {delay:.2f}s)")
        threading.Timer(delay, self._become_ready).start()

    def _become_ready(self) -> None:
        self.ready = True


def wait_until(condition: Callable[[], bool], timeout: float = 5.0,
               interval: float = 0.1, message: str = "condition") -> float:
    """Poll `condition` every `interval` seconds until it returns True.

    Returns the seconds waited. Raises TimeoutError after `timeout`.
    """
    start = time.perf_counter()
    while True:
        if condition():
            return time.perf_counter() - start
        if time.perf_counter() - start > timeout:
            raise TimeoutError(f"Timed out after {timeout}s waiting for {message}")
        time.sleep(interval)           # small sleep INSIDE a poll loop is fine


def main() -> int:
    app = FakeApp()
    app.start()
    try:
        waited = wait_until(lambda: app.ready, timeout=5, message="app ready")
    except TimeoutError as exc:
        print("[FAIL]", exc)
        return 1
    print(f"[PASS] app ready after {waited:.2f}s (no time wasted)")
    return 0


if __name__ == "__main__":
    results = [main() for _ in range(5)]
    print(f"\nFailures: {sum(results)} of {len(results)} runs")

    # A broken app that never gets ready -> clear, fast failure message
    print("\nDemo: condition that never becomes true (timeout=1s)")
    try:
        wait_until(lambda: False, timeout=1, message="never-ready window")
    except TimeoutError as exc:
        print("Got expected error:", exc)
