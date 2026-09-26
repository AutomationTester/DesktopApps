"""
12_mouse_keyboard_hybrid.py
===========================
Day 2 - Real mouse and keyboard actions: pywinauto + pyautogui TOGETHER

WHO DOES WHAT
    pywinauto  -> finds the window, brings it to the front, tells us WHERE it
                  is, and checks focus before we type.
    pyautogui  -> moves the REAL mouse and presses REAL keys: hover, click,
                  double-click, right-click + context menu, drag and drop,
                  scroll, typing and hotkeys.

    You need pyautogui when the app has no usable UI Automation tree
    (Electron apps, canvases, charts, games, Citrix/RDP) or when the action
    itself is the feature under test (drag and drop, hover tooltips,
    right-click menus, mouse-wheel scrolling).

TARGET APP
    apps/mouse_playground.py - a harmless window started by this script.
    It writes every event to a JSON file: that file is our TEST ORACLE.

THE KEY TECHNIQUE: WINDOW-RELATIVE COORDINATES
    Never hard-code screen positions like click(812, 455). Ask pywinauto
    where the window is and add a fixed OFFSET inside the window:

        screen point = window client origin + offset of the target

    The window can then be anywhere on the screen. Find offsets with the
    --where mode below (hover a target and read its offset).

HOW TO RUN
    python 12_mouse_keyboard_hybrid.py           -> run all mouse/keyboard checks
    python 12_mouse_keyboard_hybrid.py --where   -> show live window-relative
                                                    mouse offsets for 15 s
    Do NOT touch the mouse or keyboard while it runs.
    Emergency stop: move the mouse into a screen CORNER (FAILSAFE).
"""

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pyautogui
import win32gui
from pywinauto import Desktop

pyautogui.FAILSAFE = True     # mouse into a corner = abort
pyautogui.PAUSE = 0.2         # pause after each pyautogui call

APP = Path(__file__).parent / "apps" / "mouse_playground.py"
TITLE = "Day2 Mouse Playground"

# Target centres, measured from the top-left of the window's CLIENT area
# (inside the title bar). Found once with --where; they do not change when
# the window moves.
TARGETS = {
    "click":        (95, 75),
    "double_click": (265, 75),
    "right_click":  (435, 75),
    "square":       (80, 230),    # the blue square in the canvas
    "drop_zone":    (575, 230),   # centre of the green drop zone
    "list":         (170, 430),
    "entry":        (520, 375),
    "hover":        (520, 430),
}


# ---- pywinauto side: find the window and convert offsets -----------------
def start_app(state_file: Path):
    """Start the playground and return (process, window wrapper)."""
    proc = subprocess.Popen([sys.executable, str(APP), "--state", str(state_file)])
    # win32 backend: the playground is a classic window with a real HWND
    spec = Desktop(backend="win32").window(title=TITLE)
    spec.wait("visible", timeout=10)
    win = spec.wrapper_object()
    win.set_focus()
    return proc, win


def to_screen(win, target: str) -> tuple[int, int]:
    """Window-relative offset -> absolute screen point for pyautogui.
    ClientToScreen skips the title bar and borders, whatever their size."""
    return win32gui.ClientToScreen(win.handle, TARGETS[target])


def ensure_focus(win) -> None:
    """pyautogui types into WHATEVER has focus - check it is our window."""
    if not win.is_active():
        win.set_focus()
    if not win.is_active():
        raise RuntimeError("Playground is not the active window - refusing to type")


# ---- the test oracle ------------------------------------------------------
def read_state(state_file: Path) -> dict:
    return json.loads(state_file.read_text(encoding="utf-8"))


def wait_for(state_file: Path, check, timeout: float = 5.0) -> dict:
    """Poll the state file until check(state) is True - never a blind sleep."""
    end = time.time() + timeout
    state = read_state(state_file)
    while not check(state) and time.time() < end:
        time.sleep(0.1)
        state = read_state(state_file)
    return state


# ---- pyautogui side: the actions ------------------------------------------
def test_hover(win, state_file):
    x, y = to_screen(win, "hover")
    pyautogui.moveTo(x, y, duration=0.5)            # motion only, no click
    state = wait_for(state_file, lambda s: s["hovered"])
    return state["hovered"], "hover label reacted to the mouse"


def test_single_click(win, state_file):
    x, y = to_screen(win, "click")
    pyautogui.click(x, y)
    pyautogui.click(x, y, clicks=2, interval=0.4)   # 2 separate clicks (slow)
    state = wait_for(state_file, lambda s: s["clicks"] >= 3)
    return state["clicks"] == 3, f"clicks counted = {state['clicks']} (expected 3)"


def test_double_click(win, state_file):
    x, y = to_screen(win, "double_click")
    pyautogui.doubleClick(x, y)                     # 2 clicks within ~500 ms
    state = wait_for(state_file, lambda s: s["double_clicks"] >= 1)
    return state["double_clicks"] == 1, f"double clicks = {state['double_clicks']}"


def test_right_click_menu(win, state_file):
    x, y = to_screen(win, "right_click")
    pyautogui.rightClick(x, y)                      # opens the context menu
    time.sleep(0.5)                                 # native menu animation
    # Menu items have no stable position -> choose with the keyboard instead
    pyautogui.press("down", presses=2, interval=0.1)   # 1st item, then 2nd
    pyautogui.press("enter")
    state = wait_for(state_file, lambda s: s["menu_choice"])
    ok = state["menu_choice"] == "Mark reviewed"
    return ok, f"menu choice = {state['menu_choice']!r}"


