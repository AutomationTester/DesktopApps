"""
04_print_control_identifiers.py
===============================
Day 2 - Object inspection from Python

Inspection tools answer: "How do I identify this button in my script?"
    * Accessibility Insights for Windows  (modern, free, from Microsoft)
    * Inspect.exe                          (Windows SDK, classic)
    * pywinauto's print_control_identifiers()  (right inside Python)

This script opens Calculator and dumps its control tree. Then it shows
how to write the dump to a text file so you can search it in VS Code.

HOW TO RUN
    python 04_print_control_identifiers.py            -> print to console (depth 4)
    python 04_print_control_identifiers.py --file     -> also save calc_tree.txt

HOW TO READ THE OUTPUT (one entry):
    Button - 'Seven'    (L..., T..., R..., B...)
    ['Seven', 'SevenButton', 'Button12']
    child_window(title="Seven", auto_id="num7Button", control_type="Button")

    line 1 : control type, name (title) and screen rectangle
    line 2 : "best match" names pywinauto accepts (calc.SevenButton)
    line 3 : a ready-made child_window(...) locator - copy/paste it!

PREFER in this order: auto_id  >  title + control_type  >  best-match names
(best-match names like 'Button12' depend on order and break easily).
"""

import subprocess
import sys
from pathlib import Path

from pywinauto import Desktop


def main() -> None:
    calc = Desktop(backend="uia").window(title="Calculator")
    if not calc.exists(timeout=1):   # reuse an open Calculator: every calc.exe
        subprocess.Popen("calc.exe")   # launch opens ANOTHER window -> "2 elements match"
    calc.wait("visible", timeout=10)

    # depth limits how deep the tree is printed (full tree is very long)
    print("=" * 70)
    print("Control tree of Calculator (depth=4)")
    print("=" * 70)
    calc.print_control_identifiers(depth=4)

    if "--file" in sys.argv:
        out = Path(__file__).with_name("calc_tree.txt")
        # filename= writes the full dump to a file instead of the console
        calc.print_control_identifiers(filename=str(out))
        print(f"\nFull tree written to {out}")

    # A few other inspection helpers worth knowing
    seven = calc.child_window(auto_id="num7Button", control_type="Button")
    wrapper = seven.wrapper_object()          # resolve the spec to a real element
    print("\nInspecting a single element:")
    print("  name          :", wrapper.window_text())
    print("  auto_id       :", wrapper.element_info.automation_id)
    print("  control_type  :", wrapper.element_info.control_type)
    print("  class_name    :", wrapper.element_info.class_name)
    print("  is_enabled    :", wrapper.is_enabled())
    print("  is_visible    :", wrapper.is_visible())
    print("  rectangle     :", wrapper.rectangle())

    calc.close()


if __name__ == "__main__":
    main()
