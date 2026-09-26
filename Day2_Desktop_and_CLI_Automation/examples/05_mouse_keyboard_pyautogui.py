"""
05_mouse_keyboard_pyautogui.py
==============================
Day 2 - Mouse and keyboard automation with pyautogui (HARMLESS demo)

pyautogui drives the REAL mouse and keyboard, exactly like a human.
It knows nothing about buttons or text boxes - only pixels and keys.

THIS DEMO IS SAFE:
    * It only MOVES the mouse (no clicks on random things).
    * It types only into a window YOU choose (optional, see --type).

SAFETY FEATURES YOU MUST KNOW
    pyautogui.FAILSAFE = True   (default)
        Slam the mouse into ANY screen corner to abort the script. pyautogui
        raises pyautogui.FailSafeException on its next call.
    pyautogui.PAUSE = 0.3
        Waits 0.3 s after EVERY pyautogui call - makes scripts watchable
        and gives the application time to react.

HOW TO RUN
    python 05_mouse_keyboard_pyautogui.py           -> mouse-only tour
    python 05_mouse_keyboard_pyautogui.py --type    -> also types a line after
                                                      a 5 s countdown (click into
                                                      an EMPTY editor first!)
"""

import sys
import time

import pyautogui

# ---- Global safety settings --------------------------------------------
pyautogui.FAILSAFE = True     # move mouse to a corner to abort
pyautogui.PAUSE = 0.3         # pause after each pyautogui call


def show_screen_info() -> None:
    """Screen size and current mouse position."""
    width, height = pyautogui.size()
    x, y = pyautogui.position()
    print(f"Screen size     : {width} x {height} pixels")
    print(f"Mouse position  : ({x}, {y})")
    print("Coordinates     : (0,0) is the TOP-LEFT corner; x grows right, y grows down")
    print("On-screen check : ", pyautogui.onScreen(x, y))


def mouse_tour() -> None:
    """Move the mouse around the centre of the screen in a square."""
    width, height = pyautogui.size()
    cx, cy = width // 2, height // 2
    start = pyautogui.position()
    print("\nMoving mouse in a square around the screen centre ...")
    for dx, dy in [(-150, -150), (150, -150), (150, 150), (-150, 150), (-150, -150)]:
        pyautogui.moveTo(cx + dx, cy + dy, duration=0.4)  # absolute move, animated
        print("  now at", pyautogui.position())
    pyautogui.moveRel(50, 0, duration=0.3)                # relative move
    print("  after moveRel(50, 0):", pyautogui.position())
    pyautogui.moveTo(start.x, start.y, duration=0.4)      # put it back
    print("Mouse returned to", pyautogui.position())

    # Other mouse functions (NOT executed here - just know they exist):
    #   pyautogui.click(x, y)            left click at x,y
    #   pyautogui.doubleClick(x, y)
    #   pyautogui.rightClick(x, y)
    #   pyautogui.dragTo(x, y, duration=0.5)
    #   pyautogui.scroll(-300)           scroll down


def keyboard_demo() -> None:
    """Type into whatever window has focus - only when --type is given."""
    print("\nKEYBOARD DEMO: click into an EMPTY text editor within 5 seconds ...")
    for i in range(5, 0, -1):
        print(f"  typing in {i} ...")
        time.sleep(1)
    pyautogui.write("Typed by pyautogui - Day 2", interval=0.05)  # char by char
    pyautogui.press("enter")                                       # single key
    pyautogui.hotkey("shift", "home")                              # key combo
    pyautogui.press("right")          # just deselect - we don't delete anything
    print("Done typing.")

    # Useful keyboard calls:
    #   pyautogui.press("tab", presses=3)
    #   pyautogui.hotkey("ctrl", "s")
    #   pyautogui.keyDown("shift"); pyautogui.keyUp("shift")
    #   pyautogui.KEYBOARD_KEYS   -> list of valid key names


def main() -> None:
    print("Tip: move the mouse into a screen CORNER at any time to abort.\n")
    try:
        show_screen_info()
        mouse_tour()
        if "--type" in sys.argv:
            keyboard_demo()
    except pyautogui.FailSafeException:
        print("\n[ABORTED] Fail-safe triggered (mouse moved to a corner).")
        sys.exit(1)


if __name__ == "__main__":
    main()
