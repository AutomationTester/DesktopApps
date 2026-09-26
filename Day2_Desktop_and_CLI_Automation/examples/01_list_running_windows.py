"""
01_list_running_windows.py
==========================
Day 2 - Desktop Application Fundamentals

GOAL
    See, with your own eyes, that a desktop is made of PROCESSES and WINDOWS.
    This script is READ-ONLY: it does not click, type or close anything.

WHAT IT SHOWS
    1. Top-level windows visible through the UI Automation (UIA) tree
       -> title, control type, class name, process id (PID)
    2. The process list for a couple of PIDs using the Windows 'tasklist' command

HOW TO RUN
    python 01_list_running_windows.py
    python 01_list_running_windows.py --all      (include windows with empty titles)

TESTER'S TAKE-AWAY
    Every automation script starts by answering: "Which process? Which window?"
    If you cannot find the window, you cannot test the application.
"""

import subprocess
import sys

from pywinauto import Desktop


def list_top_level_windows(include_untitled: bool = False) -> list:
    """Return a list of dicts describing every top-level window on the desktop."""
    # Desktop(backend="uia") = the ROOT of the UI Automation tree.
    # .windows() = its direct children = all top-level windows.
    desktop = Desktop(backend="uia")
    rows = []
    for win in desktop.windows():
        info = win.element_info            # lightweight description object
        title = info.name or ""
        if not title and not include_untitled:
            continue
        rows.append(
            {
                "title": title,
                "control_type": info.control_type,
                "class_name": info.class_name,
                "pid": info.process_id,
                "visible": win.is_visible(),
            }
        )
    return rows


def process_name_for_pid(pid: int) -> str:
    """Use the Windows 'tasklist' command to find the exe name for a PID."""
    # /FI = filter, /FO CSV = comma-separated output, /NH = no header row
    result = subprocess.run(
        ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
        capture_output=True,
        text=True,
    )
    line = result.stdout.strip()
    if line.startswith('"'):
        return line.split('","')[0].strip('"')
    return "?"


def main() -> None:
    include_untitled = "--all" in sys.argv
    windows = list_top_level_windows(include_untitled)

    print(f"Found {len(windows)} top-level window(s)\n")
    print(f"{'PID':>7}  {'PROCESS':<22} {'TYPE':<10} {'CLASS':<28} TITLE")
    print("-" * 100)
    for w in windows:
        exe = process_name_for_pid(w["pid"])
        # Keep output ASCII-safe (some titles contain unicode symbols)
        title = w["title"].encode("ascii", "replace").decode()[:40]
        print(
            f"{w['pid']:>7}  {exe[:22]:<22} {str(w['control_type'])[:10]:<10} "
            f"{str(w['class_name'])[:28]:<28} {title}"
        )

    print("\nObservations to discuss in class:")
    print(" * One process can own several windows (e.g. Explorer).")
    print(" * Store apps (Calculator/Notepad) often show 'ApplicationFrameWindow'")
    print("   or a WinUI class name - that tells you: use backend='uia'.")
    print(" * Classic Win32 apps show classes like '#32770' (dialog) or custom names.")


if __name__ == "__main__":
    main()
