"""
03_cleanup_finally.py  -  cleanup that ALWAYS runs
==================================================
A test that fails half-way must still:
  * close the app / tab it opened
  * delete the temp files it created
  * stop child processes it started
Otherwise the NEXT test starts from a dirty state and fails too
(one real failure turns into 20 "cascade" failures).

Three equivalent tools are shown:
  A) try / finally
  B) a context manager (with ... :)  via contextlib.contextmanager
  C) a pytest fixture with yield     (shown as code in the docstring below)

    @pytest.fixture
    def temp_text_file(tmp_path):
        path = tmp_path / "notes.txt"
        path.write_text("", encoding="utf-8")
        yield path                  # <- the test runs here
        path.unlink(missing_ok=True)  # <- teardown runs even if the test failed

Run:
    python 03_cleanup_finally.py
"""

import contextlib
import os
import tempfile
from pathlib import Path


# ---------- A) try / finally ---------------------------------------------
def test_with_try_finally(should_fail: bool) -> None:
    fd, name = tempfile.mkstemp(prefix="day5_", suffix=".txt")
    os.close(fd)        # mkstemp returns an OPEN handle - close it, or Windows
    tmp = Path(name)    # refuses to delete the file later (WinError 32)
    print(f"  created {tmp.name}")
    try:
        tmp.write_text("result=15", encoding="utf-8")
        if should_fail:
            raise AssertionError("expected 16 but got 15")
        print("  test body passed")
    finally:
        tmp.unlink(missing_ok=True)       # runs on success AND on failure
        print(f"  cleanup: deleted {tmp.name} -> exists? {tmp.exists()}")


# ---------- B) context manager -------------------------------------------
@contextlib.contextmanager
def temp_file(prefix: str = "day5_ctx_"):
    fd, name = tempfile.mkstemp(prefix=prefix, suffix=".txt")
    os.close(fd)
    path = Path(name)
    print(f"  [setup] {path.name}")
    try:
        yield path
    finally:
        path.unlink(missing_ok=True)
        print(f"  [teardown] removed {path.name}")


def main() -> None:
    print("A) try/finally - passing test")
    test_with_try_finally(should_fail=False)

    print("\nA) try/finally - FAILING test (error is caught for the demo)")
    try:
        test_with_try_finally(should_fail=True)
    except AssertionError as exc:
        print("  test failed as expected:", exc)

    print("\nB) context manager - failing body")
    try:
        with temp_file() as path:
            path.write_text("data", encoding="utf-8")
            raise RuntimeError("something broke inside the test")
    except RuntimeError as exc:
        print("  caught:", exc)
        print("  file still exists?", path.exists())


if __name__ == "__main__":
    main()
