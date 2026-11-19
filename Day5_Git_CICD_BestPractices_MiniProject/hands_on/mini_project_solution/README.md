# Mini Project - Reference Solution

Reference implementation of the Day 5 capstone. Every file is designed to be **copied into
`automation_framework/`** (in your own copy / personal GitHub repo of the course framework).
Nothing in the shared framework has to be edited except `config/config.yaml`, where you
**merge** one block.

## Where each file goes

| File in this folder | Copy to | Purpose |
|---|---|---|
| `workflows/__init__.py` | `automation_framework/workflows/__init__.py` | new package |
| `workflows/mini_project_settings.py` | `automation_framework/workflows/` | reads the `mini_project:` config block with defaults |
| `workflows/calc_to_notepad.py` | `automation_framework/workflows/` | end-to-end workflow: parse -> Calculator -> report -> Notepad |
| `pages/report_notepad_page.py` | `automation_framework/pages/` | `ReportNotepadPage(NotepadPage)`: `write_lines()`, `append_line()`, `saved_text_normalised()` |
| `tools/log_archiver_cli.py` | `automation_framework/tools/` | CLI system task: `collect` system info, `archive` logs, `--keep N` |
| `tests/test_e2e_calc_to_notepad.py` | `automation_framework/tests/` | **desktop** end-to-end tests (needs Windows desktop) |
| `tests/test_workflow_helpers.py` | `automation_framework/tests/` | pure unit tests (marker `cli`, run anywhere) |
| `tests/test_log_archiver_cli.py` | `automation_framework/tests/` | CLI tests for the archiver (marker `cli`) |
| `test_data/expressions.csv` | `automation_framework/test_data/` | dev data (4 rows) |
| `test_data/expressions_qa.csv` | `automation_framework/test_data/` | qa data (8 rows) |
| `config/mini_project_config_snippet.yaml` | **merge** into `automation_framework/config/config.yaml` | per-environment settings |
| `ci/mini-project-ci.yml` | `.github/workflows/mini-project-ci.yml` (repo root) | CI pipeline |

Copy commands (Git Bash, run from the repo root that contains `automation_framework/`):

```bash
SOL=path/to/Day5_Git_CICD_BestPractices_MiniProject/hands_on/mini_project_solution
cp -r "$SOL/workflows"              automation_framework/
cp    "$SOL"/pages/*.py             automation_framework/pages/
cp    "$SOL"/tools/*.py             automation_framework/tools/
cp    "$SOL"/tests/*.py             automation_framework/tests/
cp    "$SOL"/test_data/*.csv        automation_framework/test_data/
mkdir -p .github/workflows && cp "$SOL/ci/mini-project-ci.yml" .github/workflows/
# then edit automation_framework/config/config.yaml and merge the mini_project: block
```

## How to run

```bash
cd automation_framework
pytest -m cli --env dev                              # CLI + unit tests (any OS)
pytest -m cli --env qa  --html=reports/report.html --self-contained-html
pytest -m desktop tests/test_e2e_calc_to_notepad.py --env dev   # Windows desktop only
pytest --env qa --html=reports/full.html --self-contained-html  # everything
python tools/log_archiver_cli.py collect --output reports/sysinfo
python tools/log_archiver_cli.py archive --source logs --dest reports/archives --keep 3
```

## Design notes (discuss in the final review)

* **Page objects only** - the workflow calls `CalculatorPage.calculate()` and the Notepad page's
  `open_file / type_text / save / close_tab`; no raw pywinauto in tests.
* **Extend, don't edit** - `ReportNotepadPage` inherits all Notepad safety rules (own temp file,
  close only own tab with Ctrl+W, never close the whole window).
* **Two oracles** - the Calculator result is compared to Python's own arithmetic, and the report
  is verified **from disk**, not from the screen.
* **Pure vs GUI layers** - parsing/formatting is unit-tested on Linux CI in seconds; only the thin
  GUI layer needs the self-hosted Windows runner.
* **Configuration-driven** - `--env dev` uses 4 expressions, `--env qa` uses 8 and keeps more archives.
* **Reliability** - `@retry` around the idempotent `calculate()` step, fixtures with teardown,
  isolated `tmp_path` data, screenshots on failure come from the framework's `conftest.py`.

## Verification status

* CLI + unit tests (`pytest -m cli`, 24 new + 9 existing) were run and pass on Windows / Python 3.14
  with both `--env dev` and `--env qa` (with and without the config snippet merged).
* Desktop end-to-end tests (`tests/test_e2e_calc_to_notepad.py`, 2 tests) were run live on a
  Windows 11 desktop and pass with both `--env dev` (4 expressions) and `--env qa` (8 expressions).
  Still run them once on the training machine before the session (display scaling/theme can differ).
