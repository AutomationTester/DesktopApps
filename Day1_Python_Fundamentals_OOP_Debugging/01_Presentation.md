---
marp: true
theme: default
paginate: true
---

# Python Desktop Application Automation Testing

## Day 1: Python Fundamentals, OOP and Debugging

From manual tester to automation engineer - step 1

<!-- Trainer notes: Welcome everyone. Introduce yourself and your testing background. Ask each participant for their name, current role, the application they test, and whether they have written any code before. Most of them will say "no coding". Tell them that is fine: today is designed for people who have never written Python. Explain the one rule for the day: "type every example yourself - do not only watch". -->

---

# Day 1 Agenda (09:00 - 17:00)

| Time | Session |
|------|---------|
| 09:00 - 09:15 | Welcome and objectives |
| 09:15 - 09:50 | Python and automation, Desktop/CLI overview, setup |
| 09:50 - 10:45 | Syntax, variables, data types, operators |
| 10:45 - 11:00 | **Tea break** |
| 11:00 - 11:55 | Conditions, loops, functions |
| 11:55 - 12:35 | **Lab 1:** Calculator using functions |
| 12:35 - 13:15 | **Lunch** |
| 13:15 - 14:15 | OOP concepts for automation |
| 14:15 - 15:00 | **Lab 2:** OOP business logic |
| 15:00 - 15:15 | **Tea break** |
| 15:15 - 16:00 | Debugging and exception handling |
| 16:00 - 16:45 | **Lab 3:** Debugging faulty scripts |
| 16:45 - 17:00 | Recap, quiz, Q&A |

<!-- Trainer notes: Walk through the agenda quickly. Point out that roughly 40% of the day is hands-on. The quiz (03_Quiz.md) can be done in the last 15 minutes, or given as homework if the labs run over. Tell them breaks are fixed, so they can plan calls around them. -->

---

# By the end of today you will be able to

- Write and run Python scripts in VS Code
- Use variables, data types, operators, conditions and loops
- Write reusable **functions**
- Build **classes and objects** - the base of every framework
- Read error messages and **debug** with breakpoints
- Handle failures safely with **try / except / finally**

<!-- Trainer notes: Connect each outcome to their daily work. Test data = variables and lists. Test steps = functions. Pages/windows = classes. Defect analysis = debugging. Tell them Day 2 onwards will use today's skills to automate real desktop apps with pywinauto and pyautogui, so today is the foundation. -->

---

# Where Day 1 fits in the course

1. **Day 1:** Python, OOP, debugging  <- *you are here*
2. Day 2+: Desktop automation tools (pywinauto, pyautogui)
3. Later days: Frameworks, pytest, reports, image-based automation

Today = **the language**. The next days = **the tools**.

<!-- Trainer notes: Use an analogy: before you drive a car on the highway (automation tools), you must learn to steer and brake (the Python language). Without Day 1, the tools on later days will look like magic and be hard to fix when they break. -->

---

<!-- _class: lead -->

# Part 1
## Python Fundamentals for Automation

<!-- Trainer notes: Section divider. Takes about 3 hours including Lab 1. -->

---

# What is Python?

- A **simple, readable** programming language (1991, Guido van Rossum)
- Code reads almost like English
- **Free**, open source, runs on Windows, Linux and macOS
- Huge library ecosystem - "batteries included"
- One of the most used languages in test automation

```python
if actual_title == "Calculator":
    print("PASS")
```

<!-- Trainer notes: Show the snippet and ask: "Who can guess what this does?" Almost everyone will understand it. That is the key selling point for testers. Mention it is interpreted: no compile step, you write and run. -->

---

# Why Python for test automation?

- **Easy to learn** - ideal for manual testers moving to automation
- **Less code** - the same test takes fewer lines than in Java or C#
- **Rich tools:** pywinauto, pyautogui, pytest, Selenium, Playwright, requests
- **One language** for desktop, web, API, CLI and data tasks
- Strong community - most error messages are easy to search online

<!-- Trainer notes: Common question: "Is Python better than Java for automation?" Answer: both are good. Python is faster to learn and has excellent desktop tools (pywinauto). Many companies use Python for automation even when the product is written in another language. -->

---

# Automation use cases for testers

