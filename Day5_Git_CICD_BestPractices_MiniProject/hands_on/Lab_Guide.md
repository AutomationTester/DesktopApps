# Day 5 - Lab Guide

## Git, GitHub Actions CI/CD & Best Practices

| Lab | Topic | Time | Solution |
|---|---|---|---|
| Lab 1 | Git hands-on: local repo, branches, conflict, rebase, tag, clone/pull, push | 25 min (+15 min stretch) | `solutions/lab1_git_solution.sh` |
| Lab 2 | Run the course framework in GitHub Actions | 25 min | `solutions/lab2_smoke_schedule.yml`, `solutions/lab2_test_break_ci.py` |
| Lab 3 | Refactor a flaky automation script | 20 min | `solutions/lab3_refactored_report_check.py`, `solutions/test_lab3_refactored.py` |
| Capstone | Mini project | 3 hours | see `Mini_Project.md` |

Expected results and answers for every lab: `solutions/Lab_Solutions.md`.

### Before you start

| Check | Command | Expected |
|---|---|---|
| Git installed | `git --version` | `git version 2.x` |
| Git Bash available | Start menu -> *Git Bash* | a bash prompt |
| Python + packages | `python -m pytest --version` | `pytest 8.x` or newer |
| GitHub account | log in at github.com | your profile page |
| Git identity | `git config --global user.name` / `user.email` | your name / email (set them if empty) |

> Use **Git Bash** for Lab 1 (commands like `sed`, `cat` and `printf` are used). PowerShell works for Labs 2 and 3.

---

## Lab 1 - Git hands-on (25 min)

**Objective:** use the full daily Git workflow on a small automation repository: init, stage, commit, branch, merge, resolve a conflict, rebase, tag, clone/fetch/pull, and push to GitHub.

Work in a practice folder **outside** the course material, e.g. `C:\git-practice`.

### Task 1 - Create and configure the repository
```bash
mkdir -p /c/git-practice/my-automation-repo && cd /c/git-practice/my-automation-repo
git init -b main
git config --local user.name  "Your Name"
git config --local user.email "you@example.com"
git status
```
**Expected:** `On branch main  No commits yet`.

### Task 2 - Professional skeleton and first commit
1. Create `README.md` (title + how to run), `requirements.txt` (`pytest`, `pytest-html`, `PyYAML`), `config/config.yaml` (`default_env: dev` and `timeout: 10`) and `tests/test_smoke.py` (`def test_truth(): assert 1 + 1 == 2`).
2. Create `.gitignore` with: `reports/`, `logs/`, `screenshots/`, `__pycache__/`, `.venv/`, `.env`.
3. Simulate a test run: `mkdir reports && echo "<html/>" > reports/report.html`.
4. Run `git status --short`, then `git add .`, then `git status --short` again.
5. Commit: `git commit -m "chore: initial project skeleton"`.

**Expected:** `reports/` never appears in the status output, because `.gitignore` works.
**Question:** why must reports, logs and `.env` never be committed?

### Task 3 - See a diff, commit again
```bash
echo "retries: 2" >> config/config.yaml
git diff                                  # red/green lines = what changed
git commit -am "feat(config): add retries setting"
git log --oneline
```
**Expected:** two commits in the log.

### Task 4 - Feature branch and merge
1. `git switch -c feature/cli-test`
2. Add `tests/test_cli.py` that runs `[sys.executable, "--version"]` with `subprocess.run` and asserts return code 0.
3. `git add tests/test_cli.py` and `git commit -m "test: add CLI version test"`
4. `git switch main` and `git merge --no-ff -m "Merge branch 'feature/cli-test'" feature/cli-test`
5. `git branch -d feature/cli-test`

**Expected:** `git log --oneline --graph` shows the branch joining main.

### Task 5 - Create and resolve a merge conflict
```bash
git switch -c feature/timeout-qa
sed -i 's/^timeout: 10$/timeout: 30/' config/config.yaml
git commit -am "feat(config): timeout 30 for slow QA machines"
git switch main
sed -i 's/^timeout: 10$/timeout: 15/' config/config.yaml
git commit -am "feat(config): timeout 15"
git merge feature/timeout-qa           # CONFLICT (content): Merge conflict in config/config.yaml
```
1. Open `config/config.yaml` and find the `<<<<<<<`, `=======` and `>>>>>>>` markers.
2. Team decision: keep `timeout: 30`. Edit the file and delete **all** markers.
3. `git add config/config.yaml` and `git commit -m "merge: resolve timeout conflict (keep 30)"`
4. `git branch -d feature/timeout-qa`

