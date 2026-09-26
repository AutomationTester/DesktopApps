---
marp: true
theme: default
paginate: true
---

# Day 4
## Automation Framework, PyTest, Logging and AI Basics

**Python Desktop Application Automation Testing**
Day 4 of 5

<!-- Trainer notes: Welcome everyone back. Day 1 was Python/OOP/debugging, Day 2 pywinauto + CLI automation, Day 3 data files, Linux and subprocess. Today we turn all those scripts into a FRAMEWORK: structured, configurable, logged, run by PyTest with reports. We finish with how AI can help (and hurt) automation work. Tomorrow's mini project builds on today's framework, so today is the foundation. -->

---

## Agenda (09:00 - 17:00)

| Time | Session |
|------|---------|
| 09:00 - 09:10 | Recap of Day 3, today's goals |
| 09:10 - 10:00 | **Framework enhancements**: modular design, utilities, config, environments, Window Object Model |
| 10:00 - 10:45 | **Logging in automation** |
| 10:45 - 11:00 | *Break* |
| 11:00 - 12:10 | **Lab 1**: logging-enabled mini framework |
| 12:10 - 12:55 | *Lunch* |
| 12:55 - 14:10 | **PyTest** for desktop and CLI automation |
| 14:10 - 15:25 | **Lab 2**: PyTest execution with reports |
| 15:25 - 15:40 | *Break* |
| 15:40 - 16:10 | **AI basics for automation** + demo |
| 16:10 - 16:50 | **Lab 3**: AI-assisted script improvement |
| 16:50 - 17:00 | Recap, Q&A, quiz handout |

<!-- Trainer notes: Point out that labs make up almost half of the day. The quiz (03_Quiz.md) can be done at home or as a warm-up at the start of Day 5. If you run late, shorten Lab 2 Part C (the course framework CLI run) - it can be demoed by you instead. -->

---

## Learning objectives

By the end of today you can:

- Explain and build a **modular, configuration-driven** automation framework
- Switch **environments** (dev / qa) without touching code
- Add professional **logging**: levels, formats, handlers, rotation, per-run files
- Write and run **PyTest** tests: fixtures, assertions, parametrize, markers
- Produce **HTML reports** with screenshots and logs on failure
- Use **AI assistants** responsibly to design, debug and improve scripts

<!-- Trainer notes: Ask: "Who has had a script that worked yesterday and failed today, and you had no idea why?" Logging + framework + pytest answers that pain. Keep this slide short. -->

---

## Quick recap: where we are

- Day 1: Python, OOP (classes, inheritance), debugging
- Day 2: `pywinauto` desktop automation, `argparse` / `subprocess` CLI automation
- Day 3: CSV / JSON / YAML, Linux basics, subprocess

**The problem today:** we have many *scripts*.
Scripts copy-paste code, hard-code paths and waits, `print()` instead of log, and nobody else can run them.

<!-- Trainer notes: Ask 2-3 trainees to name one annoying thing about their Day 2 scripts. Typical answers: hard-coded sleep, a path that only works on my PC, duplicated login/open code, no idea which step failed. Write them on the whiteboard and tick them off during the day. -->

---

# Part 1
## Automation Framework Enhancements

<!-- Trainer notes: Section 1, about 50 minutes. Goal: the "why" and "what" of a framework, then a walk through automation_framework/. -->

---

## Script vs framework

| Script | Framework |
|--------|-----------|
| One file, top to bottom | Layers with one responsibility each |
| Locators inside test steps | Locators in one window class |
| `time.sleep(5)` | `wait_until(condition, timeout)` |
| Hard-coded paths/timeouts | `config.yaml` per environment |
| `print()` | Logging to console + file |
| Manual run, eyeball result | `pytest -m smoke --html=report.html` |

A **framework** is a set of conventions + reusable code that makes tests **easy to write, read, run and maintain**.

<!-- Trainer notes: Emphasise maintainability: 80% of automation cost is maintenance, not writing. When the Calculator's "=" button changes its automation_id, a framework needs one line changed; a script collection needs 50. -->

---

## Modular framework design: the layers

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

Rule: **a layer only calls the layers below it.**

<!-- Trainer notes: Draw this on the whiteboard. Ask: "If the Calculator UI changes, which layer changes?" (pages). "If we move from dev to qa?" (config). "If we add 20 more data rows?" (test_data). "If the log format changes?" (core/logger). Tests should change only when REQUIREMENTS change. -->

---

## Framework architecture (course framework)

```
            tests/ (WHAT)      test_calculator.py  test_notepad.py  test_cli.py
               |  fixtures + hooks
               v
      tests/conftest.py --- --env ---> core/config_reader.py <-- config/config.yaml
               |
   +-----------+------------------+-----------------------+
   v                              v                       v
 pages/ (HOW - UI)         core/cli_runner.py     utils/data_reader.py <-- test_data/
 CalculatorPage            (HOW - CLI)            utils/screenshot.py
 NotepadPage                      |
   |                              v
   v                        tools/sysinfo_cli.py (CLI app under test)
 core/base_window.py -- pywinauto (UIA) --> Calculator / Notepad
 core/waits.py (wait_until, @retry)   core/logger.py --> logs/automation_<ts>.log
```

<!-- Trainer notes: This is automation_framework/ at the project root. Open it in VS Code side by side and click through the folders while you talk. It's the base for tomorrow's mini project. Point out generated folders: logs/, reports/, screenshots/ - these are never committed to git. -->

---

## Folder responsibilities

| Folder | Responsibility |
|--------|----------------|
| `config/` | Environment settings (timeouts, retries, log level, app paths) |
| `core/` | Engine: config, logging, waits/retry, `BaseWindow`, CLI runner, paths |
| `pages/` | One class per application window. **Locators live only here** |
| `utils/` | Small reusable helpers: data readers, screenshots |
| `tools/` | `sysinfo_cli.py`, the CLI application under test |
| `test_data/` | CSV / JSON / YAML data for data-driven tests |
| `tests/` | Test cases + `conftest.py` |
| `logs/ reports/ screenshots/` | Generated at run time |

