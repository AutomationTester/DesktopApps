# Day 5 Capstone - Mini Project

## "Calculator Report" - end-to-end desktop + CLI automation, configuration-driven, in CI

**Duration:** 3 hours · **Teams:** 3-4 trainees · **Pass mark:** 60 / 100

---

## 1. Business scenario

The finance team verifies calculations by hand. For each release they:
1. take a list of expressions,
2. compute each one in the Windows Calculator,
3. type the results into a Notepad report and save it,
4. collect system information and archive the old log files of the test machine.

Your team automates all of this on top of the course framework (`automation_framework/`), so it runs with one command on a laptop, and automatically in CI.

```
 (A) Desktop E2E
     test_data/expressions*.csv --> CalculatorPage.calculate()
                                --> ReportNotepadPage on OUR OWN temp file
                                --> save --> verify the file ON DISK
 (B) CLI / system task
     tools/log_archiver_cli.py   collect | archive --keep N
     tested with pytest -m cli (Linux + Windows)
 (C) config.yaml  mini_project: block   -->  pytest --env dev | qa
 (D) logging, screenshot on failure, HTML report, CI workflow
```

---

## 2. Requirements

### Part A - Desktop end-to-end workflow (Windows)

| ID | Requirement |
|---|---|
| A1 | Read expressions (`id,expression,expected`) from the CSV named in config (`expressions.csv` for dev, `expressions_qa.csv` for qa). |
| A2 | Parse each expression (`"7 + 8"` -> `"7", "+", "8"`); support `+ - * /`, decimals and negative numbers. Invalid text raises `ValueError`. |
| A3 | Compute each expression in Calculator **only through** `CalculatorPage.calculate()`. |
| A4 | Compare with an independent oracle: Python's own arithmetic. |
| A5 | Build report lines like `EXP_01 \| 7 + 8 = 15 \| expected 15 \| PASS`, plus a `TOTAL n \| PASSED p \| FAILED f` line. |
| A6 | Write the report in Notepad using a new `ReportNotepadPage(NotepadPage)` (`write_lines`, `append_line`, `saved_text_normalised`), on a file **the test created** in `tmp_path`. |
| A7 | Save it, then verify the **file on disk** equals the expected text. Don't trust the screen alone. |
| A8 | Close **only your own tab** (`close_tab()`), in fixture teardown. **Never** close the whole Notepad window. |

### Part B - CLI / system task (any OS)

`tools/log_archiver_cli.py`:

| Command | Behaviour |
|---|---|
| `collect --output DIR` | Writes `sysinfo_<timestamp>.json` (os, os_release, machine, python, hostname, cpu_count, disk_free_gb, collected_at) and prints `collected: <path>`. |
| `archive --source DIR --dest DIR [--pattern "*.log"] [--keep N]` | Zips the matching files into `logs_<timestamp>.zip`, then deletes the oldest archives so only `N` remain. |
| `--version` | Prints `log_archiver_cli 1.0.0`. |

Exit-code contract: **0** success · **1** nothing to do (no files matched) · **2** usage error or source folder not found (the message goes to stderr).

### Part C - Configuration-driven execution
- Merge a `mini_project:` block into **each** environment in `config/config.yaml` (`expressions_file`, `report_prefix`, `archive.pattern`, `archive.keep_last`).
- `--env dev` and `--env qa` must visibly change behaviour: dev uses 4 rows and keeps 3 archives, qa uses 8 rows and keeps 5.
- Missing keys fall back to defaults (`workflows/mini_project_settings.py`).

