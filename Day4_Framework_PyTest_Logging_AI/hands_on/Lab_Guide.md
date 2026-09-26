# Day 4 Hands-on Lab Guide
## Framework, PyTest, Logging and AI-Assisted Automation

| Lab | Topic | Time |
|-----|-------|------|
| Lab 1 | Build a logging-enabled mini framework (structure, logger, config, one window object) | 70 min |
| Lab 2 | PyTest execution: fixtures, markers, parametrize, HTML report, failure capture | 75 min |
| Lab 3 | AI-assisted script improvement (flaky script, then prompt, then reviewed improvement) | 40 min |

### Folder map

```
hands_on/
  Lab_Guide.md                  <- this file
  starter/                      <- YOU work here (files contain "# TODO")
    mini_framework/             <- Lab 1 + Lab 2
    lab3/                       <- Lab 3
  solutions/                    <- complete, working versions (try first, peek later)
    mini_framework/
    lab3/
../examples/pytest_demo/        <- used in Lab 2 part A
../../automation_framework/     <- the course framework, used in Lab 2 part C (read-only today)
```

### Before you start

```powershell
python --version                  # 3.10 or newer (course PCs: 3.14)
python -m pip show pytest pytest-html pyyaml
cd C:\Users\<you>\Documents\Training_Materials\DesktopApps\Day4_Framework_PyTest_Logging_AI\hands_on\starter
code .                            # open in VS Code
```

> **No GUI needed.** The mini framework drives a **simulated Calculator** (`app_sim/simulated_desktop.py`). It has the same methods as pywinauto (`window()`, `child_window()`, `wait()`, `invoke()`, `window_text()`), so your framework code works the same way with the real app. On Day 5 you will use the real framework against the real Calculator.

---

## Lab 1: Build a logging-enabled mini framework (70 min)

### Objective
Build a small **modular, configuration-driven** framework that has:
- a clear folder structure (`config / core / pages / utils / tests / test_data`)
- a YAML config with **two environments** (dev, qa), selected with `--env` or `TEST_ENV`
- a logger that writes to the **console and one log file per run**, and cleans up old logs
- a `BaseWindow` parent class plus **one window object** (`CalculatorWindow`)

### Structure you will complete

```
mini_framework/
  config/config.yaml          TODO: add the qa environment
  core/paths.py               done (all folder paths in one place)
  core/config_reader.py       TODO: load YAML, choose env
  core/logger.py              TODO: handlers, formatter, cleanup
  core/waits.py               done (wait_until, @retry)
  core/base_window.py         TODO: read config, find/click/read_text
  pages/calculator_window.py  TODO: enter_number, press_operator, calculate
  app_sim/simulated_desktop.py done (the "application under test")
  utils/data_reader.py        done (read_csv/read_json/read_yaml)
  run_demo.py                 done (uses everything above)
  test_data/calculator_data.csv
  tests/                      Lab 2
```

### Steps

**Step 1: Explore (5 min).** Open every file and read the docstrings. For each folder, answer: *what is its single responsibility?*

**Step 2: Config (5 min).** In `config/config.yaml`, add a `qa:` block with the **same keys** as `dev` (values are in the TODO comment).
- Hint: YAML indentation must be spaces, never tabs. `qa:` must line up with `dev:`.
- Check it:
  ```powershell
  cd mini_framework
  python -c "import yaml; print(list(yaml.safe_load(open('config/config.yaml'))['environments']))"
  ```
  Expected: `['dev', 'qa']`

**Step 3: Config reader (10 min).** Implement `load_raw()` and `get_config()` in `core/config_reader.py`.
Priority: argument, then `TEST_ENV`, then `default_env`. An unknown env must raise `ValueError`.
```powershell
python -c "from core.config_reader import get_config; print(get_config()['env'], get_config('qa')['timeouts'])"
```
Expected: `dev {'app_start': 10, 'element': 5}`

**Step 4: Logger (15 min).** Implement `cleanup_old_logs()`, the two handlers in `setup_logging()`, and `get_logger()`.
```powershell
python -c "from core.logger import setup_logging, get_logger; setup_logging('DEBUG'); get_logger('check').debug('file only'); get_logger('check').info('console and file')"
```
Expected: only `INFO     minifw.check | console and file` (plus the "Log file" line) appears on the console. Open `logs/run_*.log`: **both** lines are in the file, with function name and line number.

**Step 5: BaseWindow (15 min).** In `core/base_window.py`:
- read the timeouts and retry values **from config** (no hard-coded numbers)
- implement `find()`, the inner `click_control()` and `read_text()`

**Step 6: Window object (15 min).** In `pages/calculator_window.py`, implement `enter_number()`, `press_operator()` and `calculate()`.
- Rule: **locators appear only at the top of this file.** Tests will never see `auto_id`.

**Step 7: Run it (5 min).**
```powershell
python run_demo.py
python run_demo.py --env qa
$env:TEST_ENV="qa"; python run_demo.py; Remove-Item Env:TEST_ENV
```

