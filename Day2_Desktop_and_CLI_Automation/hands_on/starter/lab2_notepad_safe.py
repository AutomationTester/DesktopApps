"""
Lab 2 - STARTER: Safe Notepad automation (write, save, verify from disk)

!!! SAFETY FIRST !!!
Windows 11 Notepad restores YOUR previous tabs and opens files as new tabs
in the SAME window. Therefore:
  * never type into "any" Notepad window - only into the tab of OUR temp file
  * never call win.close() on Notepad - close only our tab with Ctrl+W

Run:  python lab2_notepad_safe.py
"""

import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from pywinauto import Desktop

TEXT = "Automated by pywinauto on Day 2. Test ID NP-001."


def create_temp_file() -> Path:
    # TODO 1: use tempfile.mkstemp(prefix="lab2_", suffix=".txt"),
    #         close the returned file descriptor with os.close(), return a Path
    raise NotImplementedError("create_temp_file")


def connect_to_notepad_tab(path: Path, timeout: int = 15):
    # TODO 2: open the file:  subprocess.Popen(["notepad.exe", str(path)])
    # TODO 3: connect with a title REGEX that matches ONLY our file:
    #         rf"\*?{re.escape(path.name)} - Notepad"   (the '*' = unsaved)
    # TODO 4: wait("visible"), get the editor: child_window(control_type="Document")
    # return win, doc
    raise NotImplementedError("connect_to_notepad_tab")


def main() -> int:
    path = create_temp_file()
    print("Working file:", path)
    try:
        win, doc = connect_to_notepad_tab(path)

        # TODO 5: doc.set_focus(); doc.type_keys(TEXT, with_spaces=True, pause=0.05)
        # TODO 6: verify doc.window_text() equals TEXT (print it)
        # TODO 7: save with win.type_keys("^s") and wait ~1 s
        # TODO 8: close ONLY our tab with win.type_keys("^w")
        # TODO 9: read the file from disk (encoding="utf-8-sig") and compare
        #         print [PASS] or [FAIL] and return 0 / 1
        return 1
    finally:
        time.sleep(0.5)
        # TODO 10: delete the temp file (path.unlink(missing_ok=True))


if __name__ == "__main__":
    sys.exit(main())
