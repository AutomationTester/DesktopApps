"""
06_image_based_click.py
=======================
Day 2 - Image-based automation with pyautogui.locateOnScreen()

IDEA
    Instead of asking the app "where is button 7?" (element-based), we take a
    screenshot and SEARCH for a small reference picture of button 7.
    Useful when an app exposes NO accessibility info (games, Citrix/RDP
    sessions, custom-drawn canvases, some old apps).

STEP 1 - CAPTURE THE REFERENCE IMAGE into examples/images/calc_seven.png
    Option A (automatic):  python 06_image_based_click.py --capture
        Opens Calculator, asks pywinauto for the rectangle of button 7 and
        screenshots exactly that region.
    Option B (manual):     open Calculator, press Win+Shift+S (Snipping Tool),
        snip ONLY the '7' button, save as examples/images/calc_seven.png
    Tips: crop tightly, keep the same theme (light/dark), same display
    scaling (100/125/150 %) and same window size as when you run the test.

STEP 2 - RUN
    python 06_image_based_click.py
        Opens Calculator, clears it, finds the image on screen, clicks it,
        and verifies (with pywinauto) that the display shows 7.

REQUIREMENTS
    confidence=... needs opencv-python (installed). Without OpenCV only
    pixel-perfect matches work.
"""

import subprocess
import sys
import time
from pathlib import Path

from pywinauto import Desktop
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

IMAGE = Path(__file__).parent / "images" / "calc_seven.png"


def open_calculator():
    calc = Desktop(backend="uia").window(title="Calculator")
    if not calc.exists(timeout=1):   # reuse an open Calculator: every calc.exe
        subprocess.Popen("calc.exe")   # launch opens ANOTHER window -> "2 elements match"
    calc.wait("visible", timeout=10)
    calc.set_focus()          # image search needs the window VISIBLE on top
    return calc


def capture_reference(calc) -> None:
    """Save a screenshot of button 7 to images/calc_seven.png."""
    seven = calc.child_window(auto_id="num7Button", control_type="Button")
    rect = seven.rectangle()               # left, top, right, bottom
    IMAGE.parent.mkdir(exist_ok=True)
    time.sleep(0.5)                        # let hover effects settle
    shot = pyautogui.screenshot(
        region=(rect.left, rect.top, rect.width(), rect.height())
    )
    shot.save(IMAGE)
    print(f"Reference image saved: {IMAGE} ({rect.width()}x{rect.height()} px)")


def find_on_screen(image: Path, confidence: float = 0.8, timeout: float = 5.0):
    """Return the centre point of the image, or None if not found in time."""
    end = time.time() + timeout
    while time.time() < end:                         # simple retry loop
        try:
            box = pyautogui.locateOnScreen(str(image), confidence=confidence)
            if box is not None:                      # older versions return None
                return pyautogui.center(box)
        except pyautogui.ImageNotFoundException:     # newer versions raise
            pass
        time.sleep(0.5)
    return None


def main() -> int:
    calc = open_calculator()

    if "--capture" in sys.argv:
        capture_reference(calc)
        calc.close()
        return 0

    if not IMAGE.exists():
        print(f"Reference image missing: {IMAGE}")
        print("Run:  python 06_image_based_click.py --capture   (or snip it manually)")
        return 2

    # Known starting state - clear with the element-based locator
    calc.child_window(auto_id="clearButton", control_type="Button").invoke()

    point = find_on_screen(IMAGE, confidence=0.8)
    if point is None:
        print("[FAIL] Image not found on screen. Possible causes:")
        print("  - Calculator hidden behind another window or minimised")
        print("  - Different theme (dark/light), scaling or window size")
        print("  - Reference image cropped too loosely - try confidence=0.7")
        return 1

    print(f"Found button 7 at {point} - clicking it with the REAL mouse")
    pyautogui.click(point)

    # Verification is easier element-based -> a HYBRID approach
    display = calc.child_window(auto_id="CalculatorResults").window_text()
    value = display.replace("Display is", "").strip()
    status = "PASS" if value == "7" else "FAIL"
    print(f"[{status}] Display shows {value!r} (expected '7')")
    time.sleep(1)
    calc.close()
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
