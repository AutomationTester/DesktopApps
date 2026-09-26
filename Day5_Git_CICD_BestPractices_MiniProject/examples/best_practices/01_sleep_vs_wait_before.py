"""
01_sleep_vs_wait_before.py  -  BAD: fixed sleeps  (anti-pattern)
=================================================================
Simulates an application that becomes "ready" after a RANDOM delay
(just like a desktop app that sometimes starts in 0.5 s and sometimes in 3 s).

The script uses a FIXED time.sleep(1). Result:
  * when the app is fast  -> we wasted time waiting for nothing
  * when the app is slow  -> the test FAILS (flaky test!)

Run it several times - you will see random PASS / FAIL:
    python 01_sleep_vs_wait_before.py
"""

import random
import threading
import time


class FakeApp:
    """Pretends to be an app that needs a random start-up time."""

    def __init__(self) -> None:
        self.ready = False

    def start(self) -> None:
        delay = random.uniform(0.2, 2.0)
        print(f"[app] starting... (will need {delay:.2f}s)")
        threading.Timer(delay, self._become_ready).start()

    def _become_ready(self) -> None:
        self.ready = True


def main() -> int:
    app = FakeApp()
    started = time.perf_counter()
    app.start()

    time.sleep(1)                      # BAD: hope 1 second is always enough

    elapsed = time.perf_counter() - started
    if app.ready:
        print(f"[PASS] app ready - but we waited a fixed {elapsed:.2f}s")
        return 0
    print(f"[FAIL] app NOT ready after {elapsed:.2f}s -> flaky test!")
    return 1


if __name__ == "__main__":
    # Run 5 attempts to make the flakiness visible
    results = [main() for _ in range(5)]
    time.sleep(2.1)                    # let background timers finish quietly
    print(f"\nFailures: {sum(results)} of {len(results)} runs")
