# Day 4 Reading Material
## Automation Framework Enhancements, Logging, PyTest and AI Basics

*Trainee handbook for the course "Python Desktop Application Automation Testing".*

---

## Table of Contents

1. [From scripts to a framework](#1-from-scripts-to-a-framework)
2. [Modular framework design](#2-modular-framework-design)
3. [Reusable utilities, configuration and environments](#3-reusable-utilities-configuration-and-environments)
4. [Window Object Model (POM for desktop apps)](#4-window-object-model-pom-for-desktop-apps)
5. [Logging in automation](#5-logging-in-automation)
6. [PyTest: why, and how a run works](#6-pytest-why-and-how-a-run-works)
7. [Fixtures, scopes and conftest.py](#7-fixtures-scopes-and-conftestpy)
8. [Assertions, parameterization and markers](#8-assertions-parameterization-and-markers)
9. [HTML & Allure reports and capturing evidence on failure](#9-html--allure-reports-and-capturing-evidence-on-failure)
10. [PyTest command-line cheat-sheet](#10-pytest-command-line-cheat-sheet)
11. [AI basics for automation](#11-ai-basics-for-automation)
12. [Common mistakes](#12-common-mistakes)
13. [Day 4 summary](#13-day-4-summary)
14. [Questions and answers](#14-questions-and-answers)

Files referenced in this handbook:

| Path | What it is |
|------|------------|
| `examples/01..08_*.py` | Small, self-contained demos (no GUI needed) |
| `examples/pytest_demo/` | Mini pytest project (fixtures, parametrize, markers, reports) |
| `examples/ai_prompt_examples.md` | Prompt templates and a review checklist |
| `hands_on/` | Labs: starter code with TODOs and full solutions |
| `../automation_framework/` | The course framework (used on Day 4 and Day 5) |

---

## 1. From scripts to a framework

On Day 2 you wrote *scripts*: one file that launches Calculator, clicks buttons and prints a result. Scripts are fine for learning. As a suite grows to hundreds of tests, they cause trouble:

- The same "open the app" code is copied into every file.
- Locators (`auto_id="num7Button"`) are spread across 50 tests. One UI change breaks all of them.
- `time.sleep(5)` makes suites slow, and they still fail on slower machines.
- Paths and timeouts are hard-coded for one PC.
- `print()` output disappears, so nobody can tell afterwards why a nightly run failed.

A **test automation framework** is a set of **conventions and reusable code** that makes tests easy to **write, read, run, debug and maintain**. It is not one tool. It combines a test runner (PyTest), a folder structure, helpers, configuration, logging and reporting.

> Most of the cost of automation is maintenance, not writing the first version. A framework exists to keep that maintenance cost low.

---

## 2. Modular framework design

### 2.1 Layers

```
 Tests            WHAT to verify      tests/test_calculator.py
   |  fixtures (conftest.py)
 Window objects   HOW to use the UI   pages/calculator_page.py
   |
 Core             engine              core/base_window.py, waits.py,
   |                                  logger.py, config_reader.py, cli_runner.py
 Utilities        helpers             utils/data_reader.py, screenshot.py
   |
 Config + Data    settings / inputs   config/config.yaml, test_data/*.csv
```

**Rule:** a layer only calls the layers **below** it. Tests never call pywinauto directly, and window objects never read CSV files.

### 2.2 The course framework

```
automation_framework/
  pytest.ini                 # markers: smoke, regression, desktop, cli; testpaths=tests
  config/config.yaml         # default_env + environments: dev, qa
  core/paths.py              # ROOT, CONFIG_DIR, TEST_DATA_DIR, LOG_DIR, REPORT_DIR, SCREENSHOT_DIR
  core/config_reader.py      # get_config(env=None)
  core/logger.py             # setup_logging(level, keep_last) + get_logger(name)
  core/waits.py              # wait_until(...), @retry(...)
  core/base_window.py        # BaseWindow: connect, find, click, read_text, wait_for_text, screenshot
  core/cli_runner.py         # run_command(cmd, timeout, cwd) -> CommandResult
  pages/calculator_page.py   # CalculatorPage(BaseWindow)
  pages/notepad_page.py      # NotepadPage(BaseWindow)
  utils/data_reader.py       # read_csv, read_json, read_yaml
  utils/screenshot.py        # take_screenshot(name) -> path
  tools/sysinfo_cli.py       # CLI "application under test"
  test_data/                 # calculator_data.csv, notepad_data.json, cli_cases.yaml
  tests/                     # conftest.py + test_calculator.py, test_notepad.py, test_cli.py
  logs/ reports/ screenshots/   (generated at run time)
```

### 2.3 Why modular?

| Change | Where you edit |
|--------|----------------|
| UI control renamed | One constant in `pages/` |
| QA server needs longer timeouts | `config/config.yaml` |
| 20 new data combinations | A CSV in `test_data/` |
| New log format | `core/logger.py` |
| New requirement | `tests/` |

**Try it yourself:** open `automation_framework/` and, for each folder, write one sentence that describes its single responsibility.

---

## 3. Reusable utilities, configuration and environments

### 3.1 Reusable helpers

Write a helper as soon as the **same code appears twice**. Good helpers:
- are small and named for what they do (`read_csv`, `run_command`, `take_screenshot`)
- contain **no test logic** (no asserts)
- log what they do
- take their settings as parameters or from config

```python
# core/cli_runner.py (course framework, shortened)
@dataclass
class CommandResult:
    command: list
    returncode: int
    stdout: str
    stderr: str
    duration: float

    @property
    def ok(self):
        return self.returncode == 0

def run_command(cmd, timeout=30, cwd=None, input_text=None):
    log.info("RUN: %s", " ".join(map(str, cmd)))
    start = time.monotonic()
    proc = subprocess.run([str(c) for c in cmd], capture_output=True, text=True,
                          timeout=timeout, cwd=cwd, input=input_text,
                          encoding="utf-8", errors="replace")
    return CommandResult(cmd, proc.returncode, proc.stdout, proc.stderr,
                         time.monotonic() - start)
```

The test becomes simple:

```python
result = run_command([sys.executable, str(TOOLS_DIR / "sysinfo_cli.py"), "info", "--json"])
assert result.ok, result.stderr
```

### 3.2 Central paths

```python
# core/paths.py
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
TEST_DATA_DIR = ROOT / "test_data"
LOG_DIR = ROOT / "logs"
```

`Path(__file__)` makes paths relative to *the file*, not to the folder you started Python from. This is the most common reason for "works in VS Code, fails in CI".

### 3.3 Configuration-driven frameworks

In a configuration-driven framework, **behaviour comes from a config file, not from code**. Anything that differs between machines or environments, or that you want to tune without changing code, belongs in config:

```yaml
default_env: dev
environments:
  dev:
    log_level: DEBUG
    timeouts: {app_start: 15, element: 10}
    retry: {times: 2, delay: 1}
    screenshots_on_failure: true
    calculator: {launch_cmd: calc.exe, window_title: Calculator}
    cli: {command_timeout: 30}
  qa:
    log_level: INFO
    timeouts: {app_start: 30, element: 15}
    retry: {times: 3, delay: 2}
    ...
```

Rules:
- Put the **same keys in every environment**.
- Load with `yaml.safe_load` (it never executes code from the file).
- Fail fast with a clear message for an unknown environment.
- **Never store secrets** in the YAML. Store the *name* of an environment variable instead (`password_env: APP_PASSWORD`) and read it with `os.environ`.

### 3.4 Environment handling

Priority used by `get_config(env=None)`:

| Priority | Source | Example |
|----------|--------|---------|
| 1 (highest) | Command-line option | `pytest --env qa` |
| 2 | Environment variable | `TEST_ENV=qa` |
| 3 | File default | `default_env: dev` |

```python
def get_config(env=None):
    data = _load_file()
    env = env or os.environ.get("TEST_ENV") or data["default_env"]
    try:
        settings = dict(data["environments"][env])
    except KeyError:
        raise ValueError(f"Unknown environment '{env}'. Available: {list(data['environments'])}") from None
    settings["env"] = env
    return settings
```

Setting an environment variable:

| Shell | Command |
|-------|---------|
| PowerShell | `$env:TEST_ENV="qa"; pytest` then `Remove-Item Env:TEST_ENV` |
| cmd.exe | `set TEST_ENV=qa && pytest` |
| bash / Git Bash | `TEST_ENV=qa pytest` |

**Try it yourself:** run `python examples/03_logger_config_from_yaml.py`, then `--env qa`, then set `TEST_ENV=qa`. Watch which log lines disappear.

---

## 4. Window Object Model (POM for desktop apps)

The **Page Object Model** (POM) comes from web testing: one class per web page. For desktop apps the idea becomes a **Window Object Model**: **one class per application window, dialog or screen**.

- The class holds the window's **locators** (as constants at the top of the file).
- It offers **business actions**: `calculate(a, op, b)`, `save()`, `login(user, pw)`.
- Tests call these actions and **never** use `child_window(...)` themselves.
- Common behaviour lives in a parent class, **`BaseWindow`** (Day 1 OOP: inheritance).

```
BaseWindow        connect, find, click, read_text, wait_for_text, press_keys, screenshot
 +-- CalculatorPage   open, clear, enter_number, press_operator, calculate, result, close
 +-- NotepadPage      open_file, type_text, text, save, saved_content, close_tab
```

```python
# core/base_window.py (course framework, shortened)
class BaseWindow:
    def __init__(self, config):
        self.config = config
        self.app_timeout = config["timeouts"]["app_start"]
        self.element_timeout = config["timeouts"]["element"]
        self.log = get_logger(f"pages.{type(self).__name__}")
        self.desktop = Desktop(backend="uia")
        self.window = None

    def connect(self, **criteria):
        self.window = self.desktop.window(**criteria)
        self.window.wait("visible", timeout=self.app_timeout)
        return self

    def find(self, **criteria):
        control = self.window.child_window(**criteria)
        control.wait("exists", timeout=self.element_timeout)
        return control

    def click(self, **criteria):
        control = self.find(**criteria)
        self.log.debug("Click %s", criteria)
        try:
            control.invoke()          # UI Automation, no mouse movement
        except Exception:
            control.click_input()     # fallback: real mouse click
```

```python
# pages/calculator_page.py (shortened)
OPERATOR_BUTTONS = {"+": "plusButton", "-": "minusButton",
                    "*": "multiplyButton", "/": "divideButton"}
EQUALS_BUTTON = "equalButton"
RESULT_TEXT = "CalculatorResults"

class CalculatorPage(BaseWindow):
    def calculate(self, a, operator, b):
        self.log.info("Calculate %s %s %s", a, operator, b)
        self.clear()
        self.enter_number(a)
        self.press_operator(operator)
        self.enter_number(b)
        self.press_equals()
        return self.result
```

The test reads like a manual test case:

```python
def test_addition(calculator):
    assert calculator.calculate(7, "+", 8) == 15
```

**Design rules**
1. Locators live only in window classes.
2. Window objects **return values**. **Tests assert.**
3. Every action waits for its control. No `sleep`.
4. Every action logs.

**Try it yourself:** in `hands_on/starter/mini_framework`, complete `CalculatorWindow` (Lab 1). It drives a simulated Calculator that has the same API as pywinauto.

---

## 5. Logging in automation

### 5.1 Why logging matters

Automated tests run **unattended**: overnight, in CI pipelines, on remote VMs. When something fails, the log is usually the only evidence. A good log answers:
- **Which step** failed, and what happened right before it?
- **Which data** and **which environment**?
- **How long** did each step take? (A 10-second gap usually means a wait timed out.)
- Is it an **application bug**, a **test bug**, or an **environment problem**?

### 5.2 print() vs logging

| `print()` | `logging` |
|-----------|-----------|
| No timestamp, level or source | Timestamp, level, logger name, function, line |
| Console only | Console, files, rotating files, network ... |
| All or nothing | Filter by level, per destination |
| Mixed with program output | Consistent, parseable format |

### 5.3 The logging module: Logger, Handler, Formatter

```
log.info("Calculator opened")
     |
  Logger "automation.pages.CalculatorPage"   (has a level)
     |   propagates up to its parent "automation"
  Handlers on "automation":
     StreamHandler -> console   (level INFO)
     FileHandler   -> logs/automation_20260926_101500.log (level DEBUG)
     |
  Formatter: "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
```

- **Logger:** what your code calls. Use `logging.getLogger(__name__)` or the framework's `get_logger("pages.calculator")`. Names form a hierarchy through dots.
- **Handler:** where records go. Each handler has its **own level**.
- **Formatter:** what one line looks like.

Quick start for small scripts:

```python
import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
log = logging.getLogger("demo")
log.info("Calculating %s + %s", 7, 5)       # lazy %s formatting
```

### 5.4 Log levels

| Level | Numeric | When to use in automation | Example |
|-------|---------|---------------------------|---------|
| `DEBUG` | 10 | Details for investigation | `Click {'auto_id': 'num7Button'}`, command line, raw stdout |
| `INFO` | 20 | Normal test steps and milestones | `Calculator opened`, `Result = 15` |
| `WARNING` | 30 | Unexpected but recovered | `click attempt 1/3 failed - retrying` |
| `ERROR` | 40 | A step or check failed | `Report mismatch: expected 'TOTAL=42', got ''` |
| `CRITICAL` | 50 | The run cannot continue | `Application crashed`, `QA server unreachable` |

A logger or handler at level `INFO` lets through INFO **and everything above it**. A typical set-up is **console at INFO** and **file at DEBUG**.

### 5.5 Formats

Useful `%(...)s` fields: `asctime`, `levelname`, `name`, `module`, `filename`, `funcName`, `lineno`, `message`, `threadName`, `process`.

```python
FILE_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"
```
```
2026-09-26 10:15:02,118 | INFO     | minifw.pages.CalculatorWindow | calculate:52 | Calculate 7 + 8
```

`-8s` pads the level name to 8 characters so the columns line up.

**Logging exceptions:** inside an `except` block, use `log.exception("message")`. It logs at ERROR level and adds the full traceback. Re-raise afterwards if the test should still fail.

### 5.6 Log file management

| Handler | Module | Behaviour | Typical use |
|---------|--------|-----------|-------------|
| `FileHandler` | `logging` | One file, append or overwrite (`mode="w"`) | **Per-run log files** (timestamp in the name) |
| `RotatingFileHandler` | `logging.handlers` | New file when `maxBytes` is reached. Keeps `backupCount` old files (`.1`, `.2` ...) | Long-running tools and agents |
| `TimedRotatingFileHandler` | `logging.handlers` | New file every `when` (`'midnight'`, `'H'`, `'D'`, ...). Keeps `backupCount` | Daily logs on a shared server |

```python
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

per_run = logging.FileHandler(f"logs/run_{datetime.now():%Y%m%d_%H%M%S}.log", encoding="utf-8")
by_size = RotatingFileHandler("logs/framework.log", maxBytes=5_000_000, backupCount=5, encoding="utf-8")
by_day  = TimedRotatingFileHandler("logs/daily.log", when="midnight", backupCount=7, encoding="utf-8")
```

**Per-run log files + folder cleanup** (from the course framework's `core/logger.py`):

```python
def setup_logging(level="INFO", keep_last=10):
    LOG_DIR.mkdir(exist_ok=True)
    old_logs = sorted(LOG_DIR.glob("automation_*.log"))          # timestamps sort by age
    for old in old_logs[:max(0, len(old_logs) - (keep_last - 1))]:
        old.unlink(missing_ok=True)
    log_file = LOG_DIR / f"automation_{datetime.now():%Y%m%d_%H%M%S}.log"
    root = logging.getLogger("automation")
    root.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(level)
    ...
def get_logger(name):
    return logging.getLogger(f"automation.{name}")
```

An alternative cleanup rule is *"delete logs older than N days"*, based on `Path.stat().st_mtime` (see `examples/02_logging_handlers_rotation.py`).

**Configure once, use everywhere.** Call `setup_logging()` once per run (the course framework does it in `pytest_configure`). Every module then calls only `get_logger()`. If you add handlers every time a logger is requested, every line appears two, three, four times.

### 5.7 Using logs to debug failures

1. Open the per-run log of the failing run (the pytest-html report and CI artefacts point to it).
2. Find the **first** `ERROR` or `WARNING`. Later errors are often side effects.
3. Read the lines **before** it: the last successful step, the data and the locator.
4. Look at the **timestamps**. A gap equal to a timeout value means something was waited for and never appeared.
5. Check the **environment** line at the top of the log.
6. Compare with the log of a passing run.

```
10:15:07 | INFO    | automation.pages.CalculatorPage | Calculate 12 / 0
10:15:07 | DEBUG   | automation.pages.CalculatorPage | Click {'auto_id': 'divideButton'}
10:15:17 | ERROR   | automation.waits | Timed out after 10s waiting for text 'Display is'
```
Diagnosis: the display showed "Cannot divide by zero", so the test data is wrong. The application is fine.

**Try it yourself:** run `python examples/02_logging_handlers_rotation.py` and inspect `examples/logs/`. Then run `hands_on/solutions/mini_framework/run_demo.py` in dev and qa and compare the log files.

---

## 6. PyTest: why, and how a run works

### 6.1 Why PyTest instead of unittest

| Topic | unittest | pytest |
|-------|----------|--------|
| Test shape | Class inheriting `TestCase` | Plain functions (classes optional) |
| Assertions | `self.assertEqual`, `assertIn` ... | Plain `assert`, with detailed failure output |
| Setup/teardown | `setUp`/`tearDown`, `setUpClass` | **Fixtures**: reusable, scoped, composable, `yield` |
| Data-driven | `subTest`, loops | `@pytest.mark.parametrize` |
| Selection | By name | By name (`-k`), marker (`-m`), last failed (`--lf`) |
| Plugins | Few | Very many: html, xdist, rerunfailures, ... |
| Compatibility | - | Also runs unittest tests |

unittest version:
```python
import unittest
class TestCalc(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator().open()
    def test_add(self):
        self.assertEqual(self.calc.calculate(2, "+", 3), 5)
```
pytest version:
```python
def test_add(calculator):
    assert calculator.calculate(2, "+", 3) == 5
```

### 6.2 Discovery rules

- pytest starts in `testpaths` from `pytest.ini`, or the current folder.
- Files: `test_*.py` or `*_test.py`.
- Functions: `test_*` (at module level).
- Classes: `Test*` **with no `__init__`**, containing `test_*` methods.
- `conftest.py` files are loaded automatically.

```powershell
pytest --collect-only -q            # list what would run
pytest test_basics.py               # one file
pytest test_basics.py::test_addition
pytest test_basics.py::TestCalculatorState::test_new_calculator_is_closed
pytest -k "divide and not zero"
```

### 6.3 Execution flow

```
1. Read pytest.ini, load plugins and conftest.py files
2. Collect tests (discovery), apply -k / -m selection
3. For every test:
     setup     fixtures run up to their `yield`
     call      the test function
     teardown  fixtures resume after `yield` (always, even after failure)
4. Report outcomes and summary
```

| Outcome | Meaning |
|---------|---------|
| `PASSED` | Test finished without exception |
| `FAILED` | Assertion or exception **in the test** |
| `ERROR` | Exception in **setup or teardown** (a fixture) |
| `SKIPPED` | Not run (skip, skipif, `pytest.skip()`) |
| `XFAIL` | Expected failure happened (known bug) |
| `XPASS` | Expected to fail but passed (an error if `strict=True`) |
| deselected | Excluded by `-m` or `-k` |

### 6.4 pytest.ini

```ini
[pytest]
testpaths = tests
pythonpath = .
addopts = -v -ra --strict-markers
markers =
    smoke: quick, critical checks - run on every commit
    regression: full coverage - run nightly
    desktop: needs a Windows desktop session (Calculator / Notepad)
    cli: command-line tests - run on any OS
log_file = logs/pytest.log
log_file_level = DEBUG
```

---

## 7. Fixtures, scopes and conftest.py

### 7.1 Fixtures with yield

A **fixture** prepares something a test needs and cleans it up afterwards. A test asks for a fixture **by naming it as a parameter**.

```python
@pytest.fixture
def calculator(logger):
    logger.info("SETUP: opening calculator")
    calc = Calculator().open()
    yield calc                    # value given to the test; the test runs now
    logger.info("TEARDOWN: closing calculator")
    calc.close()                  # always runs, even if the test failed

def test_add(calculator):
    assert calculator.calculate(1, "+", 1) == 2
```

Alternatives for teardown: `request.addfinalizer(calc.close)`. The xUnit style (`setup_module`, `teardown_function`, `setup_method`) also works in pytest.

### 7.2 Fixture scope table

| Scope | Created ... | Destroyed ... | Desktop/CLI example |
|-------|-------------|---------------|---------------------|
| `function` (default) | before each test | after each test | a fresh temp file for Notepad, `tmp_path` |
| `class` | before first test of a class | after last test of the class | a dialog shared by a test class |
| `module` | before first test in a file | after last test in the file | the Calculator window (slow to start) |
| `package` | before first test in a package | after last test in the package | an app instance per feature folder |
| `session` | once per pytest run | at the end of the run | config, logger, test data cache |

Wider scope is faster but gives less isolation. If you share an app across tests, **reset its state** at the start of each test (the course `calculate()` calls `clear()` first).

A fixture may only use fixtures of the **same or wider** scope. A session fixture cannot use a function fixture.

### 7.3 conftest.py

- Holds fixtures and hooks shared by all tests in its folder and sub-folders.
- It is loaded automatically. **Never import it.**
- Typical contents: `pytest_addoption` (`--env`), `pytest_configure` (set up logging), `config`/`logger`/app fixtures, `pytest_runtest_makereport` (evidence on failure), `pytest_collection_modifyitems` (for example, skipping desktop tests on Linux).

```python
def pytest_addoption(parser):
    parser.addoption("--env", default=None, help="environment from config/config.yaml")

def pytest_configure(config):
    settings = get_config(config.getoption("--env"))
    setup_logging(settings["log_level"])

@pytest.fixture(scope="session")
def config(request):
    return get_config(request.config.getoption("--env"))

@pytest.fixture(scope="module")
def calculator(config):
    page = CalculatorPage(config).open()
    yield page
    page.close()
```

### 7.4 Useful built-in fixtures

| Fixture | Use |
|---------|-----|
| `tmp_path` | Unique empty folder (a `Path`) per test, cleaned up automatically |
| `caplog` | Capture log records: `caplog.text`, `caplog.records`, `caplog.set_level("DEBUG")` |
| `capsys` | Capture stdout/stderr: `out, err = capsys.readouterr()` |
| `monkeypatch` | Temporarily change env vars/attributes: `monkeypatch.setenv("TEST_ENV", "qa")` |
| `request` | Info about the current test (`request.node.name`), `addfinalizer`, `config.getoption` |

**Try it yourself:** `cd examples/pytest_demo` then `pytest test_fixtures.py -s --setup-show`. Find where the module fixture is created and destroyed.

---

## 8. Assertions, parameterization and markers

### 8.1 Assertions and validations

```python
assert result == 15
assert result == 6, f"Expected 6 but display showed {result}"      # custom message
assert calc.calculate(0.1, "+", 0.2) == pytest.approx(0.3)         # floats
assert calc.calculate(10, "/", 3) == pytest.approx(3.333, rel=1e-3)
assert "Cannot divide by zero" in calc.display_text()              # substring
assert (1.0, "+", 1.0, 2.0) in calc.history                         # membership
assert len(calc.history) == 2
assert not is_valid_username("abc")

with pytest.raises(ZeroDivisionError, match="divide by zero"):      # negative test
    calc.calculate(5, "/", 0)
```

What to validate in desktop tests: displayed values, window titles, control states (enabled/visible), saved file contents.
What to validate in CLI tests: **return code**, **stdout**, **stderr**, and optionally duration and files created.

```python
result = run_command([*TOOL, "count", "no_such_file.txt"])
assert result.returncode == 2, f"stdout={result.stdout!r} stderr={result.stderr!r}"
assert "file not found" in result.stderr
```

### 8.2 Parameterization (basic)

```python
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-5, 5, 0),
])
def test_add(calculator, a, b, expected):
    assert calculator.calculate(a, "+", b) == expected
```

Each row is a **separate test** with its own result. This is better than a loop, which stops at the first failure.

- **Readable ids:** `ids=["min-1", "min", "max"]`, or `pytest.param(..., id="name")`.
- **Marker on one row:** `pytest.param(1, "/", 3, 0.333, marks=pytest.mark.xfail(reason="..."))`.
- **Stacked decorators** give the cross product (2 values x 3 values = 6 tests).

**Data from CSV:**

```python
def load_csv_cases(path):
    with open(path, newline="", encoding="utf-8") as f:
        return [pytest.param(r["a"], r["op"], r["b"], float(r["expected"]), id=r["case_id"])
                for r in csv.DictReader(f)]

@pytest.mark.parametrize("a, op, b, expected", load_csv_cases(DATA_FILE))
def test_calculator_from_csv(calculator, a, op, b, expected):
    assert calculator.calculate(a, op, b) == pytest.approx(expected)
```

The course framework uses `utils.data_reader.read_csv("calculator_data.csv")` and `read_yaml("cli_cases.yaml")` in the same way. CSV values are always **strings**, so convert them.

### 8.3 Markers

Built-in markers:

| Marker | Effect |
|--------|--------|
| `@pytest.mark.skip(reason=...)` | Never run |
| `@pytest.mark.skipif(condition, reason=...)` | Skip when the condition is true (OS, Python version, env) |
| `@pytest.mark.xfail(reason=..., strict=True)` | Expected to fail (known bug). With strict, an unexpected pass becomes a failure |
| `pytest.skip("...")` inside a test | Skip at run time (for example, depending on config) |
| `@pytest.mark.parametrize` | Data-driven (see above) |
| `@pytest.mark.usefixtures("name")` | Use a fixture without receiving it as a parameter |

**Custom markers** must be registered in `pytest.ini` (and `--strict-markers` turns typos into errors):

```ini
markers =
    smoke: quick, critical checks
    regression: full coverage
    desktop: needs a Windows desktop session
    cli: command-line tests
```

```python
pytestmark = pytest.mark.cli              # applies to every test in the module

@pytest.mark.smoke
def test_info_json_is_valid(run_tool): ...
```

Selection with `-m` supports `and`, `or`, `not` and parentheses:

```powershell
pytest -m smoke
pytest -m "cli and not regression"
pytest -m "(desktop or cli) and smoke"
pytest --markers                          # list registered markers
```

**Opt-in tests:** add `-m "not demo_fail"` to `addopts`. A `-m` given on the command line overrides it, so `pytest -m demo_fail` runs only those tests.

**Try it yourself:** in `examples/pytest_demo`, predict the counts for `pytest -m smoke` and `pytest -m "regression and not slow"`, then run them.

---

## 9. HTML & Allure reports and capturing evidence on failure

### 9.1 pytest-html

```powershell
pip install pytest-html
pytest --html=reports/report.html --self-contained-html
```

- The report shows a summary, environment metadata, and each test with its outcome, duration, captured logs and traceback.
- `--self-contained-html` embeds CSS and images in **one file**. It is easy to e-mail or attach as a CI artefact.
- Change the title with an optional hook:

```python
@pytest.hookimpl(optionalhook=True)
def pytest_html_report_title(report):
    report.title = "Day 4 - PyTest Demo Report"
```

### 9.2 The pytest_runtest_makereport hook

pytest calls this hook **three times per test** (setup, call, teardown). With `hookwrapper=True`, you `yield` to let pytest build the report and then inspect or extend it:

```python
import base64
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)          # lets fixtures see the result

    if report.when == "call" and report.failed:
        path = take_screenshot(item.name)                 # PIL.ImageGrab -> .png (None if no display)
        html = item.config.pluginmanager.getplugin("html")
        if html is not None and path is not None:
            b64 = base64.b64encode(path.read_bytes()).decode()
            report.extras = getattr(report, "extras", []) + [html.extras.png(b64, name="Screenshot")]
```

Notes:
- pytest-html 4.x uses **`report.extras`**. Older tutorials show `report.extra`.
- Other extras: `html.extras.text(...)`, `html.extras.url(...)`, `html.extras.html(...)`, `html.extras.json(...)`.
- Only take screenshots for failures (and only for desktop tests). Screenshots are large.
- A real screenshot captures **everything on screen**. Close private windows before running desktop suites.

### 9.3 Capturing logs on failure

- pytest captures log records per test automatically. They appear as *"Captured log setup/call/teardown"* in the terminal and in the HTML report.
- In the hook, `report.caplog`, `report.capstdout`, `report.capstderr` and `report.longreprtext` (the traceback text) are available. You can write them to an artefact file and attach it as `html.extras.text(...)`.
- In tests, use the `caplog` fixture to **assert** on logging: `assert "HEALED" in caplog.text`.
- `log_file = logs/pytest.log` in `pytest.ini` writes a full log for the run. `--log-cli-level=INFO` streams logs live to the console.

**Try it yourself:**
```powershell
cd examples/pytest_demo
pytest -m demo_fail --html=reports/failure_report.html --self-contained-html
```
Open the report, expand the failed test, and look at the screenshot and the "Failure log". Then look in `artifacts/`.

### 9.4 Allure reports (and exporting them to PDF)

**Allure** is the most widely used reporting tool in test automation. It works in two phases:

```
1. DURING the run   pytest + allure-pytest plugin  -->  allure-results/   (raw JSON + attachments)
2. AFTER the run    allure generate                -->  allure-report/    (interactive HTML report)
```

Setup used in `automation_framework`:

```powershell
pip install allure-pytest                 # the pytest plugin (writes results)
npm install                               # Allure 3 report generator - Node.js, no Java needed
pytest --alluredir=allure-results --clean-alluredir     # already in pytest.ini addopts
npx allure generate allure-results        # -> allure-report/index.html
npx allure open                           # serve and open it in the browser
```

> **Allure 2 vs 3:** Allure 2 (still common in companies) is a Java tool: `allure serve allure-results`. Allure 3 is its Node.js successor, which is why the framework needs Node.js but not Java. The pytest side (`allure-pytest`) is the same for both.

**Enrich the report from your tests:**

```python
import allure

@allure.epic("Desktop automation")          # top-level grouping
@allure.feature("Calculator")               # feature under test
@allure.story("Basic arithmetic")           # user story / scenario group
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Addition 7 + 8 = 15")        # readable name (can use parameters: "{case[test_id]}")
def test_addition(calculator):
    with allure.step("Calculate 7 + 8"):    # shows as a step, with its own status and time
        result = calculator.calculate(7, "+", 8)
    allure.attach(str(result), name="result", attachment_type=allure.attachment_type.TEXT)
    assert result == 15
```

In the framework, page objects record steps through `core/reporting.py` (`step`, `@step_method`, `attach_text`, `attach_png`). So every test gets detailed steps without extra code, and the screenshot on failure is attached automatically.

**Exporting to PDF.** The Allure report is an interactive web app and has no "Export to PDF" option; printing it from the browser only captures the first screen. The framework includes `tools/allure_pdf_report.py`, which reads the **same** `allure-results` and writes a PDF with:
- a summary (totals, pass rate, pie chart, environment)
- results by feature, and a table of all tests
- a failures section (message, trace, steps, screenshot)
- the steps of every test

It is built with the `reportlab` library.

```powershell
cd automation_framework
python run_tests.py -m smoke --open      # pytest + Allure HTML + PDF in one command
python tools/allure_pdf_report.py --title "Sprint 42 regression" --details failed
```

| | pytest-html | Allure | PDF (framework tool) |
|---|---|---|---|
| Setup | `pip install pytest-html` | plugin + report CLI | `pip install reportlab` |
| Steps / attachments | extras only | rich steps, attachments, severity, grouping | from Allure results |
| History / trends | no | yes (`allure-history`) | no |
| Best for | quick single page | daily analysis by the team | e-mail, sign-off, audits |

**Try it yourself:** run `python run_tests.py -m cli`. Open `allure-report/index.html` and find the *stdout* attachment of the "CLI case: count missing file" test. Then open `reports/test_report.pdf`.

---

## 10. PyTest command-line cheat-sheet

| Command / option | What it does |
|------------------|--------------|
| `pytest` | Run all tests found from `testpaths` / current folder |
| `pytest path/to/test_file.py` | Run one file |
| `pytest file.py::test_name` | Run one test |
| `pytest file.py::TestClass::test_name` | Run one test method |
| `-v` / `-q` | Verbose / quiet output |
| `-k "expr"` | Select by name substring (`and`, `or`, `not`) |
| `-m "expr"` | Select by marker |
| `-x` | Stop at the first failure |
| `--maxfail=N` | Stop after N failures |
| `--lf` | Run only the tests that failed last time |
| `--ff` | Run failures first, then the rest |
| `-s` | Do not capture output (show `print`) |
| `-ra` | Summary line for all non-passed outcomes |
| `-rA` | Summary for all outcomes |
| `--collect-only -q` | Only list tests |
| `--setup-show` | Show fixture setup/teardown |
| `--durations=10` | Show the 10 slowest tests |
| `--tb=short` / `--tb=line` / `--tb=no` | Traceback detail |
| `--log-cli-level=INFO` | Live logging to the console |
| `--log-file=logs/run.log` | Write logs to a file |
| `--markers` | List registered markers |
| `--fixtures` | List available fixtures |
| `--html=reports/report.html --self-contained-html` | HTML report (pytest-html) |
| `--junitxml=reports/junit.xml` | JUnit XML for CI tools |
| `--env qa` | *Custom* option (defined in our `conftest.py`) |
| `-n auto` | Parallel run (needs `pytest-xdist`) |
| `--reruns 2` | Re-run failures (needs `pytest-rerunfailures`). Use with care |
| `python -m pytest ...` | Same as `pytest`, but also adds the current folder to `sys.path` |

---

## 11. AI basics for automation

### 11.1 The role of AI in automation testing

| Area | How AI helps | What you must still do |
|------|--------------|------------------------|
| Test design | Suggests test cases, edge cases, BVA/ECP data | Check them against the real requirement |
| Script writing | Drafts tests, page objects, helpers, regexes | Make it fit your framework, run it, review it |
| Debugging | Explains tracebacks and logs, spots race conditions | Confirm the root cause with evidence |
| Maintenance | Refactors, adds logging, suggests locators | Review every change |
| Self-healing / smart waits | Tools find controls whose locators changed | Review healed locators, update page objects |
| Analysis | Groups failures, summarises reports | Decide whether each failure is a bug |

Examples of tools: IDE assistants (GitHub Copilot and similar), chat assistants (ChatGPT, Claude, ...), and commercial AI test platforms. **Use the tools and accounts your company approves.**

### 11.2 AI-assisted script design: prompting

Use **R-C-T-F-C**:

| Part | Example |
|------|---------|
| **R**ole | "You are a senior Python test automation engineer." |
| **C**ontext | "Windows 11, Python 3.14, pytest 9, pywinauto uia. Page object CalculatorPage has open(), calculate(a, op, b) -> float." |
| **T**ask | "Write parametrized pytest tests for division, including divide by zero." |
| **F**ormat | "One code block, then a list of assumptions." |
| **C**onstraints | "Use the `calculator` fixture and markers smoke/desktop. No time.sleep. Standard library only." |

More templates are in `examples/ai_prompt_examples.md`: test cases from a requirement, debugging a flaky script, explaining a failure log, converting manual steps to pytest, and suggesting fallback locators.

### 11.3 Reviewing AI output critically

| Check | Why |
|-------|-----|
| Run it, several times | AI code often has small errors |
| Are all APIs real? | AI can *hallucinate* functions and parameters |
| Did it weaken the test? | Removed asserts, `except: pass`, retries around assertions |
| Are expected values right? | The AI guesses the oracle. The requirement decides |
| Is it secure? | Look for `shell=True`, `eval`, hard-coded secrets |
| Does it fit the framework? | Logger, config, page objects, markers |
| Can you explain every line? | If not, do not commit it |

### 11.4 Never paste secrets or confidential data

Never paste passwords, API keys, tokens, connection strings, customer or personal data, production logs, or proprietary source code into an AI tool that your company has not approved for that data. Anonymise (`<SERVER>`, `user@example.com`) and reduce the problem to a minimal example.

### 11.5 Smart retries and synchronisation

**Polling wait:** wait for a *state* instead of sleeping.

```python
def wait_until(condition, timeout=10, interval=0.5, message="condition"):
    end = time.monotonic() + timeout
    while True:
        try:
            result = condition()
            if result:
                return result
        except Exception:
            pass
        if time.monotonic() >= end:
            raise WaitTimeoutError(f"Timed out after {timeout}s waiting for {message}")
        time.sleep(interval)
```

**Retry with exponential backoff:** retry a flaky *action*.

```python
@retry(times=3, delay=1.0, backoff=2.0, exceptions=(ElementNotFoundError, TimeoutError))
def click_save():
    window.child_window(auto_id="saveBtn").invoke()
# waits 1 s, then 2 s between attempts; re-raises after the 3rd failure
```

Rules:
- **Wait for states, retry actions, never retry assertions.**
- Always bound retries (`times`, `timeout`) and log every retry as a WARNING.
- Retry only specific exception types.
- Take timeouts and retry counts from config.

### 11.6 Self-healing locators (concept)

Keep a **list of locators** per control. Try them in order, and log a WARNING when a fallback works. AI-based tools add similarity scoring on text, control type and position.

```python
LOCATORS = {"plus": [{"auto_id": "plusButton"},
                     {"title": "Plus", "control_type": "Button"}]}
```

Risk: healing can pick the **wrong** control (see the "memory" example in `examples/05_self_healing_locator_concept.py`). Healing must always be logged and reviewed.

### 11.7 AI-based test data generation

AI can propose boundary values, invalid formats, unicode, very long strings and realistic-looking records. Check its output against the classic techniques:

- **Equivalence class partitioning:** one representative from each valid and invalid class.
- **Boundary value analysis:** min-1, min, min+1, max-1, max, max+1.
- **Reproducibility:** generate random data with `random.Random(seed)` so failures can be reproduced.

`examples/06_test_data_generation.py` generates this data in pure Python (no Faker, no AI) and writes a CSV for parametrize.

### 11.8 Demo: AI-assisted debugging and optimisation

`examples/07_ai_debugging_before.py` is a flaky test for an export job. `08_ai_debugging_after.py` is the reviewed improvement:

| Before | After |
|--------|-------|
| `time.sleep(1)` | `proc.communicate(timeout=...)` + `wait_until(REPORT.exists, ...)` |
| `except: pass` | Specific exceptions, `log.exception` |
| `open()` never closed | `with open(...)` |
| `data == "TOTAL=42"` (fails on `\n`) | `.strip()` before comparing |
| Stale report from the last run | Deleted before each run |
| `shell=True`, `"python"` | `[sys.executable, "-c", ...]` |
| No exit code | `sys.exit(0 or 1)` |
| `print` | Console + file logging |

---

## 12. Common mistakes

**Framework**
- Locators copied into tests instead of kept in window classes.
- Asserts inside window objects, which hide *what* the test checks.
- Hard-coded paths (`C:\Users\me\...`) and timeouts.
- Different keys in different environments, which gives a `KeyError` only in qa.
- Secrets committed in `config.yaml`.

**Logging**
- `print()` in framework code.
- Handlers added repeatedly, so every line is duplicated.
- Everything logged at INFO (noise), or DEBUG flooding the console.
- Logging passwords or tokens.
- `except: pass` with no log and no re-raise.
- No log cleanup, so CI agents run out of disk space.

**PyTest**
- File named `calc_tests.py` or function named `check_add`, so 0 tests are collected.
- Importing `conftest.py`.
- Tests that depend on the order or state left by other tests.
- A loop over data instead of `parametrize`.
- `==` on floats.
- Unregistered custom markers.
- Catching exceptions inside tests.
- Using `report.extra` with pytest-html 4 (it must be `report.extras`).

**AI**
- Pasting confidential code or data into public tools.
- Accepting code without running and reviewing it.
- "Fixing" flakiness with longer sleeps or retries around assertions.

---

## 13. Day 4 summary

- A **framework** is layered: tests, window objects, core, utilities, config/data. Each layer has one responsibility.
- **Configuration-driven** means settings live in YAML per **environment**, selected by `--env`, then `TEST_ENV`, then `default_env`.
- **Window Object Model:** `BaseWindow` plus one class per window. Locators live in one place. Tests read like manual test cases.
- **Logging:** Logger, Handler, Formatter. Five levels. Console at INFO, file at DEBUG. Per-run files, rotation and cleanup. Configure once, then `get_logger()` everywhere.
- **PyTest:** discovery rules, setup/call/teardown, `yield` fixtures with scopes, `conftest.py`, plain asserts with `approx`/`raises`, `parametrize` (including CSV data), built-in and custom markers with `-m`.
- **Reports:** `pytest-html` with `--self-contained-html`. The `pytest_runtest_makereport` hook attaches screenshots and logs as `extras`.
- **AI:** structured prompts, critical review, no secrets. Waits for states, retries with backoff for actions. Self-healing needs review. BVA/ECP for data.

---

## 14. Questions and answers

**Q1. What is a test automation framework, and why use one instead of scripts?**
A framework is a set of conventions and reusable components: a runner, folder structure, helpers, configuration, logging and reporting. It makes tests easy to write, run and maintain. It removes duplicated code, keeps locators in one place, allows switching environments without code changes, and gives consistent evidence on failures.

**Q2. Explain the Page Object Model and how it applies to desktop applications.**
POM represents each page or screen as a class that holds its locators and exposes business actions. For desktop apps it becomes one class per window or dialog (a "Window Object Model"), usually inheriting from a `BaseWindow` with common methods (connect, find, click, read_text, wait). Tests call `calculator.calculate(7, "+", 8)` and never touch locators, so a UI change is fixed in one class.

**Q3. How do you handle multiple environments in a framework?**
Keep settings per environment in a config file (YAML) with identical keys. Select the environment by priority: command-line option (`--env qa`), then an environment variable (`TEST_ENV`), then a default. Secrets are read from environment variables or a vault, never from the repository.

**Q4. What are the Python logging levels and when do you use each?**
DEBUG (10) for diagnostic detail such as locators and commands. INFO (20) for normal steps. WARNING (30) for unexpected but recovered situations such as retries. ERROR (40) for a failed step. CRITICAL (50) when the run cannot continue. A handler at level X outputs X and higher.

**Q5. What is the difference between a Logger, a Handler and a Formatter?**
The Logger is the object your code calls. It is named hierarchically and passes records up to its parents. A Handler decides where records go (console, file, rotating file) and has its own level. A Formatter defines the layout of each line.

**Q6. How do you manage log files in a long-running automation setup?**
Create a per-run file with a timestamp in its name, and clean up old files (keep the last N or delete files older than N days). Or use `RotatingFileHandler` (by size, with `backupCount`) or `TimedRotatingFileHandler` (for example, at midnight, keeping 7 files). Attach the per-run log to the report or CI artefacts.

**Q7. Why pytest over unittest?**
Plain `assert` with rich failure output, powerful fixtures with scopes and `yield` teardown, built-in parametrization, marker-based selection, a large plugin ecosystem (html, xdist, rerunfailures), and it still runs unittest tests.

**Q8. What are fixture scopes? Give a desktop example for each common scope.**
`function` (default): a fresh Notepad file per test. `class`: one dialog per test class. `module`: one Calculator window per test file. `session`: config and logger for the whole run. Wider scope is faster but less isolated.

**Q9. What is conftest.py?**
A file that pytest loads automatically. It holds fixtures and hooks shared by the tests in its directory tree, such as the `--env` option, config and app fixtures, and screenshot-on-failure hooks. It must not be imported.

**Q10. What is the difference between FAILED and ERROR in pytest?**
FAILED means an assertion or exception occurred in the test function itself. ERROR means an exception occurred in setup or teardown, typically in a fixture (for example, the application did not start).

**Q11. How do you run only smoke tests, or exclude slow tests?**
Register custom markers in `pytest.ini`, decorate tests with `@pytest.mark.smoke`, and select with `pytest -m smoke` or `pytest -m "regression and not slow"`. `--strict-markers` catches marker typos.

**Q12. How do you implement data-driven tests in pytest?**
Use `@pytest.mark.parametrize` with a list of tuples, or with data loaded from CSV/JSON/YAML (for example, `csv.DictReader` rows converted to `pytest.param(..., id=...)`). Each row becomes an independent test with its own result.

**Q13. How do you capture screenshots on failure and put them in an HTML report?**
Implement `pytest_runtest_makereport` as a hookwrapper in `conftest.py`. After `yield`, get the report. If `report.when == "call"` and `report.failed`, take a screenshot (for example, `PIL.ImageGrab.grab()`), base64-encode it, and append `html_plugin.extras.png(b64)` to `report.extras`. Run with `--html=reports/report.html --self-contained-html`.

**Q14. What is the difference between xfail and skip?**
`skip` does not run the test (feature missing, wrong platform). `xfail` runs it and expects it to fail (known bug). The result is XFAIL, or XPASS if it unexpectedly passes. With `strict=True`, XPASS is treated as a failure, so you notice when the bug is fixed.

**Q15. How do you handle flaky tests caused by timing?**
Replace fixed sleeps with polling waits on a condition, with a timeout (`wait_until`, or pywinauto `wait("visible")`). Retry flaky *actions* with bounded exponential backoff, and log every retry. Never retry assertions to hide bugs. Investigate the root cause using logs and timestamps.

**Q16. How can AI help in test automation, and what are the risks?**
It helps draft test cases and scripts, generate data, explain failures and refactor code. The risks are hallucinated APIs, weakened tests (removed asserts, broad excepts), wrong expected values, insecure code, and leaking confidential data. Always use approved tools, anonymise inputs, run and review the output, and stay accountable for what you commit.

**Q17. What is a self-healing locator?**
A mechanism that tries alternative locators (or similarity matching) when the primary locator fails, and logs that it healed. It reduces maintenance, but it can select the wrong element, so healed locators must be reviewed and the page object updated.