<!-- Trainer notes: Common question: "Is this structure a standard?" There's no single standard, but this layering (tests / pages / core / utils / config / data) is found in almost every Selenium, Appium and desktop framework. Once you know it, you can find your way around any company's framework. -->

---

## Reusable utilities and helpers

Write a helper when the **same code appears twice**.

```python
# utils/data_reader.py
def read_csv(name):
    with open(TEST_DATA_DIR / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

# core/cli_runner.py
result = run_command([sys.executable, "tools/sysinfo_cli.py", "info"], timeout=30)
assert result.ok and "python" in result.stdout
```

Good helpers are **small, named for what they do, have no test logic, and log what they do.**

<!-- Trainer notes: Show core/cli_runner.py: it wraps subprocess.run (Day 3) and returns a CommandResult dataclass with returncode, stdout, stderr, duration and .ok. Tests become one-liners. Point out it NEVER raises on a non-zero return code - the test decides what failure means. -->

---

## Central paths: no hard-coded folders

```python
# core/paths.py
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR     = ROOT / "config"
TEST_DATA_DIR  = ROOT / "test_data"
LOG_DIR        = ROOT / "logs"
SCREENSHOT_DIR = ROOT / "screenshots"
```

- Works from **any** working directory, on any PC
- `Path(__file__)` means "relative to this file", not to where you ran `python`

<!-- Trainer notes: Classic failure: script works in VS Code, fails in CI, because the current working directory is different. Demo: run a script with open("data.csv") from another folder and show FileNotFoundError. -->

---

## Configuration-driven frameworks

**Behaviour comes from a config file, not from code.**

```yaml
# config/config.yaml
default_env: dev
environments:
  dev:
    log_level: DEBUG
    timeouts: {app_start: 15, element: 10}
    retry: {times: 2, delay: 1}
    calculator: {launch_cmd: calc.exe, window_title: Calculator}
  qa:
    log_level: INFO
    timeouts: {app_start: 30, element: 15}
    retry: {times: 3, delay: 2}
```

<!-- Trainer notes: Ask: "What values would you put in config vs in code?" Config: anything that differs per environment/machine or that you want to tune without code review - URLs, paths, timeouts, credentials REFERENCES (never the secret itself), log level. Code: logic. -->

---

## Reading config

```python
# core/config_reader.py
def get_config(env=None):
    data = _load_file()                     # yaml.safe_load, cached
    env = env or os.environ.get("TEST_ENV") or data["default_env"]
    try:
        settings = dict(data["environments"][env])
    except KeyError:
        raise ValueError(f"Unknown environment '{env}'. "
                         f"Available: {list(data['environments'])}") from None
    settings["env"] = env
    return settings
```

- Use `yaml.safe_load`, never `yaml.load` on untrusted files
- Fail **fast and clearly** on an unknown env

<!-- Trainer notes: Demo examples/03_logger_config_from_yaml.py with no argument, then --env qa, then TEST_ENV=qa. Show that the log level changes the output: DEBUG line disappears in qa. -->

---

## Environment handling

Priority (highest first):

1. **Command line**: `pytest --env qa`
2. **Environment variable**: `TEST_ENV=qa`
3. **Default** in YAML: `default_env: dev`

```powershell
pytest -m cli --env qa                       # explicit
$env:TEST_ENV="qa"; pytest -m cli            # PowerShell
TEST_ENV=qa pytest -m cli                    # Linux / Git Bash
```

**Secrets** (passwords, tokens): environment variables or a vault, **never** in YAML in git.

<!-- Trainer notes: CI servers (Jenkins, GitHub Actions, Azure DevOps) usually set environment variables per pipeline, which is why TEST_ENV support matters. Secrets: show os.environ["APP_PASSWORD"] pattern verbally; mention a .env file in .gitignore as a local-only option. -->

---

## Page Object Model becomes the "Window Object Model"

- **POM** (web): one class per web page
- **Desktop version**: one class per **application window / dialog / screen**
- The class holds **locators** + **business actions**
- Tests call `calc.calculate(7, "+", 8)`, never `child_window(auto_id="num7Button")`

```
BaseWindow  (connect, find, click, read_text, wait_for_text, screenshot)
   +-- CalculatorPage   (open, calculate, clear, result, close)
   +-- NotepadPage      (open_file, type_text, save, close_tab)
   +-- LoginDialog ...  (your app)
```

<!-- Trainer notes: Link back to Day 1 OOP: inheritance. BaseWindow holds everything common; each window only adds what is specific. The name "Page" in CalculatorPage is kept because people search for "page object"; "Window Object Model" is the concept. -->

---

## BaseWindow (course framework)

```python
class BaseWindow:
    def __init__(self, config):
        self.element_timeout = config["timeouts"]["element"]
        self.log = get_logger(f"pages.{type(self).__name__}")
        self.desktop = Desktop(backend="uia")

    def find(self, **criteria):
        control = self.window.child_window(**criteria)
        control.wait("exists", timeout=self.element_timeout)
        return control

    def click(self, **criteria):
        control = self.find(**criteria)
        self.log.debug("Click %s", criteria)
        try:
            control.invoke()          # UIA pattern, no mouse
        except Exception:
            control.click_input()     # fallback: real mouse click
```

<!-- Trainer notes: Open core/base_window.py. Points: (1) timeouts come from config, (2) every action waits for the control first - no sleeps, (3) every action is logged, (4) invoke() uses UI Automation and works even when the window is behind another; click_input moves the real mouse. -->

---

