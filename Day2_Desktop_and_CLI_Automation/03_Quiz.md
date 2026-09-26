# Day 2 Quiz - Desktop & Command-Line Automation

20 multiple-choice questions. Time: 15 minutes. Choose ONE answer per question.
Answer key with explanations at the end.

---

**1. On Windows, a running instance of a program with its own memory and a unique ID is called a:**
- A) Process
- B) Window
- C) Control
- D) Thread pool

**2. Which Microsoft framework exposes UI elements to screen readers AND to automation tools such as pywinauto (`backend="uia"`)?**
- A) DirectX
- B) COM+
- C) UI Automation
- D) WebDriver

**3. Which statement about the message loop is TRUE?**
- A) Keyboard input is delivered to every open window
- B) Keyboard input is delivered to the focused window
- C) The message loop only exists in web browsers
- D) A busy application processes messages faster

**4. Windows 11 Calculator and Notepad are best described as:**
- A) Classic Win32 applications
- B) Java Swing applications
- C) Store (UWP/WinUI) applications
- D) Electron applications

**5. Which pywinauto backend should you use for a WPF or Windows 11 Store app?**
- A) `win32`
- B) `uia`
- C) `wpf`
- D) `store`

**6. Which locator is generally the MOST stable for a desktop element?**
- A) `found_index=3`
- B) Best-match name such as `Button12`
- C) `auto_id` (AutomationId) combined with `control_type`
- D) Screen coordinates (x, y)

**7. Why does `Application(backend="uia").start("calc.exe")` followed by `app.window(title="Calculator")` fail on Windows 11?**
- A) Calculator has no window title
- B) `calc.exe` is a launcher that starts another process and exits
- C) pywinauto cannot start any program
- D) Calculator requires administrator rights

**8. What does the third line of each `print_control_identifiers()` entry give you?**
- A) The process ID
- B) The element's screenshot path
- C) The keyboard shortcut of the element
- D) A ready-to-use `child_window(...)` locator

**9. Which of the following is an advantage of IMAGE-based automation over element-based automation?**
- A) It is faster
- B) It is unaffected by theme and DPI changes
- C) It can automate applications that expose no accessibility information
- D) It can easily read the text and enabled state of controls

**10. `button.invoke()` differs from `button.click_input()` because `invoke()`:**
- A) Uses the UIA Invoke pattern and does not need the mouse
- B) Moves the real mouse pointer to the button
- C) Only works on Win32 applications
- D) Always opens a dialog

**11. You must type text into Windows 11 Notepad safely. Which approach is correct?**
- A) Open your own temp file, connect by its unique title, type, save with Ctrl+S, close only that tab with Ctrl+W
- B) Connect to any window whose title ends with "Notepad" and type
- C) Call `win.close()` first to get a clean Notepad, then start a new one
- D) Use `taskkill /IM notepad.exe` before each test

**12. In `type_keys("^s")`, the `^` character means:**
- A) Shift
- B) Alt
- C) Ctrl
- D) A literal caret

**13. What happens by default when `pyautogui.FAILSAFE` is True and you move the mouse into a screen corner?**
- A) The script pauses for 10 seconds
- B) The mouse is locked in the corner
- C) Nothing - FAILSAFE only affects the keyboard
- D) pyautogui raises `FailSafeException` and the script stops

**14. The `confidence=` parameter of `pyautogui.locateOnScreen()` requires which package?**
- A) numpy only
- B) opencv-python
- C) pywinauto
- D) pytesseract

**15. Which is the BEST way to wait for a window to appear?**
- A) `win.wait("visible", timeout=10)`
- B) `time.sleep(10)`
- C) A `while True:` loop with no timeout
- D) Ask the user to press Enter

**16. For `python tool.py add 12 30`, what is `sys.argv[2]`?**
- A) `12` (an int)
- B) `'12'` (a str)
- C) `'add'`
- D) `'tool.py'`

**17. Which argparse definition creates a boolean flag that is True only when `--verbose` is given?**
- A) `add_argument("--verbose", type=bool)`
- B) `add_argument("verbose")`
- C) `add_argument("--verbose", nargs="+")`
- D) `add_argument("--verbose", action="store_true")`