### Part D - Quality and delivery
- Markers: desktop tests `@pytest.mark.desktop`, CLI/unit tests `@pytest.mark.cli`, and one test of each type also `smoke`.
- Logging through `core.logger.get_logger`. No `print` in framework code.
- Screenshots on failure and an HTML report (the framework's `conftest.py` already does this, so make sure it works for your tests).
- Retry only the **idempotent** Calculator step (`@retry`). Never retry assertions.
- Git: work on `feature/mini-project`, commit small and often, and open a PR into `main`.
- CI: CLI and unit tests run green in GitHub Actions and upload the report as an artifact.

---

## 3. Acceptance criteria ("done" means all of these)

- [ ] `pytest -m cli --env dev` and `pytest -m cli --env qa` pass, locally and in CI (ubuntu + windows)
- [ ] `pytest -m desktop --env dev` passes on a Windows 11 desktop, and so does `--env qa` (8 rows)
- [ ] The saved report file on disk matches the expected text exactly (line endings normalised)
- [ ] After the run: no extra Calculator windows, no leftover Notepad tabs, no temp files outside `tmp_path`
- [ ] Running the suite **3 times in a row** gives the same result (no flakiness)
- [ ] No `pytest.skip("TODO")`, no `time.sleep` in tests, no bare `except`
- [ ] `reports/report.html` shows all tests; a forced failure shows an embedded screenshot
- [ ] The README section explains how to run the project, for each environment
- [ ] The PR has a meaningful title, small commits, and green checks

---

## 4. Getting started

1. Use your repo from Lab 2 (`desktop-automation-course`) and create the branch:
   ```bash
   git switch -c feature/mini-project
   ```
2. Copy the starter kit into the framework. The exact commands are in `mini_project_starter/README.md`.
3. Run the tests. The helper tests fail (`NotImplementedError`) and the TODO tests are skipped:
   ```bash
   cd automation_framework
   pytest -m cli -v
   ```
4. Work test-first: make `tests/test_workflow_helpers.py` green, then the CLI tool, then the desktop E2E.

### What's in the starter kit

| File | State | Your job |
|---|---|---|
| `workflows/mini_project_settings.py` | complete | read it, then use `get_mini_project_settings(config)` |
| `workflows/calc_to_notepad.py` | TODO | regex, `parse_expression`, `expected_value`, `format_number`, `build_report_lines`, `compute_all`, `write_report`, `@retry` |
| `pages/report_notepad_page.py` | TODO | `write_lines`, `append_line`, `saved_text_normalised` |
| `tools/log_archiver_cli.py` | parser done | `collect_system_info`, `collect`, `archive` with `--keep` |
| `tests/test_workflow_helpers.py` | complete (test-first) | make them pass |
| `tests/test_log_archiver_cli.py` | 2 examples + 5 TODO | write the 5 tests (collect, archive, keep, missing source, no files) |
| `tests/test_e2e_calc_to_notepad.py` | TODO | fixture (own temp file + `close_tab` teardown) + E2E test + smoke test |
| `config/mini_project_config_snippet.yaml` | TODO for qa | merge into `config/config.yaml` |

### Framework API you will use

```python
from pages.calculator_page import CalculatorPage        # calculate(a, op, b) -> float
from pages.notepad_page import NotepadPage              # open_file(path), type_text(text), text,
                                                        # save(), saved_content(), close_tab()
from utils.data_reader import read_csv                  # read_csv("expressions.csv") -> list of dicts
from core.cli_runner import run_command                 # run_command([...], timeout) -> CommandResult
from core.logger import get_logger
from core.waits import retry, wait_until, WaitTimeoutError
from core.paths import TOOLS_DIR, TEST_DATA_DIR
# fixtures from tests/conftest.py: config (session), calculator (module), notepad (function), tmp_path
```

---

## 5. Suggested team split

| Role | Owns | Hand-off |
|---|---|---|
| **Workflow developer** | `calc_to_notepad.py` pure helpers + unit tests | helpers green by 14:30 |
| **UI automation engineer** | `ReportNotepadPage`, E2E fixture and tests | E2E green on one laptop by 15:45 |
| **CLI / system engineer** | `log_archiver_cli.py` + its tests | `pytest -m cli` green by 14:55 |
| **DevOps / lead** (team of 4) | config merge, CI workflow, PR, README, demo | CI green by 16:00 |

In a team of 3, the lead role is shared.

---

## 6. Timeline

| Time | Activity | Checkpoint |
|---|---|---|
| 13:35 - 13:45 | Brief, teams, branch, copy starter kit | everyone can run `pytest -m cli` |
| 13:45 - 14:55 | Build helpers, CLI tool, CLI tests | **`pytest -m cli` green** |
| 14:55 - 15:05 | *Break* | |
| 15:05 - 16:05 | Desktop E2E, config per env, CI, stabilise (3x repeat run) | E2E green, CI green |
| 16:05 - 16:35 | Team demos (5 min each) + review & optimization discussion | |

> **Trainer rule:** at 14:55 a team without green CLI tests gets the matching file from `mini_project_solution/`, so they can still do the desktop part. The goal is learning, not suffering.

---

## 7. Evaluation rubric (100 marks)

| Area | Marks | Excellent (full) | Adequate (about half) | Missing (0) |
|---|---|---|---|---|
| Desktop E2E workflow | 25 | All rows computed via page objects, report verified **on disk**, own tab closed, works for dev and qa | Works for dev only, or verifies only the screen | Not working |
| CLI tool + tests | 20 | All commands, exit codes 0/1/2 verified, `tmp_path` isolation, `--keep` tested | Main commands work, some tests missing | Not working |
| Configuration-driven | 10 | `mini_project:` in each env, dev/qa visibly differ, defaults work | Only one env configured | Hard-coded values |
| Reliability | 15 | No sleeps, retry only the idempotent step, fixtures clean up, 3 green runs in a row | Occasional flakiness or leftovers | Frequent failures |
| Logging, screenshots, report | 10 | Meaningful INFO/DEBUG logs, screenshot on a forced failure, HTML report | Report only | None |
| CI workflow | 10 | CLI jobs green on ubuntu + windows, artifacts uploaded | Workflow runs but red or no artifacts | No CI |
| Git hygiene | 10 | Feature branch, small conventional commits, PR, README, clean `.gitignore` | Few large commits | Committed reports/logs, or work on main only |

**Bonus (up to +5):** CI status badge, a scheduled regression workflow, self-hosted runner running the desktop job, or a `pytest -m smoke` job on every PR.

---

## 8. Demo checklist (5 minutes per team)

1. Show the architecture: which files you added and why (1 min).
2. Run `pytest -m desktop --env qa` live. The audience watches Calculator and Notepad (1.5 min).
3. Open the saved report file from disk, then `reports/report.html` (0.5 min).
4. Run `python tools/log_archiver_cli.py archive --source logs --dest reports/archives --keep 3` twice, then show that only 3 zips remain (0.5 min).
5. Show the green GitHub Actions run and the downloaded artifact (0.5 min).
6. One thing that was flaky and how you fixed it (1 min).

---

## 9. Final review - discussion questions

- Which tests belong in **smoke** and which in **regression**? What runs on every PR, and what runs nightly?
- Where could a file/CLI check **replace** a slow UI check?
- Module-scoped Calculator fixture versus full isolation: what's the trade-off?
- How would you run this on 3 Windows VMs in parallel? (pytest-xdist, a self-hosted runner pool)
- What would you monitor over time? (duration, flaky rate, retry counts)

**Reference solution:** `mini_project_solution/`, verified live on Windows 11. See its README for where each file goes.