| Use case | Example |
|----------|---------|
| Desktop GUI testing | Log in to a billing app, create an invoice |
| CLI testing | Run `app.exe --version`, check the output |
| Test data | Generate 1,000 customer records |
| Log checks | Search logs for "ERROR" after a run |
| Reports | Build an HTML test report automatically |
| Regression | Re-run 300 tests every night |

<!-- Trainer notes: Ask the group: "Which repetitive task in your current project would you automate first?" Write 3-4 answers on the whiteboard and refer back to them during the day. -->

---

# Desktop and CLI automation - overview

**Desktop (GUI) automation**
- Controls Windows apps: windows, buttons, text boxes, menus
- **Object-based:** pywinauto (reads controls by name/ID)
- **Image-based:** pyautogui + OpenCV (finds things on screen)

**CLI automation**
- Runs command-line tools from a script: `subprocess`
- Checks the exit code and the output text

<!-- Trainer notes: Explain the difference simply. Object-based automation asks Windows "give me the button named Save" - reliable. Image-based automation looks at pixels - flexible but fragile (resolution, theme). CLI testing is the easiest to automate and is often forgotten. We start both properly from Day 2. -->

---

# Demo: CLI automation preview

```python
import subprocess, sys

result = subprocess.run([sys.executable, "--version"],
                        capture_output=True, text=True)
print("Exit code:", result.returncode)     # 0 = success
print("Output   :", result.stdout.strip())
```

**Run:** `examples/02_cli_automation_preview.py`

<!-- Trainer notes: Run examples/02_cli_automation_preview.py. Show that the script collects environment details (OS, Python version, machine name), which testers put in every test report. Then it runs a command and marks PASS/FAIL. Do not explain every line yet. The goal is to show "this is what automation looks like". -->

---

# Installing Python on Windows

1. Download from **python.org/downloads** (Python 3.12 or newer)
2. Run the installer and tick **"Add python.exe to PATH"**
3. Verify it in a new terminal:

```
python --version
pip --version
```

4. Install packages with pip: `pip install pytest`

<!-- Trainer notes: Most training machines are already set up (Python 3.14 is installed). Still, show the installer screen, because trainees will install it at their workplace. The number one setup problem is forgetting "Add to PATH". Symptom: 'python' is not recognized. Fix: re-run the installer, choose Modify, and tick the option. Also mention the "py" launcher on Windows as an alternative. -->

---

# IDE setup - VS Code (recommended)

- Install **VS Code** from code.visualstudio.com
- Install the **Python** extension (Microsoft) - it includes the debugger
- **File > Open Folder** -> open the course folder
- Select the interpreter: `Ctrl+Shift+P` -> *Python: Select Interpreter*
- Run a file: the **Run** button, or `python file.py` in the terminal

**PyCharm Community** is a good alternative (right-click -> Run)