def test_drag_and_drop(win, state_file):
    sx, sy = to_screen(win, "square")
    tx, ty = to_screen(win, "drop_zone")
    pyautogui.moveTo(sx, sy, duration=0.3)          # 1. go to the source
    # 2. press, move slowly, release. duration > 0 matters: the app must see
    #    the in-between motion events, not a teleport.
    pyautogui.dragTo(tx, ty, duration=1.0, button="left")
    state = wait_for(state_file, lambda s: s["dropped"])
    return state["dropped"], (f"dropped inside zone = {state['dropped']}, "
                              f"motion events seen = {state['drag_moves']}")


def test_drag_manual_steps(win, state_file):
    """The same drag in small steps - for apps that ignore dragTo()
    (some need a pause after mouseDown or several intermediate moves)."""
    tx, ty = to_screen(win, "drop_zone")
    sx, sy = to_screen(win, "square")
    pyautogui.moveTo(tx, ty, duration=0.3)          # square is now in the zone
    pyautogui.mouseDown(button="left")
    time.sleep(0.2)                                 # let the app notice the press
    for step in range(1, 11):                       # 10 small moves back
        pyautogui.moveTo(tx + (sx - tx) * step / 10, ty + (sy - ty) * step / 10,
                         duration=0.05)
    pyautogui.mouseUp(button="left")                # ALWAYS release the button
    state = wait_for(state_file, lambda s: not s["dropped"])
    return not state["dropped"], "square dragged back OUT of the zone"


def test_scroll(win, state_file):
    x, y = to_screen(win, "list")
    pyautogui.click(x, y)                           # focus the list
    # GOTCHA: on Windows the number is RAW wheel units, and one wheel notch
    # is 120. scroll(-5) is 1/24 of a notch and most apps ignore it.
    pyautogui.scroll(-3 * 120)                      # 3 notches down (negative = down)
    state = wait_for(state_file, lambda s: s["list_top"] > 0)
    return state["list_top"] > 0, f"first visible item after scroll = {state['list_top']}"


def test_typing_and_hotkeys(win, state_file):
    x, y = to_screen(win, "entry")
    pyautogui.click(x, y)                           # put the caret in the box
    ensure_focus(win)                               # pywinauto safety check
    pyautogui.write("draft", interval=0.03)
    pyautogui.hotkey("ctrl", "a")                   # select all ...
    pyautogui.press("backspace")                    # ... and delete it
    pyautogui.write("Day 2 hybrid test", interval=0.03)
    pyautogui.keyDown("shift")                      # hold Shift ...
    pyautogui.press("1")                            # ... "1" becomes "!"
    pyautogui.keyUp("shift")                        # ALWAYS release it
    pyautogui.hotkey("ctrl", "enter")               # the app's submit shortcut
    state = wait_for(state_file, lambda s: s["submitted_text"])
    ok = state["submitted_text"] == "Day 2 hybrid test!"
    return ok, f"submitted text = {state['submitted_text']!r}"


TESTS = [
    test_hover,
    test_single_click,
    test_double_click,
    test_right_click_menu,
    test_drag_and_drop,
    test_drag_manual_steps,
    test_scroll,
    test_typing_and_hotkeys,
]


def where_mode(win, seconds: int = 15) -> None:
    """Print the mouse position relative to the client area - use it to
    measure the offsets for TARGETS in any application."""
    print(f"Hover over targets in '{TITLE}' - offsets for {seconds} s ...")
    origin = win32gui.ClientToScreen(win.handle, (0, 0))
    end = time.time() + seconds
    while time.time() < end:
        x, y = pyautogui.position()
        print(f"\r  screen=({x:4}, {y:4})   offset in window=({x - origin[0]:4}, "
              f"{y - origin[1]:4})   ", end="", flush=True)
        time.sleep(0.2)
    print()


def main() -> int:
    fd, name = tempfile.mkstemp(prefix="day2_playground_", suffix=".json")
    os.close(fd)
    state_file = Path(name)
    proc, win = start_app(state_file)
    print("Connected to:", win.window_text(), "| client origin on screen:",
          win32gui.ClientToScreen(win.handle, (0, 0)))
    failures = 0
    try:
        if "--where" in sys.argv:
            where_mode(win)
            return 0
        print("Hands off the mouse and keyboard! (corner = emergency stop)\n")
        for test in TESTS:
            win.set_focus()                        # every step starts focused
            ok, detail = test(win, state_file)
            failures += not ok
            print(f"[{'PASS' if ok else 'FAIL'}] {test.__name__:<26} {detail}")
        time.sleep(1)                              # let the trainees see the result
    except pyautogui.FailSafeException:
        print("\n[ABORTED] Fail-safe triggered (mouse moved to a corner).")
        failures += 1
    finally:
        pyautogui.mouseUp()                        # never leave a button held down
        proc.terminate()                           # our own app - safe to close
        proc.wait(timeout=5)
        state_file.unlink(missing_ok=True)
        state_file.with_suffix(".tmp").unlink(missing_ok=True)
    print(f"\n{len(TESTS) - failures}/{len(TESTS)} checks passed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
