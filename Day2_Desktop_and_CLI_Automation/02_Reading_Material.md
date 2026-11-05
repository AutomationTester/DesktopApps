# Day 2 - Desktop & Command-Line Automation with Python
### Trainee Handbook

> Course: Python Desktop Application Automation Testing (Day 2 of 5)
> Prerequisites: Day 1 (Python basics, functions, exceptions, classes/OOP)
> Environment: Windows 11, Python 3.x, VS Code, `pywinauto`, `pyautogui`, `opencv-python`, `pillow`

---

## Table of Contents

1. [How desktop applications work](#1-how-desktop-applications-work)
2. [Types of desktop applications](#2-types-of-desktop-applications)
3. [Desktop UI elements and their states](#3-desktop-ui-elements-and-their-states)
4. [Object inspection tools](#4-object-inspection-tools)
5. [Desktop automation challenges](#5-desktop-automation-challenges)
6. [Element-based vs image-based automation](#6-element-based-vs-image-based-automation)
7. [Element-based automation with pywinauto](#7-element-based-automation-with-pywinauto)
8. [Mouse, keyboard and image-based automation with pyautogui](#8-mouse-keyboard-and-image-based-automation-with-pyautogui)
9. [Handling focus, windows and dialogs](#9-handling-focus-windows-and-dialogs)
10. [Command-line automation](#10-command-line-automation)
11. [Cheat-sheets: pywinauto, pyautogui, argparse](#11-cheat-sheets)
12. [Questions and answers](#12-questions-and-answers)
13. [Day 2 summary](#13-day-2-summary)

All example scripts live in `examples/`; labs in `hands_on/`.

---

## 1. How desktop applications work

A **desktop application** runs locally on the operating system, outside any browser. Think of Notepad, Calculator, MS Excel, SAP GUI, Tally, a bank's teller application, or VS Code. Many business-critical systems are still desktop apps, and browser tools like Selenium cannot automate them - which is why we need desktop automation tools.

### 1.1 Processes

When you start a program, Windows creates a **process**: a running instance of the program with its own memory, threads and a unique **Process ID (PID)**. You can see processes in **Task Manager > Details**.

```
 double-click calc.exe  --->  launcher process (exits quickly)
                                   |
                                   v
                     CalculatorApp.exe  (PID 4312)  <- the real app
                        +-- main window "Calculator"
```

Important for automation: the program you *start* is not always the process that *owns the window*. On Windows 11, `calc.exe` is only a **launcher** - it starts `CalculatorApp.exe` and exits. That is why we connect to Calculator by its window title instead of tracking the process we started.

### 1.2 Windows

A **window** is a rectangular area on screen owned by a process. A process may own many windows (main window, dialogs, tool windows). Windows are organised in a **parent-child hierarchy**:

```
Desktop (root)
 +-- Calculator                    <- top-level window
 |    +-- Text     "Display is 0"
 |    +-- Button   "Seven"   (AutomationId: num7Button)
 |    +-- Button   "Plus"    (AutomationId: plusButton)
 +-- day2_notepad_x1y2.txt - Notepad
      +-- Document                 <- the editor area
```

In classic Win32 apps every control (button, text box) is itself a real window with a **window handle (HWND)**. Modern frameworks (WPF, UWP/WinUI, Electron) draw their controls themselves and expose them through UI Automation instead.

### 1.3 The message loop

How does a mouse click reach a button? Windows puts **messages** into the application's message queue (`WM_LBUTTONDOWN`, `WM_KEYDOWN`, `WM_PAINT`, ...). Each GUI app runs a **message loop** that takes messages one by one and dispatches them to the right control.

```
Mouse / keyboard -> Windows -> message queue -> message loop -> button handler
```

Two consequences for testers:

- **Keyboard input goes only to the focused window.** If a pop-up steals focus, your keystrokes land in the wrong place.
- **A busy app does not process messages.** The window shows "(Not Responding)" and your automation must *wait* instead of blindly continuing.

### 1.4 The UI Automation (UIA) tree

**Microsoft UI Automation (UIA)** is the accessibility framework built into Windows. Screen readers such as Narrator use it to "see" applications - and automation tools use exactly the same API. Every element in the UIA tree exposes:

**Properties**

| Property | Example | Use in automation |
|---|---|---|
| Name | "Seven" | Human-readable label (language dependent!) |
| AutomationId | `num7Button` | Stable ID - the best locator |
| ControlType | Button | Element type |
| ClassName | Button | Framework class |
| FrameworkId | XAML / WPF / Win32 | Tells you the technology |
| IsEnabled, IsOffscreen, HasKeyboardFocus | True/False | State checks |

**Control patterns** (what an element can *do*)

| Pattern | Meaning | pywinauto method |
|---|---|---|
| Invoke | Click-like action | `invoke()` |
| Value | Get/set text | `set_edit_text()`, `get_value()` |
| Toggle | Checkbox on/off | `toggle()`, `get_toggle_state()` |
| SelectionItem | Select list/radio/tab item | `select()`, `is_selected()` |
| ExpandCollapse | Combo box, tree node | `expand()`, `collapse()` |
| Window | Close, minimise | `close()`, `minimize()` |

> **Key idea:** an accessible application is an automatable application. Good accessibility = good testability.

**Try it yourself:** run `python examples/01_list_running_windows.py`. Find Calculator's PID in the output, then find the same PID in Task Manager.

---

## 2. Types of desktop applications

| Type | Technology | Examples | Automation notes |
|---|---|---|---|
| **Win32 / MFC** | Native C/C++, HWND controls | Legacy tools, older Windows utilities | pywinauto `backend="win32"` works well; `uia` also works |
| **WinForms** | .NET, wraps Win32 controls | Many in-house business apps | `win32` or `uia` |
| **WPF** | .NET, vector-drawn UI | Visual Studio, modern enterprise apps | `uia` only (controls have no HWND) |
| **UWP / WinUI (Store apps)** | Modern Windows app platform | **Windows 11 Calculator, Notepad**, Settings | `uia` only |
| **Electron** | Chromium + Node.js | VS Code, Slack, Postman | `uia` sees a lot; deep web content sometimes better via Playwright/Selenium |
| **Java Swing / JavaFX** | JVM | Some trading and banking apps | Needs **Java Access Bridge** enabled, otherwise the tree is empty |

**Windows 11 note:** Calculator and Notepad used to be classic Win32 apps. On Windows 11 they are **Store (UWP/WinUI) apps**, so always use `backend="uia"` with them.

### How to recognise the type

Inspect the top-level window's **ClassName** / **FrameworkId**:

| ClassName / FrameworkId | Technology |
|---|---|
| `#32770` | Classic Win32 dialog |
| `WindowsForms10.*` / WinForm | WinForms |
| `HwndWrapper[...]` / WPF | WPF |
| `ApplicationFrameWindow`, WinUI class names / XAML | Store (UWP/WinUI) |
| `Chrome_WidgetWin_1` / Chrome | Electron or Chromium |
| `SunAwtFrame` | Java Swing |

**Common mistakes**
- Using `backend="win32"` on a WPF or Store app and wondering why no buttons are found.
- Assuming Windows 11 Notepad behaves like the old Notepad (it has tabs and restores sessions).

---

## 3. Desktop UI elements and their states

### 3.1 Common elements

| Element | UIA ControlType | Typical test actions |
|---|---|---|
| Window / Dialog | Window | Wait for it, focus, close |
| Button | Button | Click (invoke), check enabled |
| Text box | Edit / Document | Type, clear, read text |
| Label | Text | Read and verify text |
| Checkbox | CheckBox | Toggle, verify checked |
| Radio button | RadioButton | Select, verify selected |
| Combo box | ComboBox | Expand, select item, read selection |
| List / Tree / Grid | List / Tree / DataGrid | Select rows, count items, read cells |
| Menu / Menu item | Menu / MenuItem | Open menus, select commands |
| Tab | Tab / TabItem | Switch tabs |
| Progress bar / Slider | ProgressBar / Slider | Read value |

### 3.2 States

| State | Meaning | Test example | pywinauto |
|---|---|---|---|
| Exists | Present in the UIA tree | "Error dialog should not exist" | `spec.exists(timeout=2)` |
| Visible | Actually shown (not hidden/off-screen) | "Advanced panel is hidden by default" | `is_visible()` |
| Enabled | Accepts input, not greyed out | "Save is disabled until data changes" | `is_enabled()` |
| Focused | Receives keyboard input | "Cursor starts in Username" | `has_keyboard_focus()` |
| Active | Window is in the foreground | After opening, app is in front | `is_active()` |
| Checked | Toggle state (0 off, 1 on, 2 indeterminate) | "Remember me is unchecked" | `get_toggle_state()` |
| Selected | Item chosen in list/tab/radio group | "Tab General is selected" | `is_selected()` |
| Minimized / Maximized | Window size state | "Window restores maximised" | `is_minimized()`, `is_maximized()` |
| Read-only | Value cannot be changed | "Invoice number is read-only" | Value pattern `is_read_only` |

The same words appear in pywinauto **wait conditions**: `spec.wait("exists visible enabled ready active")` - where `ready` means *visible and enabled*.

---

## 4. Object inspection tools

Before automating an element you must know how to **identify** it. Never guess locators - inspect them.

### 4.1 Accessibility Insights for Windows (recommended)

Free tool from Microsoft (https://accessibilityinsights.io). Use **Live Inspect**: hover over any element and read its Name, AutomationId, ControlType, ClassName, FrameworkId, patterns and the element hierarchy. Bonus for testers: it can also run automated accessibility checks.

```
Hover "7" in Calculator:
  Name          : Seven
  AutomationId  : num7Button      <- use this
  ControlType   : Button
  FrameworkId   : XAML            <- UWP/WinUI -> backend "uia"
  Patterns      : Invoke
```

### 4.2 Inspect.exe

The classic tool from the **Windows SDK**, typically at
`C:\Program Files (x86)\Windows Kits\10\bin\<version>\x64\inspect.exe`.
Shows the same UIA information in a tree view. Make sure "UI Automation" mode (not MSAA) is selected.

### 4.3 pywinauto `print_control_identifiers()`

Prints the control tree from inside Python:

```python
from pywinauto import Desktop
calc = Desktop(backend="uia").window(title="Calculator")
calc.print_control_identifiers(depth=4)               # console
calc.print_control_identifiers(filename="calc.txt")   # to a file
```

Each element is printed in three lines:

```
Button - 'Seven'    (L1012, T604, R1092, B660)                        <- type, name, rectangle
['Seven', 'SevenButton', 'Button12']                                   <- "best match" names
child_window(title="Seven", auto_id="num7Button", control_type="Button")  <- copy-paste locator
```

**Locator priority:** `auto_id` > `title` + `control_type` > best-match names / `found_index`. Names change with the Windows display language ("Seven" vs "Sieben"); AutomationIds do not. Best-match names such as `Button12` depend on element order and break easily.

Example: `examples/04_print_control_identifiers.py` (`--file` writes the full tree to `calc_tree.txt`).

**Try it yourself:** open Accessibility Insights, hover over Calculator's `=` button and write down its AutomationId. Then find the same element in the output of example 04.

---

## 5. Desktop automation challenges

| Challenge | What goes wrong | Counter-measure |
|---|---|---|
| Timing / synchronisation | Script acts before the window/control is ready | Explicit waits: `wait("visible")`, `exists(timeout=)` |
| Focus | Keys go to a pop-up or another app | `set_focus()` right before typing; prefer `invoke()` |
| Unstable locators | Names differ per language/version; no AutomationId | Use `auto_id`; ask developers to add AutomationIds |
| Unknown start state | App restores last session (Win11 Notepad tabs), last mode, old data | Create your own test data; reset state (e.g. press C) |
| Modal dialogs | Main window blocked, script "hangs" | Detect, handle, `wait_not("visible")` |
| Screen dependence | Resolution, DPI scaling, theme, multi-monitor break images/coordinates | Element-based first; images only as fallback |
| Launcher processes | `start("calc.exe")` tracks a process that exits | `subprocess.Popen` + `Desktop().window(...)` |
| Environment | Locked screen, minimised RDP session = no interactive desktop | Dedicated VM / unlocked session for GUI tests |
| Custom-drawn controls | Canvas/game/Citrix content invisible to UIA | Image-based automation, OCR |
| Clean-up | Leftover windows or files affect the next test | `try/finally`, close only what you opened |

> **Real-world lesson - never assume a clean application state.** Windows 11 Notepad restores the user's previous tabs (even unsaved ones) and opens every new file as a tab in the same window. A script that grabs "the Notepad window" and types into it, or calls `close()` on it, can damage real documents. Section 7.8 shows the safe pattern.

---

## 6. Element-based vs image-based automation

**Element-based** automation asks the application's object model (UIA) for an element - "the button whose AutomationId is `num7Button`" - and acts on it through the API. **Image-based** automation takes a screenshot, searches for a reference picture and clicks at its pixel coordinates with the real mouse.

| Aspect | Element-based (pywinauto) | Image-based (pyautogui) |
|---|---|---|
| Identifies elements by | AutomationId, name, control type | Pixel matching of a reference image |
| Speed | Fast | Slower (whole-screen scans) |
| Robust to resolution / DPI / theme | Yes | No - images must be re-captured |
| Window must be visible and on top | Often not (`invoke()` works when covered) | Yes |
| Can read text and states | Yes (`window_text()`, `is_enabled()`) | No (would need OCR) |
| Works without accessibility support | No | Yes |
| Typical targets | Win32, WinForms, WPF, UWP/WinUI business apps | Games, Citrix/RDP, canvas/custom-drawn UIs, some legacy apps |
| Maintenance effort | Low | High |
| Failure messages | Precise ("element not found: num7Button") | Vague ("image not found") |

**Strategy:** use element-based automation first, image-based as a fallback, and a **hybrid** when useful - for example click by image, verify by element (as in `examples/06_image_based_click.py`).

---

## 7. Element-based automation with pywinauto

### 7.1 Backends

```python
from pywinauto import Application, Desktop

Desktop(backend="uia")        # Microsoft UI Automation - modern & legacy apps
Desktop(backend="win32")      # Win32 API messages - classic HWND apps only
```

| | `win32` | `uia` |
|---|---|---|
| Underlying API | Win32 messages / HWND | Microsoft UI Automation |
| Supports | Win32, MFC, WinForms, VB6 | All of those + WPF, UWP/WinUI, Electron, Qt (partly) |
| Speed | Faster | Slower but richer |
| When to use | Legacy apps where `uia` is slow or incomplete | Default choice |

Conceptual Win32 example (a legacy app, not installed in class):

```python
app = Application(backend="win32").start(r"C:\Tools\LegacyApp.exe")
dlg = app.window(title_re=".*Legacy App.*")
dlg.Edit1.set_edit_text("tester01")        # win32 Edit controls support set_edit_text
dlg.child_window(title="&OK", class_name="Button").click()
```

### 7.2 Start or connect?

```python
# Normal apps: pywinauto starts and owns the process
app = Application(backend="uia").start(r"C:\MyApp\MyApp.exe")
main = app.window(title="My App")

# Already running app
app = Application(backend="uia").connect(title="My App", timeout=10)

# Store apps with a launcher (Win11 Calculator / Notepad)
import subprocess
calc = Desktop(backend="uia").window(title="Calculator")
if not calc.exists(timeout=1):      # reuse an already-open Calculator
    subprocess.Popen("calc.exe")
calc.wait("visible", timeout=10)
```

`Application().start("calc.exe")` tracks the launcher process, which exits immediately - so the window is never found. `Desktop()` searches all top-level windows and works regardless of which process owns them.

**Why the `exists()` check?** Every `calc.exe` launch opens *another* Calculator window. If a previous run left one open, `window(title="Calculator")` now matches two windows and pywinauto raises `ElementAmbiguousError: There are 2 elements that match the criteria`. Reusing an open window (or always closing it in cleanup) avoids this. It's a classic "unclean start state" failure.

### 7.3 Specifications vs wrappers

`window()` and `child_window()` return a **WindowSpecification** - a *description* of what to find, not the element itself. It is resolved lazily each time you use it, retrying until the element appears or the timeout expires. This built-in retry is what makes pywinauto scripts stable.

```python
spec = calc.child_window(auto_id="num7Button", control_type="Button")  # nothing searched yet
spec.invoke()                        # searched now (with retries), then invoked
wrapper = spec.wrapper_object()      # resolve explicitly -> real element object
```

### 7.4 Locators

```python
win.child_window(auto_id="num7Button", control_type="Button")   # best
win.child_window(title="Seven", control_type="Button")          # ok
win.child_window(title_re=r"^Display is .*")                    # regular expression
win.child_window(control_type="Document")                       # unique type in window
win.child_window(control_type="Button", found_index=0)          # fragile
win.SevenButton                                                  # best-match attribute
```

- `ElementNotFoundError` - nothing matched: inspect again, or wait longer.
- `ElementAmbiguousError` - several matched: add criteria (`control_type`, `auto_id`).

### 7.5 Actions and reading values

| Goal | Method | Notes |
|---|---|---|
| Click via API | `invoke()` | No mouse movement, works when covered |
| Click with real mouse | `click_input()` | Window must be visible |
| Type keys | `type_keys("text", with_spaces=True, pause=0.05)` | Sets focus first; special characters see 11.1 |
| Set text directly | `set_edit_text("text")` | Only when the Value pattern is supported |
| Read text | `window_text()` | Name or value |
| Checkbox | `toggle()`, `get_toggle_state()` | |
| Select | `select("item")` | ComboBox, ListBox, Tab |
| Window | `set_focus()`, `minimize()`, `maximize()`, `restore()`, `close()` | |
| Children | `children()`, `descendants(control_type="Button")` | |

### 7.6 Waits

```python
spec.exists(timeout=5)               # True / False, never raises
spec.wait("visible", timeout=10)     # raises pywinauto.timings.TimeoutError
spec.wait("ready")                   # visible + enabled
spec.wait_not("visible", timeout=5)  # until it disappears
```

Never use `time.sleep()` to wait for the UI: it is either too long (slow suite) or too short (flaky test). Explicit waits return as soon as the condition is met.

### 7.7 Worked example - Calculator

`examples/02_calculator_pywinauto.py`

```python
BUTTONS = {"7": "num7Button", "8": "num8Button", "+": "plusButton",
           "=": "equalButton", "C": "clearButton"}  # ... all digits and operators

def press(calc, key):
    calc.child_window(auto_id=BUTTONS[key], control_type="Button").invoke()

def read_result(calc):
    raw = calc.child_window(auto_id="CalculatorResults").window_text()  # "Display is 15"
    return raw.replace("Display is", "").strip().replace(",", "")

subprocess.Popen("calc.exe")
calc = Desktop(backend="uia").window(title="Calculator")
calc.wait("visible", timeout=10)
press(calc, "C")                         # known start state
for key in "7+8=":
    press(calc, key)
assert read_result(calc) == "15"
calc.close()                             # OK: Calculator holds no user data
```

Calculator AutomationIds: `num0Button` ... `num9Button`, `plusButton`, `minusButton`, `multiplyButton`, `divideButton`, `equalButton`, `clearButton`, display `CalculatorResults`. Large numbers are shown with thousands separators (`1,000`), so strip commas before comparing.

### 7.8 Worked example - Notepad, the safe way

`examples/03_notepad_safe_automation.py`

```python
import os, re, subprocess, tempfile
from pywinauto import Desktop

fd, path = tempfile.mkstemp(prefix="day2_", suffix=".txt")
os.close(fd)                                                    # 1. our own file
subprocess.Popen(["notepad.exe", path])                         # 2. open ONLY that file
name = os.path.basename(path)
win = Desktop(backend="uia").window(title_re=rf"\*?{re.escape(name)} - Notepad")
win.wait("visible", timeout=15)                                 # 3. connect by OUR title
doc = win.child_window(control_type="Document")

doc.set_focus()
doc.type_keys("Hello Day 2", with_spaces=True, pause=0.05)      # 4. type slowly
assert doc.window_text().strip() == "Hello Day 2"               #    verify on screen
win.type_keys("^s")                                             # 5. save (no dialog)
win.type_keys("^w")                                             # 6. close ONLY our tab
with open(path, encoding="utf-8-sig") as f:
    assert f.read().strip() == "Hello Day 2"                    # 7. verify on disk
os.remove(path)                                                 # 8. clean up
```

Why each step matters:

- The title is `name.txt - Notepad` and gets a leading `*` once modified - hence `\*?` in the regex, and `re.escape()` because file names contain dots.
- The Windows 11 Notepad editor (`Document`) does not support `set_edit_text()`; use `type_keys()`.
- `type_keys()` may drop characters when typing very fast; `pause=0.05` plus verification catches this.
- Ctrl+S shows no dialog because the file already exists.
- **Never** call `win.close()` on Notepad - it would close all the user's tabs and trigger save prompts. Ctrl+W closes only the active tab (ours).
- The file on disk is the true test oracle.

**Common mistakes (section 7)**
- `Application(backend="uia").start("calc.exe")` then `app.window(...)` - the window is never found (launcher process).
- Forgetting `control_type` so a locator matches several elements.
- Comparing `"Display is 15"` with `"15"` - parse the text first.
- `type_keys("a+b")` types `aB` because `+` means Shift - use `"a{+}b"`.
- Forgetting `with_spaces=True` - all spaces disappear.
- Typing into "any Notepad window".

**Try it yourself**
1. Extend example 02 with a test case for `12*12` and one that you expect to fail. Does the FAIL line tell you enough to debug?
2. In example 03, change the text to contain a `+` sign. What happens? Fix it with `{+}`.

---

## 8. Mouse, keyboard and image-based automation with pyautogui

`pyautogui` drives the **real** mouse and keyboard, exactly like a human user. It knows nothing about buttons - only screen coordinates, pixels and keys.

### 8.1 Safety first

```python
import pyautogui
pyautogui.FAILSAFE = True   # default: move mouse to any screen corner -> FailSafeException
pyautogui.PAUSE = 0.3       # wait 0.3 s after every pyautogui call
```

Never disable FAILSAFE while developing: it is your emergency brake when a script clicks wildly.

### 8.2 Screen coordinates and the mouse

```
(0,0) -------------> x         pyautogui.size()      -> Size(width=1920, height=1080)
  |                            pyautogui.position()  -> Point(x=512, y=300)
  v y
```

```python
pyautogui.moveTo(960, 540, duration=0.5)    # absolute, animated
pyautogui.moveRel(100, 0)                   # relative
pyautogui.click(960, 540)                   # left click
pyautogui.doubleClick(); pyautogui.rightClick()
pyautogui.dragTo(1200, 540, duration=0.5)
pyautogui.scroll(-300)                      # scroll down
```

Harmless demo: `examples/05_mouse_keyboard_pyautogui.py` (only moves the mouse; `--type` types into a window you choose).

### 8.3 Keyboard

```python
pyautogui.write("Hello", interval=0.05)    # types into WHATEVER has focus
pyautogui.press("enter")
pyautogui.press("tab", presses=3)
pyautogui.hotkey("ctrl", "s")
```

pyautogui types into the focused window - whatever it is. pywinauto's `type_keys()` first focuses a specific element, which is safer.

### 8.4 Image-based automation

```python
try:
    box = pyautogui.locateOnScreen("images/calc_seven.png", confidence=0.8)
    if box is not None:                         # older versions return None
        pyautogui.click(pyautogui.center(box))
except pyautogui.ImageNotFoundException:        # newer versions raise
    print("not found")
```

- `confidence=` requires **opencv-python**.
- Capture the reference image tightly, at the same theme, scaling and window size as the test run.
- The target must be visible (not covered or minimised).
- Wrap searches in a retry loop with a timeout (see `find_on_screen()` in example 06).
- `python examples/06_image_based_click.py --capture` creates `examples/images/calc_seven.png` automatically using pywinauto to find the button rectangle.

**Common mistakes (section 8)**
- Hard-coded coordinates (`click(812, 455)`) - break on every other screen.
- Moving the mouse yourself while the script runs.
- Reference image captured in dark mode, test run in light mode.
- Forgetting that `locateOnScreen` may raise instead of returning `None`.

**Try it yourself:** capture the reference image, run example 06, then switch Windows to dark mode (Settings > Personalization > Colors) and run it again. Explain the result.

### 8.5 Real mouse actions: pywinauto + pyautogui together

Some things can only be tested with the real mouse:
- the action is the feature: drag and drop, hover effects and tooltips, right-click menus, mouse-wheel scrolling
- the app has no usable UI Automation tree: Electron apps, canvases, charts, games, Citrix/RDP sessions

Each library has its own job:

| pywinauto | pyautogui |
|---|---|
| finds the window and brings it to the front | moves the mouse, clicks, drags, scrolls |
| tells you **where** the window is | presses keys and hotkeys |
| checks focus before you type (`is_active()`) | |

**Window-relative coordinates.** Never hard-code screen points. Add a fixed offset to the window's client-area origin:

```python
import win32gui
from pywinauto import Desktop

win = Desktop(backend="win32").window(title="Day2 Mouse Playground").wrapper_object()
win.set_focus()
x, y = win32gui.ClientToScreen(win.handle, (80, 230))   # offset inside the window
```

`ClientToScreen` skips the title bar and borders. pywinauto's `client_to_screen()` measures from the outer window edge, so its points land too high and too far left.

```python
pyautogui.moveTo(x, y, duration=0.5)            # hover (motion only)
pyautogui.click(x, y); pyautogui.doubleClick(x, y)
pyautogui.rightClick(x, y); pyautogui.press("down"); pyautogui.press("enter")  # context menu

pyautogui.moveTo(sx, sy)                        # drag and drop
pyautogui.dragTo(tx, ty, duration=1.0, button="left")   # duration > 0 !

pyautogui.mouseDown(); time.sleep(0.2)          # step-by-step drag for picky apps
pyautogui.moveTo(tx, ty, duration=0.5); pyautogui.mouseUp()

pyautogui.scroll(-3 * 120)                      # Windows: 120 units = 1 wheel notch
pyautogui.keyDown("shift"); pyautogui.press("1"); pyautogui.keyUp("shift")   # "!"
```

Full demo: `examples/12_mouse_keyboard_hybrid.py`. It drives `examples/apps/mouse_playground.py`, a harmless practice window that records every event in a JSON file. The script reads that file to check each action (the test oracle). Use `--where` to print live window-relative offsets while you hover, and measure targets in any app this way.

**Common mistakes (section 8.5)**
- `dragTo(x, y)` without `duration`: the mouse teleports and the app sees no movement between press and release.
- `scroll(-5)`: on Windows this is 1/24 of a wheel notch and does nothing. Use multiples of 120.
- Typing after a click without checking focus: the keys go to whatever window is active. Call `win.is_active()` first.
- Forgetting `mouseUp()` / `keyUp()` after an exception: the button or Shift stays held down. Release them in `finally`.
- Clicking context-menu items by coordinates: menus open in different places. Choose items with the arrow keys and Enter.

### 8.6 Real Electron app: Notion desktop

Notion, VS Code, Teams and Slack are **Electron** apps: a Chromium browser inside a window (class `Chrome_WidgetWin_1`). pywinauto finds the window easily. The page content is HTML, and its UIA tree is only partly usable or missing. The practical mix:

| Need | Tool |
|---|---|
| Find the window, pick the right one among many `Notion.exe` processes | pywinauto (`class_name=`, `process_module()`) |
| Know which page is open | pywinauto `window_text()`. Electron copies the page title into the window title |
| Create pages, type text, slash commands, move blocks | pyautogui keyboard shortcuts (`Ctrl+N`, `/todo`, `Esc`, `Ctrl+Shift+Up`) |
| Drag a block by its hover-only drag handle | pyautogui `mouseDown` → small moves → `mouseUp` |
| Check the result | **clipboard**: select all blocks, `Ctrl+C`, read the text |

Safety rules for an app full of real user data:
- Work only on a **new page with a unique title**.
- **Gate:** before typing anything, check that the window title shows a new, empty page. Stop if it doesn't.
- Check the title again before deleting, so you only ever trash your own page.
- Save the user's clipboard and restore it at the end.

Full demo: `examples/13_notion_electron_hybrid.py` (needs Notion desktop, signed in). Start Notion with `--force-renderer-accessibility` so Chromium builds its UIA tree. If the tree is missing, the script moves the block with the keyboard instead of dragging it. Notion changes its UI often: `--inspect` writes the UIA tree to `notion_tree.txt` so you can update button names.

---

## 9. Handling focus, windows and dialogs

### 9.1 Focus

```python
calc.set_focus()                       # bring to front + keyboard focus
calc.is_active()                       # is it the foreground window?
edit.has_keyboard_focus()              # does this element have the caret?
```

- Keyboard input (`type_keys`, `pyautogui.write`) goes only to the focused window.
- Call `set_focus()` immediately before typing.
- Prefer API actions (`invoke()`, `select()`, `toggle()`) which do not depend on focus.
- Windows' focus-stealing prevention may block focus changes if the user is actively using the machine - run GUI tests on a dedicated, unlocked session.

### 9.2 Multiple windows

```python
for w in Desktop(backend="uia").windows():
    print(w.window_text(), w.element_info.process_id)

calc = Desktop(backend="uia").window(title="Calculator")
note = Desktop(backend="uia").window(title_re=r"\*?my_file\.txt - Notepad")
calc.set_focus(); ...; note.set_focus()
```

### 9.3 Dialogs

A **modal dialog** blocks its owner window until it is closed. In modern apps the dialog usually appears as a **child** of the main window in the UIA tree; classic Win32 dialogs are separate top-level windows with class `#32770`.

```python
notepad.type_keys("^+s")                                   # Save as...
dlg = notepad.child_window(title_re="(?i)^save as$", control_type="Window")
if dlg.exists(timeout=5):
    print([b.window_text() for b in dlg.descendants(control_type="Button")])
    dlg.child_window(title="Cancel", control_type="Button").invoke()
    dlg.wait_not("visible", timeout=5)
```

Strategies for **unexpected** dialogs (update notices, crash reports, "Save changes?"):
- Check for known dialogs after risky steps with `exists(timeout=1)`.
- Handle them explicitly or fail the test with a clear message - never let the test hang.
- Avoid "Save changes?" prompts by saving before closing your own documents.

Full demo: `examples/07_handle_dialogs_focus.py` (focus switching, element states, Save-as dialog cancelled, timeout handling).

**Common mistakes (section 9)**
- `time.sleep(10)` instead of `wait()`.
- Looking for a dialog only at desktop level when it is a child of the main window (or vice versa).
- Leaving a dialog open when a test fails, so every following test fails too - clean up in `finally`.

---

## 10. Command-line automation

### 10.1 What is a CLI and why automate it?

A **command-line interface (CLI)** takes text commands and returns text output plus an **exit code**. Examples: `cmd`, PowerShell, `ipconfig`, `ping`, `git`, `pip`, `pytest`, `adb`, `sqlcmd`.

Automation use cases for testers:
- Launch/stop the application under test, install builds, copy files.
- Prepare test data, reset databases.
- Check the environment before a run (versions, tools, disk space).
- Search logs for errors after a run.
- Run test suites from CI servers (Jenkins, Azure DevOps, GitHub Actions) - which only run commands.

### 10.2 Running Python scripts from the command line

```powershell
PS> python hello.py                       # run a script
PS> python -m pip list                    # run a module
PS> python -c "print(2 + 3)"              # one-liner
PS> python .\examples\08_sys_argv_demo.py add 12 30
PS> echo $LASTEXITCODE                    # exit code (cmd.exe: echo %ERRORLEVEL%)
```

In VS Code use **Terminal > New Terminal**. If `python` opens the Microsoft Store, disable the App execution alias or use `py`.

```python
def main() -> int:
    ...
    return 0

if __name__ == "__main__":        # runs only when executed, not when imported
    sys.exit(main())              # exit code visible to the shell / CI
```

| Exit code | Convention |
|---|---|
| 0 | Success |
| 1 | Check/test failed |
| 2 | Wrong usage (argparse uses 2) |
| other | Tool specific (pytest: 5 = no tests collected) |

### 10.3 `sys.argv`

`sys.argv` is a list of strings: `sys.argv[0]` is the script name, the rest are the arguments.

```powershell
PS> python 08_sys_argv_demo.py add 12 30
sys.argv = ['08_sys_argv_demo.py', 'add', '12', '30']
PS> python 08_sys_argv_demo.py "hello world"     # quotes -> ONE argument
```

Limitations: everything is a string, no `--help`, manual validation and error messages, optional flags are painful. Fine for one or two simple arguments.

### 10.4 `argparse`

```python
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Demo test runner")
parser.add_argument("app", help="application under test")                  # positional
parser.add_argument("--env", choices=["dev", "qa", "uat"], default="dev")  # choices
parser.add_argument("-r", "--retries", type=int, default=1)                # typed
parser.add_argument("-v", "--verbose", action="store_true")                # flag
parser.add_argument("--tags", nargs="+", default=["smoke"])                # many values
parser.add_argument("--report", type=Path, default=Path("report.txt"))
args = parser.parse_args()          # or parse_args(["Calculator", "--env", "qa"]) in tests
```

You get `--help`, type conversion, validation and consistent error messages (exit code 2) for free. Run `python examples/09_argparse_demo.py --help`.

Sub-commands (like `git commit` / `git push`) use `add_subparsers()` - see `examples/11_reusable_cli_utility.py`.

### 10.5 Writing reusable utility scripts

1. Put logic in **functions that return data** (no printing, no `sys.exit`) - importable from pytest and other scripts.
2. Keep `main()` thin: parse arguments, call functions, print, return an exit code.
3. Use the `if __name__ == "__main__":` guard.
4. Return **meaningful exit codes** (0 ok, 1 check failed, 2 usage, 3 file error).
5. Provide good `--help`, sensible defaults, no hard-coded paths.
6. Results to `stdout`, errors to `stderr`.
7. Handle expected problems (missing file, invalid regex) with clear messages instead of tracebacks.
8. Give modules import-friendly names (`testkit.py`, `log_analyzer.py` - not `11_tool.py`).

```powershell
PS> python examples\11_reusable_cli_utility.py search ERROR hands_on\starter\app.log
PS> python examples\11_reusable_cli_utility.py disk --min-free-gb 5
PS> python examples\11_reusable_cli_utility.py which python notepad.exe
```

### 10.6 Automating system commands: `subprocess` and `os`

```python
import subprocess, sys

result = subprocess.run([sys.executable, "--version"],
                        capture_output=True, text=True, timeout=30)
result.returncode    # 0
result.stdout        # 'Python 3.14.7\n'
```

| Need | Code |
|---|---|
| Run and wait, capture output | `subprocess.run([...], capture_output=True, text=True)` |
| Fail on non-zero exit | `check=True` -> `CalledProcessError` |
| Protect against hangs | `timeout=30` -> `TimeoutExpired` |
| Program missing | catch `FileNotFoundError` |
| cmd built-ins (`dir`, `echo`) | `["cmd", "/c", "dir"]` or `shell=True` |
| Start without waiting (GUI apps) | `subprocess.Popen("calc.exe")` |
| Check a tool is on PATH | `shutil.which("git")` or `where git` |

Prefer the **list form** without `shell=True`: no quoting problems and no command-injection risk.

`os` and friends:

```python
os.getcwd(); os.listdir("."); os.environ.get("USERNAME")
os.makedirs("reports", exist_ok=True); os.path.join("logs", "app.log")
os.system("cls")                   # runs a command; returns only the exit code
shutil.disk_usage("C:\\"); platform.system(); platform.release()
```

`os.system()` cannot capture output - use `subprocess.run()` in test code.

Full demo: `examples/10_subprocess_demo.py` (python --version, where python, ipconfig parsing, return codes, check=True, timeout, missing program, cmd built-ins, Popen, os).

**Common mistakes (section 10)**
- Forgetting to convert `sys.argv` values (`"12" + "30"` = `"1230"`).
- Ignoring `returncode` - a failed command looks like a success.
- No `timeout=` - one hanging tool freezes the whole pipeline.
- `subprocess.run("dir")` fails - `dir` is a cmd built-in, not an .exe.
- `shell=True` with user-provided input.
- Using `*` unquoted in Git Bash - the shell expands it to file names.
- Putting options before a `nargs="+"` list and a positional after it - `--tags a b Calculator` swallows `Calculator` as a tag.

**Try it yourself**
1. Run `python examples\11_reusable_cli_utility.py which python git` and then `echo $LASTEXITCODE`. Add a tool that does not exist and check the exit code again.
2. Add a `--json` flag to the `sysinfo` sub-command that prints the dict with `json.dumps(..., indent=2)`.

---

## 11. Cheat-sheets

### 11.1 pywinauto

```python
from pywinauto import Application, Desktop
from pywinauto.timings import TimeoutError, Timings
from pywinauto.findwindows import ElementNotFoundError, ElementAmbiguousError

# --- connect ---
app  = Application(backend="uia").start(r"C:\App\app.exe")
app  = Application(backend="uia").connect(title="My App", timeout=10)
win  = app.window(title="My App")
win  = Desktop(backend="uia").window(title_re=r".*Calculator.*")
Desktop(backend="uia").windows()                    # all top-level windows

# --- locate ---
btn = win.child_window(auto_id="okButton", control_type="Button")
btn = win.child_window(title="OK", control_type="Button")
txt = win.child_window(control_type="Edit", found_index=0)
win.print_control_identifiers(depth=3, filename=None)

# --- wait ---
win.wait("visible", timeout=10)     # exists | visible | enabled | ready | active
win.wait_not("visible", timeout=5)
btn.exists(timeout=2)               # bool
Timings.window_find_timeout = 10    # global default

# --- act ---
btn.invoke(); btn.click_input(); btn.double_click_input()
txt.set_edit_text("abc")            # if Value pattern supported
txt.type_keys("abc def{ENTER}", with_spaces=True, pause=0.05)
chk.toggle(); combo.select("Item 2"); win.menu_select("File->Save")
win.set_focus(); win.minimize(); win.maximize(); win.restore(); win.close()

# --- read / verify ---
btn.window_text(); btn.is_enabled(); btn.is_visible(); win.is_active()
chk.get_toggle_state(); item.is_selected(); btn.rectangle()
btn.element_info.automation_id; btn.element_info.control_type
win.descendants(control_type="Button"); win.children()
```

`type_keys` special characters:

| Code | Key | Code | Key |
|---|---|---|---|
| `^` | Ctrl | `{ENTER}` | Enter |
| `+` | Shift | `{TAB}` / `{TAB 3}` | Tab (x3) |
| `%` | Alt | `{ESC}` | Escape |
| `{+}` `{^}` `{%}` | literal + ^ % | `{DELETE}` `{BACKSPACE}` | Delete / Backspace |
| `{F1}`..`{F12}` | Function keys | `{VK_LWIN}` | Windows key |
| `{UP}` `{DOWN}` `{LEFT}` `{RIGHT}` | Arrows | `{HOME}` `{END}` | Home / End |

### 11.2 pyautogui

```python
import pyautogui
pyautogui.FAILSAFE = True; pyautogui.PAUSE = 0.3

pyautogui.size(); pyautogui.position(); pyautogui.onScreen(x, y)
pyautogui.moveTo(x, y, duration=0.5); pyautogui.moveRel(dx, dy)
pyautogui.click(x, y); pyautogui.doubleClick(); pyautogui.rightClick()
pyautogui.dragTo(x, y, duration=0.5); pyautogui.scroll(-300)   # Windows: 120 = 1 notch
pyautogui.mouseDown(); pyautogui.moveTo(x, y, duration=0.5); pyautogui.mouseUp()
x, y = win32gui.ClientToScreen(win.handle, (dx, dy))  # window offset -> screen point

pyautogui.write("text", interval=0.05); pyautogui.press("enter")
pyautogui.press("tab", presses=3); pyautogui.hotkey("ctrl", "shift", "s")
pyautogui.keyDown("shift"); pyautogui.keyUp("shift")

pyautogui.screenshot("full.png"); pyautogui.screenshot(region=(x, y, w, h))
box = pyautogui.locateOnScreen("img.png", confidence=0.8)   # needs opencv
pyautogui.center(box); pyautogui.locateCenterOnScreen("img.png", confidence=0.8)
# may raise pyautogui.ImageNotFoundException ; FailSafeException on corner
```

### 11.3 argparse

```python
import argparse
p = argparse.ArgumentParser(prog="tool", description="...", epilog="...")
p.add_argument("file")                                   # positional, required
p.add_argument("-o", "--output", default="out.txt")      # optional with default
p.add_argument("--count", type=int, required=True)       # required option, typed
p.add_argument("--level", choices=["INFO", "ERROR"], type=str.upper)
p.add_argument("-v", "--verbose", action="store_true")   # flag
p.add_argument("--tags", nargs="+")                      # 1..n values
p.add_argument("--extra", nargs="*", default=[])         # 0..n values
p.add_argument("--min-free-gb", type=float)              # -> args.min_free_gb
p.add_argument("--version", action="version", version="%(prog)s 1.0")
g = p.add_mutually_exclusive_group(); g.add_argument("--json"); g.add_argument("--csv")

sub = p.add_subparsers(dest="command", required=True)
s = sub.add_parser("search", help="..."); s.set_defaults(func=cmd_search)

args = p.parse_args()                 # or p.parse_args(["a.log", "--count", "3"])
p.error("custom message")             # prints usage, exits with code 2
```

---

## 12. Questions and answers

**Q1. What is the difference between the `win32` and `uia` backends in pywinauto?**
`win32` uses the Win32 API (window handles and messages) and sees only classic HWND controls (Win32, MFC, WinForms, VB6). `uia` uses Microsoft UI Automation and also supports WPF, UWP/WinUI Store apps and Electron. `uia` is the default choice; `win32` can be faster for legacy apps.

**Q2. What is the UI Automation tree?**
The hierarchical representation of all UI elements exposed by Windows' accessibility framework, rooted at the desktop. Each element has properties (Name, AutomationId, ControlType ...) and control patterns (Invoke, Value, Toggle ...). Automation tools and screen readers navigate this tree.

**Q3. Element-based vs image-based automation - when would you use each?**
Element-based (pywinauto) is fast, robust and can read states; use it whenever the app exposes accessibility info. Image-based (pyautogui) works on pixels; use it only when elements are not exposed - games, Citrix/RDP sessions, custom-drawn canvases. A hybrid (find by image, verify by element) is common.

**Q4. What is the most reliable locator for a desktop element?**
The AutomationId (`auto_id`), combined with `control_type`. Names change with language and version; indexes change with layout.

**Q5. `invoke()` vs `click_input()`?**
`invoke()` triggers the element through the UIA Invoke pattern without moving the mouse and works even if the window is partly covered. `click_input()` moves the real mouse and clicks - use it when you specifically test mouse behaviour or the element does not support Invoke.

**Q6. Why does `Application().start("calc.exe")` fail to find the Calculator window on Windows 11?**
`calc.exe` is a launcher that starts `CalculatorApp.exe` and exits. pywinauto tracks the launcher's process, which owns no window. Launch with `subprocess.Popen` and connect with `Desktop(backend="uia").window(title="Calculator")` (or `Application().connect(...)`).

**Q7. How do you handle an application that takes a long time to start?**
With explicit waits: `win.wait("visible", timeout=60)` or `exists(timeout=...)`, optionally raising `Timings` globally. Never use fixed `time.sleep()`.

**Q8. Why is `time.sleep()` bad in automation?**
A fixed delay is either too short (flaky failures on slow machines) or too long (wasted time on fast machines). Explicit waits poll for a condition and continue as soon as it is met.

**Q9. How do you handle an unexpected dialog?**
After risky steps, check for known dialogs with `exists(timeout=1)`, handle them (click the right button), and wait until they close with `wait_not("visible")`. If an unknown dialog blocks the app, fail the test clearly and capture a screenshot. Always clean up in `finally`.

**Q10. What does `pyautogui.FAILSAFE` do?**
When enabled (default), moving the mouse into any screen corner raises `FailSafeException` on the next pyautogui call, stopping a runaway script.

**Q11. Name some challenges of desktop automation.**
Synchronisation, focus loss, missing/unstable AutomationIds, unknown start state (restored sessions), modal dialogs, screen resolution/DPI/theme, launcher processes, locked screens on CI agents, custom-drawn controls.

**Q12. `sys.argv` vs `argparse`?**
`sys.argv` is a raw list of strings - you convert and validate everything yourself. `argparse` adds automatic `--help`, type conversion, defaults, choices, required options, sub-commands and consistent error messages (exit code 2).

**Q13. `subprocess.run` vs `subprocess.Popen` vs `os.system`?**
`run` starts a command and waits, returning a `CompletedProcess` with `returncode`, `stdout`, `stderr`. `Popen` starts a process without waiting (used for GUI apps or streaming output). `os.system` runs a command through the shell and returns only the exit code - no output capture; avoid it in test code.

**Q14. What does `check=True` do in `subprocess.run`, and why use `timeout`?**
`check=True` raises `CalledProcessError` when the exit code is non-zero, so failures cannot go unnoticed. `timeout` kills the process and raises `TimeoutExpired` if it runs too long, preventing a hung tool from freezing the pipeline.

**Q15. Why are exit codes important for test scripts?**
CI servers decide pass/fail from the exit code: 0 = success, non-zero = failure. A script that prints "FAIL" but exits with 0 produces a green build.

**Q16. Why is `shell=True` risky?**
The command string is interpreted by the shell, so special characters in user input can inject extra commands. The list form passes arguments directly to the program.

**Q17. How do you make a Python CLI script reusable?**
Logic in functions returning data, a thin `main()`, the `__name__ == "__main__"` guard, argparse with good help and defaults, meaningful exit codes, errors to stderr, no hard-coded paths, import-friendly file names.

**Q18. What inspection tools do you use for desktop apps?**
Accessibility Insights for Windows, Inspect.exe (Windows SDK), and pywinauto's `print_control_identifiers()`. They show AutomationId, Name, ControlType, ClassName, patterns and hierarchy.

---

## 13. Day 2 summary

- Desktop apps are **processes** that own **windows**; input arrives via the **message loop**; elements are exposed through the **UI Automation tree**.
- App types: Win32/MFC, WinForms, WPF, UWP/WinUI (Win11 Calculator & Notepad), Electron, Java. Use `backend="uia"` for modern apps, `win32` for legacy ones.
- Verify **states**: exists, visible, enabled, focused, checked, selected.
- **Inspect, don't guess**: Accessibility Insights / Inspect.exe / `print_control_identifiers()`. Locator priority: `auto_id` > title + control_type > index.
- **Element-based first**, image-based as fallback, hybrid when useful.
- Handle **focus** (`set_focus`), **waits** (`wait`, `exists`), **dialogs** (detect, handle, `wait_not`).
- **Never assume a clean app state**: own your test data, close only what you opened, verify the real outcome.
- CLI automation: run scripts with `python`, read arguments with `sys.argv` or better `argparse`, run system commands with `subprocess.run` (capture output, check return codes, use timeouts), and write reusable utilities with functions and exit codes.

**Further reading**
- pywinauto docs: https://pywinauto.readthedocs.io
- pyautogui docs: https://pyautogui.readthedocs.io
- argparse tutorial: https://docs.python.org/3/howto/argparse.html
- subprocess: https://docs.python.org/3/library/subprocess.html
- Accessibility Insights: https://accessibilityinsights.io