## A window object (CalculatorPage)

```python
OPERATOR_BUTTONS = {"+": "plusButton", "-": "minusButton",
                    "*": "multiplyButton", "/": "divideButton"}
EQUALS_BUTTON, RESULT_TEXT = "equalButton", "CalculatorResults"

class CalculatorPage(BaseWindow):
    def calculate(self, a, operator, b):
        self.log.info("Calculate %s %s %s", a, operator, b)
        self.clear()
        self.enter_number(a)
        self.press_operator(operator)
        self.enter_number(b)
        self.press_equals()
        return self.result          # 'Display is 15' -> 15.0
```

Test: `assert calculator.calculate(7, "+", 8) == 15`

<!-- Trainer notes: Locators are constants at the top of the file - one place to fix. The test reads like a manual test case. Ask: "What if Microsoft renames plusButton?" -> change one line. -->

---

## Framework design rules of thumb

- **One responsibility per module** (config reader doesn't log in, pages don't assert)
- **No asserts in window objects**: they return values, tests assert
- **No sleeps**: wait for a state
- **No hard-coded data** in tests: parametrize from `test_data/`
- **Every action logs**, every failure leaves evidence
- **Independent tests**: any test can run alone, in any order

<!-- Trainer notes: "No asserts in page objects" is debated; the common rule is page objects may VERIFY they are on the right window (e.g. wait for title) but business assertions belong in tests. Keep it simple for freshers. -->

---

# Part 2
## Logging in Automation

<!-- Trainer notes: About 45 minutes. Demo examples 01, 02, 03 live. -->

---

## Why logging matters in automation

- Tests run **unattended**: at night, in CI, on remote machines
- When a test fails, the log is often the **only evidence**
- Logs answer: *which step? which data? which environment? how long?*
- Logs separate **app bugs** from **test bugs** from **environment problems**

> "The test failed" is useless.
> "Step 3: Save button not found after 10s (auto_id=saveBtn, env=qa)" is actionable.

<!-- Trainer notes: Story: a nightly run fails once a week. With print() you have nothing. With logs + timestamps you see it always fails at 02:00 = antivirus scan slows the VM. Ask trainees for their own "mystery failure" stories. -->

---

## print() vs logging

| `print()` | `logging` |
|-----------|-----------|
| No time, level or source | Timestamp, level, module, line |
| Only to console | Console, file, rotating files, ... |
| Can't switch off selectively | Filter by level per destination |
| Mixed with program output | Structured, consistent format |

```python
import logging
log = logging.getLogger(__name__)
log.info("Calculator opened")
```

<!-- Trainer notes: Demo examples/01_logging_basics.py. Point at each part of a log line: time | level | logger name | function:line | message. -->

---

## Log levels

| Level | Value | Use in automation |
|-------|-------|-------------------|
| `DEBUG` | 10 | Locators, raw values, commands, stdout |
| `INFO` | 20 | Test steps and milestones ("Calculator opened") |
| `WARNING` | 30 | Unexpected but recovered ("retrying click") |
| `ERROR` | 40 | A step/test failed |
| `CRITICAL` | 50 | Cannot continue (app crashed, env down) |

A logger/handler set to `INFO` shows INFO **and above**.

<!-- Trainer notes: Typical set-up: console at INFO (readable), file at DEBUG (everything for investigation). Common question: "Should a failed assertion be logged as ERROR?" pytest already reports it; log ERROR for the step that failed with context (expected vs actual). -->

---

## Python logging: the building blocks

```
logger.info("msg")
     |
  Logger  ("automation.pages.CalculatorPage", level)
     |  propagates to parent "automation"
  Handlers  -- StreamHandler (console, INFO)
            -- FileHandler   (logs/run.log, DEBUG)
     |
  Formatter  "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
```

- **Logger**: what you call. Named hierarchically with dots
- **Handler**: where the record goes (+ its own level)
- **Formatter**: how the line looks

<!-- Trainer notes: The hierarchy is key: get_logger("pages.X") creates "automation.pages.X", which propagates to "automation" where the handlers are attached ONCE. That's why every module can just call get_logger(). -->

---

## Formats

```python
fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt, datefmt="%H:%M:%S")
```

Output:
```
10:15:02 | INFO     | automation.pages.CalculatorPage | calculate:62 | Calculate 7 + 8
```

Useful fields: `asctime`, `levelname`, `name`, `module`, `funcName`, `lineno`, `message`, `threadName`, `process`

<!-- Trainer notes: -8s pads the level to 8 characters so columns line up, which makes logs much easier to scan. Also show lazy formatting: log.info("x=%s", x) instead of f-strings, so the string is only built if the level is enabled. -->

---

## Logging exceptions

```python
try:
    calc.calculate(5, "/", 0)
except Exception:
    log.exception("Division step failed")   # ERROR + full traceback
    raise                                   # don't swallow it!
```

- `log.exception()` only inside `except`
- Log **and re-raise**: the test must still fail

<!-- Trainer notes: Show the traceback in the 01 example output. Anti-pattern: except Exception: log.error("failed") with no traceback and no re-raise - the test passes and nobody knows. -->

---

## Log file management: handlers

```python
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# 1. one file per run
logging.FileHandler(f"logs/run_{datetime.now():%Y%m%d_%H%M%S}.log", encoding="utf-8")

# 2. size based: 5 MB x 5 backups
RotatingFileHandler("logs/framework.log", maxBytes=5_000_000, backupCount=5)

# 3. time based: new file every midnight, keep 7 days
TimedRotatingFileHandler("logs/daily.log", when="midnight", backupCount=7)
```

<!-- Trainer notes: Demo examples/02_logging_handlers_rotation.py. It shows rotating.log, .1, .2, .3 and timed.log with timestamp suffixes. Which to use? Per-run files are the easiest for test automation (one run = one file = attach to the report). Rotating handlers suit long-running services and agents. -->

