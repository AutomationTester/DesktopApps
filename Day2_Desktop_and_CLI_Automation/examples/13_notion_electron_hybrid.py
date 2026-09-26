"""
13_notion_electron_hybrid.py
============================
Day 2 - Automating a REAL Electron app (Notion desktop): pywinauto + pyautogui

WHY NOTION?
    Notion desktop is an ELECTRON app: a Chromium browser inside a window
    (class name Chrome_WidgetWin_1, like VS Code, Teams, Slack). pywinauto
    sees the window, but the page content is HTML drawn by Chromium.
    Its UI Automation tree is only partly usable: names change, many blocks
    have no ID, and features like drag and drop exist ONLY for the mouse.
    Typical real-world mix:
        pywinauto  -> find the window, check its title, find rough element
                      positions (when the Chromium tree exposes them)
        pyautogui  -> keyboard shortcuts, typing, hover, drag and drop
        clipboard  -> the test ORACLE: copy the page as text and check it

SAFETY - NOTION HOLDS SOMEBODY'S REAL NOTES
    Same rule as Notepad in example 03: never touch existing content.
      1. Create our OWN new page (Ctrl+N) with a unique title.
      2. GATE: before typing anything, check the window title shows a new,
         empty page. If not, stop - otherwise we could type into a real page.
      3. Check the title again before cleanup, so we only ever trash OUR page.
      4. Save and restore the user's clipboard text.

WHAT IT DOES
    1. Connect to Notion (or start it) and bring it to the front
    2. Ctrl+N -> new page, type a unique title (gate: window title check)
    3. Slash command "/todo" -> to-do block, then two text blocks A and B
    4. Oracle: select all blocks, Ctrl+C, read the clipboard
    5. Hover block B -> Notion shows its drag handle; DRAG B above A
       Fallback when the mouse drag fails: Esc + Ctrl+Shift+Up (keyboard)
    6. Oracle again: B must now come before A
    7. Clean-up: "..." menu -> Move to trash (or tell you to delete it)

REQUIREMENTS
    Notion desktop installed and SIGNED IN (a free account is enough).
    Written for Notion desktop 4.x on Windows 11. Notion changes its UI
    often: if a step fails, run with --inspect and update the names below.

HOW TO RUN
    python 13_notion_electron_hybrid.py              -> full demo
    python 13_notion_electron_hybrid.py --keep       -> do not trash the page
    python 13_notion_electron_hybrid.py --inspect    -> dump Notion's UIA tree
                                                        to notion_tree.txt
    Hands off the mouse and keyboard. Emergency stop: mouse into a corner.
"""

import argparse
import ctypes
import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path

import pyautogui
import win32clipboard
from pywinauto import Desktop
from pywinauto.application import process_module

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.25

DEFAULT_EXE = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Notion" / "Notion.exe"

# Title Notion shows for a brand-new, empty page. Adjust if your version differs.
NEW_PAGE_TITLE_RE = re.compile(r"(?i)^(untitled|new page)\b")
# Names of the "..." page menu and its trash item (check them with --inspect)
MORE_BUTTON_RE = r"(?i)^(more actions|more|actions)$"
TRASH_ITEM_RE = r"(?i)^(move to trash|delete)"

TODO_TEXT = "Review the test results"
BLOCK_A = "Block A typed by pyautogui"
BLOCK_B = "Block B dragged by the mouse"
HANDLE_OFFSET = 18      # px (at 100 % scaling) from block text to its drag handle


# ---- pywinauto: find the Notion window ------------------------------------
def find_notion_window(timeout: float = 30):
    """Return the main Notion window. Electron starts MANY Notion.exe
    processes; we pick the visible Chrome_WidgetWin_1 window owned by one."""
    end = time.time() + timeout
    while time.time() < end:
        for w in Desktop(backend="uia").windows(class_name="Chrome_WidgetWin_1",
                                                visible_only=True):
            exe = process_module(w.element_info.process_id) or ""
            if exe.lower().endswith("notion.exe") and w.window_text():
                return w
        time.sleep(0.5)
    return None


def connect_or_start(exe: Path):
    win = find_notion_window(timeout=1)
    if win is None:
        if not exe.exists():
            raise SystemExit(f"Notion not found at {exe} - install it or pass --exe")
        # --force-renderer-accessibility: ask Chromium to build its UIA tree,
        # so pywinauto can see page elements (only works on a fresh start)
        subprocess.Popen([str(exe), "--force-renderer-accessibility"])
        win = find_notion_window(timeout=30)
        if win is None:
            raise SystemExit("Notion window did not appear within 30 s")
        time.sleep(3)                          # let the workspace finish loading
    win.set_focus()
    return win


