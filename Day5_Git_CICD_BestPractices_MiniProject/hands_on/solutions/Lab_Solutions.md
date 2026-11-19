# Day 5 - Lab Solutions

| Lab | Solution files | How to check |
|---|---|---|
| Lab 1 - Git | `lab1_git_solution.sh` | `bash lab1_git_solution.sh` (Git Bash) - builds everything in `solutions/sandbox_repo/`; `--clean` removes it |
| Lab 2 - GitHub Actions | `lab2_smoke_schedule.yml`, `lab2_test_break_ci.py`, answers below | done on GitHub.com |
| Lab 3 - Refactoring | `lab3_refactored_report_check.py`, `test_lab3_refactored.py` | `python -m pytest test_lab3_refactored.py -v` |

---

## Lab 1 - expected results

* After `git add .` in Task 2, `git status --short` lists README.md, requirements.txt, .gitignore,
  config/, tests/ - but **not** `reports/` (ignored).
* Task 5 conflict markers in `config/config.yaml`:

  ```
  <<<<<<< HEAD
  timeout: 15
  =======
  timeout: 30
  >>>>>>> feature/timeout-qa
  ```
  Resolution = edit the file to the agreed content, delete ALL markers, `git add`, `git commit`.
* Task 6: after `git rebase main` the feature commit gets a **new hash** (it was replayed); the
  final `git merge --ff-only` creates no merge commit, so the top of the graph is a straight line.
* Task 7: `git status -sb` in the clone shows `[behind 1]` after `fetch`; `pull` fast-forwards.
* Task 8 (GitHub): the repo page shows all commits and, under *Tags*, `v1.0.0`.
  If `git push` asks for a password: GitHub needs a **Personal Access Token** or the Git Credential
  Manager browser login - account passwords do not work for Git over HTTPS.

## Lab 2 - answers to the observation questions

1. **Which jobs ran on push?** 4 CLI jobs (ubuntu/windows x Python 3.12/3.13). The desktop job
   shows as *skipped* because the repository variable `DESKTOP_RUNNER_AVAILABLE` is not `true`
   (there is no self-hosted Windows runner).
2. **Why are desktop tests not run on `windows-latest`?** GitHub-hosted Windows runners are
   Windows Server VMs: no Store Calculator / Windows 11 Notepad and no interactive logged-in
   desktop. Desktop UI tests need a self-hosted Windows 10/11 runner started with `run.cmd` in an
   unlocked session.
3. **Where is the HTML report?** Run summary page -> *Artifacts* -> `cli-report-<os>-py<ver>`
   (a zip containing `reports/report.html` and `logs/`).
4. **Why `if: always()` on upload-artifact?** Without it the step is skipped when tests fail -
   exactly when you need the report.
5. **Schedule (Task 5):** cron uses **UTC**. `30 20 * * *` = 02:00 IST. Scheduled workflows run
   only from the **default branch** and GitHub may delay them; after 60 days without repository
   activity GitHub disables them. `workflow_dispatch` gives the manual "Run workflow" button with
   the `env` drop-down.
6. **Break the build (Task 6):** the PR shows a red X, the job log ends with
   `AssertionError: tool says: sysinfo_cli 1.0.0` and `Error: Process completed with exit code 1`.
   pytest exits with a non-zero code -> the step fails -> the job fails -> the workflow fails.
   Fixing the test and pushing again re-runs the checks automatically on the same PR.

## Lab 3 - problems found in `flaky_report_check.py`

| # | Problem | Fix in the solution |
|---|---|---|
| 1 | `time.sleep(2)` - generator needs 0.5-3 s -> random failures | wait for the process (`communicate(timeout=...)`) |
| 2 | cwd-dependent, Windows-only path string | `pathlib`, path relative to `__file__` |
| 3 | shared output file -> stale report from a previous run can make it PASS | fresh `TemporaryDirectory` per run |
| 4 | `shell=True` + string command, `python` may be another interpreter | list command + `sys.executable` |
| 5 | process handle discarded -> hung child left running | keep `Popen`, `kill()` in `finally` |
| 6 | no timeout | `timeout` from `CONFIG` |
| 7 | transient "busy" (exit 75) treated as failure | retry with exponential backoff |
| 8 | bare `except: pass` hides real errors | specific exception classes |
| 9 | `open()` without encoding and never closed | `read_text(encoding="utf-8")` |
| 10 | `print` | `logging` with timestamps / levels |
| 11 | exit code always 0 -> CI would never fail | `return 0 if all(results) else 1` |
| 12 | return code of the generator never checked | explicit checks for 0 / 75 / other |
