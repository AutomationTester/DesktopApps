# Day 2 - Hands-on Lab Guide

| Lab | Topic | Syllabus item | Time | Starter | Solution |
|---|---|---|---|---|---|
| 0 | Inspect Calculator | Object inspection tools | 10 min | - | - |
| 1 | Automating Calculator | Automating Notepad / Calculator | 45 min | `starter/lab1_calculator_test.py` | `solutions/lab1_calculator_test.py` |
| 2 | Safe Notepad automation | Automating Notepad / Calculator | 30 min | `starter/lab2_notepad_safe.py` | `solutions/lab2_notepad_safe.py` |
| 3 | Log analyzer CLI | Writing reusable CLI utilities | 30 min | `starter/log_analyzer.py` + `starter/app.log` | `solutions/log_analyzer.py` |
| 4 | Calculator from the command line | Passing arguments to Python scripts | 25 min | `starter/calc_cli.py` | `solutions/calc_cli.py` |
| 5 (extra) | Environment pre-check | Automating system commands | 20 min | `starter/env_check.py` | `solutions/env_check.py` |

**General setup**

```powershell
PS> cd C:\Users\<you>\Documents\Training_Materials\DesktopApps\Day2_Desktop_and_CLI_Automation\hands_on\starter
PS> python --version
PS> python -c "import pywinauto, pyautogui, cv2; print('ok')"
```

**Rules for GUI labs**
- Save and close your own Notepad documents before Lab 2 (belt and braces - the lab never touches them if done correctly).
- Do not touch the mouse or keyboard while a GUI script is running.
- If a script runs wild: move the mouse into a screen corner (pyautogui fail-safe) or press Ctrl+C in the terminal.

---

## Lab 0 - Inspect Calculator (10 min)

**Objective:** find the locators you need for Lab 1 using inspection tools.

**Steps**
1. Open Calculator (Start > Calculator). Make sure it is in **Standard** mode.
2. Open **Accessibility Insights for Windows** (or Inspect.exe) and switch to Live Inspect.
3. Hover over these elements and write down **Name**, **AutomationId**, **ControlType**:
   `7`, `+`, `=`, `C`, and the result display.
4. Note the **FrameworkId** of the Calculator window. What backend does it imply?
5. Run `python ..\..\examples\04_print_control_identifiers.py` and find the same elements in the output.

**Expected result**

| Element | AutomationId | ControlType |
|---|---|---|
| 7 | `num7Button` | Button |
| + | `plusButton` | Button |
| = | `equalButton` | Button |
| C | `clearButton` | Button |
| Display | `CalculatorResults` | Text |

FrameworkId is `XAML` -> Store app -> `backend="uia"`.

---

## Lab 1 - Automating Calculator (45 min)

**Objective:** write a data-driven test that drives Windows 11 Calculator with pywinauto and verifies the results of several operations.

**File:** `starter/lab1_calculator_test.py`

**Steps**
1. **TODO 1** - complete `BUTTON_IDS` for all digits and `+ - * / = C`.
2. **TODO 2** - add at least four more test cases: a subtraction with a negative result, a multiplication, a division with a decimal result (`10/4` -> `2.5`) and a result of 1000 or more (`999+1`).
3. **TODO 3-5** - `open_calculator()`: start `calc.exe` with `subprocess.Popen`, connect with `Desktop(backend="uia").window(title="Calculator")`, `wait("visible", timeout=10)`, `set_focus()`.
4. **TODO 6** - `click_button()`: `child_window(auto_id=..., control_type="Button").invoke()`.
5. **TODO 7** - `get_display()`: read `CalculatorResults`, remove `"Display is"` and thousands separators.
6. **TODO 8** - `calculate()`: press `C`, each key, then `=`, return the display.
7. **TODO 9-10** - count passes, print PASS/FAIL lines, close Calculator in `finally`.
8. Run: `python lab1_calculator_test.py`, then `echo $LASTEXITCODE`.

**Expected output**

