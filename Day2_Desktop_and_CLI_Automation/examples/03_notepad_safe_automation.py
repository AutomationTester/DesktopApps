r"""
03_notepad_safe_automation.py
=============================
Day 2 - SAFE automation of Windows 11 Notepad

REAL-WORLD LESSON: "NEVER ASSUME A CLEAN APPLICATION STATE"
    Windows 11 Notepad is a Store app with TABS. It RESTORES the user's
    previous tabs on start, and opening a file adds a NEW TAB to the SAME
    window. If a script simply grabs "the Notepad window" and types, it may
    type into somebody's real, unsaved document!

    Our safe pattern:
      1. Create our OWN temporary file (unique name).
      2. Open exactly that file:  notepad.exe <path>
      3. Connect to the window whose title contains OUR file name.
      4. Type, verify, save (Ctrl+S - no dialog because the file exists).
      5. Close ONLY our tab with Ctrl+W.   NEVER call win.close() on Notepad.
      6. Verify the file content FROM DISK (the real test oracle).
      7. Delete the temp file.

TECHNICAL NOTES (verified on Windows 11)
    * backend="uia"
    * Window title: '<filename> - Notepad', gets a leading '*' once modified
      -> use a regular expression: r"\*?name\.txt - Notepad"
    * Editor control: control_type="Document"
    * set_edit_text() is NOT supported here -> use type_keys()
    * type_keys() can drop characters when typing very fast -> use pause=0.05
      and VERIFY with doc.window_text()

HOW TO RUN
    python 03_notepad_safe_automation.py
"""

import os
import re
import subprocess
import tempfile
import time
from pathlib import Path

from pywinauto import Desktop

TEXT_TO_TYPE = "Hello from pywinauto. Day 2 automation test."


def create_temp_file() -> Path:
    """Create an empty, uniquely named .txt file and return its path."""
    fd, path = tempfile.mkstemp(prefix="day2_notepad_", suffix=".txt")
    os.close(fd)                     # we only need the file to exist
    return Path(path)


def open_in_notepad(path: Path, timeout: int = 15):
    """Open OUR file in Notepad and return (window, document) specs."""
    subprocess.Popen(["notepad.exe", str(path)])
    # Match ONLY the window/tab showing our file. re.escape() protects the
    # dots and other special characters in the file name.
    title_pattern = rf"\*?{re.escape(path.name)} - Notepad"
    win = Desktop(backend="uia").window(title_re=title_pattern)
    win.wait("visible", timeout=timeout)
    doc = win.child_window(control_type="Document")
    doc.wait("ready", timeout=timeout)
    return win, doc


def type_text(doc, text: str) -> None:
    """Type text into the editor slowly enough that no key is dropped."""
    doc.set_focus()
    # with_spaces=True -> spaces are typed (by default type_keys ignores them)
    doc.type_keys(text, with_spaces=True, pause=0.05)


def main() -> int:
    path = create_temp_file()
    print("Temp file:", path)
    win = None
    try:
        win, doc = open_in_notepad(path)
        print("Connected to window:", win.window_text())

        type_text(doc, TEXT_TO_TYPE)

        # --- Verification 1: what does the UI show? ---
        on_screen = doc.window_text()
        print("Editor text :", repr(on_screen))
        assert on_screen.strip() == TEXT_TO_TYPE, "Text in editor differs!"

        # --- Save (file already exists -> no Save As dialog) ---
        win.type_keys("^s")
        time.sleep(1)                # give Notepad a moment to write to disk

        # --- Close ONLY our tab ---
        win.type_keys("^w")
        win = None                   # do not touch it any more

        # --- Verification 2: what is really on disk? (the true oracle) ---
        on_disk = path.read_text(encoding="utf-8-sig").strip()
        print("Disk text   :", repr(on_disk))
        if on_disk == TEXT_TO_TYPE:
            print("[PASS] File content matches typed text")
            return 0
        print("[FAIL] File content does not match")
        return 1
    finally:
        # Clean-up must run even if an assertion failed.
        if win is not None:
            try:
                # Close only our tab; if unsaved, Notepad would ask - so save first.
                win.type_keys("^s")
                win.type_keys("^w")
            except Exception:
                pass
        time.sleep(0.5)
        try:
            path.unlink()
            print("Temp file deleted.")
        except OSError as exc:
            print("Could not delete temp file:", exc)


if __name__ == "__main__":
    raise SystemExit(main())
