# Day 1 - Trainee Handbook
## Python Fundamentals, OOP Concepts and Debugging for Automation Testers

**Course:** Python Desktop Application Automation Testing
**Audience:** Manual testers and freshers. No Python knowledge is needed.
**How to use this handbook:** Read each chapter, type the examples yourself, and do the "Try it yourself" tasks. All demo scripts mentioned here are in the `examples/` folder.

---

## Table of Contents

**Part A - Python Fundamentals for Automation**
1. [Introduction to Python and Automation Use Cases](#1-introduction-to-python-and-automation-use-cases)
2. [Desktop and CLI Automation Overview](#2-desktop-and-cli-automation-overview)
3. [Python Installation and IDE Setup (VS Code / PyCharm)](#3-python-installation-and-ide-setup-vs-code--pycharm)
4. [Python Syntax and Your First Program](#4-python-syntax-and-your-first-program)
5. [Variables and Data Types](#5-variables-and-data-types)
6. [Operators (Arithmetic, Comparison, Logical)](#6-operators-arithmetic-comparison-logical)
7. [Conditional Statements](#7-conditional-statements)
8. [Loops (for, while)](#8-loops-for-while)
9. [Functions and Reusability](#9-functions-and-reusability)

**Part B - OOP Concepts Using Python**

10. [Why OOP is Critical for Automation Frameworks](#10-why-oop-is-critical-for-automation-frameworks)
11. [Class and Object](#11-class-and-object)
12. [Constructor (`__init__`)](#12-constructor-__init__)
13. [Methods and Attributes](#13-methods-and-attributes)
14. [Inheritance (Basic)](#14-inheritance-basic)
15. [Encapsulation (Basic)](#15-encapsulation-basic)
16. [Automation-oriented OOP Example](#16-automation-oriented-oop-example)

**Part C - Debugging Concepts**

17. [Common Python and Automation Errors](#17-common-python-and-automation-errors)
18. [Print-based Debugging](#18-print-based-debugging)
19. [IDE Debugging (Breakpoints, Step Into / Step Over)](#19-ide-debugging-breakpoints-step-into--step-over)
20. [Exception Handling (try, except, finally)](#20-exception-handling-try-except-finally)

**Part D - Wrap-up**

21. [Hands-on Summary](#21-hands-on-summary)
22. [Questions and answers](#22-questions-and-answers)
23. [Quick Reference Card](#23-quick-reference-card)

---

# Part A - Python Fundamentals for Automation

## 1. Introduction to Python and Automation Use Cases

### What is Python?

Python is a general-purpose programming language. It was created by Guido van Rossum and first released in 1991. It is known for being **easy to read**, and Python code often looks close to plain English:

```python
if actual_title == "Calculator":
    print("PASS")
```

Even without any training, most people can guess what this code does. This is why Python is a popular first language for testers.

Key facts:

- **Interpreted:** you write the code and run it directly. There is no separate "compile" step.
- **Free and open source.** It runs on Windows, Linux and macOS.
- **"Batteries included":** the standard library already has modules for files, dates, text, running commands and more.
- **Huge ecosystem:** thousands of free packages can be installed with `pip`.

### What is test automation?

Test automation means using a program (a **script**) to do the steps a manual tester would do: open the application, enter data, click buttons, and **compare the actual result with the expected result**. The script then reports PASS or FAIL.

Automation does not replace manual testing. It takes over the **repetitive** work, such as regression, smoke tests and data-heavy tests. This gives testers more time for exploratory testing and for thinking about risk.

### Why Python for automation?

| Reason | What it means for you |
|--------|-----------------------|
| Easy to learn | You can write useful scripts in the first week |
| Less code | The same test takes fewer lines than in Java or C# |
| Rich libraries | pywinauto, pyautogui (desktop), Selenium/Playwright (web), requests (API), pytest (framework) |
| One language for everything | Desktop, web, API, CLI, test data, reports |
| Big community | Most error messages can be searched online and answered quickly |

### Automation use cases for testers

- **Desktop GUI testing:** log in to a billing application, create an invoice, verify the total.
- **CLI testing:** run `app.exe --export report.csv`, check the exit code and the output file.
- **Test data generation:** create 1,000 customer records for a load test.
- **Log analysis:** search application logs for `ERROR` or `Exception` after a test run.
- **Environment checks:** verify the OS version, free disk space and installed software before testing.
- **Reporting:** produce an HTML report automatically after each run.
- **Regression:** re-run hundreds of tests every night without anyone watching.

### Common mistakes

- Thinking automation will find *new* bugs by itself. Automation mostly finds **regressions**, which are old features that broke again.
- Trying to automate everything. Automate stable, repetitive, high-value tests first.

### Try it yourself

List three repetitive tasks from your current project. For each one, write down whether it is GUI, CLI, data or report work.

### Chapter summary

Python is simple, readable and powerful. It is one of the most used languages for test automation because testers can learn it quickly, and it has tools for every kind of testing.

---

## 2. Desktop and CLI Automation Overview

### Desktop (GUI) automation

Desktop applications are programs installed on the computer, such as Notepad, Calculator, a billing application or an ERP client. Desktop automation controls their **windows, buttons, text boxes, menus and grids**.

There are two main approaches:

| Approach | How it works | Tool (later in the course) | Pros | Cons |
|----------|--------------|----------------------------|------|------|
| **Object-based** | Asks Windows for a control by name, ID or type | `pywinauto` | Reliable; works when the window is resized | Needs apps that expose control information |
| **Image-based** | Finds things by matching pictures on the screen | `pyautogui` + OpenCV | Works with almost any app | Breaks when the resolution, theme or scaling changes |

### CLI (command-line) automation

Many applications and tools have a command-line interface. CLI automation runs these commands from a Python script and checks:

- the **exit code** (0 usually means success),
- the **output text** (stdout / stderr),
- any **files** that were created.

Python's built-in `subprocess` module does this:

```python
import subprocess, sys

result = subprocess.run([sys.executable, "--version"],
                        capture_output=True, text=True)
print(result.returncode)        # 0
print(result.stdout.strip())    # Python 3.x.x
```

**Demo:** `examples/02_cli_automation_preview.py` collects environment details for a test report and runs one CLI test.

### How a desktop automation script is organised (preview)

1. **Launch** the application (or connect to one that is already running).
2. **Find** the window and its controls.
3. **Act:** type, click, select.
4. **Verify:** read a value and compare it with the expected value.
5. **Clean up:** close the application, even if the test failed.

Today you learn the Python needed for every one of these steps.

### Common mistakes

- Using image-based automation when object-based automation is possible. Image matching is more fragile.
- Forgetting cleanup, which leaves application windows open for the next test.

### Try it yourself

Run `python examples/02_cli_automation_preview.py`. Find the line in the output that shows the exit code of the CLI command.

### Chapter summary

Desktop automation controls GUI applications, either through their objects or through images. CLI automation runs commands and checks their results. Python supports both.

---

## 3. Python Installation and IDE Setup (VS Code / PyCharm)

### Installing Python on Windows

1. Go to **https://www.python.org/downloads/** and download the latest Python 3 (3.12 or newer).
2. Run the installer. **Tick "Add python.exe to PATH"** on the first screen. This is important.
3. Click **Install Now**.
4. Open a **new** terminal (PowerShell or Command Prompt) and check:
   ```
   python --version
   pip --version
   ```

If you see `'python' is not recognized...`, Python is not on your PATH. Re-run the installer, choose **Modify**, and enable the PATH option. Alternatively, use the Windows launcher: `py --version`.

### Installing packages with pip

`pip` is Python's package installer:

```
pip install pytest
pip install pywinauto pyautogui
pip list                    # show installed packages
pip show pywinauto          # details of one package
```

### VS Code setup (recommended for this course)

1. Install VS Code from **https://code.visualstudio.com/**.
2. Open the Extensions view (`Ctrl+Shift+X`) and install **Python** (by Microsoft). It also installs the Python Debugger.
3. **File > Open Folder** and select the course folder.
4. Press `Ctrl+Shift+P`, type **Python: Select Interpreter**, and choose your Python installation.
5. Open a terminal with ``Ctrl+` ``.
6. Run a file: click the **Run** (triangle) button at the top right, or type `python file_name.py` in the terminal.

### PyCharm setup (alternative)

1. Install **PyCharm Community Edition** from jetbrains.com.
2. **New Project** (or **Open**), and select the Python interpreter.
3. Right-click a file and choose **Run**. Use **Debug** (`Shift+F9`) to debug.

### Virtual environments (for real projects)

A virtual environment keeps each project's packages separate:

```
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

`requirements.txt` lists the packages the project needs. For Day 1 we only use the standard library, so no virtual environment is needed.

### Common mistakes

- Not ticking **Add to PATH** during installation.
- Having two Python versions installed, with VS Code using a different one from the terminal. Check the interpreter in the VS Code status bar.
- Saving files as `test.py.txt` in Notepad. Always save from your IDE.
- Naming your own file after a package, such as `pywinauto.py` or `random.py`. This hides the real package when you import it.

### Try it yourself

Run `python --version` and `pip list` in the VS Code terminal. Find `pytest` in the list.

### Chapter summary

Install Python with "Add to PATH" ticked, install the Python extension in VS Code (or use PyCharm), and run scripts from the terminal or the Run button.

---

## 4. Python Syntax and Your First Program

### Your first program

Create a file named `hello.py`:

```python
# My first Python program
print("Hello, Automation World!")
```

Run it:

```
python hello.py
```

Output:

```
Hello, Automation World!
```

`print()` is a built-in **function** that shows output. The text inside quotes is called a **string**.

### Key syntax rules

| Rule | Example |
|------|---------|
| **Indentation** groups code (use 4 spaces) | lines inside `if`, `for`, `def` are indented |
| A block starts with a **colon** `:` | `if app_is_open:` |
| **Case-sensitive** | `Title` and `title` are different names |
| Comments start with `#` | `# check the title` |
| Strings use `'...'` or `"..."` | `'PASS'` is the same as `"PASS"` |
| No semicolons needed | one statement per line |

```python
app_is_open = True
if app_is_open:
    print("Step 1: Application window is open")   # inside the if
    print("Step 2: Ready to start testing")       # inside the if
print("This always runs")                         # outside the if
```

### A tiny test script

```python
expected_title = "Notepad"
actual_title = "Notepad"
print("Expected:", expected_title)
print("Actual  :", actual_title)
print("Result  :", "PASS" if expected_title == actual_title else "FAIL")
```

**Demo:** `examples/01_first_program.py`

### Common mistakes

- `Print("hi")`. It must be lowercase `print`.
- Missing quotes: `print(Hello)` gives `NameError`.
- Missing colon after `if` / `for` / `def`.
- Mixing tabs and spaces. Let VS Code insert 4 spaces for you.

### Try it yourself

Write a script that prints a header for the test case `TC_101 - Verify Save dialog`, then prints `Expected: Saved` and `Actual: Saved`, and finally prints a result line.

### Chapter summary

Python code runs from top to bottom. Indentation and colons define blocks. `print()` shows output, and `#` starts a comment.

---

## 5. Variables and Data Types

### Variables

A **variable** is a name that refers to a value. You create one with `=`:

```python
test_case_id = "TC_LOGIN_001"
retry_count = 3
```

You do not declare the type. Python works it out from the value. This is called **dynamic typing**.

**Naming rules:** a name can use letters, digits and `_`. It cannot start with a digit, and it cannot be a keyword such as `if`, `for` or `class`.
**Naming style (PEP 8):** use `snake_case` with meaningful names, such as `expected_title` or `max_wait_seconds`. Use UPPER_CASE for constants, such as `MAX_WAIT_SECONDS = 30`.

### Basic data types

| Type | Example | Testing use |
|------|---------|-------------|
| `str` | `"Untitled - Notepad"` | window titles, labels, messages |
| `int` | `3` | counts, retries, row numbers |
| `float` | `1.75` | response time, amounts |
| `bool` | `True`, `False` | pass/fail flags, "is visible" |
| `NoneType` | `None` | "no value yet" (e.g. no defect ID) |

Use `type()` to check the type of any value:

```python
print(type(1.75))    # <class 'float'>
```

### Strings in detail

```python
title = "Untitled - Notepad"
title.upper()                   # 'UNTITLED - NOTEPAD'
title.lower()                   # 'untitled - notepad'
len(title)                      # 18
"Notepad" in title              # True
title.startswith("Untitled")    # True
title.replace("Untitled", "report.txt")
"  PASS  ".strip()              # 'PASS'  (removes spaces at both ends)
title[0:8]                      # 'Untitled'  (slicing: start to end-1)
title[-7:]                      # 'Notepad'
```

**f-strings** put values inside text:

```python
tester, test_id, secs = "Priya", "TC_001", 1.756
print(f"{tester} executed {test_id} in {secs:.2f} seconds")
# Priya executed TC_001 in 1.76 seconds
```

### Type conversion

Values read from screens, files and text boxes are **strings**. Convert them before you do maths:

```python
int("42")          # 42
float("99.5")      # 99.5
str(3)             # '3'
bool(0), bool(1)   # False True
int("12a")         # ValueError: invalid literal for int()
```

### Collection types

**List:** ordered and changeable. Use it for a list of results or test cases.

```python
results = ["PASS", "FAIL", "PASS"]
results.append("SKIP")       # add at the end
results[0]                   # 'PASS'  (index starts at 0)
results[-1]                  # 'SKIP'  (last item)
len(results)                 # 4
results.count("PASS")        # 2
```

**Tuple:** ordered and **not** changeable. Use it for fixed values.

```python
screen_resolution = (1920, 1080)
```

**Dictionary (dict):** key-value pairs. Use it for one row of test data or for configuration.

```python
login_data = {"username": "admin", "password": "Admin@123"}
login_data["username"]               # 'admin'
login_data["role"] = "tester"        # add or update a key
login_data.get("otp", "none")        # safe read with a default value
login_data.keys(), login_data.values(), login_data.items()
```

**Set:** unique values only.

```python
{"Chrome", "Edge", "Chrome"}         # {'Chrome', 'Edge'}
```

**Demo:** `examples/03_variables_datatypes.py`

### Common mistakes

- `"Total: " + 5` gives `TypeError`. Use `f"Total: {5}"` or `str(5)`.
- `"5" + "5"` gives `"55"`, not 10, because both are strings.
- Using index `3` in a list of 3 items gives `IndexError`. The valid indexes are 0, 1 and 2.
- Dictionary keys are case-sensitive: `"Status"` is not the same as `"status"`.
- Writing `true` or `none`. The correct forms are `True` and `None`.

### Try it yourself

Create a dictionary for one test case with the keys `id`, `title`, `priority` and `status`. Print a sentence using an f-string. Then change `status` to `"PASS"` and print it again.

### Chapter summary

Variables are names for values. The main types are `str`, `int`, `float`, `bool` and `None`. Lists, tuples, dictionaries and sets hold groups of values. Convert strings to numbers before doing maths.

---

## 6. Operators (Arithmetic, Comparison, Logical)

### Arithmetic operators

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | add | `10 + 3` | `13` |
| `-` | subtract | `10 - 3` | `7` |
| `*` | multiply | `10 * 3` | `30` |
| `/` | divide (always float) | `10 / 3` | `3.333...` |
| `//` | floor division | `10 // 3` | `3` |
| `%` | modulus (remainder) | `10 % 3` | `1` |
| `**` | power | `2 ** 5` | `32` |

```python
total, passed = 17, 14
pass_percentage = passed / total * 100
print(f"{pass_percentage:.2f}%")     # 82.35%
```

**Assignment shortcuts:** `retry += 1` is the same as `retry = retry + 1`. The same works with `-=`, `*=` and `/=`.

### Comparison operators (the result is always True or False)

| Operator | Meaning |
|----------|---------|
| `==` | equal to |
| `!=` | not equal to |
| `>` / `<` | greater than / less than |
| `>=` / `<=` | greater or equal / less or equal |

Every test verification is a comparison: `actual == expected`.

### Logical operators

| Operator | True when... | Example |
|----------|--------------|---------|
| `and` | **both** sides are True | `username_ok and password_ok` |
| `or` | **at least one** side is True | `is_admin or is_manager` |
| `not` | it reverses the value | `not window_found` |

```python
build_ok = pass_percentage >= 80 and failed < 5
```

### Membership and identity

```python
"Edit" in ["File", "Edit", "View"]          # True
"Error" in "10:01 Error: window not found"  # True
defect_id is None                           # identity - use it with None
```

**Demo:** `examples/04_operators.py`

### Common mistakes

- Using `=` (assignment) when you mean `==` (comparison).
- Expecting `10 / 2` to give `5`. It gives `5.0`, a float.
- Comparing floats exactly: `0.1 + 0.2 == 0.3` is **False**. Use `abs(a - b) < 1e-9` or `round()`.
- Writing `if status == "PASS" or "SKIP":`. This is always True. Write `if status == "PASS" or status == "SKIP":` or `if status in ("PASS", "SKIP"):`.

### Try it yourself

Given `executed = 40` and `failed = 6`, calculate the pass percentage. Print `ACCEPTED` if it is at least 85% **and** fewer than 8 tests failed; otherwise print `REJECTED`.

### Chapter summary

Arithmetic operators calculate values, comparison operators produce True or False, and logical operators combine conditions. `in` checks membership, and `is None` checks for "no value".

---

## 7. Conditional Statements

Conditions let a script **make decisions**. This is what turns a script into a *test*: it checks something and chooses PASS or FAIL.

### if / else

```python
if actual_status == expected_status:
    print("PASS")
else:
    print(f"FAIL: expected '{expected_status}' but got '{actual_status}'")
```

### if / elif / else

Python checks the conditions from **top to bottom** and runs **only the first** block whose condition is True.

```python
if crash_count == 0:
    severity = "None"
elif crash_count <= 2:
    severity = "Medium"
elif crash_count <= 5:
    severity = "High"
else:
    severity = "Critical"
```

### Combined conditions

```python
if not username or not password:
    print("Error: username and password are required")
elif account_locked:
    print("Error: account is locked")
elif username == "admin" and password == "Admin@123":
    print("Login successful")
else:
    print("Error: invalid credentials")
```

### Nested if

```python
if window_found:
    if window_title == "Calculator":
        print("Correct window - continue")
    else:
        print("Wrong window in focus")
else:
    print("Window not found - test BLOCKED")
```

### One-line if (conditional expression)

```python
result = "PASS" if response_time <= 3 else "FAIL"
```

### Truthy and falsy values

`""` (an empty string), `0`, `[]`, `{}` and `None` behave like `False`. Everything else behaves like `True`.

```python
error_message = ""
if error_message:
    print("Error shown:", error_message)
else:
    print("No error message displayed")
```

### match / case (Python 3.10+)

```python
match environment:
    case "DEV":
        path = r"C:\apps\dev\billing.exe"
    case "QA":
        path = r"C:\apps\qa\billing.exe"
    case _:
        path = "unknown"
```

**Demo:** `examples/05_conditionals.py`

### Common mistakes

- Wrong **order** of `elif` conditions. A broad condition placed first hides the later ones. (You will fix this bug in Lab 3, bug file 4.)
- Forgetting the colon, or indenting the block incorrectly.
- Writing `if x = 5:`. This is a SyntaxError; use `==`.

### Try it yourself

Write code that takes `response_time` and prints `FAST` (up to 1 second), `ACCEPTABLE` (up to 3 seconds) or `SLOW` (more than 3 seconds). Test it with 0.5, 2 and 4.2.

### Chapter summary

`if / elif / else` chooses one path. Conditions can be combined with `and`, `or` and `not`. The order of `elif` branches matters. Empty values count as False.

---

## 8. Loops (for, while)

Loops repeat work: run many test cases, go through rows of test data, or wait for a window to appear.

### for loop

```python
test_cases = ["TC_001 Login", "TC_002 Logout", "TC_003 Search"]
for test in test_cases:
    print("Executing:", test)
```

**range():**

```python
for step in range(1, 4):      # 1, 2, 3  (the stop value is NOT included)
    print(f"Step {step} of 3")
```

**enumerate()** gives you both the position and the value:

```python
for number, test in enumerate(test_cases, start=1):
    print(number, test)
```

**Looping over a dictionary:**

```python
results = {"TC_001": "PASS", "TC_002": "FAIL"}
for test_id, status in results.items():
    print(test_id, status)
```

### Data-driven testing

The same steps run for every row of data:

```python
login_data = [
    {"user": "admin", "pwd": "Admin@123", "expected": "success"},
    {"user": "admin", "pwd": "wrong",     "expected": "failure"},
]
for row in login_data:
    actual = login(row["user"], row["pwd"])
    print("PASS" if actual == row["expected"] else "FAIL")
```

### while loop

A `while` loop repeats **as long as** a condition is True. It is useful for waiting or polling:

```python
attempt = 0
while not window_ready and attempt < 5:
    attempt += 1
    window_ready = check_window()
```

Always include a limit (such as `attempt < 5`) to avoid an **infinite loop**. If a script hangs, press `Ctrl+C` in the terminal to stop it.

### break and continue

```python
for status in statuses:
    if status == "CRITICAL":
        break        # stop the loop completely
    if status == "SKIP":
        continue     # skip the rest of this round, go to the next item
    print(status)
```

### List comprehension (a short way to build a list)

```python
failed = [tid for tid, st in results.items() if st == "FAIL"]
```

**Demo:** `examples/06_loops.py`

### Common mistakes

- **Off-by-one:** `range(1, len(items))` skips the first item, and `range(5)` gives 0 to 4.
- Infinite `while` loops with no exit condition.
- Changing a list while you loop over it.
- Wrong indentation: a line that should be inside the loop is outside it, so it runs only once.

### Try it yourself

Given `durations = [2.1, 5.4, 1.2, 7.9, 3.3]`, use a loop to count how many tests took more than 3 seconds. Also find the largest value without using `max()`.

### Chapter summary

`for` loops go through sequences such as lists, ranges and dictionaries. `while` loops repeat until a condition changes. `break` stops a loop and `continue` skips to the next item. Loops are the engine of data-driven testing.

---

## 9. Functions and Reusability

### What is a function?

A **function** is a named, reusable block of code. You **define** it once with `def`, and then **call** it as many times as you need.

```python
def verify_equal(expected, actual):
    """Return 'PASS' if both values are equal, else 'FAIL'."""
    if expected == actual:
        return "PASS"
    return "FAIL"

print(verify_equal("Login", "Login"))    # PASS
print(verify_equal("Login", "Logon"))    # FAIL
```

Think of a function as a **reusable test step**. "Login" is written once and used by many test cases.

### Parameters, arguments and return values

- **Parameters** are the names in the definition: `expected`, `actual`.
- **Arguments** are the values you pass when you call it: `"Login"`, `"Login"`.
- `return` sends a value back to the caller. A function without `return` gives back `None`.

### Default and keyword arguments

```python
def log(message, level="INFO"):
    print(f"[{level}] {message}")

log("Test started")                    # [INFO] Test started
log("Disk space low", level="WARNING") # [WARNING] Disk space low
```

### Returning several values

```python
def summarize(results):
    passed = results.count("PASS")
    failed = results.count("FAIL")
    return passed, failed              # returned as a tuple

p, f = summarize(["PASS", "FAIL", "PASS"])
```

### Type hints (optional)

```python
def is_within_sla(response_time: float, sla: float = 3.0) -> bool:
    return response_time <= sla
```

Type hints do not change how the code runs. They make the code easier to read, and they help the IDE find mistakes.

### Scope

Variables created inside a function are **local**. They do not exist outside the function.

### Useful built-in functions

`print()`, `len()`, `type()`, `int()`, `str()`, `float()`, `min()`, `max()`, `sum()`, `sorted()`, `round()`, `range()`, `enumerate()`, `input()`.

### Why functions matter for automation

- **Less duplication:** the login code is written once.
- **Easy maintenance:** fix it in one place.
- **Readable tests:** `login("admin", "Admin@123")` explains itself.
- **The building blocks of frameworks:** helper modules such as `utils.py` are collections of functions.

**Demo:** `examples/07_functions.py`

### Common mistakes

- Confusing `print` with `return`. `print` only shows a value; `return` gives it back so it can be used.
- Forgetting the brackets: `log` refers to the function, while `log()` calls it.
- Passing the wrong number of arguments, which gives `TypeError: missing 1 required positional argument`.
- Defining a function *after* the line that calls it (in the same script).

### Try it yourself

Write a function `classify(pass_percent)` that returns `"GREEN"` for 90% and above, `"AMBER"` for 75% and above, and `"RED"` otherwise. Call it with 95, 80 and 50.

### Chapter summary

Functions package reusable logic. They take parameters, can have default values, and return results. Good automation code is built from small, well-named functions.

**Hands-on:** Lab 1 - Calculator using functions (`hands_on/Lab_Guide.md`).

---

# Part B - OOP Concepts Using Python

## 10. Why OOP is Critical for Automation Frameworks

**Object-Oriented Programming (OOP)** organises code around **objects**. An object bundles **data** (attributes) together with the **actions** that work on that data (methods).

Why automation engineers need OOP:

1. **Scale:** real projects have hundreds of tests and dozens of screens. Loose variables and functions become hard to manage.
2. **Page / Window Object Model:** each screen of the application becomes one class, such as `LoginWindow` or `InvoiceWindow`. Tests call its methods instead of touching controls directly.
3. **Maintenance:** when a control's name changes, you update **one** class instead of 100 test scripts.
4. **Reuse:** common behaviour (open, close, screenshot, wait) is written once in a `BasePage` class and inherited by all screens.
5. **Readability:** `login_page.login("admin", "Admin@123")` reads like a manual test step.
6. **Tools are built with OOP:** pywinauto windows, pytest fixtures and Selenium drivers are all objects.

**The four pillars of OOP** are encapsulation, inheritance, polymorphism and abstraction. Today we cover the first two at a basic level, and you will see polymorphism in Lab 2.

### Chapter summary

OOP gives structure to automation code. It makes large frameworks readable, reusable and cheap to maintain.

---

## 11. Class and Object

- A **class** is a blueprint or template. Example: the "test case" template in your test management tool.
- An **object** (also called an **instance**) is a real thing created from the class. Example: TC_001 and TC_002, each with its own data.

```python
class TestCase:
    """Blueprint for a test case."""

    def __init__(self, test_id, title):
        self.test_id = test_id
        self.title = title
        self.status = "Not Run"

    def mark(self, status):
        self.status = status

    def show(self):
        print(f"{self.test_id} | {self.title} | {self.status}")


tc1 = TestCase("TC_001", "Login with valid user")      # object 1
tc2 = TestCase("TC_002", "Login with wrong password")  # object 2
tc1.mark("PASS")
tc2.mark("FAIL")
tc1.show()     # TC_001 | Login with valid user | PASS
tc2.show()     # TC_002 | Login with wrong password | FAIL
```

Each object keeps its **own** data. Changing `tc1.status` does not change `tc2.status`.

**Everything in Python is an object.** When you write `"calculator".upper()`, you call the `upper` method of a `str` object.

**Naming:** class names use `CamelCase` (`TestCase`, `LoginWindow`). Variables and methods use `snake_case`.

**Demo:** `examples/08_classes_objects.py`

### Common mistakes

- Forgetting the brackets when you create an object: `tc = TestCase` (this refers to the class) instead of `tc = TestCase("TC_001", "Login")`.
- Mixing up the class and the object: call methods on the **object** (`tc1.mark()`), not on the class.

### Try it yourself

Create a class `Defect` with the attributes `defect_id`, `summary`, `severity` and `status="Open"`, and a method `close()`. Create two defects, close one of them, and print both.

### Chapter summary

A class is the design, and objects are the real instances. One class can create many independent objects.

---

## 12. Constructor (`__init__`)

`__init__` is a special method (called "dunder init") that Python runs **automatically** when you create an object. Its job is to set up the object's starting state.

```python
class AppWindow:
    def __init__(self, title, width=800, height=600):
        self.title = title
        self.width = width
        self.height = height
        self.is_open = False
        self.controls = []

calc = AppWindow("Calculator", 400, 600)   # __init__ runs now
notepad = AppWindow("Notepad")             # uses the default width and height
```

### What is `self`?

`self` means **"this object"**. When you call `calc.open()`, Python actually runs `AppWindow.open(calc)`. The object is passed in automatically as the first argument. That is why:

- every instance method has `self` as its **first parameter**, and
- you use `self.something` to store or read the object's data.

### Common mistakes

- Spelling it `_init_` (single underscores) or `__int__`. The method is then never called.
- Forgetting `self.` when you store a value: `title = title` creates a local variable that disappears when `__init__` ends.
- Forgetting `self` as the first parameter, which gives `TypeError: ... takes 1 positional argument but 2 were given`.

### Try it yourself

Add a `created_at` attribute to `AppWindow` using `datetime.now()` inside `__init__`. Create two windows and print their creation times.

### Chapter summary

`__init__` runs automatically when an object is created and sets its initial attributes. `self` refers to the current object.

---

## 13. Methods and Attributes

### Attributes: what an object HAS

- **Instance attributes** belong to one object. They are set with `self.name = ...`, usually in `__init__`.
- **Class attributes** are shared by **all** objects of the class. They are defined directly in the class body.

```python
class AppWindow:
    window_count = 0                     # class attribute (shared)

    def __init__(self, title):
        self.title = title               # instance attribute
        AppWindow.window_count += 1
```

### Methods: what an object DOES

A method is a function defined inside a class. It can read and change attributes, and it can return values.

```python
    def open(self):
        self.is_open = True

    def add_control(self, name):
        self.controls.append(name)

    def has_control(self, name):
        return name in self.controls

    def __str__(self):                   # special method used by print()
        return f"AppWindow(title='{self.title}')"
```

Usage:

```python
calc.open()
calc.add_control("Button_Plus")
print(calc.has_control("Button_Plus"))   # True
print(calc)                              # AppWindow(title='Calculator')
print(AppWindow.window_count)            # 2
```

**Demo:** `examples/09_constructor_methods_attributes.py`

### Common mistakes

- Calling a method without brackets: `window.open` only refers to the method and does nothing. Use `window.open()`.
- Using a mutable class attribute (such as a list) for per-object data. All objects then share the same list. Create lists in `__init__` instead.

### Try it yourself

Add a method `resize(width, height)` to `AppWindow` that rejects values below 100 by printing a warning. Add a method `area()` that returns `width * height`.

### Chapter summary

Attributes store an object's data, and methods define its behaviour. Instance attributes belong to one object; class attributes are shared by all.

---

## 14. Inheritance (Basic)

**Inheritance** lets a **child** class reuse everything from a **parent** class. The child can then **add** new behaviour or **change** (override) existing behaviour.

```python
class BasePage:
    def __init__(self, window_title):
        self.window_title = window_title

    def open(self):
        print(f"[{self.window_title}] opened")

    def take_screenshot(self, name):
        print(f"[{self.window_title}] screenshot {name}.png")


class LoginPage(BasePage):                      # LoginPage IS-A BasePage
    def __init__(self):
        super().__init__("Login - Billing App") # run the parent's constructor
        self.username = ""

    def enter_username(self, username):
        self.username = username


class DashboardPage(BasePage):
    def __init__(self):
        super().__init__("Dashboard - Billing App")

    def open(self):                             # overriding
        super().open()                          # keep the parent behaviour...
        print("waiting for widgets")            # ...and add more
```

```python
login = LoginPage()
login.open()                  # inherited from BasePage
login.enter_username("admin") # LoginPage's own method
login.take_screenshot("tc1")  # inherited
```

Key terms:

- **Parent / base / super class:** `BasePage`
- **Child / derived / sub class:** `LoginPage`
- **`super()`:** calls the parent's version of a method
- **Overriding:** redefining a parent method with the same name in the child
- `isinstance(login, BasePage)` returns `True`, and `issubclass(LoginPage, BasePage)` returns `True`

**Demo:** `examples/10_inheritance.py`

### Why it matters in automation

Frameworks put common actions (open, close, wait, screenshot, verify title) in a base class. Each screen class inherits them, so this code is never duplicated.

### Common mistakes

- Forgetting `super().__init__(...)` in the child constructor. The parent's attributes are then never created, which gives `AttributeError`.
- Using inheritance where it does not fit. Use it only for real "is-a" relationships: a LoginPage **is a** page.

### Try it yourself

Create a `SettingsPage(BasePage)` with a method `change_theme(theme)`. Override `take_screenshot` so that it adds `"_settings"` to the file name, then calls the parent version.

### Chapter summary

Inheritance lets child classes reuse and extend parent classes. `super()` calls the parent, and overriding changes behaviour for the child.

---

## 15. Encapsulation (Basic)

**Encapsulation** means keeping data together with the code that protects it, and **controlling** how outside code can change that data.

### Naming conventions in Python

| Style | Meaning |
|-------|---------|
| `self.app_path` | **public**: anyone can use it |
| `self._timeout` | **protected**: "internal, please don't touch" (a convention) |
| `self.__password` | **private**: Python renames it (name mangling) so outside code cannot reach it easily |

### Controlled access with `@property`

```python
class TestConfig:
    def __init__(self, app_path, timeout_seconds=10, password="secret"):
        self.app_path = app_path
        self.__password = password
        self.timeout = timeout_seconds         # uses the setter below

    @property
    def timeout(self):                         # getter
        return self._timeout

    @timeout.setter
    def timeout(self, value):                  # setter with validation
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"timeout must be positive, got {value!r}")
        self._timeout = value

    def masked_password(self):
        return "*" * len(self.__password)
```

```python
config = TestConfig(r"C:\apps\qa\billing.exe", 15, "Qa@2026")
config.timeout = 30          # OK
config.timeout = -5          # ValueError - an invalid value is rejected
config.masked_password()     # '*******'
config.__password            # AttributeError
```

A property **without** a setter is **read-only**. In Lab 2, `account.balance` works this way, so nobody can write `account.balance = 1000000`.

**Demo:** `examples/11_encapsulation.py`

### Why it matters in automation

- It protects configuration from bad values, such as a negative timeout.
- It hides secrets such as passwords from logs.
- It gives each class a clean, stable **public interface**, so the internal details can change safely.

### Common mistakes

- Thinking Python makes attributes truly private. It does not. The underscores are about **intent**.
- Printing passwords or tokens in logs and reports.

### Try it yourself

Add a `retries` property to `TestConfig` that only accepts whole numbers from 0 to 5.

### Chapter summary

Encapsulation bundles data with its rules. Use `_name` for internal attributes, and use `@property` to validate values or make them read-only.

---

## 16. Automation-oriented OOP Example

`examples/12_automation_oop_example.py` combines everything from Part B in a small, **simulated** framework for a calculator application:

| Class | Role in a real framework |
|-------|--------------------------|
| `FakeCalculatorApp` | The application under test (on Day 2 this becomes real pywinauto code) |
| `BaseScreen` | Parent class with common actions such as logging |
| `CalculatorScreen(BaseScreen)` | Screen object with `clear()`, `enter()`, `equals()` and `read_display()` |
| `TestResult` | Stores expected, actual and status for one test |
| `TestRunner` | Runs the test data through the screen object and prints a report |

A test then reads like a manual test case:

```python
screen.clear()
screen.enter("2+3")
screen.equals()
actual = screen.read_display()      # "5"
```

In the demo, test CALC_04 (`8/2`, expected `"4"`) **fails** on purpose because the app shows `"4.0"`. Discuss it in class: is this an application defect, or a wrong expectation in the test? Automation engineers must ask this question for every failure.

### Chapter summary

Real frameworks separate the **test data**, the **test logic**, the **screen objects** and the **application driver**. OOP makes this separation natural.

**Hands-on:** Lab 2 - OOP-based business logic (PyBank).

---

# Part C - Debugging Concepts

## 17. Common Python and Automation Errors

### Three kinds of errors

| Kind | When it appears | How you notice it |
|------|-----------------|-------------------|
| **Syntax error** | Before the program runs | Python refuses to start and shows `SyntaxError` |
| **Runtime error (exception)** | While the program runs | A traceback appears and the program stops |
| **Logic error** | Never reported | The program runs but gives the wrong result |

Logic errors are the most dangerous in automation, because they can produce **false PASS** results.

### Reading a traceback

```
Traceback (most recent call last):
  File "C:\...\17_debugging_demo_buggy.py", line 53, in <module>
    counts = count_by_status(test_run)
  File "C:\...\17_debugging_demo_buggy.py", line 37, in count_by_status
    counts[result["Status"]] += 1
           ~~~~~~^^^^^^^^^^
KeyError: 'Status'
```

1. Read the **last line** first. It gives the error **type** (`KeyError`) and the **message** (`'Status'`).
2. Read the frame just above it: the file, the **line number** (37) and the function name.
3. The lines above that show the chain of calls that led to the error (the call stack).

### Common Python errors

| Error | Example cause | Typical fix |
|-------|---------------|-------------|
| `SyntaxError` | missing `:` `)` `"`, `=` instead of `==` | read the `^` marker; check the line above too |
| `IndentationError` | a block is not indented | use 4 spaces consistently |
| `NameError` | a typo such as `window_titel` | check the spelling; define the variable first |
| `TypeError` | `"Total: " + 5`; a missing argument | convert types; pass the correct arguments |
| `ValueError` | `int("12a")` | validate or clean the input |
| `KeyError` | `data["user_name"]` when the key is `"username"` | check the key; use `.get()` |
| `IndexError` | `results[3]` in a list of 3 items | check `len()`; remember indexes start at 0 |
| `AttributeError` | `"text".click()`; a missing `self.x` | check the object type; call `super().__init__` |
| `ZeroDivisionError` | pass % when 0 tests were executed | check for 0 before dividing |
| `FileNotFoundError` | test data file missing / wrong path | check the path; use absolute paths |
| `ModuleNotFoundError` | package not installed or name misspelled | `pip install ...`; check the VS Code interpreter |

### Common automation errors (you will meet these from Day 2)

- **Element / control not found:** the locator is wrong, or the control is not visible yet.
- **Timeout / window not found:** the application starts slowly. Use proper waits, not fixed `sleep` calls.
- **Stale state:** a dialog was closed but the script still tries to use it.
- **Focus problems:** another window is in front of the application.
- **Resolution, scaling or theme differences:** image-based matching fails.
- **Test data problems:** a wrong key, an extra space, or a number stored as text.

**Demo:** `examples/13_common_errors.py` triggers and catches each common error, so you can see the exact messages.

### Try it yourself

Before running `13_common_errors.py`, write down the error type you expect for each demo. Then run it and check your answers.

### Chapter summary

Learn to recognise error types. Read tracebacks from the bottom up. Logic errors need extra care because nothing warns you about them.

---

## 18. Print-based Debugging

The simplest debugging technique is to add temporary `print()` statements so you can **see** what the program is doing.

```python
for index, status in enumerate(results):
    print(f"[DEBUG] index={index} status={status!r}")
    if status == "PASS":
        passed += 1
```

The output shows `status='PASS '`, with a hidden trailing space, and `status='pass'` in lower case. This explains why the count was wrong. The fix is to clean the value first: `status.strip().upper()`.

### Useful tricks

- `print(f"{total=}")` prints both the name and the value, for example `total=5`.
- `!r` shows the "raw" form, so hidden spaces and quotes become visible.
- `print(type(x))` helps when you suspect a type problem.
- Use a `DEBUG = True/False` switch so you can turn the prints on and off.
- In frameworks, use the **logging** module, which adds levels, timestamps and file output:

```python
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")
logging.debug("Clicking Save")
logging.info("File saved")
logging.warning("Save took 4.2s")
logging.error("Confirmation dialog not found")
```

**Demo:** `examples/14_print_debugging.py`

### Common mistakes

- Printing a value without its name, which gives a confusing list of numbers.
- Leaving debug prints in the final code.

### Chapter summary

Print debugging is quick and works everywhere. Print names, values and types. Move to `logging` for real projects.

---

## 19. IDE Debugging (Breakpoints, Step Into / Step Over)

A debugger lets you **pause** a running program, look at every variable, and move through the code one line at a time.

### Breakpoints in VS Code

1. Open the file and click in the **gutter** (left of the line numbers). A **red dot** appears. You can also press `F9` on the line.
2. Press **F5** and choose **Python Debugger: Current File**.
3. The program pauses **before** running the line with the red dot.
4. Look at the panels on the left:
   - **Variables:** the current values of all variables.
   - **Watch:** expressions you add yourself, such as `invoice_total`.
   - **Call Stack:** which function called which.
5. **Conditional breakpoint:** right-click the red dot, choose **Edit Breakpoint**, choose **Expression**, and enter for example `qty > 5`. The program pauses only when the condition is True.

### Stepping controls

| VS Code | PyCharm | Action | Use it when... |
|---------|---------|--------|----------------|
| `F10` | `F8` | **Step Over** | you trust the function on this line; run it in one go |
| `F11` | `F7` | **Step Into** | you want to go **inside** the function being called |
| `Shift+F11` | `Shift+F8` | **Step Out** | finish the current function and return to the caller |
| `F5` | `F9` | **Continue** | run until the next breakpoint |
| `Shift+F5` | `Ctrl+F2` | **Stop** | end debugging |

**Example:** in `examples/15_ide_debugging_walkthrough.py`, put a breakpoint on the line that calls `line_total(...)`.

- Press `F10` (step over): the line runs, and `total` shows the result.
- Press `F11` (step into): you move inside `line_total`, where you can watch `gross`, `discount` and `net` being calculated.

### `breakpoint()` in code

Writing `breakpoint()` on a line pauses the program there. In a plain terminal it opens **pdb**, the Python debugger. In pdb, type `n` (next), `s` (step), `p variable` (print) or `c` (continue).

### Print debugging vs IDE debugging

| Print debugging | IDE debugging |
|-----------------|---------------|
| Quick; no setup | Shows **all** variables at once |
| Works anywhere, including CI servers | Pause, step and inspect interactively |
| You must edit the code | No code changes needed |
| Good for simple checks | Best for logic errors and complex flows |

**Live demo:** `examples/17_debugging_demo_buggy.py` has 4 bugs (a KeyError, a TypeError and two logic errors). Fix them using the traceback, prints and breakpoints. Compare your fixes with `17_debugging_demo_fixed.py`.

### Common mistakes

- Setting a breakpoint on a line that never runs, such as inside an `if` branch that is not taken.
- Pressing `F11` on a line with built-in calls and getting lost in library code. Use `Shift+F11` to step out.

### Chapter summary

Breakpoints pause the program. Step Over runs a line, Step Into enters a function, and Step Out returns. Use the Variables and Watch panels to see what is really happening.

---

## 20. Exception Handling (try, except, finally)

An **exception** is an error that happens while the program runs. Without handling, it stops the program. With handling, you decide what happens next.

### Basic structure

```python
try:
    value = int(text_from_screen)        # code that might fail
except ValueError:
    print("Not a number - test marked FAIL")
```

### Full structure

```python
try:
    launch_app()
    run_steps()
except RuntimeError as error:            # catch a specific error; 'error' holds the details
    print(f"FAIL - {error}")
else:
    print("PASS")                        # runs only if there was NO exception
finally:
    close_app()                          # ALWAYS runs - cleanup
```

| Block | Runs when |
|-------|-----------|
| `try` | always (the risky code) |
| `except` | an exception of that type happened |
| `else` | no exception happened |
| `finally` | **always**, whether there was an error or not |

### Several except blocks

```python
try:
    rate = summary["passed"] / summary["total"] * 100
except KeyError as error:
    print("Missing key:", error)
except ZeroDivisionError:
    print("No tests executed")
```

Put the **more specific** exceptions first.

### Raising exceptions

```python
def set_timeout(seconds):
    if seconds <= 0:
        raise ValueError(f"Timeout must be positive, got {seconds}")
    return seconds
```

### Custom exceptions

```python
class WindowNotFoundError(Exception):
    """Raised when an expected window is not present."""

raise WindowNotFoundError("Window 'Calculator' not found")
```

A custom exception is a class that inherits from `Exception`, so it uses the OOP you learned today. Automation tools define many of these, for example pywinauto's `ElementNotFoundError`.

### Retry pattern (common in desktop automation)

```python
for attempt in range(1, 6):
    try:
        click_ok()
        break                           # success - leave the loop
    except WindowNotFoundError:
        print(f"Attempt {attempt} failed, retrying")
else:
    print("Gave up after 5 attempts")   # runs only if the loop never hit break
```

### Files and `with`

`with open(...) as f:` closes the file automatically, even if an error happens. It acts like a built-in `finally`.

**Demo:** `examples/16_exception_handling.py`

### Best practices

- Catch **specific** exceptions. Avoid a bare `except:`.
- **Never** write `except: pass` in test code. It hides failures and creates false passes.
- Put cleanup (closing the application, files and connections) in `finally`.
- Write clear messages that say **what** failed and **where**.
- Only catch an exception if you can do something useful with it. Otherwise, let it fail visibly.

### Common mistakes

- Catching `Exception` everywhere, which also hides your own bugs.
- Putting too much code inside one `try`, so you cannot tell which line failed.
- Expecting `else` to run after an exception. It runs only when there was **no** exception.

### Try it yourself

Write a function `safe_percentage(passed, total)` that returns the percentage. If `total` is 0, it should print a clear message and return `0.0`. If the inputs are not numbers, it should raise a `TypeError` with a helpful message.

### Chapter summary

`try / except / else / finally` lets your scripts handle failures in a controlled way: report them clearly, clean up, and continue. `raise` and custom exceptions make failures meaningful.

**Hands-on:** Lab 3 - Debugging faulty scripts.

---

# Part D - Wrap-up

## 21. Hands-on Summary

| Lab | Syllabus item | What you practise |
|-----|---------------|-------------------|
| Lab 1 | Calculator using functions | functions, return values, a dictionary of functions, raise, data-driven self-test |
| Lab 2 | OOP-based business logic | classes, `__init__`, properties, inheritance, overriding, custom exceptions |
| Lab 3 | Debugging faulty scripts | syntax, KeyError, TypeError, logic and OOP bugs; tracebacks; breakpoints |
| Lab 4 (extra) | Fundamentals practice | lists, dictionaries, loops, functions on test results |
| Lab 5 (extra) | Exception handling practice | try/except/else/finally, a custom exception, file cleanup |

All instructions are in `hands_on/Lab_Guide.md`.

---

## 22. Questions and answers

**Q1. Why is Python popular for test automation?**
It is easy to read and learn, and it needs less code than many other languages. It also has strong libraries for desktop automation (pywinauto, pyautogui), web (Selenium, Playwright), API (requests) and test frameworks (pytest), and it has a large community.

**Q2. What is the difference between a list and a tuple?**
Both are ordered collections. A list is **mutable**: you can add, remove and change items. A tuple is **immutable**: it cannot be changed after it is created. Use a tuple for fixed values such as a screen resolution `(1920, 1080)`.

**Q3. What is a dictionary, and where do you use it in automation?**
A dictionary stores key-value pairs, for example `{"username": "admin", "password": "Admin@123"}`. It is used for rows of test data, configuration settings and locator maps. Use `.get()` to read a key safely.

**Q4. What is the difference between `==` and `is`?**
`==` checks whether two values are **equal**. `is` checks whether two names point to the **same object** in memory. Use `is` mainly with `None` (`if value is None:`).

**Q5. What is the difference between `/` and `//`?**
`/` is true division and always returns a float (`7 / 2 = 3.5`). `//` is floor division and returns the whole-number part (`7 // 2 = 3`).

**Q6. What is the difference between `break` and `continue`?**
`break` exits the loop completely. `continue` skips the rest of the current round and moves to the next item.

**Q7. What is the difference between `print` and `return` in a function?**
`print` only shows a value on the screen. `return` sends the value back to the caller so that it can be stored, compared or used. A function without `return` returns `None`.

**Q8. What are class and object?**
A class is a blueprint that defines attributes and methods. An object is an instance created from that class, with its own data. For example, `LoginPage` is a class, and `login_page = LoginPage()` creates an object.

**Q9. What is `__init__` and what is `self`?**
`__init__` is the constructor. It runs automatically when an object is created and sets up the initial attributes. `self` refers to the current object. Python passes it automatically as the first argument of every instance method.

**Q10. Explain inheritance with an automation example.**
Inheritance lets a child class reuse a parent class's code. In a framework, `BasePage` contains common methods such as `open()`, `take_screenshot()` and `verify_title()`. `LoginPage(BasePage)` inherits them and adds `enter_username()` and `click_login()`. Common code is written once.

**Q11. What is encapsulation, and how is it done in Python?**
Encapsulation bundles data with the methods that control it, and protects the data from invalid changes. Python uses conventions: `_name` is protected, and `__name` is private (name-mangled). It also uses `@property` getters and setters for validation or read-only access.

**Q12. What is method overriding?**
A child class defines a method with the same name as a method in the parent class, in order to change its behaviour. It can still call the parent version with `super().method_name()`.

**Q13. Why is OOP important in automation frameworks?**
It gives structure (the Page/Window Object Model) and reuse (base classes), and it makes maintenance easy: a UI change is fixed in one class instead of many tests. It also makes tests readable and lets teams work on different screens in parallel.

**Q14. What is the difference between a syntax error, a runtime error and a logic error?**
A syntax error breaks Python's grammar rules, so the program does not start (for example, a missing colon). A runtime error (exception) happens while the program is running (for example, `KeyError` or `ZeroDivisionError`). A logic error gives a wrong result without any error message (for example, a wrong condition order). Logic errors are the hardest to find.

**Q15. Explain try, except, else and finally.**
`try` holds code that might fail. `except` handles a specific error. `else` runs only when no error happened. `finally` always runs and is used for cleanup, such as closing the application under test or closing files.

**Q16. Why should you avoid `except: pass` in test scripts?**
It silently swallows every error, including real failures and your own bugs. The test then reports PASS when something actually broke (a false positive). Catch specific exceptions and report or re-raise them.

**Q17. What is the difference between Step Over and Step Into in a debugger?**
Step Over (F10 in VS Code) runs the current line completely, including any function it calls, and stops at the next line. Step Into (F11) goes inside the function being called, so you can debug it line by line.

**Q18. How do you read a Python traceback?**
Start from the **last line**, which gives the error type and message. Then look at the frame above it, which gives the file, the line number and the function where the error happened. The earlier frames show the chain of calls that led there.

---

## 23. Quick Reference Card

```python
# Variables and types
name = "Notepad"; count = 3; secs = 1.5; ok = True; defect = None

# Strings
f"{name} took {secs:.2f}s"   s.strip()  s.upper()  "x" in s  s.replace(a, b)

# Collections
lst = [1, 2]; lst.append(3); lst[0]; lst[-1]; len(lst)
d = {"k": "v"}; d["k"]; d.get("x", "default"); d.items()

# Conditions
if a == b: ...
elif a > b: ...
else: ...
result = "PASS" if ok else "FAIL"

# Loops
for item in items: ...
for i, item in enumerate(items, start=1): ...
for k, v in d.items(): ...
while condition and attempt < 5: ...
break / continue

# Functions
def verify(expected, actual, strict=True):
    return expected == actual

# Classes
class Child(Parent):
    def __init__(self, x):
        super().__init__()
        self.x = x
    def action(self):
        return self.x

# Exceptions
try: ...
except ValueError as e: ...
else: ...
finally: ...
raise ValueError("message")
```

**VS Code debugging keys:** `F9` breakpoint | `F5` start/continue | `F10` step over | `F11` step into | `Shift+F11` step out | `Shift+F5` stop

---

*End of Day 1 handbook. Next: automating real Windows desktop applications.*