**18. What exit code does argparse use when the user passes an invalid argument?**
- A) 0
- B) 1
- C) 2
- D) -1

**19. Which call runs `ipconfig`, waits for it, and captures its output as text?**
- A) `os.system("ipconfig")`
- B) `subprocess.Popen("ipconfig")`
- C) `subprocess.run(["ipconfig"], capture_output=True, text=True)`
- D) `subprocess.call("ipconfig", output=True)`

**20. In `subprocess.run(cmd, check=True, timeout=5)`, what happens if the command returns exit code 1?**
- A) Nothing, `result.returncode` is 1
- B) `subprocess.TimeoutExpired` is raised
- C) `subprocess.CalledProcessError` is raised
- D) The command is retried automatically

---

## Answer key with explanations

| # | Answer | Explanation |
|---|---|---|
| 1 | **A** | A process is a running program instance with its own memory and a PID. Windows are owned by processes. |
| 2 | **C** | Microsoft UI Automation (UIA) is the accessibility framework; pywinauto's `uia` backend uses it. WebDriver is for browsers. |
| 3 | **B** | Keyboard messages go only to the focused window - that is why focus handling matters. A busy app stops processing messages ("Not Responding"). |
| 4 | **C** | On Windows 11 both are Store (UWP/WinUI) apps, so they need `backend="uia"`. |
| 5 | **B** | `win32` only sees classic HWND controls; WPF and Store apps require `uia`. There is no `wpf` or `store` backend. |
| 6 | **C** | AutomationIds are set by developers and do not change with language or layout. Indexes, best-match names and coordinates break easily. |
| 7 | **B** | `calc.exe` launches `CalculatorApp.exe` and exits, so pywinauto tracks a process without windows. Use `subprocess.Popen` + `Desktop(backend="uia").window(...)`. |
| 8 | **D** | Line 1: type, name, rectangle. Line 2: best-match names. Line 3: a `child_window(...)` locator you can copy into your script. |
| 9 | **C** | Image-based automation only needs pixels, so it works on apps without accessibility support (games, Citrix). It is slower, fragile to theme/DPI and cannot read states. |
| 10 | **A** | `invoke()` uses the UIA Invoke pattern (no mouse, works when partly covered); `click_input()` moves and clicks the real mouse. |
| 11 | **A** | Win11 Notepad restores the user's tabs and opens files in the same window. Work only on your own file and close only your tab. Options B, C and D can destroy the user's work. |
| 12 | **C** | In pywinauto `type_keys`: `^` = Ctrl, `+` = Shift, `%` = Alt. Use `{^}` for a literal caret. |
| 13 | **D** | FAILSAFE is an emergency brake: the next pyautogui call raises `FailSafeException`. |
| 14 | **B** | Approximate matching with `confidence` is implemented with OpenCV (`opencv-python`). |
| 15 | **A** | Explicit waits continue as soon as the condition is met and fail clearly after the timeout. Fixed sleeps are slow or flaky; infinite loops can hang forever. |
| 16 | **B** | `sys.argv` = `['tool.py', 'add', '12', '30']`; all items are strings, so `sys.argv[2]` is `'12'`. Convert with `int()`. |
| 17 | **D** | `action="store_true"` stores True when the flag is present, False otherwise. `type=bool` is a classic trap: `bool("False")` is True. |
| 18 | **C** | argparse prints the usage and exits with code 2 (conventional "usage error"). |
| 19 | **C** | `run` waits; `capture_output=True` collects stdout/stderr; `text=True` decodes to str. `os.system` cannot capture output; `Popen` alone does not wait or capture. |
| 20 | **C** | `check=True` turns a non-zero exit code into `CalledProcessError`. `TimeoutExpired` is only raised if the command runs longer than 5 s. |

**Scoring guide:** 18-20 excellent, 14-17 good, 10-13 revise sections 6-10 of the reading material, below 10 redo the labs with the trainer.