---

## Per-run log files + folder cleanup

```python
# core/logger.py (course framework)
def setup_logging(level="INFO", keep_last=10):
    old_logs = sorted(LOG_DIR.glob("automation_*.log"))
    for old in old_logs[:max(0, len(old_logs) - (keep_last - 1))]:
        old.unlink(missing_ok=True)          # cleanup
    log_file = LOG_DIR / f"automation_{datetime.now():%Y%m%d_%H%M%S}.log"
    ...
```

- Timestamped names sort chronologically
- Keep the last N runs **or** delete files older than N days
- Otherwise the disk fills up on CI agents

<!-- Trainer notes: Ask: "What happens after 6 months of nightly runs with 50 MB logs?" Disk full, CI agent dies. Cleanup is part of the framework, not a manual chore. -->

---

## Framework logger: configure once, use everywhere

```python
# core/logger.py
def setup_logging(level="INFO", keep_last=10):   # called ONCE (conftest)
    root = logging.getLogger("automation")
    root.addHandler(file_handler)                # DEBUG+ to file
    root.addHandler(console)                     # INFO+ to console

def get_logger(name):                            # called in every module
    return logging.getLogger(f"automation.{name}")
```

```python
# tests/conftest.py
def pytest_configure(config):
    settings = get_config(config.getoption("--env"))
    setup_logging(settings["log_level"])
```

<!-- Trainer notes: The #1 logging bug is duplicate lines, caused by adding handlers every time get_logger is called. The fix: configure once (guard flag), and only fetch loggers afterwards. -->

---

## Using logs to debug failures

1. Open the **per-run log** for the failing run
2. Search for the **first** `ERROR` / `WARNING`, not the last
3. Read the lines **before** it: last successful step, data used
4. Check **timing** (gaps = waits/timeouts), **env**, **locators**
5. Compare with a **passing run's** log

```
10:15:07 | INFO    | Calculate 12 / 0
10:15:07 | DEBUG   | Click {'auto_id': 'divideButton'}
10:15:17 | ERROR   | Timed out after 10s waiting for text 'Display is'
```

<!-- Trainer notes: The 10-second gap between the last DEBUG and the ERROR tells you it was a wait timing out, not a crash. The display said "Cannot divide by zero" - a test data problem, not an app bug. Practise reading logs in Lab 1. -->

---

## Logging: common mistakes

- `print()` in framework code
- Adding handlers in every function, which gives **duplicate lines**
- Logging passwords/tokens (logs get shared and attached to tickets!)
- Everything at INFO (noise) or everything at DEBUG in the console
- `except: pass` with no log
- Not closing handlers, so files stay locked on Windows

<!-- Trainer notes: Security point: mask secrets - log "password=***". Logs end up in bug trackers, emails and CI artefacts visible to many people. -->

---

## Lab 1 (70 min)

**Build a logging-enabled mini framework**

- `hands_on/starter/mini_framework`
- config with dev + qa, `get_config()`
- `setup_logging()` / `get_logger()` with per-run file + cleanup
- `BaseWindow` + `CalculatorWindow` against a **simulated** Calculator
- Run: `python run_demo.py` and `python run_demo.py --env qa`

See `hands_on/Lab_Guide.md`.

<!-- Trainer notes: The simulated desktop has the same API as pywinauto, so nobody's mouse gets hijacked and it works on any laptop. In dev, clicks fail randomly (flaky_click_rate) so trainees SEE the retry warnings in the log. Walk around; the common blockers are YAML indentation and duplicate handlers. -->

---

# Part 3
## PyTest for Desktop and CLI Automation

<!-- Trainer notes: About 75 minutes. Demo everything from examples/pytest_demo - no GUI needed. Keep a terminal open in that folder. -->

---

## Why PyTest (vs unittest)?

| unittest | pytest |
|----------|--------|
| Classes required (`TestCase`) | Plain functions work |
| `self.assertEqual(a, b)` ... | Plain `assert a == b` with rich diff |
| `setUp` / `tearDown` | **Fixtures** (reusable, scoped, composable) |
| Parametrize: awkward | `@pytest.mark.parametrize` |
| Few plugins | 1000+ plugins: html, xdist, rerunfailures |
| - | Runs unittest tests too |

<!-- Trainer notes: pytest is the de-facto standard for Python testing. It can run existing unittest suites, so migration is gradual. Show a 3-line pytest test next to a 7-line unittest equivalent. -->

---

## Test discovery rules

- Starts in `testpaths` (pytest.ini) or the current folder
- Files: `test_*.py` or `*_test.py`
- Functions: `test_*`
- Classes: `Test*` **without** `__init__`, methods `test_*`
- `conftest.py` is loaded automatically

```powershell
pytest --collect-only -q        # what would run?
pytest test_basics.py::test_addition
pytest -k "divide and not zero"
```

<!-- Trainer notes: Most common beginner issue: "pytest found 0 tests" - file named calc_tests.py or function named check_add. Demo --collect-only in examples/pytest_demo. -->

---

## A first test

```python
from calculator import Calculator

def test_addition():
    calc = Calculator().open()
    assert calc.calculate(2, "+", 3) == 5
```

Run and read the output:

```
test_basics.py::test_addition PASSED                        [  1%]
```

Arrange, Act, Assert: **one behaviour per test**.

<!-- Trainer notes: examples/pytest_demo/calculator.py is pure Python "business logic" standing in for the desktop Calculator. The same test shape is used against CalculatorPage in the real framework. -->

---

## Execution flow

```
pytest
  1. read pytest.ini, load plugins + conftest.py
  2. collect tests (discovery)
  3. for each test:
       setup    -> fixtures run (before yield)
       call     -> test function
       teardown -> fixtures finish (after yield)
  4. report: PASSED / FAILED / SKIPPED / XFAIL / ERROR
```

