"""
04_kill_leftover_process.py  -  stop leftover processes SAFELY
==============================================================
A crashed test can leave its application running (a hung Calculator,
a CLI tool stuck waiting for input...). The next test then connects to
the wrong window or finds a locked file.

GOLDEN RULE: only kill processes that YOUR test started.
    * Keep the Popen object / PID of what you launched.
    * NEVER do  "taskkill /IM notepad.exe /F"  on a shared machine -
      that kills the user's (or a colleague's) Notepad too!
    * For Store apps (Win11 Calculator/Notepad) the launcher PID is not the
      window's PID - close via the UI (e.g. Ctrl+W for your Notepad tab) or
      via the window's own process_id() obtained from pywinauto.

This demo is 100% safe: it starts its OWN child Python process that
"hangs", then terminates exactly that child.

Run:
    python 04_kill_leftover_process.py
"""

import subprocess
import sys
import time

HANG_FOREVER = "import time\nwhile True: time.sleep(1)"


def start_hung_child() -> subprocess.Popen:
    """Start a child python process that never exits (simulated hung app)."""
    return subprocess.Popen([sys.executable, "-c", HANG_FOREVER])


def stop_process(proc: subprocess.Popen, timeout: float = 5.0) -> str:
    """Politely terminate, then force-kill if needed. Returns what happened."""
    if proc.poll() is not None:
        return f"already exited with code {proc.returncode}"
    proc.terminate()                         # polite request (SIGTERM / TerminateProcess)
    try:
        proc.wait(timeout=timeout)
        return f"terminated (code {proc.returncode})"
    except subprocess.TimeoutExpired:
        proc.kill()                          # last resort
        proc.wait(timeout=timeout)
        return f"killed (code {proc.returncode})"


class ProcessTracker:
    """Remembers every process a test starts and stops them all at the end."""

    def __init__(self) -> None:
        self._procs: list[subprocess.Popen] = []

    def start(self, args: list[str]) -> subprocess.Popen:
        proc = subprocess.Popen(args)
        self._procs.append(proc)
        return proc

    def cleanup(self) -> None:
        for proc in self._procs:
            print(f"  cleanup PID {proc.pid}: {stop_process(proc)}")
        self._procs.clear()


def main() -> None:
    print("1) Single leftover process")
    child = start_hung_child()
    time.sleep(0.5)
    print(f"  started child PID {child.pid}, running? {child.poll() is None}")
    print(f"  -> {stop_process(child)}")
    print(f"  running now? {child.poll() is None}")

    print("\n2) Tracker used like a fixture: cleanup runs even if the test fails")
    tracker = ProcessTracker()
    try:
        tracker.start([sys.executable, "-c", HANG_FOREVER])
        tracker.start([sys.executable, "-c", HANG_FOREVER])
        raise AssertionError("simulated test failure")
    except AssertionError as exc:
        print("  test failed:", exc)
    finally:
        tracker.cleanup()


if __name__ == "__main__":
    main()