```
[PASS] 2+3      = 5        (expected 5)
[PASS] 7*8      = 56       (expected 56)
[PASS] 15-20    = -5       (expected -5)
[PASS] 144/12   = 12       (expected 12)
[PASS] 10/4     = 2.5      (expected 2.5)
[PASS] 999+1    = 1000     (expected 1000)

Result: 6/6 passed
```
Exit code `0`. Change one expected value to see a FAIL and exit code `1`.

**Hints**
- `Application(backend="uia").start("calc.exe")` will NOT work: `calc.exe` is a launcher that exits.
- `ElementAmbiguousError`? Add `control_type="Button"`.
- The display text is like `Display is 1,000` - strip `"Display is"` and `","`.
- Always press `C` first - never assume Calculator starts at 0.
- If Calculator opens in Scientific mode the IDs are the same; in Programmer/Date mode switch back to Standard.

**Stretch goals**
- Turn `BUTTON_IDS` + functions into a `CalculatorPage` class (page-object style - Day 1 OOP!).
- Image-based: run `python ..\..\examples\06_image_based_click.py --capture`, then click `7` via `pyautogui.locateOnScreen(..., confidence=0.8)` and verify the display with pywinauto (hybrid approach).
- Read the test cases from a CSV file.
- Test chained operations (`2+3*4=`) - what does Standard mode return? (Standard mode evaluates left to right: `20`.)

---

## Lab 2 - Safe Notepad automation (30 min)

**Objective:** write text into Notepad, save it and verify the file content on disk **without ever touching the user's other Notepad tabs**.

> **Why so careful?** Windows 11 Notepad restores the user's previous tabs (even unsaved ones) and opens each new file as a tab in the same window. A script that types into "the Notepad window" or calls `win.close()` can destroy real work. **Never assume a clean application state.**

**File:** `starter/lab2_notepad_safe.py`

**Steps**
1. **TODO 1** - create a unique temp file with `tempfile.mkstemp(prefix="lab2_", suffix=".txt")`; close the descriptor with `os.close()`.
2. **TODO 2** - open it: `subprocess.Popen(["notepad.exe", str(path)])`.
3. **TODO 3** - connect with a title regex matching only your file:
   `Desktop(backend="uia").window(title_re=rf"\*?{re.escape(path.name)} - Notepad")`
   (the title gets a leading `*` as soon as the text is modified).
4. **TODO 4** - `wait("visible", timeout=15)`; editor = `child_window(control_type="Document")`.
5. **TODO 5** - `doc.set_focus()` then `doc.type_keys(TEXT, with_spaces=True, pause=0.05)`.
   (`set_edit_text()` is NOT supported by the Win11 Notepad editor.)
6. **TODO 6** - verify `doc.window_text()` equals `TEXT`.
7. **TODO 7** - save with `win.type_keys("^s")` (no dialog, the file exists), wait about 1 s.
8. **TODO 8** - close ONLY your tab with `win.type_keys("^w")`. **Never `win.close()`.**
9. **TODO 9** - read the file (`encoding="utf-8-sig"`) and compare - print `[PASS]`/`[FAIL]`, return 0/1.
10. **TODO 10** - delete the temp file in `finally`.

**Expected output**

```
Working file: C:\Users\<you>\AppData\Local\Temp\lab2_abc123.txt
Connected   : lab2_abc123.txt - Notepad
Editor text : 'Automated by pywinauto on Day 2. Test ID NP-001.'
Disk text   : 'Automated by pywinauto on Day 2. Test ID NP-001.'
[PASS] File on disk contains the typed text
```
Your other Notepad tabs are untouched.

**Hints**
- Window "disappears" right after typing? Your regex misses the optional `*`.
- Spaces missing? `with_spaces=True`.
- Characters missing? Increase `pause`. Always verify with `doc.window_text()`.
- `+ ^ % ~ ( ) { }` are special in `type_keys` - escape as `{+}` etc. or avoid them.

**Stretch goals**
- Add `--text` and `--keep` options with argparse (see the solution).
- Retry typing once if the verification fails (clear with `^a{DELETE}` - safe, because it is your own file).
- Wait until the `*` disappears from the title instead of sleeping after Ctrl+S.
- Open Notepad's Save-as dialog (`^+s`) on your file, detect it and cancel it (see `examples/07_handle_dialogs_focus.py`).