- **FAILED** = assertion/exception in the test
- **ERROR** = exception in setup/teardown (fixture)

<!-- Trainer notes: The setup/call/teardown phases matter later for the makereport hook (report.when). Run pytest test_fixtures.py --setup-show to see SETUP/TEARDOWN lines. -->

---

## Assertions and validations

```python
assert result == 15
assert result == 6, f"Expected 6 but display showed {result}"
assert calc.calculate(0.1, "+", 0.2) == pytest.approx(0.3)
assert "Cannot divide by zero" in calc.display_text()
assert (1.0, "+", 1.0, 2.0) in calc.history
assert not is_valid_username("abc")

with pytest.raises(ZeroDivisionError, match="divide by zero"):
    calc.calculate(5, "/", 0)
```

pytest rewrites `assert` to show **both sides** on failure.

<!-- Trainer notes: Demo a failing assert and show the introspection: "assert 4.0 == 5". pytest.approx for floats: 0.1 + 0.2 != 0.3. pytest.raises for negative tests. Validate state (history), text (in), and types. -->

---

## Validations for desktop and CLI

```python
# Desktop
assert calculator.calculate(7, "+", 8) == 15
assert "Cannot divide by zero" in calculator.display_text()
assert notepad.saved_content() == expected_text

# CLI
result = run_command([*TOOL, "info", "--json"])
assert result.returncode == 0, result.stderr
data = json.loads(result.stdout)
assert data["cpu_count"] >= 1
assert result.duration < 5
```

<!-- Trainer notes: For CLI always check: return code, stdout content, stderr content, and optionally duration. Put stderr in the assert message so the failure explains itself. -->

---

## Fixtures: setup and teardown

```python
@pytest.fixture
def calculator(logger):
    logger.info("SETUP: opening calculator")
    calc = Calculator().open()
    yield calc                   # test runs here
    logger.info("TEARDOWN: closing calculator")
    calc.close()                 # runs even if the test failed

def test_add(calculator):        # request by NAME
    assert calculator.calculate(1, "+", 1) == 2
```

- Code **before** `yield` = setup, **after** = teardown
- Fixtures can use other fixtures

<!-- Trainer notes: Emphasise: teardown after yield runs even when the test fails - this is how we guarantee the app is closed. If setup (before yield) fails, the test shows ERROR, not FAILED. -->

---

## Fixture scopes

| Scope | Created | Desktop example |
|-------|---------|-----------------|
| `function` (default) | per test | fresh Notepad file |
| `class` | per test class | dialog for a group |
| `module` | per test file | Calculator window (slow to start) |
| `package` | per package | - |
| `session` | once per run | config, logger, DB connection |

```python
@pytest.fixture(scope="module")
def calculator(config):
    page = CalculatorPage(config).open()
    yield page
    page.close()
```

<!-- Trainer notes: Trade-off: wider scope = faster but less isolation. The course framework uses module scope for Calculator (clear() is called at the start of calculate) and function scope for Notepad (each test gets a new temp file). Demo test_fixtures.py -s to see the module fixture printed once. -->

---

## conftest.py

- Shared **fixtures** and **hooks** for its folder and sub-folders
- Loaded automatically, **never import it**
- Typical content: `--env` option, `config`, `logger`, app fixtures, report hooks

```python
def pytest_addoption(parser):
    parser.addoption("--env", default=None, help="dev or qa")

@pytest.fixture(scope="session")
def config(request):
    return get_config(request.config.getoption("--env"))
```

<!-- Trainer notes: Open automation_framework/tests/conftest.py and walk through it: --env option, pytest_configure calling setup_logging, collection hook skipping desktop tests on Linux, fixtures, screenshot hook. -->

---

## Built-in fixtures you will use

| Fixture | Purpose |
|---------|---------|
| `tmp_path` | Unique temp folder per test (Path) |
| `caplog` | Capture and assert on log records |
| `capsys` | Capture stdout / stderr |
| `request` | Info about the running test, `addfinalizer` |
| `monkeypatch` | Temporarily set env vars / attributes |

```python
def test_caplog(calculator, caplog):
    caplog.set_level("DEBUG")
    calculator.calculate(6, "/", 3)
    assert "6.0 / 3.0 = 2.0" in caplog.text
```

<!-- Trainer notes: monkeypatch.setenv("TEST_ENV", "qa") is a neat way to test the config reader. caplog lets you assert that a warning WAS logged, e.g. that self-healing reported a fallback. -->

---

## Parameterization (basic)

```python
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-5, 5, 0),
])
def test_add(calculator, a, b, expected):
    assert calculator.calculate(a, "+", b) == expected
```

```
test_add[1-2-3] PASSED
test_add[0-0-0] PASSED
test_add[-5-5-0] PASSED
```

One function, **3 independent tests**. If one fails, the others still run.

<!-- Trainer notes: Compare with a for-loop inside one test: the first failure stops the loop and you don't know about the others. Parametrize gives one result per data row. -->

---

## Parametrize: ids, pytest.param, stacking

```python
@pytest.mark.parametrize("name, valid", [("abcd", False), ("abcde", True)],
                         ids=["min-1", "min"])

@pytest.mark.parametrize("a, op, b, expected", [
    (8, "/", 2, 4),
    pytest.param(1, "/", 3, 0.333, marks=pytest.mark.xfail, id="one-third"),
])

@pytest.mark.parametrize("a", [10, -10])
@pytest.mark.parametrize("op", ["+", "-", "*"])   # 2 x 3 = 6 tests
```

<!-- Trainer notes: ids make reports readable ("test_username[min-1]" beats "test_username[abcd-False]"). pytest.param attaches a marker to ONE row - e.g. a known bug for one data set. -->

---