def wait_title(win, check, timeout: float = 8) -> str:
    """Electron apps copy the page title into the window title - a cheap
    oracle that needs no access to the page content."""
    end = time.time() + timeout
    title = win.window_text()
    while not check(title) and time.time() < end:
        time.sleep(0.2)
        title = win.window_text()
    return title


def find_text_element(win, text: str):
    """Look for the innermost UIA element showing `text`. Returns None when
    Chromium does not expose the page content (then we use the keyboard)."""
    best = None
    try:
        for el in win.descendants():
            try:
                if text in el.window_text():
                    r = el.rectangle()
                    if r.width() > 0 and (best is None or
                                          r.width() * r.height() <
                                          best.rectangle().width() * best.rectangle().height()):
                        best = el
            except Exception:                  # elements vanish while we look
                continue
    except Exception:
        return None
    return best


def dpi_scale(win) -> float:
    return ctypes.windll.user32.GetDpiForWindow(win.handle) / 96


# ---- clipboard oracle -------------------------------------------------------
def get_clipboard() -> str:
    for _ in range(10):                        # the clipboard may be busy
        try:
            win32clipboard.OpenClipboard()
            try:
                if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                    return win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                return ""
            finally:
                win32clipboard.CloseClipboard()
        except Exception:
            time.sleep(0.1)
    return ""


def set_clipboard(text: str) -> None:
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    finally:
        win32clipboard.CloseClipboard()


def copy_page_text() -> str:
    """Select every block of the page and copy it as plain text."""
    set_clipboard("")
    pyautogui.press("esc")                     # Esc = select the current block
    pyautogui.hotkey("ctrl", "a")              # with a block selected: all blocks
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.5)
    text = get_clipboard()
    pyautogui.press("esc")                     # clear the selection
    return text


def order_ok(text: str, first: str, second: str) -> bool:
    return first in text and second in text and text.index(first) < text.index(second)


# ---- the steps ----------------------------------------------------------------
def create_test_page(win, title: str) -> bool:
    old_title = win.window_text()
    pyautogui.hotkey("ctrl", "n")              # Notion: new page
    now = wait_title(win, lambda t: t != old_title and NEW_PAGE_TITLE_RE.search(t))
    if not NEW_PAGE_TITLE_RE.search(now):
        # THE SAFETY GATE: typing now could change a real page -> stop
        print(f"[STOP] Expected a new empty page, window title is {now!r}.")
        print("       Nothing was typed. Adjust NEW_PAGE_TITLE_RE if needed.")
        return False
    pyautogui.write(title, interval=0.02)      # the caret starts in the title
    now = wait_title(win, lambda t: title in t)
    ok = title in now
    print(f"[{'PASS' if ok else 'FAIL'}] new page created, window title = {now!r}")
    return ok


def type_blocks() -> None:
    pyautogui.press("enter")                   # title -> first body block
    pyautogui.write("/todo", interval=0.05)    # slash command menu
    time.sleep(0.8)                            # wait for the menu to filter
    pyautogui.press("enter")                   # -> to-do block
    pyautogui.write(TODO_TEXT, interval=0.02)
    pyautogui.press("enter")                   # new to-do ...
    pyautogui.press("backspace")               # ... turned back into plain text
    pyautogui.write(BLOCK_A, interval=0.02)
    pyautogui.press("enter")
    pyautogui.write(BLOCK_B, interval=0.02)    # caret stays in block B


def check_typed_blocks() -> bool:
    text = copy_page_text()
    ok = order_ok(text, TODO_TEXT, BLOCK_A) and order_ok(text, BLOCK_A, BLOCK_B)
    print(f"[{'PASS' if ok else 'FAIL'}] blocks typed, clipboard = {text!r}")
    return ok