**Expected:** `git status` is clean, and the file contains no markers.

### Task 6 - Rebase and tag a release
```bash
git switch -c feature/docs
echo "## Branching: feature/* -> PR -> main" >> README.md
git commit -am "docs: describe branching"
git switch main
echo "# tests live in tests/" > tests/README.md
git add tests/README.md && git commit -m "docs: tests folder readme"   # main moved on
git switch feature/docs
git rebase main                          # replay our commit on top of main
git switch main
git merge --ff-only feature/docs         # fast-forward, no merge commit
git branch -d feature/docs
git tag -a v1.0.0 -m "Lab 1 release"
git log --oneline --graph --decorate --all
```
**Question:** the feature commit has a **different hash** after the rebase. Why? And why should you never rebase commits that are already pushed and shared?

### Task 7 - Clone, fetch and pull (a "teammate")
```bash
cd /c/git-practice
git clone my-automation-repo teammate-clone
cd my-automation-repo && echo "log_level: INFO" >> config/config.yaml && git commit -am "feat(config): add log_level"
cd ../teammate-clone
git remote -v                 # origin -> ../my-automation-repo
git fetch origin              # download only
git status -sb                # ## main...origin/main [behind 1]
git log --oneline main..origin/main
git pull                      # fetch + merge (fast-forward)
```
**Expected:** after `pull`, the teammate has the `log_level` commit.

### Task 8 - Push to your own GitHub repository
1. On github.com, click **New repository**, name it `my-automation-repo`, **do not** add a README, and click **Create**.
2. In `my-automation-repo`:
   ```bash
   git remote add origin https://github.com/<your-user>/my-automation-repo.git
   git push -u origin main
   git push origin v1.0.0
   ```
3. Refresh the page. You should see the commits, the files, and under *Tags* `v1.0.0`.

> If Git asks for a password: GitHub accepts a **Personal Access Token** or the Git Credential Manager browser login, not your account password.

**Hints:** `git status` tells you what to do next. `git log --oneline --graph --all` shows where you are. Made a mess? `git merge --abort` / `git rebase --abort`.

**Stretch:** open a Pull Request from a new branch `feature/readme-badge` on GitHub, review your own diff, and merge it with **Squash and merge**. Then `git pull` locally.

---

## Lab 2 - Run the framework in GitHub Actions (25 min)

**Objective:** push the course framework to your GitHub repo, watch CI run on Linux and Windows, download the HTML report, add a scheduled workflow, and see a broken test turn the build red.

### Task 1 - Create the repository
1. Create a new empty GitHub repo `desktop-automation-course` (no README).
2. Copy these items from the course folder into a new local folder `C:\git-practice\desktop-automation-course`:
   - `automation_framework/`
   - `.github/`
   - `requirements.txt`
   - `.gitignore`
3. Commit and push:
   ```bash
   cd /c/git-practice/desktop-automation-course
   git init -b main && git add . && git commit -m "chore: add automation framework and CI"
   git remote add origin https://github.com/<your-user>/desktop-automation-course.git
   git push -u origin main
   ```

### Task 2 - Watch the pipeline
1. Open the **Actions** tab and click the running **Automation CI** workflow.
2. Watch the jobs. **Expected:** 4 `CLI tests` jobs (ubuntu/windows x Python 3.12/3.13) turn green. `Desktop tests` shows as **skipped**.
3. Open one job and expand the step **Run CLI tests**. Find the pytest summary line.

**Question:** why is the desktop job skipped? (Read the comment at the top of `automation-ci.yml`.)

### Task 3 - Download the evidence
1. On the run summary page, scroll to **Artifacts**.
2. Download `cli-report-ubuntu-latest-py3.12`, unzip it, and open `reports/report.html` in a browser.
3. Find the log file inside `logs/`.

**Question:** what does `if: always()` on the upload step do, and why does it matter?

### Task 4 - Run it manually with another environment
1. **Actions** -> **Automation CI** -> **Run workflow** -> choose `env: dev` -> **Run workflow**.
2. Open the log of the pytest step. **Expected:** `Environment: dev` in the output.

### Task 5 - Add a scheduled smoke workflow
Create `.github/workflows/smoke-schedule.yml` that:
- runs on `schedule` (weekdays 08:30 IST, which is **03:00 UTC**) and on `workflow_dispatch`
- uses one `ubuntu-latest` job with `timeout-minutes: 10`
- runs only `pytest -m "cli and smoke"` and uploads the report (retention 5 days)