## Data-driven: parametrize from CSV

```python
def load_csv_cases(path):
    with open(path, newline="", encoding="utf-8") as f:
        return [pytest.param(r["a"], r["op"], r["b"], float(r["expected"]),
                             id=r["case_id"])
                for r in csv.DictReader(f)]

@pytest.mark.parametrize("a, op, b, expected", load_csv_cases(DATA_FILE))
def test_calculator_from_csv(calculator, a, op, b, expected):
    assert calculator.calculate(a, op, b) == pytest.approx(expected)
```

Testers add rows to the CSV: **no code change**.

<!-- Trainer notes: The course framework does the same with test_data/calculator_data.csv via utils.data_reader.read_csv and with cli_cases.yaml for CLI tests. CSV values are strings - convert types! -->

---

## Markers: built-in

```python
@pytest.mark.skip(reason="Scientific mode not implemented")
def test_scientific(): ...

@pytest.mark.skipif(sys.platform != "win32", reason="Windows only")
def test_windows_only(): ...

@pytest.mark.xfail(reason="BUG-101: percentage uses integer division", strict=True)
def test_percentage(): ...

def test_qa_only(config):
    if config["env"] != "qa":
        pytest.skip("qa only")
```

<!-- Trainer notes: skip = don't run. xfail = run it, expected to fail (known bug); strict=True makes an unexpected PASS a failure, so you notice when the bug is fixed. Always give a reason - with a ticket number for xfail. -->

---

## Markers: custom + selection

```ini
# pytest.ini
[pytest]
addopts = -v --strict-markers
markers =
    smoke: quick, critical checks
    regression: full coverage
    desktop: needs a Windows desktop session
    cli: command-line tests
```

```python
pytestmark = pytest.mark.cli          # whole module

@pytest.mark.smoke
def test_info_json_is_valid(run_tool): ...
```

```powershell
pytest -m smoke
pytest -m "cli and not regression"
pytest -m "desktop or cli"
```

<!-- Trainer notes: --strict-markers turns a typo like @pytest.mark.smok into an error instead of a silently unselected test. Demo pytest --markers. In the course framework, CI on Linux runs -m cli while Windows agents also run -m desktop. -->

---

## Useful pytest command line options

| Option | Meaning |
|--------|---------|
| `-v` / `-q` | verbose / quiet |
| `-k "expr"` | select by name |
| `-m "expr"` | select by marker |
| `-x` / `--maxfail=2` | stop after first / 2 failures |
| `--lf` / `--ff` | last-failed only / failed first |
| `-s` | show print output |
| `-ra` | summary of skips, xfails, failures |
| `--setup-show` | show fixture setup/teardown |
| `--log-cli-level=INFO` | live log output |
| `--durations=5` | 5 slowest tests |

<!-- Trainer notes: The full cheat-sheet is in 02_Reading_Material.md. The most used in daily life: -k, -m, -x, --lf, -s. -->

---

## HTML reports (pytest-html)

```powershell
pip install pytest-html
pytest --html=reports/report.html --self-contained-html
```

- Summary, environment, each test with duration, logs and traceback
- `--self-contained-html`: CSS + images **embedded** in ONE file, easy to email or attach to CI
- Customise the title:

```python
@pytest.hookimpl(optionalhook=True)
def pytest_html_report_title(report):
    report.title = "Day 4 - PyTest Demo Report"
```

<!-- Trainer notes: Demo in examples/pytest_demo: run the command, open reports/report.html in a browser. Show filters (passed/failed/skipped), captured log per test. optionalhook=True means no error if the plugin isn't installed. -->

---

## Screenshot and log capture on failure: the hook

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield                        # let pytest build the report
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        path = take_screenshot(item.name)  # PIL ImageGrab
        html = item.config.pluginmanager.getplugin("html")
        if html and path:
            b64 = base64.b64encode(path.read_bytes()).decode()
            report.extras = getattr(report, "extras", []) + [html.extras.png(b64)]
```

<!-- Trainer notes: The hook is called 3 times per test (setup, call, teardown). We only act on a failed "call". hookwrapper + yield: pytest builds the report first, then we add to it. pytest-html 4.x uses report.extras (older blog posts use report.extra - that's outdated). -->

---

## Capturing logs on failure

- pytest **captures** logs per test automatically, shown under "Captured log call"
- `report.caplog`, `report.capstdout`, `report.longreprtext` in the hook
- Write them to an artefact + attach to the report:

```python
log_path.write_text(f"--- captured log ---\n{report.caplog}\n"
                    f"--- failure ---\n{report.longreprtext}")
extras.append(html.extras.text(log_path.read_text(), name="Failure log"))
```

```ini
log_file = logs/pytest_demo.log
log_file_level = DEBUG
```

<!-- Trainer notes: Demo: pytest -m demo_fail --html=reports/failure_report.html --self-contained-html in examples/pytest_demo. Open the report, expand the failure: screenshot (a real desktop capture on Windows, a text placeholder on headless machines) and Failure log. Show the artifacts/ folder. Note: a real screenshot shows EVERYTHING on screen - close private windows first. -->

---

## The opt-in failing demo test

```ini
# pytest.ini
addopts = -v -ra --strict-markers -m "not demo_fail"
markers =
    demo_fail: deliberately failing test (opt-in)
```

```python
@pytest.mark.demo_fail
def test_deliberate_failure_captures_evidence(calculator, logger):
    logger.info("Step 1: add 2 + 2")
    assert calculator.calculate(2, "+", 2) == 5
```

- `pytest` gives all green (demo_fail deselected)
- `pytest -m demo_fail` gives 1 failure + artefacts

<!-- Trainer notes: A later -m on the command line overrides the -m from addopts. This trick keeps the demo suite green while still letting you show failure capture on demand. -->

---

## Desktop + CLI with PyTest: putting it together

```python
# tests/test_calculator.py
pytestmark = pytest.mark.desktop
CASES = read_csv("calculator_data.csv")

