"""
07_handle_dialogs_focus.py
==========================
Day 2 - Handling focus, multiple windows, waits and dialogs

SCENARIO
    1. Open Calculator AND our own temp file in Notepad (two apps).
    2. Switch focus between them and check which one is active.
    3. Open a real MODAL dialog in Notepad - "Save as" (Ctrl+Shift+S) -
       detect it, inspect it, and CANCEL it (harmless: nothing is saved).
    4. Show what happens when we wait for a window that never appears.
    5. Clean up: close Calculator, close ONLY our Notepad tab (Ctrl+W).

WHY IT MATTERS FOR TESTERS
    * Keyboard input goes to the FOCUSED window only. Wrong focus = keys
      typed into the wrong app (maybe your e-mail!).
    * Dialogs are separate windows that BLOCK their owner. Until the dialog
      is handled, the main window ignores input -> tests "hang".
    * Never use time.sleep() to wait for UI; use wait()/exists(timeout=...).

NOTE: Notepad restores the user's tabs. We never call close() on Notepad.
"""

import os
import re
import subprocess
import tempfile
import time
from pathlib import Path

from pywinauto import Desktop
from pywinauto.timings import TimeoutError as UiTimeoutError


def open_calculator():
    calc = Desktop(backend="uia").window(title="Calculator")
    if not calc.exists(timeout=1):   # reuse an open Calculator: every calc.exe
        subprocess.Popen("calc.exe")   # launch opens ANOTHER window -> "2 elements match"
    calc.wait("visible", timeout=10)
    return calc


def open_temp_notepad():
    fd, name = tempfile.mkstemp(prefix="day2_dialogs_", suffix=".txt")
    os.close(fd)
    path = Path(name)
    subprocess.Popen(["notepad.exe", str(path)])
    win = Desktop(backend="uia").window(
        title_re=rf"\*?{re.escape(path.name)} - Notepad"
    )
    win.wait("visible", timeout=15)
    return path, win


def find_save_as_dialog(notepad_win, timeout: float = 5):
    """The Save-as dialog is usually a CHILD of the Notepad window in the UIA
    tree; on some builds it is top-level. Check both places."""
    candidates = [
        notepad_win.child_window(title_re="(?i)^save as$", control_type="Window"),
        Desktop(backend="uia").window(title_re="(?i)^save as$"),
    ]
    end = time.time() + timeout
    while time.time() < end:
        for dlg in candidates:
            if dlg.exists(timeout=0.5):
                return dlg
    return None


def main() -> None:
    calc = open_calculator()
    path, notepad = open_temp_notepad()
    print("Opened Calculator and", path.name)

    # ---- 1. Focus switching -------------------------------------------
    for target, label in [(calc, "Calculator"), (notepad, "Notepad"), (calc, "Calculator")]:
        target.set_focus()                    # bring to front + keyboard focus
        time.sleep(0.5)
        print(f"set_focus({label:<10}) -> calc active={calc.is_active()}, "
              f"notepad active={notepad.is_active()}")

    # ---- 2. Element states -------------------------------------------
    eq = calc.child_window(auto_id="equalButton", control_type="Button")
    print("\nEquals button states: exists =", eq.exists(),
          "| visible =", eq.is_visible(), "| enabled =", eq.is_enabled())

    # ---- 3. A modal dialog -------------------------------------------
    notepad.set_focus()
    notepad.type_keys("^+s")                  # Ctrl+Shift+S = Save as...
    dlg = find_save_as_dialog(notepad)
    if dlg is None:
        print("\n[WARN] Save as dialog did not appear")
    else:
        print("\nDialog detected:", repr(dlg.window_text()))
        # Inspect the dialog's buttons (a mini print_control_identifiers)
        for btn in dlg.descendants(control_type="Button"):
            text = btn.window_text()
            if text:
                print("   button:", text)
        # Handle it: press Cancel (fallback: Escape key)
        cancel = dlg.child_window(title="Cancel", control_type="Button")
        if cancel.exists(timeout=2):
            cancel.invoke()
        else:
            dlg.type_keys("{ESC}")
        dlg.wait_not("visible", timeout=5)    # wait until it is GONE
        print("Dialog cancelled and closed.")

    # ---- 4. Waiting for something that never comes ------------------
    ghost = Desktop(backend="uia").window(title="Window That Does Not Exist")
    print("\nexists(timeout=2) ->", ghost.exists(timeout=2))   # returns False
    try:
        ghost.wait("visible", timeout=2)                        # raises
    except UiTimeoutError:
        print("wait('visible') raised TimeoutError -> report a clear failure")

    # ---- 5. Clean-up ------------------------------------------------
    calc.close()
    notepad.set_focus()
    notepad.type_keys("^w")          # close ONLY our tab (file is unmodified)
    time.sleep(0.5)
    path.unlink(missing_ok=True)
    print("\nClean-up done.")


if __name__ == "__main__":
    main()
