"""
mouse_playground.py
===================
Day 2 - A small, SAFE target application for mouse and keyboard automation.

Used by examples/12_mouse_keyboard_hybrid.py. You can also run it on its own
and try every action by hand first:

    python apps/mouse_playground.py

WHAT IT OFFERS (positions are pixels from the top-left of the CLIENT area)
    Click me          -> counts single clicks
    Double-click me   -> counts double clicks
    Right-click me    -> opens a context menu ("Copy", "Mark reviewed")
    Hover over me     -> reacts when the mouse moves over it
    Blue square       -> drag it into the green drop zone
    List (200 items)  -> scroll it with the mouse wheel
    Text box          -> type, then press Ctrl+Enter to "submit"

WHY A PLAYGROUND?
    Real apps (Electron apps like VS Code/Teams, canvases, games, remote
    desktops) often expose NO usable UI Automation tree - only a window.
    This app behaves the same way: pywinauto finds the WINDOW, but the
    targets inside are custom-drawn, so we must use the mouse (pyautogui).

TEST ORACLE
    With --state <file.json> every event is written to that JSON file.
    The test reads the file to verify that an action really worked.
"""

import argparse
import ctypes
import json
import os
import sys
import tkinter as tk
from pathlib import Path

TITLE = "Day2 Mouse Playground"
WIDTH, HEIGHT = 700, 520

# x, y, width, height inside the client area - the test uses the same numbers
LAYOUT = {
    "click":        (20, 50, 150, 50),
    "double_click": (190, 50, 150, 50),
    "right_click":  (360, 50, 150, 50),
    "canvas":       (20, 120, 660, 220),
    "list":         (20, 360, 300, 140),
    "entry":        (360, 360, 320, 30),
    "hover":        (360, 410, 320, 40),
}
SQUARE = (30, 80, 90, 140)          # drag source, canvas coordinates
DROP_ZONE = (480, 50, 630, 170)     # drop target, canvas coordinates