@pytest.mark.regression
@pytest.mark.parametrize("case", CASES, ids=[c["test_id"] for c in CASES])
def test_calculator_from_csv(calculator, case):
    result = calculator.calculate(case["num1"], case["operator"], case["num2"])
    assert result == pytest.approx(float(case["expected"]))
```

```powershell
cd automation_framework
pytest -m smoke
pytest -m cli --env qa
pytest --html=reports/report.html --self-contained-html
```

<!-- Trainer notes: If the room allows (and nobody else shares the desktop), you can demo pytest -m "desktop and smoke" on the trainer PC - hands off the keyboard while it runs. Otherwise demo -m cli only. -->

---

## PyTest: common mistakes

- Test file/function not named `test_*` gives **0 tests collected**
- Importing `conftest.py` manually
- Tests that depend on each other's order/state
- Loops instead of parametrize
- `==` on floats instead of `pytest.approx`
- Unregistered markers (typo, silently ignored without `--strict-markers`)
- Catching exceptions in tests, so failures are hidden
- `report.extra` (old) instead of `report.extras` (pytest-html 4)

<!-- Trainer notes: Ask trainees which of these they did in Lab 2. Everyone hits at least one. -->

---

## Lab 2 (75 min)

**PyTest execution with reports**

- **A**: explore `examples/pytest_demo`: markers, `-k`, `--env qa`, `--setup-show`, HTML report, `-m demo_fail`
- **B**: write fixtures, parametrized and negative tests + failure hook for your mini framework
- **C**: run `pytest -m cli` in `automation_framework`, with an HTML report

<!-- Trainer notes: Expected numbers are in the Lab Guide: pytest_demo shows "49 passed, 3 skipped, 1 deselected, 2 xfailed". Mini framework shows "12 passed, 1 deselected". If a trainee's numbers differ, ask them to explain why - good learning. -->

---

# Part 4
## AI Basics for Automation

<!-- Trainer notes: About 30 minutes including the live demo. Tone: AI is a powerful assistant, not a replacement for testing skill. Check your company's AI usage policy and mention it explicitly. -->

---

## Role of AI in automation testing

| Area | What AI can help with |
|------|-----------------------|
| Test design | Suggest test cases, edge cases, BVA/ECP data |
| Scripting | Draft tests, page objects, helpers, regexes |
| Debugging | Explain tracebacks and logs, spot flakiness |
| Maintenance | Refactor, add logging, self-healing locators |
| Analysis | Cluster failures, summarise reports |
| Tools | Copilot-style IDE assistants, chat assistants, AI test platforms |

**Humans still own:** requirements understanding, risk, oracles (what is correct), final review.

<!-- Trainer notes: Keep it vendor-neutral: "an AI coding assistant such as GitHub Copilot, ChatGPT or Claude". Ask who already uses one. Stress that the tester remains accountable for everything committed. -->

---

## AI-assisted script design: prompting

**R-C-T-F-C**: Role, Context, Task, Format, Constraints

```text
Role: You are a senior Python test automation engineer.
Context: Windows 11, Python 3.14, pytest 9, pywinauto (uia). Our page object
CalculatorPage has open(), calculate(a, op, b) -> float, clear(), close().
Task: Write pytest tests for addition and division incl. divide by zero.
Format: one code block, then a short list of assumptions.
Constraints: use the `calculator` fixture, @pytest.mark.parametrize,
markers smoke/desktop, no time.sleep.
```

<!-- Trainer notes: Weak prompt: "write calculator tests". Strong prompt gives the tools, versions, existing API and constraints, so the AI doesn't invent its own framework. More prompts are in examples/ai_prompt_examples.md. -->

---

## Reviewing AI output critically

- **Run it**, more than once
- **Hallucinations**: methods/parameters that don't exist
- **Silent weakening**: removed asserts, broad `except`, retries around asserts
- **Wrong oracle**: expected values the AI guessed
- **Security**: `shell=True`, `eval`, hard-coded secrets
- **Fit**: does it use *our* logger, config, page objects?
- **Explainability**: if you can't explain a line, don't commit it

<!-- Trainer notes: Real example: an assistant "fixed" a flaky test by adding @retry(times=5) around the whole test including the assertion - the bug was still there, the test just stopped reporting it. -->

---

## Never paste secrets or confidential data

- Passwords, API keys, tokens, connection strings
- Customer / personal data, production logs with personal data
- Proprietary source code, unless your **company-approved** tool allows it
- Internal hostnames, IPs, URLs

**Instead:** anonymise (`<SERVER>`, `user@example.com`), trim to a minimal example, and use the enterprise tool your company approves.

<!-- Trainer notes: Many companies have policies - some allow only an enterprise Copilot/ChatGPT/Claude tenant. Anything pasted into a public tool may be stored. When in doubt, ask your lead or security team. -->

---

## Smart retries: exponential backoff

```python
def retry(times=3, delay=1.0, backoff=2.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == times:
                        raise
                    log.warning("attempt %d failed: %s - retry in %.1fs", attempt, e, wait)
                    time.sleep(wait)
                    wait *= backoff        # 1s, 2s, 4s ...
        return wrapper
    return decorator
```

<!-- Trainer notes: Demo examples/04_retry_and_wait.py. Backoff gives a busy system more time on each attempt. Retry ACTIONS (click, connect, run a command), never assertions. Limit the exceptions you retry on - retrying on AssertionError hides bugs. -->

---

## Synchronisation: polling waits

```python
def wait_until(condition, timeout=10, interval=0.5, message="condition"):
    end = time.monotonic() + timeout
    while True:
        try:
            result = condition()
            if result:
                return result
        except Exception:
            pass                           # not ready yet
        if time.monotonic() >= end:
            raise WaitTimeoutError(f"Timed out after {timeout}s waiting for {message}")
        time.sleep(interval)

wait_until(lambda: "Display is 0" in calc.display_text(), timeout=5,
           message="display reset")
```

<!-- Trainer notes: A fixed sleep(10) wastes time when the app is fast and still fails when it's slower. Polling returns as soon as the condition is true. pywinauto's .wait("visible", timeout=...) is the same idea built in. -->

---

## Self-healing locators (concept)

```python
LOCATORS = {"plus": [{"auto_id": "plusButton"},
                     {"title": "Plus", "control_type": "Button"}]}

def find_with_healing(name, locators):
    for i, criteria in enumerate(locators):
        try:
            element = find(**criteria)
            if i > 0:
                log.warning("[%s] HEALED with fallback %s - update page object",
                            name, criteria)
            return element
        except ElementNotFound:
            continue
    raise ElementNotFound(name)
```

AI tools go further: similarity scoring on text, type and position.

<!-- Trainer notes: Demo examples/05_self_healing_locator_concept.py. Show the WRONG heal: 'memory' gets matched to the Seven button by similarity. Lesson: healing must be logged and reviewed, otherwise tests pass while clicking the wrong control. -->

---

## AI-based test data generation

- AI can propose data: boundaries, invalid formats, unicode, long strings, realistic names
- **You** must check it against the requirement
- Classic techniques the AI *should* apply:
  - **Equivalence partitioning**: one value per class
  - **Boundary value analysis**: min-1, min, min+1, max-1, max, max+1
- Make generated data **reproducible**: `random.Random(seed)`

```python
def boundary_values(lo, hi, step=1):
    return [(lo-step, False), (lo, True), (lo+step, True),
            (hi-step, True), (hi, True), (hi+step, False)]
```

<!-- Trainer notes: Demo examples/06_test_data_generation.py - pure Python, no Faker, no AI. It writes generated_test_data.csv, which can feed parametrize. Ask an AI for the same field spec and compare: did it miss max+1? Did it invent rules? -->

---

## Demo: AI-assisted debugging and optimisation

1. Run `examples/07_ai_debugging_before.py` 3 times: inconsistent output
2. Prompt (see `ai_prompt_examples.md`):
   *"Role... Context: export job writes report after 0.5-2s... Task: list every bug and flakiness cause, then rewrite... Constraints: no fixed sleep, logging, exit code, no shell=True"*
3. Review the answer with the checklist
4. Run `examples/08_ai_debugging_after.py`: PASS every time, rc 0, log file

<!-- Trainer notes: LIVE DEMO. If an AI tool is available and allowed, paste the prompt live and compare the answer with 08. If not, show the representative answer in ai_prompt_examples.md. Run 08 with --timeout 0.3 to show a clean, logged failure with rc=1. -->

---

## Before vs after (what changed)

| Before | After |
|--------|-------|
| `time.sleep(1)` | `communicate(timeout)` + `wait_until(file exists)` |
| `except: pass` | specific exceptions, `log.exception` |
| `open()` never closed | `with open(...)` |
| `data == "TOTAL=42"` | `.strip()` then compare |
| stale report reused | deleted before run |
| `shell=True`, `"python"` | `[sys.executable, "-c", ...]` |
| no exit code | `sys.exit(0 / 1)` |
| `print` | console + file logging |

<!-- Trainer notes: Each row is a general lesson that applies to desktop tests too: wait for state, never swallow errors, clean state, use exit codes for CI. -->

---

## Lab 3 (40 min)

**AI-assisted script improvement**

1. Run `flaky_backup_test.py`: observe
2. List **8+ problems yourself** first
3. Write an R-C-T-F-C prompt (no secrets!)
4. Review the AI answer with the checklist
5. Finish `improved_backup_test.py`: must PASS 5 times in a row, from any folder

<!-- Trainer notes: If trainees have no AI access, they do step 3 as a written prompt and use the "typical AI answer" table in solutions/lab3/lab3_prompt_and_review.md for step 4. The critical-review step is the real learning goal. -->

---

## Day 4 recap

- **Framework**: layers (tests, pages, core, utils, config/data), reusable helpers, paths
- **Config + environments**: YAML, `--env` > `TEST_ENV` > default
- **Window Object Model**: `BaseWindow` + one class per window
- **Logging**: levels, formats, handlers, rotation, per-run files, cleanup
- **PyTest**: discovery, fixtures + scopes, conftest, asserts, parametrize, markers
- **Reports**: pytest-html, screenshots + logs on failure
- **AI**: prompts, critical review, retries/waits, self-healing, test data

<!-- Trainer notes: Go back to the whiteboard list of "annoying things" from the morning and tick them off together. -->

---

## Tomorrow (Day 5)

- Mini project on `automation_framework/`
- Add a new window object + tests + data
- Run by markers and environments, HTML report as deliverable

**Homework:** `03_Quiz.md` (20 questions) + read `02_Reading_Material.md` sections 7-9

<!-- Trainer notes: Ask trainees to make sure automation_framework runs "pytest -m cli" on their machine before tomorrow. -->

---

# Q&A

Questions?

Reference: `02_Reading_Material.md` | Examples: `examples/` | Labs: `hands_on/Lab_Guide.md`

<!-- Trainer notes: Common questions: (1) "unittest or pytest at work?" - pytest runs both. (2) "Should we use Robot Framework instead?" - a different style (keyword-driven); the concepts (layers, config, logging, reports) are identical. (3) "Will AI replace testers?" - it replaces repetitive typing, not test thinking; testers who use AI well will replace testers who don't. (4) "How do we run this in CI?" - pytest -m cli --env qa --html=... in a pipeline step, publish reports/ and logs/ as artefacts. -->