def drag_block_b_above_a(win, a, b) -> bool:
    """Mouse drag using Notion's drag handle - the part only pyautogui can do."""
    ra, rb = a.rectangle(), b.rectangle()
    scale = dpi_scale(win)
    pyautogui.moveTo(rb.left + 20, rb.mid_point().y, duration=0.4)   # hover block B
    time.sleep(0.5)                                                  # handle fades in
    hx, hy = rb.left - int(HANDLE_OFFSET * scale), rb.mid_point().y
    pyautogui.moveTo(hx, hy, duration=0.3)                           # onto the handle
    # Web apps need a real press, a pause and several small moves (see ex. 12)
    pyautogui.mouseDown()
    time.sleep(0.3)
    pyautogui.moveRel(0, -5, duration=0.1)                           # start the drag
    pyautogui.moveTo(ra.left + 40, ra.top + 3, duration=0.8)         # top edge of A
    time.sleep(0.3)                                                  # drop indicator
    pyautogui.mouseUp()
    time.sleep(0.5)
    ok = order_ok(copy_page_text(), BLOCK_B, BLOCK_A)
    print(f"[{'PASS' if ok else 'FAIL'}] mouse drag: block B is above block A")
    return ok


def move_block_b_with_keyboard(b=None) -> bool:
    """Fallback: Notion's own shortcut. Needs the caret in block B - either
    still there after typing, or put there by clicking the element b."""
    if b is not None:
        r = b.rectangle()
        pyautogui.click(r.right - 2, r.mid_point().y)   # caret at the end of B
    pyautogui.press("esc")                     # select block B
    pyautogui.hotkey("ctrl", "shift", "up")    # move it one block up
    pyautogui.press("esc")
    ok = order_ok(copy_page_text(), BLOCK_B, BLOCK_A)
    print(f"[{'PASS' if ok else 'FAIL'}] keyboard fallback: block B is above block A")
    return ok


def trash_test_page(win, title: str) -> bool:
    if title not in win.window_text():         # never trash somebody else's page
        print(f"[SKIP] window shows {win.window_text()!r}, not our page - not trashing")
        return False
    try:
        more = win.child_window(title_re=MORE_BUTTON_RE, control_type="Button")
        more.wait("visible", timeout=3)
        pyautogui.click(*more.rectangle().mid_point())
        item = win.child_window(title_re=TRASH_ITEM_RE)
        item.wait("visible", timeout=3)
        pyautogui.click(*item.rectangle().mid_point())
    except Exception:
        pyautogui.press("esc")
        print(f"[INFO] could not find the page menu - delete {title!r} by hand "
              "(sidebar > right-click > Delete)")
        return False
    gone = wait_title(win, lambda t: title not in t)
    ok = title not in gone
    print(f"[{'PASS' if ok else 'INFO'}] test page moved to trash")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Notion desktop automation demo")
    parser.add_argument("--exe", type=Path, default=DEFAULT_EXE, help="path to Notion.exe")
    parser.add_argument("--keep", action="store_true", help="do not trash the test page")
    parser.add_argument("--inspect", action="store_true",
                        help="write the UIA tree to notion_tree.txt and exit")
    args = parser.parse_args()

    win = connect_or_start(args.exe)
    print("Connected to Notion window:", repr(win.window_text()))

    if args.inspect:
        out = Path("notion_tree.txt")
        win.print_control_identifiers(filename=str(out))
        print(f"UIA tree written to {out.resolve()} - search it for button names")
        return 0

    title = f"Day2 automation {datetime.now():%Y%m%d-%H%M%S}"
    saved_clipboard = get_clipboard()
    results = []
    try:
        if not create_test_page(win, title):
            return 1
        type_blocks()
        a, b = find_text_element(win, BLOCK_A), find_text_element(win, BLOCK_B)
        if a is not None and b is not None:        # positions known -> use the mouse
            results.append(check_typed_blocks())
            results.append(drag_block_b_above_a(win, a, b)
                           or move_block_b_with_keyboard(b))
        else:
            # No UIA page tree: move B while the caret is still in it, then check
            print("[INFO] Chromium exposes no page elements - no positions for a "
                  "mouse drag, using the keyboard")
            results.append(move_block_b_with_keyboard())
            text = copy_page_text()
            ok = order_ok(text, TODO_TEXT, BLOCK_B) and order_ok(text, BLOCK_B, BLOCK_A)
            print(f"[{'PASS' if ok else 'FAIL'}] page content = {text!r}")
            results.append(ok)
        if not args.keep:
            trash_test_page(win, title)
    except pyautogui.FailSafeException:
        print("\n[ABORTED] Fail-safe triggered (mouse moved to a corner).")
        return 1
    finally:
        pyautogui.mouseUp()                    # never leave the button held down
        set_clipboard(saved_clipboard)         # give the user their clipboard back
    print(f"\n{sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
