"""
Lab 2 - SOLUTION: Safe Notepad automation (write, save, verify from disk)

Run:  python lab2_notepad_safe.py
      python lab2_notepad_safe.py --text "Custom text to type" --keep

Rules followed (Windows 11 Notepad restores the user's own tabs!):
  * Work ONLY on our own temp file, found by its unique file name
  * Close ONLY our tab with Ctrl+W - never call close() on the window
  * The oracle is the file on disk, not the screen
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from pywinauto import Desktop

DEFAULT_TEXT = "Automated by pywinauto on Day 2. Test ID NP-001."


def create_temp_file() -> Path:
    fd, name = tempfile.mkstemp(prefix="lab2_", suffix=".txt")
    os.close(fd)
    return Path(name)


def connect_to_notepad_tab(path: Path, timeout: int = 15):
    subprocess.Popen(["notepad.exe", str(path)])
    win = Desktop(backend="uia").window(
        title_re=rf"\*?{re.escape(path.name)} - Notepad"
    )
    win.wait("visible", timeout=timeout)
    doc = win.child_window(control_type="Document")
    doc.wait("ready", timeout=timeout)
    return win, doc


def type_and_verify(doc, text: str, attempts: int = 2) -> str:
    """type_keys may drop characters; retry once after clearing the editor."""
    shown = ""
    for attempt in range(1, attempts + 1):
        doc.set_focus()
        if attempt > 1:
            doc.type_keys("^a{DELETE}")          # clear OUR file's content
        doc.type_keys(text, with_spaces=True, pause=0.05)
        shown = doc.window_text().strip()
        if shown == text:
            break
        print(f"  attempt {attempt}: editor shows {shown!r} - retrying")
    return shown


def main() -> int:
    parser = argparse.ArgumentParser(description="Safe Notepad automation lab")
    parser.add_argument("--text", default=DEFAULT_TEXT, help="text to type")
    parser.add_argument("--keep", action="store_true", help="keep the temp file")
    args = parser.parse_args()

    # type_keys treats + ^ % ~ ( ) { } as special keys - refuse them here
    if re.search(r"[+^%~(){}\[\]]", args.text):
        parser.error("text must not contain + ^ % ~ ( ) { } [ ] (type_keys specials)")

    path = create_temp_file()
    print("Working file:", path)
    win = None
    result = 1
    try:
        win, doc = connect_to_notepad_tab(path)
        print("Connected   :", win.window_text())

        shown = type_and_verify(doc, args.text)
        print("Editor text :", repr(shown))

        win.type_keys("^s")                          # save - no dialog
        # Wait until the '*' (unsaved marker) disappears from the title
        saved_title = f"{path.name} - Notepad"
        deadline = time.time() + 5
        while time.time() < deadline and win.window_text() != saved_title:
            time.sleep(0.2)

        win.type_keys("^w")                          # close ONLY our tab
        win = None

        on_disk = path.read_text(encoding="utf-8-sig").strip()
        print("Disk text   :", repr(on_disk))
        if on_disk == args.text:
            print("[PASS] File on disk contains the typed text")
            result = 0
        else:
            print("[FAIL] File on disk differs from typed text")
    finally:
        if win is not None:                          # something went wrong mid-way
            try:
                win.type_keys("^s")
                win.type_keys("^w")
            except Exception as exc:
                print("Clean-up warning:", exc)
        if not args.keep:
            time.sleep(0.5)
            path.unlink(missing_ok=True)
    return result


if __name__ == "__main__":
    sys.exit(main())