### Expected output (dev)
```
INFO     minifw | Log file: run_20260926_101500_123456.log (deleted 0 old log(s))
INFO     minifw.run_demo | Environment: dev
INFO     minifw.pages.CalculatorWindow | Launching Calculator
INFO     minifw.pages.CalculatorWindow | Waiting up to 5s for window 'Calculator'
INFO     minifw.pages.CalculatorWindow | Connected to 'Calculator'
INFO     minifw.pages.CalculatorWindow | Calculate 7 + 8
WARNING  minifw.waits | click_control attempt 1/3 failed: plusButton did not respond (simulated flakiness) - retrying in 0.10s
...
INFO     minifw.run_demo | PASS 84 / 4 = 21.0
INFO     minifw.run_demo | Finished: 4 check(s), 0 failure(s). Log: ...\logs\run_....log
```
In **qa** there are no WARNING lines (flaky_click_rate is 0) and the log file has no DEBUG lines (log_level INFO).
Run the script 7 times. The `logs/` folder never holds more than 5 `run_*.log` files, because of `keep_logs` in dev.

### Hints
- `NotImplementedError` in the traceback shows which TODO you have not done yet. Read the traceback bottom-up.
- Duplicate log lines mean you added handlers twice. `setup_logging()` must return early if it is already configured.
- `KeyError: 'qa'` means the YAML indentation is wrong.
- Stuck? Compare your file with `solutions/mini_framework/<same path>`.

### Stretch goals
1. Add a `RotatingFileHandler` (`maxBytes=50_000, backupCount=3`) as a third handler writing `logs/framework.log`.
2. Add a `common:` section to the YAML that is merged into every environment (see `examples/03_logger_config_from_yaml.py`).
3. Add a fallback locator list to `BaseWindow.find()` (see `examples/05_self_healing_locator_concept.py`) and log a WARNING when a fallback is used.

---

## Lab 2: PyTest execution with markers, parametrize and HTML reports (75 min)

### Objective
Run and write pytest tests, select them with markers, drive them with data, and produce a self-contained HTML report that contains failure evidence.

### Part A: Explore the demo project (20 min)

```powershell
cd ..\..\..\examples\pytest_demo     # from hands_on\starter\mini_framework
pytest                               # all tests except the opt-in demo_fail
pytest --collect-only -q             # discovery only, nothing runs
pytest test_fixtures.py -s --setup-show   # watch setup/teardown order
pytest -m smoke                      # only smoke
pytest -m "regression and not slow"
pytest -k csv                        # by name
pytest --env qa                      # custom option from conftest.py
pytest --lf                          # re-run only last failures
```

Expected result of plain `pytest`:
```
=========== 49 passed, 3 skipped, 1 deselected, 2 xfailed in 0.xxs ============
```
With `--env qa`: `50 passed, 2 skipped` (the runtime skip in `test_skip_at_runtime` no longer applies).

Now opt in to the deliberate failure and create an HTML report:
```powershell
pytest -m demo_fail --html=reports/failure_report.html --self-contained-html
pytest --html=reports/report.html --self-contained-html
```
Open both reports in a browser. In `failure_report.html`, expand the failed test: it shows the **screenshot** (or a text placeholder on a machine with no display), the **Failure log** and the captured log. Look in `artifacts/` for the files.

Questions to answer:
1. Why was `test_deliberate_failure_captures_evidence` not run by plain `pytest`?
2. Which hook created the artefacts, and in which phase (`setup`, `call` or `teardown`)?
3. What is the difference between `XFAIL` and `SKIPPED`?