def make_dpi_aware() -> None:
    """Use real pixels. Without this, Windows stretches the window at
    125/150 % scaling and our pixel offsets would be wrong."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)   # per-monitor aware
    except (AttributeError, OSError):
        pass                                             # not Windows / too old


class Playground:
    def __init__(self, root: tk.Tk, state_file: Path | None):
        self.root = root
        self.state_file = state_file
        self.state = {
            "clicks": 0,
            "double_clicks": 0,
            "menu_choice": None,
            "hovered": False,
            "drag_moves": 0,
            "dropped": False,
            "list_top": 0,
            "submitted_text": None,
        }
        self.drag_offset = (0, 0)
        self._build()
        self._save()

    # ---- UI -----------------------------------------------------------
    def _place(self, widget, name):
        x, y, w, h = LAYOUT[name]
        widget.place(x=x, y=y, width=w, height=h)

    def _build(self) -> None:
        root = self.root
        root.title(TITLE)
        root.geometry(f"{WIDTH}x{HEIGHT}+100+100")
        root.resizable(False, False)

        self.status = tk.Label(root, text="Ready", anchor="w", bg="#eeeeee")
        self.status.place(x=0, y=0, width=WIDTH, height=30)

        click = tk.Button(root, text="Click me", command=self._on_click)
        self._place(click, "click")

        dbl = tk.Label(root, text="Double-click me", relief="raised", bg="#ddeeff")
        dbl.bind("<Double-Button-1>", self._on_double_click)
        self._place(dbl, "double_click")

        rc = tk.Label(root, text="Right-click me", relief="raised", bg="#ffeedd")
        rc.bind("<Button-3>", self._on_right_click)
        self._place(rc, "right_click")
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Copy", command=lambda: self._on_menu("Copy"))
        self.menu.add_command(label="Mark reviewed",
                              command=lambda: self._on_menu("Mark reviewed"))

        self.canvas = tk.Canvas(root, bg="white", highlightthickness=1,
                                highlightbackground="#999999")
        self._place(self.canvas, "canvas")
        self.zone = self.canvas.create_rectangle(*DROP_ZONE, outline="green",
                                                 width=3, dash=(4, 2))
        self.canvas.create_text((DROP_ZONE[0] + DROP_ZONE[2]) // 2, DROP_ZONE[1] - 12,
                                text="Drop zone")
        self.square = self.canvas.create_rectangle(*SQUARE, fill="#3377dd", outline="")
        self.canvas.create_text((SQUARE[0] + SQUARE[2]) // 2, SQUARE[1] - 12,
                                text="Drag me", tags="label")
        self.canvas.tag_bind(self.square, "<ButtonPress-1>", self._drag_start)
        self.canvas.tag_bind(self.square, "<B1-Motion>", self._drag_move)
        self.canvas.tag_bind(self.square, "<ButtonRelease-1>", self._drag_end)

        self.listbox = tk.Listbox(root)
        for i in range(200):
            self.listbox.insert("end", f"Test case {i:03d}")
        self.listbox.bind("<MouseWheel>", self._on_scroll, add="+")
        self._place(self.listbox, "list")

        self.entry = tk.Entry(root)
        self.entry.bind("<Control-Return>", self._on_submit)
        self._place(self.entry, "entry")

        self.hover = tk.Label(root, text="Hover over me", relief="groove")
        self.hover.bind("<Enter>", self._on_hover)
        self._place(self.hover, "hover")

    # ---- event handlers --------------------------------------------------
    def _on_click(self):
        self.state["clicks"] += 1
        self._record(f"Clicked {self.state['clicks']} time(s)")

    def _on_double_click(self, _event):
        self.state["double_clicks"] += 1
        self._record(f"Double-clicked {self.state['double_clicks']} time(s)")

    def _on_right_click(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)   # native context menu

    def _on_menu(self, choice):
        self.state["menu_choice"] = choice
        self._record(f"Context menu: {choice}")

    def _on_hover(self, _event):
        self.hover.config(bg="#ffff99", text="Hovered!")
        self.state["hovered"] = True
        self._record("Mouse is over the hover label")

    def _drag_start(self, event):
        x1, y1, _, _ = self.canvas.coords(self.square)
        self.drag_offset = (event.x - x1, event.y - y1)

    def _drag_move(self, event):
        dx, dy = self.drag_offset
        self.canvas.moveto(self.square, event.x - dx, event.y - dy)
        self.state["drag_moves"] += 1        # pyautogui sends MANY small moves

    def _drag_end(self, _event):
        x1, y1, x2, y2 = self.canvas.coords(self.square)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        zx1, zy1, zx2, zy2 = DROP_ZONE
        self.state["dropped"] = zx1 <= cx <= zx2 and zy1 <= cy <= zy2
        if self.state["dropped"]:
            self.canvas.itemconfig(self.zone, fill="#ccffcc")
        self._record(f"Dropped {'INSIDE' if self.state['dropped'] else 'outside'} "
                     f"the zone after {self.state['drag_moves']} move events")

    def _on_scroll(self, _event):
        # the Listbox scrolls itself; read the new position once it is done
        self.root.after_idle(self._record_scroll)

    def _record_scroll(self):
        self.state["list_top"] = self.listbox.nearest(0)
        self._record(f"List scrolled - first visible item is {self.state['list_top']}")

    def _on_submit(self, _event):
        self.state["submitted_text"] = self.entry.get()
        self._record(f"Submitted: {self.state['submitted_text']!r}")
        return "break"

    # ---- state file ------------------------------------------------------
    def _record(self, message):
        self.status.config(text=message)
        self._save()

    def _save(self):
        if self.state_file is None:
            return
        tmp = self.state_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=2), encoding="utf-8")
        os.replace(tmp, self.state_file)     # atomic: reader never sees half a file


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--state", type=Path, help="JSON file that receives every event")
    args = parser.parse_args()

    if sys.platform == "win32":
        make_dpi_aware()
    root = tk.Tk()
    Playground(root, args.state)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