---

## Lab 3 - Reusable CLI utility: log analyzer (30 min)

**Objective:** build `log_analyzer.py`, a command-line tool with argparse that filters and summarises an application log.

**Files:** `starter/log_analyzer.py`, sample log `starter/app.log` (28 lines).

Log format:
```
2026-09-21 09:00:15,102 ERROR [InvoiceModule] Validation failed: field 'GSTIN' is empty
```

**Steps**
1. **TODO 1** - `read_entries()`: open the file, `parse_line()` each line, keep non-`None` results.
2. **TODO 2** - `filter_entries()`: keep entries of the requested level.
3. **TODO 3-6** - arguments: `-f/--file` (required, `type=Path`), `-l/--level` (`type=str.upper`, `choices=LEVELS`), `-c/--count`, `-s/--summary`.
4. **TODO 7** - missing file -> message to `sys.stderr`, return 3.
5. **TODO 8-9** - output: summary per level, only the count, or the matching lines.
6. Test all commands below and check the exit codes with `echo $LASTEXITCODE`.

**Expected output**

```powershell
PS> python log_analyzer.py --file app.log --level ERROR
2026-09-21 09:00:15,102 ERROR    [InvoiceModule] Validation failed: field 'GSTIN' is empty
2026-09-21 09:00:30,012 ERROR    [PaymentService] Timeout while contacting gateway after 30 s
2026-09-21 09:00:41,998 ERROR    [ReportModule] NullReferenceException in ReportBuilder.Render()
2026-09-21 09:01:14,093 ERROR    [ExportModule] Access denied: C:\Exports\invoices.xlsx is locked by another process

PS> python log_analyzer.py --file app.log --level error --count
4

PS> python log_analyzer.py --file app.log --summary
Summary for app.log (28 lines)
  DEBUG        4
  INFO        15
  WARNING      4
  ERROR        4
  CRITICAL     1

PS> python log_analyzer.py --file missing.log ; echo $LASTEXITCODE
ERROR: log file not found: missing.log
3

PS> python log_analyzer.py --file app.log --level FATAL ; echo $LASTEXITCODE
usage: log_analyzer ...
log_analyzer: error: argument -l/--level: invalid choice: 'FATAL' (choose from ...)
2
```

**Hints**
- `type=str.upper` runs before `choices`, so `--level error` is accepted.
- `collections.Counter(e["level"] for e in entries)` builds the summary in one line.
- Test parsing without the shell: `main(["--file", "app.log", "--count"])`.

**Stretch goals**
- `--contains TEXT` with `-i/--ignore-case` (`--contains timeout -i` -> 1 line).
- `--min` together with `--level WARNING` -> WARNING and above (9 lines).
- `--fail-on ERROR` -> exit code 1 if any ERROR/CRITICAL line exists (a CI quality gate).
- `--component PaymentService` filter; `--since 09:01:00` time filter.
- Write a pytest file that calls `filter_entries()` directly (reusability!).

---

## Lab 4 - Passing arguments to the Calculator script (25 min)

**Objective:** combine CLI and GUI automation: `python calc_cli.py 12 + 30` validates the arguments, computes the expected result in Python (the test **oracle**), drives Calculator, and prints PASS/FAIL with a matching exit code.

> **Git Bash gotcha:** Git Bash rewrites a lone `/` argument into a Windows path (`C:/Program Files/Git/`), so `python calc_cli.py 10 / 4` fails with "invalid choice". Run this lab in **PowerShell or cmd**, or in Git Bash prefix the command: `MSYS_NO_PATHCONV=1 python calc_cli.py 10 / 4`.

**File:** `starter/calc_cli.py` (reuse your Lab 1 code!)