<!-- Trainer notes: Live demo: open the Day1 folder in VS Code and show the Explorer, the editor, the terminal (Ctrl+`) and the Run button. Show the interpreter in the status bar (bottom right). PyCharm users: the concepts are the same - Run with Shift+F10, Debug with Shift+F9. Let trainees choose, but support VS Code for the labs. -->

---

# Virtual environments (good practice)

```
python -m venv .venv
.venv\Scripts\activate
pip install pywinauto pytest
pip freeze > requirements.txt
```

- Keeps each project's packages **separate**
- `requirements.txt` = the list of packages to reinstall anywhere

<!-- Trainer notes: Keep it short - awareness only. On Day 1 we use only the standard library, so no venv is needed. If PowerShell blocks activate.ps1, run: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned. Real projects always use a venv plus requirements.txt. -->

---

# Your first Python program

```python
# This is a comment - Python ignores it
print("Hello, Automation World!")
print("Day:", 1)
```

Run it:
```
python 01_first_program.py
```

<!-- Trainer notes: Run examples/01_first_program.py. Then ask everyone to create hello.py and type the print line themselves. Walk around the room and check. Common mistakes: Print with a capital P, missing quotes, saving the file as hello.py.txt. -->

---

# Python syntax rules

- **Indentation** (4 spaces) groups code - no `{ }`
- A line that starts a block ends with a **colon** `:`
- **Case-sensitive:** `Title` and `title` are different
- `#` starts a comment
- One statement per line - no `;` needed

```python
if app_is_open:
    print("Window is open")      # inside the if
print("Always printed")          # outside the if
```

<!-- Trainer notes: Indentation is the biggest surprise for beginners. Show what happens when you remove the indent: IndentationError. VS Code inserts 4 spaces automatically when you press Tab. Tell them never to mix tabs and spaces. -->

---

# Variables

- A variable is a **name** that points to a **value**
- There is no type declaration - Python works out the type
- Use `snake_case` and meaningful names

```python
test_case_id = "TC_LOGIN_001"
retry_count = 3
response_time = 1.75
is_passed = True
```

<!-- Trainer notes: Analogy: a variable is a label stuck on a box. You can move the label to another box (re-assign). Good names: expected_title, max_wait. Bad names: x, a1, data2. Rules: cannot start with a number, no spaces, not a keyword (if, for, class). -->

---

# Basic data types

| Type | Example | Used for |
|------|---------|----------|
| `str` | `"Notepad"` | titles, labels, messages |
| `int` | `3` | counts, retries |
| `float` | `1.75` | time, amounts |
| `bool` | `True` / `False` | pass/fail flags |
| `None` | `None` | "no value yet" |

```python
print(type(retry_count))   # <class 'int'>
```

<!-- Trainer notes: Run the first part of examples/03_variables_datatypes.py. Stress that True/False and None start with a capital letter. type() is a good debugging tool - use it when a value behaves strangely. -->

---

# Strings - the tester's favourite type

```python
title = "Untitled - Notepad"
title.upper()                 # 'UNTITLED - NOTEPAD'
len(title)                    # 18
"Notepad" in title            # True
title.replace("Untitled", "report.txt")
title[0:8]                    # 'Untitled'
f"{tester} ran {test_id}"     # f-string
```

<!-- Trainer notes: Most GUI verification is string checking: window titles, labels, error messages. Spend time on f-strings, because we use them everywhere. Mention strip() for removing extra spaces - a very common source of false failures. -->

---

# Type conversion

- Text from screens and files arrives as **str**
- Convert it before you do maths

```python
qty_text = "42"
int(qty_text) + 8        # 50
str(3) + " retries"      # '3 retries'
float("99.5")            # 99.5
int("12a")               # ValueError!
```

<!-- Trainer notes: Common trainee question: "Why does '5' + '5' give '55'?" Because both are strings, and + joins strings. This comes back in the debugging lab (lab3_bug3). -->

---

# Collections: list, tuple, dict, set

```python
results = ["PASS", "FAIL", "PASS"]       # list  - ordered, changeable
results.append("SKIP"); results[0]       # index starts at 0

resolution = (1920, 1080)                # tuple - fixed

login = {"username": "admin",            # dict  - key: value
         "password": "Admin@123"}
login["username"]

browsers = {"Chrome", "Edge", "Chrome"}  # set   - unique values
```

<!-- Trainer notes: Run the rest of examples/03_variables_datatypes.py. Test-data rows are dictionaries, and a test suite is a list. Show negative indexing: results[-1] is the last item. Show dict.get() as a safe way to read a key that may be missing. -->

---

# Operators - arithmetic

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+ - *` | add, subtract, multiply | `10 * 3` | `30` |
| `/` | divide (float) | `10 / 3` | `3.33...` |
| `//` | floor divide | `10 // 3` | `3` |
| `%` | remainder | `10 % 3` | `1` |
| `**` | power | `2 ** 5` | `32` |

```python
pass_pct = passed / total * 100
print(f"{pass_pct:.2f}%")
```

<!-- Trainer notes: Run examples/04_operators.py. Point out that / always returns a float. Use of %: "take a screenshot every 5th step" (step % 5 == 0). Also mention += as a shortcut: retry += 1. -->

---

# Operators - comparison and logical

```python
expected == actual        # equal
expected != actual        # not equal
response_time < 3         # <, >, <=, >=

username_ok and password_ok   # both must be True
is_admin or is_manager        # at least one True
not window_found              # reverses the value

"Edit" in menu_items          # membership
defect_id is None             # identity (use with None)
```

<!-- Trainer notes: Comparison operators always return True/False - every test assertion is one of these. The classic mistake is = vs ==. Draw a quick truth table for and/or. Ask: "Build is accepted if pass% >= 80 AND failures < 5. Write it in Python." Answer is in the demo file. -->

---

# Conditional statements - if / elif / else

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

- Python checks from the **top** and runs the **first** True block only

<!-- Trainer notes: Run examples/05_conditionals.py. Emphasise the ORDER: the first True condition wins. The logic-error lab (lab3_bug4) has exactly this bug. Ask: "What happens if we put <= 5 first?" -->

---

# Conditions in testing

```python
if actual_status == expected_status:
    print("PASS")
else:
    print(f"FAIL: expected {expected_status}, got {actual_status}")

result = "PASS" if response_time <= 3 else "FAIL"   # one-line if
```

- Empty values are **falsy:** `""`, `0`, `[]`, `None`
- `match / case` (Python 3.10+) is useful for fixed choices

<!-- Trainer notes: Show nested if (window found -> correct title?) and match/case for choosing the environment (DEV/QA/PROD) - both are in examples/05_conditionals.py. Truthy/falsy: "if error_message:" means "if there is any error text". -->

---

# Loops - for

```python
test_cases = ["TC_001 Login", "TC_002 Logout", "TC_003 Search"]

for test in test_cases:
    print("Executing:", test)

for step in range(1, 4):          # 1, 2, 3 (4 is not included)
    print(f"Step {step}")

for i, test in enumerate(test_cases, start=1):
    print(i, test)
```

<!-- Trainer notes: Run examples/06_loops.py. A for loop is the heart of data-driven testing: the same steps run for each row of data. range(stop) does not include stop - that causes off-by-one bugs. -->

---

# Data-driven testing with a loop

```python
login_data = [
    {"user": "admin", "pwd": "Admin@123", "expected": "success"},
    {"user": "admin", "pwd": "wrong",     "expected": "failure"},
]
for row in login_data:
    actual = login(row["user"], row["pwd"])
    print("PASS" if actual == row["expected"] else "FAIL")
```

<!-- Trainer notes: This is a key "aha" moment for testers. One test script plus a table of data gives many test cases. The same idea is used in pytest parametrize and in Excel-driven frameworks later in the course. -->

---

# Loops - while, break, continue

```python
attempt = 0
while not window_ready and attempt < 5:    # wait / poll
    attempt += 1
    window_ready = check_window()

for status in statuses:
    if status == "CRITICAL":
        break        # stop the loop
    if status == "SKIP":
        continue     # jump to the next item
```

<!-- Trainer notes: while = "repeat until something changes" - perfect for waiting for a window to appear. ALWAYS have an exit condition (max attempts), or you get an infinite loop. If that happens, press Ctrl+C in the terminal to stop it. -->

---

# Functions - why?

- A **named, reusable** block of code
- Write once, call many times
- Change it in **one** place, and it is fixed everywhere
- Makes scripts short and readable

```python
def verify_equal(expected, actual):
    return "PASS" if expected == actual else "FAIL"

verify_equal("Login", "Login")    # 'PASS'
```

<!-- Trainer notes: Analogy: a function is a reusable test step, like a "Login" step in a manual test case that many other test cases refer to. Without functions, you copy-paste code, and one change means editing 50 places. -->

---

# Functions - parameters and return values

```python
def log(message, level="INFO"):           # default value
    print(f"[{level}] {message}")

def summarize(results):
    passed = results.count("PASS")
    failed = results.count("FAIL")
    return passed, failed                  # returns a tuple

log("Test started")
log("Disk low", level="WARNING")           # keyword argument
p, f = summarize(["PASS", "FAIL", "PASS"])
```

<!-- Trainer notes: Run examples/07_functions.py. Explain print vs return: print only shows a value on screen, while return gives the value back to the caller so it can be used. A function without a return gives back None - this appears in Lab 1. Mention type hints as optional documentation: def is_within_sla(t: float) -> bool. -->

---

# Functions - scope and built-ins

- Variables created inside a function are **local** to it
- Useful built-ins: `len()`, `min()`, `max()`, `sum()`, `sorted()`, `round()`, `type()`

```python
times = [1.2, 0.8, 2.9]
print(max(times), round(sum(times), 2))
```

- Put reusable functions in one file and **import** them (framework style)

<!-- Trainer notes: Keep scope simple: what happens inside a function stays inside it. Tell them that on later days, helper functions will live in a utils.py file and be imported. -->

---

# Lab 1 - Calculator using functions (40 min)

- File: `hands_on/starter/lab1_calculator.py`
- Complete `subtract`, `multiply`, `divide`, `power`, `modulus`
- Build `calculate(a, operator, b)` using a dictionary of functions
- A built-in **self-test** shows PASS/FAIL for each case
- Goal: **Passed 9/9**

See `hands_on/Lab_Guide.md` - Lab 1

<!-- Trainer notes: Show the starter running with all FAILs and actual=None. Explain that this is test-driven: the tests exist, and trainees make them pass. Walk around the room. Typical issues: forgetting return, writing add() instead of add in the dict, the float comparison in CALC_07. Fast finishers: stretch goals (interactive mode). Solution: hands_on/solutions/lab1_calculator.py. -->

---

<!-- _class: lead -->

# Part 2
## OOP Concepts Using Python

<!-- Trainer notes: Section divider after lunch. Energy is low after lunch - keep this interactive and ask many questions. -->

---

# Why OOP is critical for automation frameworks

- Real frameworks have **hundreds** of tests and screens
- OOP groups **data + actions** into one unit (a class)
- **Page/Window Object Model:** one class per screen
- **Reuse** through inheritance (BasePage -> LoginPage)
- **Maintenance:** if the UI changes, fix one class, not 100 tests
- pywinauto, pytest and Selenium are all built with classes

<!-- Trainer notes: Tell a story: "The Login button's ID changed. In a script without OOP, you edit 120 test files. With a LoginPage class, you edit one line." This is the single most important reason to learn OOP as an automation engineer. -->

---

# Without OOP vs with OOP

```python
# Without OOP - loose variables, easy to mix up
tc1_id, tc1_title, tc1_status = "TC_001", "Login", "Not Run"
tc2_id, tc2_title, tc2_status = "TC_002", "Logout", "Not Run"

# With OOP - one blueprint, many objects
tc1 = TestCase("TC_001", "Login")
tc2 = TestCase("TC_002", "Logout")
tc1.mark("PASS")
```

<!-- Trainer notes: Ask: "Imagine 500 test cases using the first style. How do you find all failed ones?" With objects, you keep a list of TestCase objects and loop over it. -->

---

# Class and Object

- **Class** = blueprint / template (the design)
- **Object** = a real thing made from the class (an instance)
- One class -> many objects, each with its **own data**

```python
class TestCase:
    def __init__(self, test_id, title):
        self.test_id = test_id
        self.title = title
        self.status = "Not Run"

tc1 = TestCase("TC_001", "Login with valid user")
```

<!-- Trainer notes: Analogy: the class is a blank test case template in your test management tool; objects are the filled-in test cases TC_001, TC_002. Run examples/08_classes_objects.py. Point out that they already use objects: "abc".upper() calls a method on a str object. Class names use CamelCase. -->

---

# Constructor - `__init__`

- A special method that runs **automatically** when an object is created
- Sets up the object's **starting state**
- `self` = "this object" - Python passes it for you

```python
class AppWindow:
    def __init__(self, title, width=800, height=600):
        self.title = title
        self.width = width
        self.is_open = False

calc = AppWindow("Calculator", 400)   # __init__ runs here
```

<!-- Trainer notes: The double underscores are called "dunder". Explain self slowly: when you write calc.open(), Python actually calls AppWindow.open(calc). So self is calc. Every method needs self as its first parameter - forgetting it is a classic bug (lab3_bug5). -->

---

# Attributes

- **Instance attribute:** belongs to one object -> `self.title`
- **Class attribute:** shared by all objects -> `AppWindow.window_count`

```python
class AppWindow:
    window_count = 0                 # class attribute

    def __init__(self, title):
        self.title = title           # instance attribute
        AppWindow.window_count += 1

print(calc.title, AppWindow.window_count)
```

<!-- Trainer notes: Run examples/09_constructor_methods_attributes.py. Show that changing notepad.title does not affect calc.title. The class attribute is a counter shared by everyone. -->

---

# Methods

- A **method** = a function defined inside a class
- Describes what an object can **do**
- Can read or change the object's attributes and **return** values

```python
    def open(self):
        self.is_open = True

    def has_control(self, name):
        return name in self.controls

calc.open()
calc.has_control("Button_Plus")      # True
```

<!-- Trainer notes: Attributes = what an object HAS (nouns). Methods = what an object DOES (verbs). For a window: HAS title, size, controls; DOES open, close, maximize. Also show __str__ - it controls what print(obj) shows. -->

---

# Inheritance (basic)

- A **child** class gets all attributes and methods of a **parent**
- The child can **add** new methods or **override** existing ones
- `super()` calls the parent's version

```python
class BasePage:
    def take_screenshot(self, name): ...

class LoginPage(BasePage):           # LoginPage IS-A BasePage
    def __init__(self):
        super().__init__("Login - Billing App")
    def click_login(self): ...
```

<!-- Trainer notes: Run examples/10_inheritance.py. This is exactly the structure of a real framework: BasePage holds common things (open, screenshot, verify_title), and each screen class adds its own actions. Write common code once in the parent. -->

---

# Method overriding

```python
class DashboardPage(BasePage):
    def open(self):                       # same name as the parent
        super().open()                    # do the parent's work
        self.log_action("Waiting for widgets to load")
```

- `isinstance(login, BasePage)` -> `True`
- `issubclass(LoginPage, BasePage)` -> `True`

<!-- Trainer notes: Overriding = same method name, new behaviour. Calling super().open() keeps the parent behaviour and adds to it. Common question: "Can a class have two parents?" Yes (multiple inheritance), but avoid it for now - keep hierarchies simple. -->

---

# Encapsulation (basic)

- Keep data and the code that **protects** it together
- Do not let outside code set **invalid** values

| Name | Meaning |
|------|---------|
| `self.name` | public |
| `self._name` | protected - "internal, please don't touch" |
| `self.__name` | private - name-mangled |

<!-- Trainer notes: Python trusts developers: these are conventions, not hard locks. A single underscore is a polite "do not touch". A double underscore renames the attribute to _ClassName__name so outside code cannot reach it easily. -->

---

# Encapsulation with @property

```python
class TestConfig:
    def __init__(self, timeout):
        self.timeout = timeout            # goes through the setter

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        if value <= 0:
            raise ValueError("timeout must be positive")
        self._timeout = value
```

<!-- Trainer notes: Run examples/11_encapsulation.py. config.timeout = -5 is rejected, and config.__password cannot be read directly. In frameworks: protect config values, never print passwords, and keep a clean public interface. -->

---

# Automation-oriented OOP example

```
FakeCalculatorApp   -> the app under test (simulated)
BaseScreen          -> common actions (parent)
CalculatorScreen    -> screen object: clear(), enter(), equals()
TestResult          -> one test's outcome
TestRunner          -> runs data, prints the report
```

**Run:** `examples/12_automation_oop_example.py`

<!-- Trainer notes: Run the script. Show the layers: test data -> runner -> screen object -> app. On Day 2 we replace FakeCalculatorApp with real pywinauto code, but the test layer stays the same. CALC_04 fails on purpose (4 vs 4.0). Ask the class: "Is it an app bug or a test bug?" Good discussion: it is a test-data/expectation issue. -->

---

# OOP in a framework - the big picture

```python
screen = CalculatorScreen(app)       # object from a class
screen.clear()                       # methods = test steps
screen.enter("2+3")
screen.equals()
assert screen.read_display() == "5"
```

- Tests read like **manual test steps**
- UI details are hidden inside screen classes

<!-- Trainer notes: Stress readability: a business analyst can read this test. Mention assert briefly - pytest (later in the course) uses plain assert statements. -->

---

# Lab 2 - OOP business logic: PyBank (45 min)

- File: `hands_on/starter/lab2_bank_account.py`
- Rules R1-R7: deposit, withdraw, minimum balance, overdraft
- Uses: class, `__init__`, `@property`, inheritance, `super()`, overriding, custom exception
- 16 automated checks -> goal **Passed 16/16**

See `hands_on/Lab_Guide.md` - Lab 2

<!-- Trainer notes: Show the starter output (3/16). Explain that the checks are the "test cases" and the rules are the "requirements" - their normal world. Typical issues: forgetting return in deposit/withdraw, forgetting super().__init__ in SavingsAccount, wrong indentation of methods. Solution: hands_on/solutions/lab2_bank_account.py. -->

---

<!-- _class: lead -->

# Part 3
## Debugging Concepts

<!-- Trainer notes: Section divider. Testers are naturally good at this - they find defects for a living. Now they will find defects in their own scripts. -->

---

# Three kinds of errors

| Kind | When | Example |
|------|------|---------|
| **Syntax error** | Before running | missing `:` or `)` |
| **Runtime error (exception)** | While running | `KeyError`, `TypeError` |
| **Logic error** | Never "errors" | wrong result, no message |

- Runtime errors **shout** (traceback); logic errors **whisper**

<!-- Trainer notes: Logic errors are the most dangerous, because the script runs "fine" and reports wrong results. In automation, that means false PASS results - the worst kind of bug for a tester. -->

---

# Common Python errors

| Error | Typical cause |
|-------|---------------|
| `SyntaxError` / `IndentationError` | missing `:` `)` `"`, wrong spaces |
| `NameError` | typo in a variable name |
| `TypeError` | `"Total: " + 5`, missing argument |
| `ValueError` | `int("12a")` |
| `KeyError` / `IndexError` | missing dict key / list position |
| `AttributeError` | method or attribute does not exist |
| `ZeroDivisionError` | no tests executed -> divide by 0 |

<!-- Trainer notes: Run examples/13_common_errors.py - it triggers and catches each error so they can see the exact messages. Ask trainees to guess the error type before you show each one. -->

---

# Common automation errors

- `FileNotFoundError` - test data or config file missing
- `ModuleNotFoundError` - package not installed / misspelled
- **Element not found** - wrong locator, control not visible yet
- **Timeout / window not found** - app slow to start
- **Stale state** - window closed while the script still uses it
- **Resolution / scaling** - image-based matching fails

<!-- Trainer notes: The last four appear from Day 2 with pywinauto and pyautogui. The fix is usually proper waits and good locators, not adding time.sleep everywhere. ModuleNotFoundError: check pip install and that VS Code uses the right interpreter. -->

---

# Reading a traceback

```
Traceback (most recent call last):
  File "17_debugging_demo_buggy.py", line 37, in count_by_status
    counts[result["Status"]] += 1
           ~~~~~~^^^^^^^^^^
KeyError: 'Status'
```

1. Read the **last line** first -> error type and message
2. Look at the **file and line number** above it
3. Check that line (and sometimes the line **before** it)

<!-- Trainer notes: Run examples/17_debugging_demo_buggy.py and read the traceback together, from the bottom up. Tell them never to panic at a red traceback - it is a free defect report with the exact location. Keep this script open for the live debugging demo. -->

---

# Print-based debugging

```python
for index, status in enumerate(results):
    print(f"[DEBUG] {index=} {status=!r}")    # shows 'PASS ' with a space!
    if status == "PASS":
        passed += 1
```

- Print variable **names and values:** `f"{total=}"`
- Use `!r` to reveal hidden spaces
- Use a `DEBUG` flag or the `logging` module

<!-- Trainer notes: Run examples/14_print_debugging.py. The bug: 'PASS ' (trailing space) and 'pass' (lowercase) are not counted. The debug prints make it obvious, and the fix is strip().upper(). Show the logging output with levels and timestamps. Remind them to remove debug prints before committing code. -->

---

# IDE debugging - breakpoints

- **Breakpoint** = a red dot in the gutter; execution **pauses** there
- Press **F5** -> *Python Debugger: Current File*
- Inspect the **Variables**, **Watch** and **Call Stack** panels
- **Conditional breakpoint:** pause only when `qty > 5`

**Practice file:** `examples/15_ide_debugging_walkthrough.py`

<!-- Trainer notes: Live demo in VS Code. Set a breakpoint on the line marked BREAKPOINT 1, press F5, and show the Variables panel. Add invoice_total to the Watch panel. Right-click the red dot -> Edit Breakpoint -> Expression -> qty > 5. Mention that breakpoint() in code does the same thing from the terminal (pdb). -->

---

# Step over, step into, step out

| Key (VS Code) | Action | Meaning |
|---------------|--------|---------|
| **F10** | Step Over | run this line, do not go into functions |
| **F11** | Step Into | go **inside** the called function |
| **Shift+F11** | Step Out | finish this function, go back |
| **F5** | Continue | run to the next breakpoint |
| **Shift+F5** | Stop | end the debug session |

PyCharm: F8 over, F7 into, Shift+F8 out, F9 resume

<!-- Trainer notes: Demonstrate on calculate_invoice(): F10 on the line_total call runs it in one go; F11 enters line_total so you can watch gross, discount and net. Then fix examples/17_debugging_demo_buggy.py live, using traceback + prints + breakpoints. The answer is in 17_debugging_demo_fixed.py (4 bugs: KeyError, TypeError, 2 logic errors). -->

---

# Exception handling - try / except

```python
try:
    value = int(text_from_screen)
except ValueError:
    print("Not a number - test marked FAIL")
```

- `try` -> code that **might** fail
- `except` -> what to do **if** it fails
- Catch **specific** errors first

<!-- Trainer notes: Run examples/16_exception_handling.py. Exceptions let a test suite continue after one test fails, instead of the whole run crashing. -->

---

# try / except / else / finally

```python
try:
    launch_app()
    run_steps()
except RuntimeError as error:
    print(f"FAIL - {error}")
else:
    print("PASS")                 # only if there was no error
finally:
    close_app()                   # ALWAYS runs
```

- `finally` = cleanup: close the app, files, take the last screenshot

<!-- Trainer notes: finally is critical in desktop automation. If a test fails halfway, you still must close the application, otherwise the next test starts with a dirty screen. Later, pytest fixtures do this job, but the idea is the same. -->

---

# raise and custom exceptions

```python
class WindowNotFoundError(Exception):
    """Expected window is not present."""

def find_window(title, open_windows):
    if title not in open_windows:
        raise WindowNotFoundError(f"Window '{title}' not found")
    return title
```

- `raise` -> fail **loudly** with a clear message
- Custom exceptions make reports **readable**

<!-- Trainer notes: A custom exception is a class that inherits from Exception - OOP and exceptions together. Also show the retry pattern in the demo file. -->

---

# Exception handling - best practices

- Catch **specific** exceptions, not a bare `except:`
- **Never** write `except: pass` in test code - it hides failures
- Put cleanup in `finally` (or use `with` blocks)
- Use clear messages: *what* failed and *where*
- In tests, a failure must be **visible** in the report

<!-- Trainer notes: Tell a real-world story: a framework with "except: pass" reported 100% PASS for months while the app was broken. Swallowing exceptions creates false passes. -->

---

# Lab 3 - Debugging faulty scripts (45 min)

| File | Bug type |
|------|----------|
| `lab3_bug1_syntax_error.py` | 4 syntax errors |
| `lab3_bug2_key_error.py` | 2 KeyErrors |
| `lab3_bug3_type_error.py` | 3 TypeErrors |
| `lab3_bug4_logic_error.py` | 3 logic errors |
| `lab3_bug5_oop_error.py` | Bonus: OOP mistakes |

Method: **run -> read the last line -> fix one -> run again**

<!-- Trainer notes: Each starter file shows its expected output in the docstring. Insist that trainees use the debugger (F10/F11) for bug file 4 - the logic errors - not just guessing. The bug explanations are in Lab_Guide.md (collapsed sections), and the fixed versions are in hands_on/solutions. Labs 4 and 5 are extra practice or homework. -->

---

# Day 1 recap

- **Python basics:** syntax, variables, types, operators, `if`, loops
- **Functions:** reusable test steps with parameters and return values
- **OOP:** class, object, `__init__`, methods, inheritance, encapsulation
- **Debugging:** tracebacks, print/logging, breakpoints, F10/F11
- **Exceptions:** `try / except / else / finally`, `raise`

<!-- Trainer notes: Ask 5 quick questions around the room: (1) list vs dict? (2) what does __init__ do? (3) what is self? (4) step over vs step into? (5) when does finally run? Then run the quiz (03_Quiz.md) or give it as homework. -->

---

# Homework and preparation for Day 2

- Finish Labs 1-3; try Labs 4 and 5 (extra practice)
- Take the Day 1 quiz: `03_Quiz.md`
- Read `02_Reading_Material.md` (including the interview questions)
- Check your setup: `pip show pywinauto pyautogui`

**Day 2:** automating real Windows desktop applications

<!-- Trainer notes: Ask trainees to make sure pywinauto and pyautogui are installed before Day 2 (they are already installed on the training machines). Share the reading material. Encourage them to re-type the examples, not copy-paste them. -->

---

# Questions and Answers

Thank you!

*"Automation does not replace testers - it frees them to test smarter."*

<!-- Trainer notes: Open the floor. Parking-lot questions that need longer answers can be covered at the start of Day 2. Collect quick feedback: one thing that was clear, one thing that was confusing. Use the feedback to plan a 10-minute recap at the start of Day 2. -->
