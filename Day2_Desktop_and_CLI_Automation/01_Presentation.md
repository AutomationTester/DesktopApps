---
marp: true
theme: default
paginate: true
---

# Day 2
## Desktop & Command-Line Automation with Python

Python Desktop Application Automation Testing - 5-Day Program

- Desktop application fundamentals
- Desktop automation with pywinauto & pyautogui
- Command-line automation with sys.argv, argparse, subprocess

<!-- Trainer notes:
Welcome back. Yesterday = Python basics + OOP. Today we finally make Python drive REAL applications.
Set expectations: by 5 pm every trainee will have automated Calculator, safely automated Notepad, and built their own command-line tool.
Check that everyone has: Python 3.x, VS Code, pywinauto, pyautogui, opencv-python installed (`pip list`).
Ask: "Who has ever repeated the same manual test on a desktop app 20 times?" - that is our motivation.
-->

---

# Agenda (8 hours)

| Time          | Topic                                                        |
|---------------|--------------------------------------------------------------|
| 09:00 - 09:15 | Welcome, Day 1 recap, goals                                  |
| 09:15 - 10:30 | Module 1: Desktop application fundamentals + inspection tools |
| 10:30 - 10:45 | Break                                                        |
| 10:45 - 12:15 | Module 2: Desktop automation with Python (pywinauto, pyautogui) |
| 12:15 - 13:00 | Lab 1: Automating Calculator                                 |
| 13:00 - 13:45 | Lunch                                                        |
| 13:45 - 14:30 | Focus, windows & dialogs + Lab 2: Safe Notepad automation    |
| 14:30 - 15:30 | Module 3: Command-line automation                            |
| 15:30 - 15:45 | Break                                                        |
| 15:45 - 16:40 | Labs 3 & 4: CLI utility, passing arguments (+ Lab 5 extra)   |
| 16:40 - 17:00 | Recap, quiz, Q&A                                             |

<!-- Trainer notes:
Walk through quickly. Emphasise that ~40% of the day is hands-on.
Mention the folder structure: 01_Presentation, 02_Reading_Material, 03_Quiz, examples/, hands_on/.
Examples are numbered in the order we use them on the slides.
-->

---

# Learning objectives

By the end of today you can:

1. Explain processes, windows, the message loop and the UI Automation tree
2. Recognise Win32, WPF, Electron and UWP/WinUI (Store) apps - and pick a backend
3. Inspect elements with Accessibility Insights / Inspect.exe / `print_control_identifiers()`
4. Automate apps element-based (pywinauto) and image-based (pyautogui)
5. Handle focus, multiple windows, waits and dialogs
6. Build reusable CLI tools with `sys.argv`, `argparse`, `subprocess`, `os`

<!-- Trainer notes:
Keep this slide visible for a minute. Return to it during the recap and tick off each objective.
-->

---

# Quick recap of Day 1

- Variables, lists, dicts, loops, functions
- Exceptions: `try / except / finally`
- Classes & objects - `__init__`, methods, attributes
- Modules & `pip install`

```python
class Calculator:
    def __init__(self, name):
        self.name = name
    def add(self, a, b):
        return a + b
```

Today: the **objects** are real windows and buttons!

<!-- Trainer notes:
2-3 quick questions: What does `finally` do? (runs always - we use it for clean-up today). What is `self`?
Tie OOP to today: pywinauto gives us objects (window, button) with methods (click, type_keys) and attributes (text, enabled).
-->

---

<!-- _class: lead -->
# Module 1
## Desktop Application Fundamentals

<!-- Trainer notes:
75 minutes. Theory-heavy but keep it interactive: open Task Manager and Accessibility Insights live.
-->

---

# What is a desktop application?

- Runs **locally** on the OS (Windows, macOS, Linux) - not inside a browser
- Installed as an `.exe` / MSI / Store package
- Has direct access to files, registry, printers, devices
- Examples: Notepad, Calculator, MS Office, SAP GUI, Tally, VS Code, banking terminals

**Why testers care:** many enterprise systems (billing, ERP, trading, healthcare) are still desktop apps - and Selenium cannot touch them.

<!-- Trainer notes:
Ask the group which desktop apps they test at work. Typical answers: SAP GUI, custom .NET WinForms tools, Tally, Citrix apps.
Selenium drives browsers via WebDriver; desktop needs different tools - that's why this course exists.
-->

---

# How a desktop app works: processes

```
  You double-click calc.exe
          |
          v
  +---------------------+       Task Manager shows:
  |  PROCESS  (PID 4312)|         Name   : CalculatorApp.exe
  |  - memory           |         PID    : 4312
  |  - threads          |         Status : Running
  |  - 1..n WINDOWS     |
  +---------------------+
```

- **Process** = running instance of a program, identified by a **PID**
- One process can own **many windows** (main window, dialogs, tool windows)
- Automation always starts with: *which process? which window?*