**Steps**
1. **TODO 1-4** - argparse: positionals `a` (int), `op` (`choices=list(OPERATORS)`), `b` (int); optional `--expected`.
2. **TODO 5** - `expected_result()`: `12 + 30` -> `'42'`; `10 / 4` -> `'2.5'` (print whole numbers without `.0`).
3. **TODO 6-9** - `run_in_calculator()`: launch/connect, press `C`, digits of `a`, operator, digits of `b`, `=`, read and clean the display, close.
4. **TODO 10** - compare, print one result line, return 0 (PASS) or 1 (FAIL).

**Expected output**

```powershell
PS> python calc_cli.py 12 + 30
12 + 30: expected='42' actual='42' -> PASS
PS> python calc_cli.py 9 x 6
9 x 6: expected='54' actual='54' -> PASS
PS> python calc_cli.py 10 / 4
10 / 4: expected='2.5' actual='2.5' -> PASS
PS> python calc_cli.py 12 + 30 --expected 43 ; echo $LASTEXITCODE
12 + 30: expected='43' actual='42' -> FAIL
1
PS> python calc_cli.py 12 % 3 ; echo $LASTEXITCODE
calc_cli: error: argument op: invalid choice: '%' (choose from '+', '-', '*', 'x', '/')
2
```

**Hints**
- `*` works in PowerShell and cmd, but Git Bash expands it to file names - that is why `x` is accepted too.
- Digits of a number: `for d in str(a): press(f"num{d}Button")`.
- Compare numbers with a tolerance for long decimals: `abs(float(e) - float(a)) < 1e-9`.

**Stretch goals**
- Reject negative numbers and decimals with a custom `type=` function (`argparse.ArgumentTypeError`).
- `7 / 0` -> Calculator shows `Cannot divide by zero`; make that the expected value.
- `--keep-open` flag to leave Calculator open for debugging.
- Run a batch: a PowerShell loop calling `calc_cli.py` for several expressions and counting failures from `$LASTEXITCODE`.

---

## Lab 5 (extra) - Environment pre-check with subprocess (20 min)

**Objective:** write `env_check.py`, a pre-test check a CI job can run before GUI tests.

**File:** `starter/env_check.py`

**Steps**
1. **TODO 1** - `run()`: `subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)`.
2. **TODO 2** - `check_python()`: parse `python --version`, compare `(major, minor)` tuples with `--min-python`.
3. **TODO 3** - `check_tool()`: `where <tool>`; return code 0 -> found (first line = path).
4. **TODO 4** - build `[PASS]`/`[FAIL]` lines for Python and every tool; track overall status.
5. **TODO 6** - print the report with `OVERALL: PASS/FAIL`; write it to `--report` if given; exit 0/1.

**Expected output**

```powershell
PS> python env_check.py
Environment check - 2026-09-26 16:48:46
[PASS] python version         Python 3.14.7 (need >= 3.10)
[PASS] tool: python           C:\...\python.exe
[PASS] tool: notepad.exe      C:\Windows\System32\notepad.exe
[PASS] tool: calc.exe         C:\Windows\System32\calc.exe
[PASS] package: pywinauto     importable
[PASS] package: pyautogui     importable
[INFO] IPv4 addresses         192.168.1.103
OVERALL: PASS

PS> python env_check.py --tools git nosuchtool ; echo $LASTEXITCODE
...
[FAIL] tool: nosuchtool       not found on PATH
OVERALL: FAIL
1
```

**Hints**
- `where` returns exit code 1 when nothing is found.
- `sys.executable` is the Python running your script - use it instead of `"python"`.
- Packages: `subprocess.run([sys.executable, "-c", "import pywinauto"])` - return code 0 means installed.

**Stretch goals**
- Add a free-disk-space check (`shutil.disk_usage`).
- Collect `ipconfig` IPv4 addresses into the report as evidence.
- Add `--json` output for machines.

---

## Wrap-up checklist

- [ ] I can find an element's AutomationId with an inspection tool
- [ ] I automated Calculator and verified results (Lab 1)
- [ ] I automated Notepad without touching any other tab (Lab 2)
- [ ] I built a CLI tool with argparse, `--help` and exit codes (Lab 3)
- [ ] I passed arguments from the command line into a GUI test (Lab 4)
- [ ] I ran system commands with subprocess and checked return codes (Lab 5)
