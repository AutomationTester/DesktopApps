# Quiz - 15 MCQ Questions

15 randomly selected multiple-choice questions. Choose **one** answer per question.
Answer key with explanations on the last page.

---

**1. Given `results = ["PASS", "FAIL", "SKIP"]`, what is `results[-1]`?**
- A) `"PASS"`
- B) `"FAIL"`
- C) `"SKIP"`
- D) `IndexError`

**2. What does `self` refer to inside an instance method?**
- A) The class itself
- B) The current object
- C) The parent class
- D) The Python interpreter

**3. What is the purpose of `super().__init__(title)` inside a child class constructor?**
- A) It creates a second, separate object
- B) It runs the parent class constructor, so the parent's attributes are set up
- C) It deletes the parent class
- D) It makes all attributes private

**4. In `try / except / else / finally`, which block ALWAYS runs, whether an error happened or not?**
- A) `try`
- B) `except`
- C) `else`
- D) `finally`

**5. Which statement about the message loop is TRUE?**
- A) Keyboard input is delivered to every open window
- B) Keyboard input is delivered to the focused window
- C) The message loop only exists in web browsers
- D) A busy application processes messages faster

**6. Why does `Application(backend="uia").start("calc.exe")` followed by `app.window(title="Calculator")` fail on Windows 11?**
- A) Calculator has no window title
- B) `calc.exe` is a launcher that starts another process and exits
- C) pywinauto cannot start any program
- D) Calculator requires administrator rights

**7. The `confidence=` parameter of `pyautogui.locateOnScreen()` requires which package?**
- A) numpy only
- B) opencv-python
- C) pywinauto
- D) pytesseract

**8.** What will `yaml.safe_load("zip: 01234")` most likely give for `zip`?

- A) `"01234"`
- B) `1234`
- C) `668` (interpreted as an octal number)
- D) A `YAMLError`

**9.** In the data-driven Calculator example, what is the main benefit of the `MockCalculator` + `--dry-run` design?

- A) It makes the GUI faster
- B) Data loading, comparison and reporting can be tested anywhere without launching the GUI
- C) It removes the need for test data
- D) It lets pywinauto work on Linux

**10.** How do you activate a venv named `.venv` in **Windows PowerShell**?

- A) `source .venv/bin/activate`
- B) `.venv\Scripts\Activate.ps1`
- C) `activate .venv`
- D) `pip activate .venv`

**11. Which of these is the correct order of Python log levels, from lowest to highest severity?**
- A) INFO < DEBUG < WARNING < ERROR < CRITICAL
- B) DEBUG < INFO < WARNING < ERROR < CRITICAL
- C) DEBUG < WARNING < INFO < ERROR < CRITICAL
- D) TRACE < DEBUG < INFO < ERROR < FATAL

**12.** Which statement about jobs and steps is TRUE?

- A) All steps of a workflow share one machine, even across jobs
- B) Jobs run in parallel by default; steps within a job run in order on the same runner
- C) Steps run in parallel; jobs always run in sequence
- D) A job can only contain one step

**13.** Why is `if: always()` added to the `actions/upload-artifact` step?

- A) To upload the report even when the test step failed
- B) To make the upload faster
- C) To retry the upload 3 times
- D) It is required syntax for every `uses:` step

**14.** Which trigger adds a "Run workflow" button (with optional inputs) to the Actions tab?

- A) `push`
- B) `schedule`
- C) `repository_dispatch`
- D) `workflow_dispatch`

**15.** Your suite has CLI tests and Windows 11 Calculator/Notepad (pywinauto) tests. Which CI setup is most appropriate?

- A) Everything on `ubuntu-latest`
- B) Everything on GitHub-hosted `windows-latest`
- C) CLI tests on an ubuntu + windows matrix; desktop tests on a self-hosted Windows 10/11 runner with an interactive logged-in session
- D) Desktop tests on `ubuntu-latest` using Xvfb

---

## Answer Key

| # | Answer | Explanation |
|---|--------|-------------|
| 1 | **C** | A negative index counts from the end. `-1` is the last item. |
| 2 | **B** | `self` is the object the method was called on. Python passes it automatically. |
| 3 | **B** | Without it, parent attributes such as `self.title` are never created, which leads to an `AttributeError`. |
| 4 | **D** | `finally` always runs, which makes it the place for cleanup such as closing the application. |
| 5 | **B** | Keyboard messages go only to the focused window - that is why focus handling matters. A busy app stops processing messages ("Not Responding"). |
| 6 | **B** | `calc.exe` launches `CalculatorApp.exe` and exits, so pywinauto tracks a process without windows. Use `subprocess.Popen` + `Desktop(backend="uia").window(...)`. |
| 7 | **B** | Approximate matching with `confidence` is implemented with OpenCV (`opencv-python`). |
| 8 | **C** | PyYAML (YAML 1.1) treats a leading-zero number as octal: `01234` becomes `668`. Quote values like zip codes and IDs. |
| 9 | **B** | Both drivers share `calculate()`. The mock lets you validate data files, comparisons and reports quickly on any machine or headless CI. It does not make pywinauto work on Linux. |
| 10 | **B** | Windows venvs use the `Scripts` folder; PowerShell runs `Activate.ps1`. `source .venv/bin/activate` is Linux/macOS. |
| 11 | **B** | DEBUG(10) < INFO(20) < WARNING(30) < ERROR(40) < CRITICAL(50). |
| 12 | **B** | Each job gets its own fresh runner and jobs run in parallel unless `needs:` is used; steps run sequentially and share the job's file system. |
| 13 | **A** | By default a step is skipped after an earlier failure. `if: always()` forces the upload, so the report exists precisely when tests fail. |
| 14 | **D** | `workflow_dispatch` enables manual runs, optionally with inputs such as a `choice` of environment. |
| 15 | **C** | CLI tests run anywhere (a matrix catches OS differences). Hosted `windows-latest` is Windows Server without the Store Calculator/Win11 Notepad and without an interactive desktop, and Linux cannot run Windows apps at all. |