### Part B: Write the tests for your mini framework (40 min)
Work in `starter/mini_framework` (Lab 1 must be finished, or copy the solution's `core/` and `pages/`).

**Step 1: pytest.ini.** Register the markers `desktop` and `demo_fail`, and add `-m "not demo_fail"` to `addopts`.

**Step 2: Fixture.** In `tests/conftest.py`, write a **module-scoped** `calculator` fixture that uses `yield`.

**Step 3: First tests.** In `tests/test_calculator_window.py`, add `pytestmark = pytest.mark.desktop` and complete `test_addition`.

**Step 4: Data-driven and negative tests.** Parametrize from `test_data/calculator_data.csv` with readable ids, then add the divide-by-zero and unsupported-operator tests (`pytest.raises`).

**Step 5: Failure capture.** Implement the `pytest_runtest_makereport` hook (the TODO shows the steps), then add the `demo_fail` test.

Run:
```powershell
pytest                                   # expected: 12 passed, 1 deselected
pytest -m smoke                          # 3 passed (addition + 2 CLI smoke)
pytest -m "desktop and regression"
pytest -m cli --env qa
pytest --html=reports/report.html --self-contained-html
pytest -m demo_fail --html=reports/fail.html --self-contained-html   # 1 failed + snapshot in report
```
Check: `screenshots/` has a snapshot file, and `logs/pytest_last_run.log` plus `logs/run_*.log` exist.

### Part C: Run the course framework's CLI tests (15 min)
```powershell
cd ..\..\..\automation_framework        # project root folder
pytest -m cli
pytest -m cli --env qa --html=reports/report.html --self-contained-html
```
Expected: all CLI tests pass (about 9 selected; desktop tests are deselected). **Do not** run the desktop tests in class unless the trainer asks you to. They take over the mouse and keyboard.
Open `tests/conftest.py` and `tests/test_cli.py` and find: the `--env` option, the `config` fixture, `pytestmark`, the YAML-driven parametrize, and the screenshot hook.

### Hints
- `'desktop' not found in markers configuration option` means you did not register the marker (`--strict-markers` is on).
- `fixture 'calculator' not found` means the fixture is not in `tests/conftest.py`, or its name is misspelled.
- `ModuleNotFoundError: core` means you are not running from the `mini_framework` folder, or `pythonpath = .` is missing.
- The HTML report has no images: use `--self-contained-html`, and check that your hook appends to `report.extras` (pytest-html 4 uses `extras`, not `extra`).

### Stretch goals
1. Add `-n auto` parallel runs (`pip install pytest-xdist`) and explain why module-scoped app fixtures can be a problem.
2. Add the `pytest_html_report_title` hook to rename the report.
3. Add `--reruns 1` (`pip install pytest-rerunfailures`) and discuss when reruns hide real bugs.

---

## Lab 3: AI-assisted script improvement (40 min)

### Objective
Take a flaky automation script, find its problems, use an AI assistant **responsibly** to improve it, and **review** the result before accepting it.

### Steps

**Step 1: Observe the flakiness (5 min).**
```powershell
cd hands_on\starter\lab3
python flaky_backup_test.py
python flaky_backup_test.py
python flaky_backup_test.py
```
Write down each result. Typical: `Backup FAILED` on the first run, then a `FileExistsError` crash on every later run. (Delete the `lab3_work` folder to "reset".)

**Step 2: Find problems yourself first (10 min).** Read `flaky_backup_test.py` and `backup_tool.py`. List at least **8** problems in a table (line, problem, effect). Think about paths, cleanup, file handles, subprocess, waiting, types, error handling, logging and exit codes.

**Step 3: Write a structured prompt (5 min).** Use the Role / Context / Task / Format / Constraints pattern from `../../../examples/ai_prompt_examples.md` (the `examples` folder of Day 4).
**Never paste** passwords, internal server names, customer data or confidential code. Here only the training script is used.

**Step 4: Ask and review (10 min).** Use the assistant your company allows (GitHub Copilot Chat, ChatGPT, Claude, ...). Compare its issue list with yours. Then go through the checklist:

| Check | Yes/No |
|-------|--------|
| It runs 5 times in a row: `RESULT: PASS`, exit code 0 | |
| No fixed `sleep` for synchronisation (polling with a timeout instead) | |
| No bare `except` / `except Exception: pass` | |
| No retries wrapped around assertions | |
| All APIs exist (checked in the Python docs) | |
| It verifies file names **and** contents, and compares `files` as int | |
| Logging goes to console + file, with useful ERROR messages | |
| Paths are built from `__file__`, and the work folder is cleaned | |
| I can explain every line | |

**Step 5: Finish `improved_backup_test.py` (10 min).** Complete the TODOs in the starter, using the AI answer **only where it passed your review**.
```powershell
python improved_backup_test.py
python improved_backup_test.py --files 5
cd ..; python lab3\improved_backup_test.py      # from another folder: must still pass
```

### Expected output
```
10:15:01 | INFO    | Starting backup of 3 file(s)
10:15:03 | INFO    | Backup finished in 1.56s, status={'status': 'done', 'files': 3}
10:15:03 | INFO    | All 3 file(s) present with correct content
10:15:03 | INFO    | RESULT: PASS
```
`logs/improved_backup_test.log` contains the DEBUG details (command, return code, stdout).

### Hints
- The tool finishes in 0.9 s to 2.1 s. A `timeout` of 10 s is generous, and polling ends as soon as it is done.
- `json.JSONDecodeError` can occur if you read `status.json` while it is being written. Treat it as "not ready yet".
- `status["files"]` is an **int**.

### Stretch goals
1. Convert the check into pytest tests (`test_backup_pytest.py` in the solution): parametrize `file_count`, and add a negative test (missing source gives exit code 2).
2. Ask the AI to generate **boundary test data** for `--files` (0, 1, many). Review it, then add the cases.
3. Write a short "AI usage note" for your team: what was accepted, what was rejected, and why.

Solution files: `solutions/lab3/improved_backup_test.py`, `solutions/lab3/test_backup_pytest.py`, `solutions/lab3/lab3_prompt_and_review.md`.