<!-- Trainer notes:
Demo: open Task Manager (Ctrl+Shift+Esc) > Details tab > show PID column. Launch Calculator and point out that the process is CalculatorApp.exe, not calc.exe - calc.exe is just a launcher. This fact returns later (why Application().start("calc.exe") doesn't work).
Run examples/01_list_running_windows.py to list windows with their PIDs.
-->

---

# How a desktop app works: windows

- A **window** is a rectangle on screen owned by a process
- Every control is (logically) a window too: buttons, text boxes, menus
- Windows form a **parent-child hierarchy**

```
Desktop
 +-- Calculator (top-level window)
 |    +-- Display  "Display is 0"
 |    +-- Button   "Seven"
 |    +-- Button   "Plus"
 +-- Notepad (top-level window)
      +-- Document (the editor)
      +-- Menu bar
```

<!-- Trainer notes:
Classic Win32: every control really IS an HWND (window handle). Modern frameworks (WPF, UWP, Electron) draw controls themselves and expose them only through UI Automation - so "logically" a window.
The tree picture is key - keep referring back to it.
-->

---

# The message loop (how clicks reach the app)

```
 Mouse/Keyboard --> Windows OS --> message queue of the app
                                          |
      +-----------------------------------+
      v
  while (GetMessage(&msg)) {      // the app's "message loop"
      TranslateMessage(&msg);
      DispatchMessage(&msg);      // -> button's click handler runs
  }
```

- Input is delivered as **messages** (WM_LBUTTONDOWN, WM_KEYDOWN, WM_PAINT ...)
- Only the **focused / foreground** window receives keyboard input
- If the app is busy, the loop stalls -> "(Not Responding)"

<!-- Trainer notes:
Testers don't write C code; the point is: 1) input goes to the focused window - wrong focus = wrong app gets your keys; 2) a busy app doesn't process messages - automation must WAIT. Both become "automation challenges" later.
Common question: "Does pyautogui send messages?" - It injects real OS input (SendInput), the same path as a physical mouse.
-->

---

# The UI Automation (UIA) tree

- Microsoft **UI Automation** = accessibility API built into Windows
- Screen readers (Narrator, NVDA) use it - **automation tools use it too**
- Every element exposes **properties** and **patterns**

| Property        | Example              |
|-----------------|----------------------|
| Name            | "Seven"              |
| AutomationId    | `num7Button`         |
| ControlType     | Button               |
| ClassName       | "Button"             |
| IsEnabled / IsOffscreen | True / False |

Patterns = what it can do: **Invoke** (click), **Value** (set text), **Toggle** (checkbox), **SelectionItem**, **ExpandCollapse**, **Window** (close)

<!-- Trainer notes:
Key message: if an app is accessible, it is automatable. Good accessibility = good testability.
AutomationId is the "id attribute" of desktop apps - just like id in Selenium.
Patterns explain pywinauto methods: .invoke() uses Invoke pattern, .toggle() Toggle pattern, etc.
-->

---

# Types of desktop applications

| Type | Technology | Examples | pywinauto backend |
|------|------------|----------|-------------------|
| **Win32 / MFC** | C/C++ native, HWND controls | Old Notepad, Paint, many legacy tools | `win32` (or `uia`) |
| **WinForms** | .NET, wraps Win32 | Many in-house business apps | `win32` or `uia` |
| **WPF** | .NET, vector-drawn UI | Visual Studio, modern enterprise apps | `uia` |
| **UWP / WinUI (Store)** | Modern Windows apps | Win11 Calculator, Notepad, Settings | `uia` |
| **Electron** | Chromium + Node.js | VS Code, Teams (classic), Slack | `uia` (limited) |
| **Java Swing / JavaFX** | JVM | Some trading/banking apps | Java Access Bridge needed |

<!-- Trainer notes:
Win11 surprise: Calculator and Notepad are Store (UWP/WinUI) apps now - so we use backend="uia" for both.
Electron: UIA tree is exposed by Chromium; often usable, but deep content may need Playwright/Selenium via remote debugging (mention only).
Java apps: need Java Access Bridge enabled - otherwise the tree is empty. Good interview point.
-->

---

# How to tell which type an app is

- **Inspect the class name** (Accessibility Insights / Inspect.exe):
  - `#32770` -> classic Win32 dialog
  - `WindowsForms10.*` -> WinForms
  - `HwndWrapper[...]` -> WPF
  - `ApplicationFrameWindow` / `Windows.UI.Core.CoreWindow` / WinUI classes -> Store app
  - `Chrome_WidgetWin_1` -> Electron / Chromium
- **Task Manager**: Store apps run from `C:\Program Files\WindowsApps\...`
- Rule of thumb: **start with `uia`**, fall back to `win32` for old apps if `uia` is slow or incomplete

<!-- Trainer notes:
Demo: run examples/01_list_running_windows.py and point at the CLASS column; open VS Code to show Chrome_WidgetWin_1.
Question: "Why not always win32?" - win32 only sees real HWND controls; WPF/UWP controls are invisible to it.
-->

---

# pywinauto backends: win32 vs uia

```python
from pywinauto import Application, Desktop

# Classic Win32 app (e.g. an old MFC/WinForms tool)
app = Application(backend="win32").start(r"C:\Tools\legacy_app.exe")
dlg = app.window(title_re=".*Legacy App.*")
dlg.Edit1.set_edit_text("hello")   # win32: direct control access

# Modern / Store app
calc = Desktop(backend="uia").window(title="Calculator")
```

| | `win32` | `uia` |
|---|---|---|
| API | Win32 messages (HWND) | Microsoft UI Automation |
| Sees | Win32, MFC, WinForms, VB6 | Everything above + WPF, UWP, WinUI, Electron |
| Speed | Fast | Slower, richer |

<!-- Trainer notes:
The win32 snippet is conceptual (we don't have a legacy app installed). Notepad was the classic win32 demo in older Windows versions; on Windows 11 it is a Store app so it needs uia.
Rule: one Application/Desktop object = one backend. You cannot mix inside the same object.
-->

---

# Desktop UI elements

| Element | ControlType | Typical actions |
|---------|-------------|-----------------|
| Window / Dialog | Window | focus, move, close |
| Button | Button | invoke / click |
| Text box | Edit / Document | type, read text |
| Label | Text | read text |
| Checkbox | CheckBox | toggle, get state |
| Radio button | RadioButton | select |
| Combo box / dropdown | ComboBox | expand, select item |
| List / Tree / Grid | List / Tree / DataGrid | select, read rows |
| Menu / Menu item | Menu / MenuItem | open, select |
| Tab | Tab / TabItem | select |

<!-- Trainer notes:
Map to what manual testers already know from test cases: "Click Save button", "Enter username", "Verify label shows Success".
Each row corresponds to a pywinauto wrapper class with specific methods.
-->

---

# Element states - what testers verify

| State | Meaning | pywinauto |
|-------|---------|-----------|
| **Exists** | Element is in the tree | `spec.exists()` |
| **Visible** | On screen, not hidden/off-screen | `is_visible()` |
| **Enabled** | Accepts input (not greyed) | `is_enabled()` |
| **Focused** | Receives keyboard input | `has_keyboard_focus()` |
| **Active** | Window is in foreground | `is_active()` |
| **Checked** | Checkbox/toggle state | `get_toggle_state()` (0/1/2) |
| **Selected** | List/radio/tab item chosen | `is_selected()` |
| **Minimized / Maximized** | Window size state | `is_minimized()`, `is_maximized()` |

<!-- Trainer notes:
Classic test cases: "Save button should be disabled until a field is changed" -> assert not save.is_enabled().
Wait conditions use the same words: spec.wait("exists visible enabled ready active").
"ready" = visible + enabled.
-->

---

# Object inspection tools

1. **Accessibility Insights for Windows** (free, Microsoft) - *recommended*
   - Hover an element -> see Name, AutomationId, ControlType, patterns
2. **Inspect.exe** (Windows SDK) - classic, same information
   - `C:\Program Files (x86)\Windows Kits\10\bin\<version>\x64\inspect.exe`
3. **pywinauto** `print_control_identifiers()` - from Python
4. (Optional) FlaUInspect, UISpy (legacy)

> Rule: **Never guess locators - inspect them.**

<!-- Trainer notes:
Live demo Accessibility Insights: Live Inspect mode, hover over the "7" in Calculator, read AutomationId = num7Button. Toggle "Hierarchy" to show the tree.
If not installed: https://accessibilityinsights.io -> Windows. Inspect.exe comes with the Windows SDK.
Common question: "Which one should I use?" - Accessibility Insights: modern, maintained, also runs accessibility checks (bonus for testers).
-->

---

# Accessibility Insights - what to read

```
 Live Inspect  >  hover "7" in Calculator
 ------------------------------------------------
 Name              : Seven
 AutomationId      : num7Button        <-- best locator
 ControlType       : Button
 ClassName         : Button
 FrameworkId       : XAML              <-- UWP/WinUI -> backend "uia"
 IsEnabled         : True
 IsOffscreen       : False
 Patterns          : Invoke
```

Locator priority: **AutomationId > Name + ControlType > index / position**

<!-- Trainer notes:
FrameworkId tells the technology: Win32, WinForm, WPF, XAML (UWP/WinUI), Chrome (Electron).
Names change with language (German Windows -> "Sieben"); AutomationId does not. That's why auto_id comes first.
-->

---

# print_control_identifiers()

```python
calc = Desktop(backend="uia").window(title="Calculator")
calc.print_control_identifiers(depth=4)
```

```
Button - 'Seven'    (L1012, T604, R1092, B660)
['Seven', 'SevenButton', 'Button12']
child_window(title="Seven", auto_id="num7Button", control_type="Button")
```

- Line 3 is a **ready-made locator** - copy it into your script
- `filename="tree.txt"` saves the dump -> search it in VS Code
- Avoid `Button12`-style names: they depend on order

Example: `examples/04_print_control_identifiers.py`

<!-- Trainer notes:
Run example 04. Show how long the output is without depth - that's why depth= and filename= exist.
Point out the 3 lines per element.
-->

---

# Desktop automation challenges

- **Timing / synchronisation** - app not ready, animations, slow startup
- **Focus** - pop-ups steal focus; keys go to the wrong window
- **Unstable locators** - no AutomationId, names change with language/version
- **Unknown start state** - app restores last session (Win11 Notepad tabs!)
- **Dialogs** - modal dialogs block the main window
- **Screen dependence** - resolution, DPI scaling, theme, multi-monitor
- **Launcher processes** - `calc.exe` starts another process and exits
- **Environment** - screen locked / RDP minimised -> no UI to automate
- **Custom-drawn controls** - invisible to UIA -> image-based fallback

<!-- Trainer notes:
Ask trainees for examples from their own manual testing: "the dialog appeared behind the window", "app took 30 s to load".
Each challenge has a counter-measure in Module 2: explicit waits, set_focus, auto_id, temp files, dialog handling, image confidence, connect instead of start.
Screen lock: GUI automation needs an unlocked interactive desktop - important for CI agents.
-->

---

# Challenges -> counter-measures

| Challenge | Counter-measure |
|-----------|-----------------|
| Timing | `wait("visible")`, `exists(timeout=)` - never blind `sleep` |
| Focus | `set_focus()` before typing; prefer `invoke()` over mouse |
| Locators | `auto_id` first; inspect, don't guess |
| Start state | Create your own test data (temp file); reset (press C) |
| Dialogs | Detect with `exists()`, handle, `wait_not("visible")` |
| Screen / DPI | Element-based first; images only as fallback |
| Launchers | `Popen` + `Desktop().window(...)` connect |
| Clean-up | `try / finally` - close only what you opened |

<!-- Trainer notes:
This table is the "cheat code" for the rest of the day. Tell trainees to photograph it.
-->

---

<!-- _class: lead -->
# Module 2
## Desktop Automation with Python

<!-- Trainer notes:
90 minutes before lunch + 45 minutes after lunch. Heavy on live demos.
-->

---

# Two ways to automate a GUI

```
 ELEMENT-BASED (pywinauto)          IMAGE-BASED (pyautogui)
 "Press the button whose            "Find this picture on the
  AutomationId is num7Button"        screen and click its centre"

  script --> UIA API --> app         script --> screenshot --> pixel match
                                             --> real mouse click
```

- Element-based: talks to the **object model** (like Selenium for desktop)
- Image-based: sees only **pixels**, acts like a human hand

<!-- Trainer notes:
Analogy: element-based = asking the receptionist for "room 207"; image-based = walking the corridor looking for the door with the red sticker.
Both are valid - choose per situation (next slide).
-->

---

# Element-based vs image-based

| Aspect | Element-based (pywinauto) | Image-based (pyautogui) |
|--------|---------------------------|-------------------------|
| Finds by | AutomationId, name, type | Screenshot pixel matching |
| Speed | Fast | Slower (screen scans) |
| Robust to theme/DPI/resolution | Yes | No - images break |
| Window hidden/covered | Often still works (`invoke`) | Fails - must be visible |
| Can read text / state | Yes | No (needs OCR) |
| Works without accessibility | No | Yes |
| Typical use | Win32/WPF/UWP business apps | Games, Citrix/RDP, canvas, legacy |
| Maintenance | Low | High |

**Strategy:** element-based first, image-based as fallback, **hybrid** when needed.

<!-- Trainer notes:
Interview favourite. Stress "can read state": image-based can click but cannot easily VERIFY - and verification is the whole point of testing.
Hybrid: find/click with image, verify with element (example 06 does exactly this).
-->

---

# pywinauto in 5 lines

```python
import subprocess
from pywinauto import Desktop

subprocess.Popen("calc.exe")                          # 1. launch
calc = Desktop(backend="uia").window(title="Calculator")  # 2. describe
calc.wait("visible", timeout=10)                      # 3. wait
calc.child_window(auto_id="num7Button",
                  control_type="Button").invoke()     # 4. act
print(calc.child_window(auto_id="CalculatorResults").window_text())  # 5. verify
```

Output: `Display is 7`

<!-- Trainer notes:
Type this live in VS Code - don't copy-paste. Let trainees type along.
Explain: window() returns a SPECIFICATION (a description), not the element. It is resolved lazily when you act on it - with automatic retries up to the timeout.
-->

---

# Application vs Desktop: start or connect?

```python
from pywinauto import Application, Desktop

# Works for normal apps: pywinauto owns the process
app = Application(backend="uia").start(r"C:\MyApp\MyApp.exe")
win = app.window(title="My App")

# Connect to an already running process
app = Application(backend="uia").connect(title="My App", timeout=10)

# Store apps (Win11 Calculator/Notepad): calc.exe is a LAUNCHER that exits
subprocess.Popen("calc.exe")
calc = Desktop(backend="uia").window(title="Calculator")
```

- `Application().start("calc.exe")` tracks the **launcher PID** -> window never found
- `Desktop()` searches **all** top-level windows -> works for launchers

<!-- Trainer notes:
Verified on Windows 11: Application().start("calc.exe") returns a process that exits; the real UI lives in CalculatorApp.exe.
Common question: "Can I connect by process name?" - Application().connect(path="CalculatorApp.exe") works too, but Desktop().window(title=...) is simplest.
-->

---

# Locating elements: child_window()

```python
win.child_window(auto_id="num7Button", control_type="Button")    # best
win.child_window(title="Seven", control_type="Button")           # ok
win.child_window(title_re=r"^Display is .*")                     # regex
win.child_window(control_type="Document")                        # only one exists
win.child_window(control_type="Button", found_index=0)           # fragile
win.SevenButton                                                   # "best match" - quick & dirty
```

- Combine criteria to be **unique**
- `ElementAmbiguousError` = more than one match -> add criteria
- `ElementNotFoundError` = no match -> inspect again / wait longer

<!-- Trainer notes:
Relate to Selenium: auto_id ~ By.ID, title ~ By.LINK_TEXT/name, control_type ~ tag name.
Demo the ambiguous error: win.child_window(control_type="Button").invoke() on Calculator.
-->

---

# Actions and reading values

| Goal | Method | Notes |
|------|--------|-------|
| Click (no mouse) | `invoke()` | UIA Invoke pattern - robust |
| Click (real mouse) | `click_input()` | Needs visible window |
| Type text | `type_keys("abc", with_spaces=True)` | Needs focus |
| Set text directly | `set_edit_text("abc")` | Only if Value pattern supported |
| Read text | `window_text()` | Name / value |
| Toggle checkbox | `toggle()`, `get_toggle_state()` | |
| Select item | `select("Item")` | ComboBox, List, Tab |
| Menu | `menu_select("File->Save")` | win32 style menus |
| Focus / close | `set_focus()`, `close()` | |

<!-- Trainer notes:
invoke() vs click_input(): invoke goes through UIA and does not move the mouse; click_input moves the real mouse. Prefer invoke unless you are testing mouse behaviour.
type_keys special characters: ^ = Ctrl, + = Shift, % = Alt, {ENTER}, {TAB}, {ESC}. To type a literal + use {+}.
-->

---

# Demo: Calculator automation

`examples/02_calculator_pywinauto.py`

```python
BUTTONS = {"7": "num7Button", "+": "plusButton", "=": "equalButton", ...}

def check(calc, expression, expected):
    press(calc, "C")                 # known start state
    enter(calc, expression + "=")
    actual = read_result(calc)       # "Display is 15" -> "15"
    print("PASS" if actual == expected else "FAIL", expression)
```

```
[PASS] 7+8        expected=15     actual=15
[PASS] 9*6        expected=54     actual=54
[PASS] 50-80      expected=-30    actual=-30
[PASS] 100/4      expected=25     actual=25
```

<!-- Trainer notes:
Run example 02. Point out: data-driven test cases (list of tuples), known start state (press C), verification (parse "Display is"), clean-up (close - safe because Calculator holds no data).
Mention thousands separator: 1000 shows as "1,000" - strip commas.
Ask: "What would make this test fail even though Calculator is fine?" (wrong mode e.g. Scientific, locale decimal comma).
-->

---

# Real-world lesson: Notepad on Windows 11

Windows 11 Notepad:
- **Restores your previous tabs** (even unsaved ones!)
- Opens files as **new tabs in the SAME window**

A naive script:
```python
win = Desktop(backend="uia").window(title_re=".*Notepad")   # which tab?!
win.type_keys("test test test")                             # into YOUR document?
win.close()                                                 # closes ALL tabs
```

> **Never assume a clean application state.**

<!-- Trainer notes:
This is the most important "mindset" slide of the day. Automation that damages user data is worse than no automation.
Real-world parallels: shared test machines, apps that remember last login/last opened project, databases with leftover test data.
Do NOT run the naive script. Ever.
-->

---

# Safe Notepad pattern

```python
fd, path = tempfile.mkstemp(prefix="day2_", suffix=".txt"); os.close(fd)
subprocess.Popen(["notepad.exe", path])                     # OUR file only
name = os.path.basename(path)
win = Desktop(backend="uia").window(title_re=rf"\*?{re.escape(name)} - Notepad")
win.wait("visible", timeout=15)
doc = win.child_window(control_type="Document")

doc.set_focus()
doc.type_keys("Hello Day 2", with_spaces=True, pause=0.05)  # slow = reliable
assert doc.window_text().strip() == "Hello Day 2"           # verify UI
win.type_keys("^s")                                         # save (no dialog)
win.type_keys("^w")                                         # close ONLY our tab
assert open(path, encoding="utf-8-sig").read().strip() == "Hello Day 2"  # verify disk
```

`examples/03_notepad_safe_automation.py`

<!-- Trainer notes:
Walk through line by line:
- unique temp file -> we own the test data
- title regex with optional '*' (title gets '*' when modified) and re.escape
- set_edit_text is NOT supported by the Win11 Notepad editor -> type_keys
- type_keys can drop characters without pause -> pause=0.05 and verify
- Ctrl+S no dialog because file exists; Ctrl+W closes only our tab
- oracle = file on disk
- NEVER win.close() on Notepad.
Run example 03.
-->

---

# Mouse automation with pyautogui

```python
import pyautogui
pyautogui.FAILSAFE = True        # mouse to a screen corner = emergency stop
pyautogui.PAUSE = 0.3            # pause after every call

print(pyautogui.size())          # Size(width=1920, height=1080)
print(pyautogui.position())      # Point(x=512, y=300)
pyautogui.moveTo(960, 540, duration=0.5)   # absolute
pyautogui.moveRel(100, 0)                  # relative
# pyautogui.click(x, y) / doubleClick / rightClick / dragTo / scroll
```

```
(0,0) ------------------> x
  |
  |        (960,540) = centre of a 1920x1080 screen
  v y
```

<!-- Trainer notes:
Run examples/05_mouse_keyboard_pyautogui.py - it only moves the mouse (harmless).
FAILSAFE: demonstrate by slamming the mouse into the top-left corner during the tour -> FailSafeException. Never disable it while learning.
DPI note: with 125/150 % scaling, coordinates are physical pixels; pyautogui and pywinauto both set DPI awareness.
-->

---

# Keyboard automation

```python
# pyautogui - types into WHATEVER has focus
pyautogui.write("Hello", interval=0.05)
pyautogui.press("enter")
pyautogui.hotkey("ctrl", "s")

# pywinauto - types into a SPECIFIC element (sets focus first)
doc.type_keys("Hello{ENTER}", with_spaces=True)
win.type_keys("^s")          # ^ Ctrl   + Shift   % Alt
win.type_keys("{TAB 3}")     # TAB three times
win.type_keys("{+}")         # a literal plus sign
```

| pywinauto | Key | pywinauto | Key |
|---|---|---|---|
| `^` | Ctrl | `{ENTER}` | Enter |
| `+` | Shift | `{ESC}` | Escape |
| `%` | Alt | `{F5}` | F5 |
| `{DELETE}` | Delete | `{VK_LWIN}` | Windows key |

<!-- Trainer notes:
Classic bug: type_keys("a+b") types "aB" because + means Shift. Escape it: "a{+}b".
Also: spaces are ignored unless with_spaces=True.
Run example 05 with --type ONLY into an empty editor window the trainer opens.
-->

---

# Image-based automation

```python
import pyautogui
try:
    box = pyautogui.locateOnScreen("images/calc_seven.png", confidence=0.8)
    if box:                                   # older versions return None
        pyautogui.click(pyautogui.center(box))
except pyautogui.ImageNotFoundException:      # newer versions raise
    print("Image not found - is the window visible? same theme/scaling?")
```

- `confidence=` needs **opencv-python**
- Crop the reference image **tightly**; capture at the **same scaling/theme**
- Window must be **visible and on top**
- Use a retry loop with a timeout

`examples/06_image_based_click.py` (`--capture` creates the reference image)

<!-- Trainer notes:
Run example 06 --capture then example 06. Then switch Windows to dark mode (or resize) and run again -> fails -> shows fragility.
Hybrid point: the script clicks by image but VERIFIES the display using pywinauto.
Common question: "Can pyautogui read text?" - No; you'd need OCR (pytesseract), which is slow and error-prone.
-->

---

# Hybrid: pywinauto finds, pyautogui acts

```python
win = Desktop(backend="win32").window(title="Day2 Mouse Playground").wrapper_object()
win.set_focus()
sx, sy = win32gui.ClientToScreen(win.handle, (80, 230))    # source, window-relative
tx, ty = win32gui.ClientToScreen(win.handle, (575, 230))   # target

pyautogui.moveTo(sx, sy, duration=0.3)
pyautogui.dragTo(tx, ty, duration=1.0)      # drag and drop
pyautogui.rightClick(x, y); pyautogui.press("down"); pyautogui.press("enter")
pyautogui.scroll(-3 * 120)                  # Windows: 120 = one wheel notch
```

- Use this for drag and drop, hover, context menus, scrolling, and apps with no UIA tree (Electron, canvas, Citrix)
- Use **window-relative** offsets, never fixed screen points
- Check the result with an **oracle** (app state, file, pywinauto), not with your eyes

`examples/12_mouse_keyboard_hybrid.py` drives `examples/apps/mouse_playground.py`

<!-- Trainer notes:
Run apps/mouse_playground.py by hand first so trainees see every target. Then run example 12 (8 checks, about 20 s, hands off the mouse).
Run it with --where and hover the targets to show how offsets are measured in any app.
Gotchas to point out in the code: dragTo needs duration > 0; scroll(-5) does nothing on Windows (raw units, 120 per notch); release mouseUp()/keyUp() in finally; is_active() check before typing.
Why win32gui.ClientToScreen and not pywinauto's client_to_screen(): the latter adds the offset to the OUTER window rectangle (title bar included).
-->

---

# Real Electron app: Notion desktop

| Step | Tool |
|---|---|
| Find the window (`Chrome_WidgetWin_1`, owned by `Notion.exe`) | pywinauto |
| Which page is open? `window_text()` = page title | pywinauto |
| `Ctrl+N`, type, `/todo`, `Ctrl+Shift+Up` | pyautogui keys |
| Hover a block → drag handle → drag and drop | pyautogui mouse |
| Verify: select all, `Ctrl+C`, read the **clipboard** | pywin32 |

- **Safety gate:** check that the window title shows a *new empty page* before typing anything
- Trash only a page whose title is **ours**; restore the user's clipboard

`examples/13_notion_electron_hybrid.py` (`--inspect` dumps the UIA tree, `--keep` keeps the page)

<!-- Trainer notes:
Needs Notion desktop installed and signed in on the presenting machine (a free account is enough). Rehearse it: Notion changes its UI often.
Show example 01 output first: Notion, VS Code and Teams all have class Chrome_WidgetWin_1, which is how you spot an Electron app.
Point out the fallback: if Chromium exposes no page elements there are no positions for a drag, so the script moves the block with Ctrl+Shift+Up. Real frameworks need a plan B like this for web-based desktop apps.
If a step fails, run --inspect and search notion_tree.txt for the "..." button and the "Move to trash" item, then update MORE_BUTTON_RE / TRASH_ITEM_RE.
-->

---

# Handling focus

- Keyboard input goes **only** to the focused window
- `set_focus()` brings a window to the front and focuses it
- Check: `is_active()`, `has_keyboard_focus()`

```python
calc.set_focus()
print(calc.is_active())        # True
notepad.set_focus()
print(calc.is_active())        # False
```

Tips:
- Prefer `invoke()` / element methods - they don't need focus
- Call `set_focus()` right **before** `type_keys()`
- Don't touch the mouse/keyboard while a GUI test runs!

<!-- Trainer notes:
Windows has "focus stealing prevention": sometimes set_focus only flashes the taskbar. pywinauto uses tricks to work around it, but a user clicking around during a run will break tests.
Mention: GUI tests need a dedicated machine/VM or an unlocked session.
-->

---

# Handling windows & waits

```python
spec = Desktop(backend="uia").window(title="Calculator")
spec.exists(timeout=5)              # True/False - never raises
spec.wait("visible", timeout=10)    # raises TimeoutError if not in time
spec.wait("ready")                  # visible + enabled
spec.wait_not("visible", timeout=5) # wait until it disappears

Desktop(backend="uia").windows()    # list all top-level windows
win.is_minimized(); win.restore(); win.maximize()
```

| Wait criteria | Meaning |
|---|---|
| `exists` | in the UIA tree |
| `visible` | shown on screen |
| `enabled` | not greyed |
| `ready` | visible + enabled |
| `active` | foreground window |

<!-- Trainer notes:
Stress: time.sleep(5) is either too long (slow suite) or too short (flaky test). Explicit waits are both fast and reliable.
Global default: from pywinauto.timings import Timings; Timings.window_find_timeout = 10.
-->

---

# Handling dialogs

Dialogs = separate (often **modal**) windows that block the owner.

```python
notepad.type_keys("^+s")                         # open "Save as"
dlg = notepad.child_window(title_re="(?i)^save as$", control_type="Window")
if dlg.exists(timeout=5):
    dlg.child_window(title="Cancel", control_type="Button").invoke()
    dlg.wait_not("visible", timeout=5)
```

- Modern apps: dialog is often a **child** of the main window in the UIA tree
- Classic apps: separate top-level window, class `#32770`
- Unexpected dialogs (update, crash, "save changes?") -> check & handle, or fail clearly

`examples/07_handle_dialogs_focus.py`

<!-- Trainer notes:
Run example 07: focus switching between Calculator and our Notepad temp file, then Save-as dialog opened and cancelled (harmless), then a ghost-window wait that times out.
Common question: "What about the 'Do you want to save?' prompt?" - avoid it by saving before closing; if it appears, click "Don't save" only for YOUR temp file.
-->

---

# Clean-up: leave the desktop as you found it

```python
calc = open_calculator()
try:
    run_tests(calc)
finally:
    calc.close()          # runs even if a test failed
```

- Close only what **you** opened
- Delete temp files
- Never kill processes by name blindly (`taskkill /IM notepad.exe` = user's work gone)
- In pytest (Day 4): fixtures with `yield` do the same

<!-- Trainer notes:
Connect back to Day 1 try/finally. Next days will use pytest fixtures for set-up/tear-down.
-->

---

# Lab 1: Automating Calculator (45 min)

`hands_on/Lab_Guide.md` - Lab 1, starter: `hands_on/starter/lab1_calculator_test.py`

- Map keys to AutomationIds
- Implement `open_calculator`, `click_button`, `get_display`, `calculate`
- Verify 5+ operations; print PASS/FAIL; exit code 0/1

Stretch: `calc_seven.png` image-based click; read the History panel

<!-- Trainer notes:
Walk around. Typical problems: forgetting control_type -> ambiguous; using Application().start; not stripping "Display is"; Calculator in Scientific mode (auto_ids are the same, so fine) or Programmer mode (different).
Solution: hands_on/solutions/lab1_calculator_test.py
-->

---

# Lab 2: Safe Notepad automation (30 min)

Starter: `hands_on/starter/lab2_notepad_safe.py`

- Create a temp file, open it, connect by **its** title
- Type text slowly, verify on screen
- Save (Ctrl+S), close **only** your tab (Ctrl+W)
- Verify the file content **from disk**, delete the file

> Golden rule: **never `win.close()` on Notepad**

<!-- Trainer notes:
Before the lab, ask everyone to save their own open Notepad tabs - belt and braces.
Common failure: title regex missing the optional '*' -> window "disappears" after typing. Another: forgetting with_spaces=True.
Solution: hands_on/solutions/lab2_notepad_safe.py (also has --text and --keep options).
-->

---

<!-- _class: lead -->
# Module 3
## Command-Line Automation

<!-- Trainer notes:
60 minutes theory + demos, then labs. Good energy boost after lunch - everything here runs instantly and never breaks the desktop.
-->

---

# What is a CLI and why automate it?

- **CLI** = command-line interface: text in, text out, exit code
- Tools: `cmd`, PowerShell, `ipconfig`, `ping`, `git`, `pip`, `pytest`, `adb`, `sqlcmd`
- Every CI server (Jenkins, Azure DevOps, GitHub Actions) runs **commands**

Tester use cases:
- Start/stop the app under test, install builds
- Prepare test data, reset databases, copy files
- Check the environment before a run
- Search logs for errors after a run
- Run test suites: `pytest -m smoke --html=report.html`

<!-- Trainer notes:
Key insight: a GUI test suite still needs CLI glue - launching, environment checks, log collection, CI integration.
Ask: "Who has used cmd or PowerShell at work?" Show a couple of commands live: ipconfig, where python.
-->

---

# Running Python scripts from the command line

```powershell
PS> python hello.py                  # run a script
PS> python -m pip list               # run a module
PS> python -c "print(2+3)"           # run a one-liner
PS> python --version
PS> cd C:\...\Day2_Desktop_and_CLI_Automation\examples
PS> python .\08_sys_argv_demo.py add 12 30
PS> echo $LASTEXITCODE               # exit code of the last command
```

- VS Code: **Terminal > New Terminal** (PowerShell by default)
- `if __name__ == "__main__":` - code that runs only when executed directly
- `sys.exit(code)` - 0 = success, non-zero = failure

<!-- Trainer notes:
cmd.exe equivalent of $LASTEXITCODE is %ERRORLEVEL%.
If "python" opens the Microsoft Store: App execution aliases setting, or use the "py" launcher.
Explain __name__ == "__main__" with a quick demo: import the module vs run it.
-->

---

# Exit codes = PASS/FAIL for machines

```python
import sys

def main() -> int:
    ok = run_checks()
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
```

| Code | Convention |
|------|-----------|
| 0 | Success |
| 1 | Test/check failed |
| 2 | Wrong usage (argparse uses 2) |
| other | Tool-specific errors |

CI marks the build **red** when a step returns non-zero.

<!-- Trainer notes:
pytest itself returns 0 (all passed), 1 (failures), 2 (interrupted), 5 (no tests collected) - nice real example.
-->

---

# Command-line arguments: sys.argv

```python
# 08_sys_argv_demo.py
import sys
print(sys.argv)
```

```powershell
PS> python 08_sys_argv_demo.py add 12 30
['08_sys_argv_demo.py', 'add', '12', '30']
PS> python 08_sys_argv_demo.py "hello world"
['08_sys_argv_demo.py', 'hello world']
```

- `sys.argv[0]` = script name, `sys.argv[1:]` = arguments
- Always **strings** -> convert: `int(sys.argv[2])`
- Quotes group words into **one** argument

<!-- Trainer notes:
Run example 08 with the listed variants, including "add 12 abc" to show manual error handling.
Ask: "What happens with python script.py add 12?" -> IndexError unless we check len(sys.argv).
-->

---

# sys.argv limitations

```python
if len(sys.argv) != 3:
    print("Usage: add <a> <b>"); sys.exit(2)
try:
    a, b = float(sys.argv[1]), float(sys.argv[2])
except ValueError:
    print("numbers please"); sys.exit(2)
```

- Manual length checks, type conversion, error messages
- No `--help`
- Optional flags (`--env qa`) must be parsed by hand
- Fine for 1-2 arguments; beyond that -> **argparse**

<!-- Trainer notes:
Show smoke --env qa parsing in example 08 - it works but is painful. Transition to argparse.
-->

---

# argparse basics

```python
import argparse
parser = argparse.ArgumentParser(description="Demo test runner")
parser.add_argument("app")                                    # positional
parser.add_argument("--env", choices=["dev", "qa", "uat"], default="dev")
parser.add_argument("-r", "--retries", type=int, default=1)
parser.add_argument("-v", "--verbose", action="store_true")   # flag
parser.add_argument("--tags", nargs="+", default=["smoke"])   # many values
args = parser.parse_args()
print(args.app, args.env, args.retries, args.verbose, args.tags)
```

```powershell
PS> python 09_argparse_demo.py Calculator --env qa -r 3 -v
PS> python 09_argparse_demo.py --help
```

<!-- Trainer notes:
Run example 09 with --help first - trainees love the free help page.
Then the error cases: --env prod (invalid choice), --retries three (invalid int), missing app. All exit with code 2.
Dashes: --min-free-gb becomes args.min_free_gb.
-->

---

# argparse features testers use most

| Need | Code |
|------|------|
| Required positional | `add_argument("file")` |
| Optional with default | `add_argument("--env", default="dev")` |
| Required option | `add_argument("--file", required=True)` |
| Type conversion | `type=int`, `type=float`, `type=Path` |
| Allowed values | `choices=["dev", "qa"]` |
| Boolean flag | `action="store_true"` |
| Several values | `nargs="+"` / `nargs="*"` |
| Short + long | `add_argument("-v", "--verbose")` |
| Custom validation | `parser.error("message")` -> exit 2 |
| Testable parsing | `parser.parse_args(["Calculator", "--env", "qa"])` |

<!-- Trainer notes:
parse_args(list) is great for unit tests - no need to fake sys.argv.
type=str.upper makes choices case-insensitive (used in the log analyzer lab).
-->

---

# Sub-commands (like git)

```python
parser = argparse.ArgumentParser(prog="testkit")
sub = parser.add_subparsers(dest="command", required=True)

p = sub.add_parser("disk", help="show free disk space")
p.add_argument("--min-free-gb", type=float)
p.set_defaults(func=cmd_disk)

p = sub.add_parser("search", help="search text in files")
p.add_argument("pattern"); p.add_argument("files", nargs="+")
p.set_defaults(func=cmd_search)

args = parser.parse_args()
sys.exit(args.func(args))       # dispatch
```

```powershell
PS> python 11_reusable_cli_utility.py search ERROR ..\hands_on\starter\app.log
```

<!-- Trainer notes:
Show python 11_reusable_cli_utility.py --help and search --help: each sub-command has its own help.
-->

---

# Writing reusable utility scripts

1. **Logic in functions** that return data (no print, no exit)
2. **Thin `main()`**: parse args -> call functions -> print -> return exit code
3. `if __name__ == "__main__":` guard -> importable from other scripts/pytest
4. **Meaningful exit codes** (0 ok, 1 failed check, 2 usage, 3 file error)
5. Good `--help`, sensible defaults, **no hard-coded paths**
6. Errors to `sys.stderr`, results to `stdout`
7. Handle expected errors (missing file, bad regex) with clear messages

`examples/11_reusable_cli_utility.py` - sysinfo, disk, search, which

<!-- Trainer notes:
Demo: from another Python shell, `import importlib; m = importlib.import_module("11_reusable_cli_utility")` is awkward because of the leading digits - mention that reusable modules should have import-friendly names (testkit.py). The labs use proper names (log_analyzer.py).
Run: which python notepad.exe nosuchtool ; echo $LASTEXITCODE -> 1.
-->

---

# Automating system commands: subprocess.run

```python
import subprocess, sys

result = subprocess.run(
    [sys.executable, "--version"],   # list form: no shell, no quoting issues
    capture_output=True,             # collect stdout/stderr
    text=True,                       # str instead of bytes
    timeout=30,                      # never hang forever
)
print(result.returncode)             # 0
print(result.stdout)                 # Python 3.14.x
```

- `check=True` -> raises `CalledProcessError` on non-zero exit
- `TimeoutExpired`, `FileNotFoundError` -> catch them
- cmd built-ins need `["cmd", "/c", "dir"]` (or `shell=True`)

<!-- Trainer notes:
Run examples/10_subprocess_demo.py - sections 1 to 8.
Security: shell=True with user input = command injection. Prefer the list form.
-->

---

# subprocess: common tester recipes

```python
# Is a tool installed?
subprocess.run(["where", "git"], capture_output=True).returncode == 0

# Parse output
out = subprocess.run(["ipconfig"], capture_output=True, text=True).stdout
ips = [l.split(":")[1].strip() for l in out.splitlines() if "IPv4" in l]

# Start an app without waiting (GUI apps!)
proc = subprocess.Popen("calc.exe")

# Run the test suite and gate on the result
rc = subprocess.run(["pytest", "-q", "tests"]).returncode
sys.exit(rc)
```

<!-- Trainer notes:
run() waits; Popen() does not - that's why we launch GUI apps with Popen.
Tie back: our pywinauto scripts use subprocess.Popen("calc.exe").
-->

---

# The os module (and friends)

```python
import os, shutil, platform
os.getcwd()                          # current folder
os.listdir(".")                      # files in a folder
os.environ.get("USERNAME")           # environment variables
os.path.join("logs", "app.log")      # build paths (or pathlib.Path)
os.makedirs("reports", exist_ok=True)
os.system("cls")                     # runs a command, returns exit code only
shutil.which("python")               # full path of a tool or None
shutil.disk_usage("C:\\")            # total / used / free
platform.system(), platform.release()
```

- `os.system` cannot capture output -> prefer `subprocess.run`

<!-- Trainer notes:
Section 10 of example 10. pathlib is the modern alternative for paths - show Path("logs") / "app.log".
-->

---

# Lab 3: CLI utility with argparse (30 min)

Starter: `hands_on/starter/log_analyzer.py` + sample `app.log`

```powershell
PS> python log_analyzer.py --file app.log --level ERROR
PS> python log_analyzer.py --file app.log --level ERROR --count
4
PS> python log_analyzer.py --file app.log --summary
```

Stretch: `--contains timeout -i`, `--level WARNING --min`, `--fail-on ERROR` (exit 1)

<!-- Trainer notes:
The log has 28 lines: DEBUG 4, INFO 15, WARNING 4, ERROR 4, CRITICAL 1 - use these numbers to check trainee output.
Solution: hands_on/solutions/log_analyzer.py
-->

---

# Lab 4: Passing arguments to a GUI script (25 min)

Starter: `hands_on/starter/calc_cli.py`

```powershell
PS> python calc_cli.py 12 + 30
12 + 30: expected='42' actual='42' -> PASS
PS> python calc_cli.py 9 x 6
PS> python calc_cli.py 12 + 30 --expected 43 ; echo $LASTEXITCODE
12 + 30: expected='43' actual='42' -> FAIL
1
```

CLI + GUI together: argparse -> oracle in Python -> Calculator -> PASS/FAIL + exit code

Lab 5 (extra): `env_check.py` - environment pre-check with subprocess

<!-- Trainer notes:
'*' works in PowerShell/cmd but Git Bash expands it - that's why 'x' is accepted.
Nice discussion: the Python calculation is the TEST ORACLE; Calculator is the system under test.
Solutions: hands_on/solutions/calc_cli.py, env_check.py
-->

---

# Putting it all together

```
 CI server (Jenkins / Azure DevOps)
      |  python env_check.py            <- subprocess, exit codes
      |  python calc_cli.py 12 + 30     <- argparse + pywinauto
      |  python log_analyzer.py --file app.log --fail-on ERROR
      v
  green build  /  red build
```

- GUI automation drives the app
- CLI automation glues everything into a repeatable pipeline

<!-- Trainer notes:
This is the big picture for the rest of the week: later days build frameworks, test suites and reports - all started from the command line.
-->

---

# Best practices - Day 2 summary

- Inspect first (Accessibility Insights / `print_control_identifiers`)
- `backend="uia"` for modern apps; `win32` for legacy
- Locators: **auto_id > title + control_type > index**
- Explicit waits, never blind `sleep`
- **Own your test data**; never assume a clean app state
- Verify via the UI **and** the real outcome (file on disk)
- Clean up in `finally`, close only what you opened
- Element-based first, image-based as fallback
- CLI scripts: argparse, functions, exit codes, `--help`

<!-- Trainer notes:
Ask trainees to pick the ONE rule they consider most important and say why - good discussion starter.
-->

---

# Recap: objectives check

- [x] Processes, windows, message loop, UIA tree
- [x] Win32 / WPF / Electron / UWP-WinUI and backends
- [x] Elements, states, inspection tools
- [x] Element-based vs image-based, mouse & keyboard
- [x] Focus, windows, dialogs
- [x] CLI: running scripts, sys.argv, argparse, subprocess, os, reusable utilities

Quiz: `03_Quiz.md` (20 questions, 15 minutes)

<!-- Trainer notes:
Run the quiz (paper or read aloud with show of hands). Discuss the most-missed questions.
Homework: read 02_Reading_Material.md sections 6-9, finish stretch goals.
-->

---

# Common interview questions (preview)

- Difference between `win32` and `uia` backends?
- Element-based vs image-based - when would you use each?
- `invoke()` vs `click_input()`?
- How do you handle a window that takes long to appear?
- Why is `time.sleep()` bad in automation?
- `subprocess.run` vs `Popen` vs `os.system`?
- `sys.argv` vs `argparse`?

Full list with answers: `02_Reading_Material.md` section 12

<!-- Trainer notes:
Pick 2-3 and ask random trainees - quick oral practice.
-->

---

# Q&A

**Questions?**

Tomorrow (Day 3): file handling, Linux & system automation - more subprocess, os and CLI tools. Day 4 turns scripts like today's into a pytest framework.

<!-- Trainer notes:
Collect feedback (1-5) on pace. Remind everyone to close any Calculator windows and delete leftover temp files (%TEMP%\day2_*.txt, lab2_*.txt) - though scripts clean up after themselves.
-->