Commit, push, and start it once manually.

**Hints:** cron is always **UTC**. Scheduled runs only fire from the **default branch** and may be delayed. For a quick test you may use `*/15 * * * *` temporarily.

### Task 6 - Break the build on purpose
```bash
git switch -c experiment/break-ci
cp <course>/Day5_Git_CICD_BestPractices_MiniProject/hands_on/solutions/lab2_test_break_ci.py automation_framework/tests/test_break_ci.py
git add . && git commit -m "test: deliberately failing test (lab 2)"
git push -u origin experiment/break-ci
```
1. Open a Pull Request. **Expected:** the checks fail with a red X.
2. Open the failed job and find `AssertionError: tool says: sysinfo_cli 1.0.0`.
3. Fix it by changing `EXPECTED_VERSION` to `"1.0.0"`, then commit and push. **Expected:** the same PR turns green automatically.
4. Close the PR without merging and delete the branch.

**Stretch:** add a CI status badge to `README.md`: `![CI](https://github.com/<user>/<repo>/actions/workflows/automation-ci.yml/badge.svg)`.

**Stretch 2 (Windows laptop owners):** register your laptop as a **self-hosted runner** (*Settings* -> *Actions* -> *Runners* -> *New self-hosted runner* -> Windows) and start it with `run.cmd` in your unlocked session. Then create the repository variable `DESKTOP_RUNNER_AVAILABLE = true` and re-run the workflow. The desktop job now drives Calculator and Notepad on your machine. Remove the runner afterwards.

---

## Lab 3 - Refactor a flaky script (20 min)

**Objective:** turn an unreliable automation script into a deterministic, CI-ready one by applying the best practices from this morning.

Files: `lab3_starter/flaky_report_check.py` (the flaky script) and `lab3_starter/report_generator.py` (the application under test; **do not modify** it).

### Task 1 - Observe the flakiness
```powershell
cd hands_on\lab3_starter
python flaky_report_check.py      # run it 5-10 times
```
**Expected:** a random mix of `PASS`, `FAIL - no report`, and sometimes a stale PASS. Now run the generator directly to understand its contract:
```powershell
python report_generator.py --out out.txt --mode ok;   echo $LASTEXITCODE   # 0
python report_generator.py --out out.txt --mode busy; echo $LASTEXITCODE   # 75
```

### Task 2 - List the problems
Find **at least 8** problems. The `# SMELL` comments mark some of them, but not all. Write them in a table: *problem -> why it causes flakiness -> fix*.

### Task 3 - Refactor
Create `lab3_refactored.py` with these fixes:
1. Build paths with `pathlib`, relative to `__file__` (no cwd dependency, no `\\`).
2. Give each run a fresh temporary folder (no stale report).
3. Use a list command with `sys.executable`: no `shell=True`.
4. Keep the `Popen` handle and wait with a **timeout**, not `sleep`.
5. On timeout, kill **only your own** child process, in `finally`.
6. Retry exit code 75 ("busy") with exponential backoff; fail on other codes.
7. Catch specific exceptions only: no bare `except`.
8. Use `logging` instead of `print`, and read files with `encoding="utf-8"`.
9. Return exit code 0 on pass and 1 on fail, so CI can see the result.

### Task 4 - Prove it with pytest
Write tests that use the generator's deterministic modes (`--mode ok`, `busy`, `hang` with a short timeout):
- `ok` -> passes
- `busy` every time -> fails after N retries with a clear message
- `hang` -> times out, and **no leftover process** remains

Run them 3 times in a row: `for i in 1 2 3; do python -m pytest -q test_lab3.py || break; done`.

**Expected:** identical results every run. That is what "deterministic" means.

**Solution:** `solutions/lab3_refactored_report_check.py`, `solutions/test_lab3_refactored.py`, and the problem table in `solutions/Lab_Solutions.md`.

---

## Wrap-up checklist

- [ ] My repo has `.gitignore`, a README, requirements.txt, and meaningful commit messages
- [ ] I can create a branch, resolve a conflict, and open a PR
- [ ] My GitHub Actions run is green and I downloaded the HTML report artifact
- [ ] I know why desktop tests need a self-hosted Windows runner
- [ ] My refactored script has no `sleep`, no bare `except`, and no leftover processes
