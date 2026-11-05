# Day 5 - Reading Material
## Git, CI/CD with GitHub Actions, Desktop & CLI Best Practices, Mini Project

Python Desktop Application Automation Testing - Trainee Handbook

---

## Table of Contents

1. [Learning objectives](#1-learning-objectives)
2. [Version control with Git](#2-version-control-with-git)
   - 2.1 Why Git for test automation
   - 2.2 The three areas and the basic workflow
   - 2.3 Configuration and a new repository
   - 2.4 status, add, commit, log, diff
   - 2.5 Remotes: clone, remote, push, fetch, pull
   - 2.6 Undoing things safely
   - 2.7 Branching and branching strategies
   - 2.8 Pull Requests and code review
   - 2.9 Merge vs rebase
   - 2.10 Resolving a merge conflict
   - 2.11 Best practices for automation repositories
   - 2.12 Git command cheat sheet
3. [CI/CD using GitHub Actions](#3-cicd-using-github-actions)
   - 3.1 CI/CD fundamentals
   - 3.2 GitHub Actions building blocks
   - 3.3 Workflow YAML structure
   - 3.4 The course workflow annotated line by line
   - 3.5 Running Python automation in CI
   - 3.6 Headless and scheduled execution
   - 3.7 Linux runner considerations for desktop and CLI automation
   - 3.8 Self-hosted Windows runner for desktop tests
   - 3.9 Reading a failed run
4. [Desktop & CLI automation best practices](#4-desktop--cli-automation-best-practices)
   - 4.1 Desktop vs CLI vs system automation
   - 4.2 UI object identification and synchronization
   - 4.3 Native dialogs and controls
   - 4.4 Never assume a clean application state
   - 4.5 Reliability and failure recovery
   - 4.6 Cross-platform challenges
5. [Mini project overview](#5-mini-project-overview)
6. [Best-practices checklist](#6-best-practices-checklist)
7. [Common mistakes (all topics)](#7-common-mistakes-all-topics)
8. [Questions and answers](#8-questions-and-answers)
9. [Day 5 summary](#9-day-5-summary)

---

## 1. Learning objectives

By the end of Day 5 you will be able to:

* Use Git daily: init, clone, add, commit, push, pull, fetch, branch, merge, rebase, tag.
* Choose a branching strategy, work through Pull Requests and resolve merge conflicts.
* Structure an automation repository professionally (.gitignore, README, requirements, no secrets).
* Explain CI/CD and read/write GitHub Actions workflow YAML.
* Run pytest-based automation in CI with caching, HTML reports and artifacts.
* Schedule runs, trigger them manually, and explain what "headless" means for desktop apps.
* Decide which tests run on Linux runners and which need a Windows desktop (self-hosted runner).
* Apply best practices for locators, waits, dialogs, clean state, retries, cleanup and cross-platform code.
* Deliver an end-to-end, configuration-driven desktop + CLI automation project with CI.

---

## 2. Version control with Git

### 2.1 Why Git for test automation

A test automation framework is software. Without version control a team quickly ends up with
copies such as `test_calc_final_v3.py` on shared drives, nobody knows which locator change broke
the nightly run, and two testers overwrite each other's work.

Git gives you:

| Benefit | What it means for a tester |
|---|---|
| History | See who changed a locator, when, and why (`git log`, `git blame`) |
| Safety net | Return to the last working version in seconds |
| Parallel work | Each tester works on a branch; changes are merged later |
| Review | Changes are checked in a Pull Request before they reach `main` |
| Automation | A push to GitHub triggers the CI pipeline |

**Git** is the version control tool that runs on your computer. **GitHub** is a hosting service
for Git repositories that adds Pull Requests, code review, issues and **GitHub Actions** (CI/CD).
GitLab, Bitbucket and Azure DevOps are alternatives; the Git commands are the same.

### 2.2 The three areas and the basic workflow

```
  Working Directory        Staging Area          Local Repository        Remote (GitHub)
  (your files)             (index)               (.git folder)           (origin)
 +----------------+      +--------------+      +------------------+     +---------------+
 | edit files     | ---> | next commit  | ---> | commit history   | --> | shared history|
 |                | add  |              |commit|                  |push |               |
 |                | <--------------------------|                  | <-- |               |
 +----------------+  switch / restore          +------------------+ fetch/pull ---------+
```

* **Working directory** - the files you see and edit.
* **Staging area (index)** - a "shopping basket" of changes that will go into the next commit.
  You choose exactly what to include with `git add`.
* **Local repository** - the `.git` folder with all commits (snapshots). Created by `git init`
  or `git clone`.
* **Remote** - a copy on a server (GitHub), usually called `origin`.

A **commit** is a snapshot of the staged files plus a message, author, timestamp and a pointer
to its parent commit. It is identified by a hash such as `3a53131`.

### 2.3 Configuration and a new repository

```bash
git --version                                   # is Git installed?
git config --global user.name  "Asha Tester"    # stamped on every commit
git config --global user.email "asha@company.com"
git config --global init.defaultBranch main
git config --global core.autocrlf true          # Windows (Linux/macOS: input)
git config --list --show-origin                 # where does each setting come from?
```

* `--global` applies to your user account; `--local` applies to one repository only
  (stored in `.git/config`) and wins over global.

Create a repository:

```bash
mkdir my-automation-repo
cd my-automation-repo
git init                # creates .git/  -> this folder is now a repository
git status
```

### 2.4 status, add, commit, log, diff

```bash
git status                  # what is modified / staged / untracked?
git status --short          # compact: ?? untracked, A added, M modified, UU conflict
git add README.md           # stage one file
git add tests/              # stage a folder
git add .                   # stage everything not ignored
git commit -m "feat: add calculator smoke test"
git log --oneline --graph --decorate --all
git diff                    # working directory vs staging area (unstaged changes)
git diff --staged           # staging area vs last commit (what will be committed)
git show HEAD               # details of the last commit
```

Reading a diff:

```
--- a/tests/test_calculator.py
+++ b/tests/test_calculator.py
@@ -10,7 +10,7 @@ def test_addition(calculator):
-    assert calculator.calculate(7, "+", 8) == 16
+    assert calculator.calculate(7, "+", 8) == 15
```

Lines starting with `-` were removed, lines with `+` were added. This is exactly what reviewers
see in a Pull Request.

### 2.5 Remotes: clone, remote, push, fetch, pull

```bash
# get an existing repository
git clone https://github.com/acme/automation_framework.git
cd automation_framework
git remote -v                       # 'origin' is where you cloned from

# publish a local repository to a new, EMPTY GitHub repository
git remote add origin https://github.com/<you>/my-automation-repo.git
git push -u origin main             # -u remembers origin/main as "upstream"
git push                            # later pushes of the current branch
git push origin v1.0.0              # push a tag (tags are not pushed by default)

# get the team's changes
git fetch origin                    # download only - your files are untouched
git status -sb                      # e.g. "## main...origin/main [behind 2]"
git log --oneline main..origin/main # what is new on the remote?
git pull                            # fetch + merge into the current branch
git pull --rebase                   # fetch + rebase (linear history)
```

**fetch vs pull**: `fetch` is always safe - it only updates `origin/main`. `pull` also changes
your branch and can produce conflicts. Good habit: *pull before you start, push when you finish*.

**Authentication**: GitHub does not accept your account password for Git over HTTPS. Use the Git
Credential Manager login (Git for Windows opens a browser on first push) or a Personal Access
Token (PAT). SSH keys are another option.

### 2.6 Undoing things safely

| Situation | Command | Safe for pushed work? |
|---|---|---|
| Discard unstaged edits in a file | `git restore file.py` | yes (local only) |
| Unstage a file (keep edits) | `git restore --staged file.py` | yes |
| Change the last commit (message/files) | `git commit --amend` | **no** - only if not pushed |
| Undo a commit by adding an inverse commit | `git revert <hash>` | **yes** |
| Move the branch back and drop commits | `git reset --hard <hash>` | **no** - destroys work |
| Put work aside temporarily | `git stash` / `git stash pop` | yes |
| Abort a merge in progress | `git merge --abort` | yes |

Rule: never rewrite history that others have already pulled. Use `revert` on shared branches.

### 2.7 Branching and branching strategies

A branch is a lightweight movable pointer to a commit. Creating one is instant.

```bash
git branch                          # list local branches (* = current)
git switch -c feature/notepad-save  # create and switch (older: git checkout -b)
git switch main                     # switch back
git merge feature/notepad-save      # merge into the current branch
git branch -d feature/notepad-save  # delete a merged branch
git push -u origin feature/notepad-save   # publish the branch
```

**Feature branch workflow** (recommended for automation repositories)

* One branch per task: `feature/calc-division-tests`, `fix/notepad-save-wait`, `chore/bump-pytest`.
* Merged into `main` through a Pull Request after CI passes and a colleague reviews.
* `main` is always green.

**GitFlow**

* Long-lived branches `main` (released versions) and `develop` (integration).
* Short-lived `feature/*`, `release/*`, `hotfix/*`.
* Suits products with planned, versioned releases; more ceremony and more merges.

**Trunk-based development**

* Everybody integrates into `main` (the trunk) at least daily; branches live hours, not weeks.
* Requires a strong automated test suite and feature flags. Fastest feedback, fewest conflicts.

```
GitFlow
main     o---------------------o-----------o   (v1.0)      (v1.1)
          \                   /           /
develop    o---o-------o-----o-----o-----o
                \     /       \       /
feature/x        o---o         o-----o feature/y

Trunk-based
main     o--o--o--o--o--o--o--o--o      (tiny branches merged the same day)
```

### 2.8 Pull Requests and code review

1. Push your branch: `git push -u origin feature/x`.
2. On GitHub click **Compare & pull request**. Describe *what*, *why* and *how you tested*.
3. CI checks run automatically and report green/red on the PR.
4. Reviewers comment; you push fixes to the same branch (the PR updates itself).
5. After approval: **Merge** (merge commit, squash or rebase - team choice) and delete the branch.

Protect `main`: *Settings -> Branches -> Add rule*: require a Pull Request, require status
checks (the CI jobs) to pass, and optionally require one approval.

Review checklist for automation code:

* Locators are stable (auto_id) and live in page objects.
* No `time.sleep()` used for synchronization.
* Test creates and cleans up its own data; tests are independent.
* No secrets, no personal paths, no commented-out junk.
* Meaningful test names and assertion messages; markers set correctly.

### 2.9 Merge vs rebase

```
Before:        main  A---B---C
                          \
               feature     D---E

git merge      A---B---C-------M       real history, one extra merge commit
                        \     /
                         D---E

git rebase     A---B---C---D'--E'      linear history; D and E are re-created (new hashes)
```

* `git merge feature` (on main): safe, preserves what actually happened. Default choice.
* `git rebase main` (on feature): replays your commits on top of the latest main. Produces a tidy
  line, but rewrites your commits. **Only rebase branches that nobody else has pulled.**
* `git merge --ff-only` merges only if no merge commit is needed (after a rebase).

### 2.10 Resolving a merge conflict

A conflict happens when two branches change the **same lines** of the same file (or one deletes a
file the other edits). Git stops and marks the file:

```
<<<<<<< HEAD
timeout: 15
=======
timeout: 30
>>>>>>> feature/timeout-qa
```

* Between `<<<<<<< HEAD` and `=======`: your current branch.
* Between `=======` and `>>>>>>>`: the incoming branch.

Steps:

```bash
git merge feature/timeout-qa         # CONFLICT (content): Merge conflict in config.yaml
git status                           # "both modified: config.yaml"
# edit the file: keep the correct content, delete ALL marker lines
#   (VS Code offers Accept Current / Accept Incoming / Accept Both / Compare)
git add config.yaml                  # tells Git the conflict is resolved
git commit                           # finishes the merge
pytest -m smoke                      # prove nothing broke
```

Changed your mind? `git merge --abort` restores the state before the merge.

Practice it safely: `examples/git_practice.sh` creates a throwaway repository with a real
conflict and resolves it.

### 2.11 Best practices for automation repositories

**Folder structure** - predictable and documented:

```
repo/
  README.md
  requirements.txt
  .gitignore
  .github/workflows/automation-ci.yml
  automation_framework/
    pytest.ini  config/  core/  pages/  tests/  test_data/  tools/  utils/
```

**.gitignore** - commit source, never output. At minimum:

```gitignore
reports/
logs/
screenshots/
__pycache__/
.pytest_cache/
.venv/
.env
```

A complete, commented version is in `examples/sample.gitignore`. Check what is ignored with
`git status --ignored`. If a file was committed before being ignored: `git rm --cached <file>`.

**No secrets in the repository**

* Read passwords/tokens from environment variables; in CI from GitHub **Secrets**.
* Commit a `.env.example` with fake values; ignore the real `.env`.
* If a secret was pushed: **revoke/rotate it immediately**. Removing the commit is not enough -
  forks, clones and caches keep it.

**Commit messages** (Conventional Commits style):

```
feat(calculator): add division by zero test
fix(notepad): wait until title loses '*' after save
test(cli): cover exit code 2 for unknown command
docs: explain --env option in README
chore: bump pytest-html to 4.1
```

Short imperative subject (< 72 characters), optional body explaining *why*.
Avoid: `update`, `fix`, `changes`, `wip`, `asdf`.

**README.md** - what the framework tests, prerequisites, installation, how to run
(`pytest -m smoke --env qa`), markers, environments, how to add a test, CI status badge.

**requirements.txt** - every dependency with a minimum or pinned version, so CI and every
laptop install the same things: `pip install -r requirements.txt`. Platform-specific packages can
use markers, e.g. `pywinauto>=0.6.8; sys_platform == "win32"` (as in the course repo).

**Tag releases** of the framework so results can be reproduced:

```bash
git tag -a v1.2.0 -m "Notepad regression suite"
git push origin v1.2.0
git checkout v1.2.0      # later: exact code that verified release X
```

**Line endings**: add a `.gitattributes`:

```
* text=auto
*.sh text eol=lf
*.bat text eol=crlf
```

### 2.12 Git command cheat sheet

| Category | Command | Purpose |
|---|---|---|
| Setup | `git config --global user.name "Name"` | Set author name |
| Setup | `git config --global user.email "e@x.com"` | Set author email |
| Setup | `git config --list` | Show settings |
| Create | `git init` | New repository in current folder |
| Create | `git clone <url> [folder]` | Copy a remote repository |
| Inspect | `git status` / `git status -sb` | State of working dir and staging |
| Inspect | `git diff` | Unstaged changes |
| Inspect | `git diff --staged` | Staged changes |
| Inspect | `git log --oneline --graph --decorate --all` | History as a graph |
| Inspect | `git show <hash>` | One commit in detail |
| Inspect | `git blame file.py` | Who last changed each line |
| Save | `git add <file>` / `git add .` | Stage changes |
| Save | `git commit -m "message"` | Record a snapshot |
| Save | `git commit -am "message"` | Stage tracked files + commit |
| Save | `git stash` / `git stash pop` | Park / restore unfinished work |
| Branch | `git branch` | List branches |
| Branch | `git switch -c feature/x` | Create + switch |
| Branch | `git switch main` | Switch branch |
| Branch | `git branch -d feature/x` | Delete merged branch |
| Combine | `git merge feature/x` | Merge branch into current |
| Combine | `git merge --abort` | Cancel a conflicted merge |
| Combine | `git rebase main` | Replay current branch on main |
| Remote | `git remote -v` | List remotes |
| Remote | `git remote add origin <url>` | Connect to a remote |
| Remote | `git fetch` | Download without merging |
| Remote | `git pull` / `git pull --rebase` | Fetch + merge / rebase |
| Remote | `git push -u origin <branch>` | First push of a branch |
| Remote | `git push` | Push current branch |
| Undo | `git restore <file>` | Discard unstaged edits |
| Undo | `git restore --staged <file>` | Unstage |
| Undo | `git revert <hash>` | Inverse commit (safe) |
| Undo | `git reset --hard <hash>` | Drop commits (dangerous) |
| Ignore | `git rm --cached <file>` | Stop tracking a file, keep it on disk |
| Release | `git tag -a v1.0.0 -m "msg"` | Annotated tag |
| Release | `git push origin v1.0.0` / `git push --tags` | Publish tags |

### Common mistakes (Git)

* Committing `reports/`, `logs/`, `.venv/` because `.gitignore` was added too late.
* Committing a password in `config.yaml` "just for testing".
* Working directly on `main` and pushing untested changes.
* Long-lived branches that diverge for weeks -> huge conflicts.
* Leaving `<<<<<<<` markers in a file after a conflict (breaks Python and YAML).
* `git push --force` on a shared branch, wiping colleagues' commits.
* Rebasing a branch that others already pulled.
* Commit messages like `update` that explain nothing.

### Try it yourself (Git)

1. Run `bash examples/git_practice.sh` and read every step of the output.
2. `cd examples/sandbox_repo` and run `git log --graph --oneline`, `git show v1.0.0`.
3. Create your own conflict: two branches change the same line of `README.md`; resolve it in VS Code.
4. Add `.gitattributes` with `* text=auto` and observe `git status`.
5. Delete the sandbox: `bash examples/git_practice.sh --clean`.

### Summary (Git)

Git records snapshots of your work in three steps (edit -> add -> commit) and shares them via
remotes (push/fetch/pull). Branches isolate work; Pull Requests with CI and review protect `main`.
Conflicts are normal and resolved by editing, `git add` and `git commit`. A professional
automation repo has a good `.gitignore`, no secrets, meaningful commits, a README, a
requirements file, a clear structure and tagged releases.

---

## 3. CI/CD using GitHub Actions

### 3.1 CI/CD fundamentals

* **Continuous Integration (CI)** - developers integrate changes frequently; every change is
  automatically built and tested. Failures are found within minutes of the change that caused them.
* **Continuous Delivery** - every green build is releasable; a human presses the button.
* **Continuous Deployment** - every green build is released automatically.

```
 code change -> push -> build -> unit/CLI tests -> desktop/E2E tests -> reports -> (release)
                           \_______________ fast feedback _______________/
```

Why it matters to testers:

* Your tests run automatically on every push, Pull Request and every night.
* Clean, repeatable environments remove "works on my machine".
* Reports, logs and screenshots are stored as evidence (artifacts).
* The team sees a red/green status on each commit and PR.

### 3.2 GitHub Actions building blocks

| Term | Meaning | Example |
|---|---|---|
| Workflow | A YAML file in `.github/workflows/` describing the pipeline | `automation-ci.yml` |
| Event | What starts a workflow | `push`, `pull_request`, `schedule`, `workflow_dispatch` |
| Job | A set of steps on one runner; jobs run in parallel unless `needs:` | `cli-tests` |
| Step | One shell command (`run:`) or one action (`uses:`) | `run: pytest -m cli` |
| Runner | The machine that runs a job | `ubuntu-latest`, `windows-latest`, `[self-hosted, windows]` |
| Action | Reusable, versioned step published by GitHub or the community | `actions/checkout@v4` |
| Secret | Encrypted value, masked in logs | `${{ secrets.QA_API_TOKEN }}` |
| Variable | Plain (non-secret) configuration value | `${{ vars.DESKTOP_RUNNER_AVAILABLE }}` |
| Artifact | Files uploaded from a run and downloadable afterwards | HTML report zip |
| Expression / context | `${{ ... }}` with data about the run | `${{ github.ref_name }}`, `${{ matrix.os }}` |

Each job starts on a **fresh machine**. Steps in the same job share the file system; different
jobs do not (use artifacts to pass files between jobs).

### 3.3 Workflow YAML structure

```yaml
name: <display name>
on: <events>
env: <variables for all jobs>            # optional
jobs:
  <job-id>:
    name: <display name>                 # optional
    runs-on: <runner label(s)>
    needs: <other job-id>                # optional ordering
    if: <condition>                      # optional
    strategy:                            # optional matrix
      matrix: { ... }
    defaults:
      run:
        working-directory: <folder>
    steps:
      - uses: <owner/action@version>
        with: { <inputs> }
      - name: <step name>
        run: <shell command(s)>
```

YAML rules: indentation with spaces only, `key: value`, lists start with `- `, `|` starts a
multi-line string, `#` starts a comment. Quote values that look like numbers or contain `*`
(`python-version: "3.12"`, `cron: "30 20 * * *"`) - unquoted `3.10` would become the number 3.1!

Samples to study, from simple to advanced, in `examples/github_actions/`:

| File | Shows |
|---|---|
| `01_hello_world.yml` | events, job, steps, contexts, checkout |
| `02_python_tests.yml` | setup-python, pip cache, pytest, HTML report artifact |
| `03_matrix_os_python.yml` | OS x Python matrix, `needs`, self-hosted desktop job |
| `04_scheduled_headless.yml` | cron, workflow_dispatch inputs, Xvfb, self-hosted Windows |
| `05_artifacts_and_secrets.yml` | secrets, variables, permissions, artifacts on failure |

### 3.4 The course workflow annotated line by line

File: `.github/workflows/automation-ci.yml` (repository root).

```yaml
name: Automation CI                     # (1) name in the Actions tab and on PR checks

on:                                     # (2) EVENTS
  push:
    branches: [main]                    #     every push to main
  pull_request:                         #     every PR (any target branch)
  schedule:
    - cron: "30 20 * * *"               #     nightly 20:30 UTC = 02:00 IST
  workflow_dispatch:                    #     manual "Run workflow" button ...
    inputs:
      env:                              #     ... with a drop-down to choose the environment
        description: "Environment from config.yaml"
        default: qa
        type: choice
        options: [dev, qa]

jobs:
  cli-tests:                            # (3) JOB 1 - command-line tests
    name: CLI tests (${{ matrix.os }}, py${{ matrix.python }})
    runs-on: ${{ matrix.os }}           #     runner comes from the matrix
    strategy:
      fail-fast: false                  #     do not cancel other combinations on failure
      matrix:
        os: [ubuntu-latest, windows-latest]
        python: ["3.12", "3.13"]        #     2 x 2 = 4 parallel jobs
    defaults:
      run:
        working-directory: automation_framework   # every run: step starts in this folder
    steps:
      - uses: actions/checkout@v4       # (4) get the repository code onto the runner

      - uses: actions/setup-python@v5   # (5) install the requested Python version
        with:
          python-version: ${{ matrix.python }}
          cache: pip                    #     cache pip downloads between runs (faster)

      - name: Install dependencies      # (6) requirements.txt is in the repo root -> ../
        run: pip install -r ../requirements.txt

      - name: Run CLI tests             # (7) only tests marked @pytest.mark.cli
        run: pytest -m cli --env ${{ inputs.env || 'qa' }} --html=reports/report.html --self-contained-html
        #     inputs.env exists only for manual runs; push/schedule fall back to 'qa'

      - name: Upload report and logs    # (8) keep evidence
        if: always()                    #     run even if the previous step failed
        uses: actions/upload-artifact@v4
        with:
          name: cli-report-${{ matrix.os }}-py${{ matrix.python }}   # unique per matrix job
          path: |
            automation_framework/reports/
            automation_framework/logs/

  desktop-tests:                        # (9) JOB 2 - Calculator / Notepad tests
    name: Desktop tests (self-hosted Windows)
    if: vars.DESKTOP_RUNNER_AVAILABLE == 'true'  # switched on by a repository variable
    runs-on: [self-hosted, windows]     #     a real Windows 10/11 machine you registered
    needs: cli-tests                    #     start only after all CLI jobs succeeded
    defaults:
      run:
        working-directory: automation_framework
    steps:
      - uses: actions/checkout@v4
      - name: Install dependencies      #     Python is pre-installed on the self-hosted machine
        run: python -m pip install -r ../requirements.txt
      - name: Run desktop tests
        run: python -m pytest -m desktop --env ${{ inputs.env || 'qa' }} --html=reports/report.html --self-contained-html
      - name: Upload report, logs and screenshots
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: desktop-report
          path: |
            automation_framework/reports/
            automation_framework/logs/
            automation_framework/screenshots/
```

Key points:

* The **CLI job** proves the CLI tool and framework core work on Linux and Windows, Python 3.12
  and 3.13, on every change - cheap and fast.
* The **desktop job** is gated by `if:` and runs on a **self-hosted** runner because
  GitHub-hosted Windows runners are Windows Server VMs without Store Calculator / Windows 11
  Notepad and without an interactive desktop session (section 3.8).
* `needs: cli-tests` avoids spending time on slow UI tests when the basics are already broken.
* `if: always()` on upload steps makes sure the report exists exactly when tests fail.

### 3.5 Running Python automation in CI

Recipe for any Python test job:

1. `actions/checkout@v4` - get the code.
2. `actions/setup-python@v5` with `python-version` and `cache: pip`
   (optionally `cache-dependency-path: requirements.txt`).
3. `pip install -r requirements.txt`.
4. Run pytest with markers, environment and report options:
   `pytest -m cli --env qa --html=reports/report.html --self-contained-html --junitxml=reports/junit.xml`
5. `actions/upload-artifact@v4` with `if: always()` for `reports/`, `logs/`, `screenshots/`.

How the job turns red: pytest exits with code 1 when any test fails (2-5 for usage/collection
errors). A non-zero exit code fails the step; a failed step fails the job and the workflow.

Useful extras:

* `timeout-minutes: 15` on a job - a hung UI test must not burn hours of runner time.
* `--junitxml` creates a machine-readable result many tools can display.
* `retention-days:` on artifacts controls storage.
* Pin actions to a major version (`@v4`) or a commit SHA for stricter supply-chain security.

### 3.6 Headless and scheduled execution

**Scheduled runs** use cron syntax, always in **UTC**:

```
 +------------- minute        (0 - 59)
 | +----------- hour          (0 - 23)
 | |  +-------- day of month  (1 - 31)
 | |  | +------ month         (1 - 12)
 | |  | | +---- day of week   (0 - 6, 0 = Sunday)
 30 20 * * *        every day 20:30 UTC  (02:00 IST)
 0 3 * * 1-5        Mon-Fri 03:00 UTC    (08:30 IST)
 */15 * * * *       every 15 minutes (testing only - wasteful)
```

Facts: scheduled workflows run on the **default branch** only, may start several minutes late
under load, and GitHub disables schedules in repositories without activity for 60 days.

**Manual runs**: `workflow_dispatch`, optionally with `inputs` (choice, string, boolean). Read
them with `${{ inputs.name }}`.

**Headless** means nobody is watching and often there is no physical monitor:

* **CLI tests** are naturally headless.
* **Browser tests** can run in real headless mode.
* **Linux GUI apps** can run on a virtual display: `xvfb-run -a pytest ...`
  (Xvfb = X virtual frame buffer).
* **Windows desktop apps** automated through UI Automation need a **real, interactive,
  unlocked desktop session**. There is no true "headless" mode for them: the session can be on a
  VM nobody watches, but it must exist, be logged in, and not be locked.

### 3.7 Linux runner considerations for desktop and CLI automation

| Test type | ubuntu-latest | windows-latest (hosted) | self-hosted Windows 10/11 |
|---|---|---|---|
| CLI tool (`sysinfo_cli.py`, archiver) | yes | yes | yes |
| Unit tests of pure helpers | yes | yes | yes |
| Linux GUI app (Tk/Qt) | yes, with Xvfb | no | no |
| Windows desktop app (Calculator, Notepad) | **no** | **not reliable** | **yes** |

* Linux runners have no Windows desktop applications and pywinauto does not work there.
  The course `requirements.txt` installs pywinauto only on Windows
  (`; sys_platform == "win32"`) and `conftest.py` **skips** tests marked `desktop` on
  non-Windows platforms.
* Run CLI/system tests on Ubuntu (cheap, fast) **and** Windows (to catch path/line-ending bugs)
  using a **matrix**.
* Use `shell: bash` in `defaults.run` if you want identical shell syntax on both OSes; otherwise
  Windows steps default to PowerShell (`$env:VAR`) and Linux steps to bash (`$VAR`).

### 3.8 Self-hosted Windows runner for desktop tests

Why not `windows-latest`? GitHub-hosted Windows runners are Windows **Server** virtual machines:
the Store Calculator and the Windows 11 Notepad are not installed, and the runner agent does
not own an interactive logged-in desktop, so UI Automation cannot drive real apps reliably.

Setting up a self-hosted runner (overview):

1. Use a dedicated Windows 10/11 PC or VM with Python and Git installed.
2. GitHub repo -> *Settings -> Actions -> Runners -> New self-hosted runner -> Windows*; follow
   the download/config commands; give it the labels `self-hosted, windows`.
3. Start it **interactively** with `run.cmd` in a logged-in user session - **not** as a Windows
   service (services run in session 0 with no desktop).
4. Disable screen lock, sleep and screensaver; use a fixed resolution and 100% display scaling.
5. Create the repository variable `DESKTOP_RUNNER_AVAILABLE = true`
   (*Settings -> Secrets and variables -> Actions -> Variables*).
6. Security: self-hosted runners execute code from your workflows - use them only with private
   repos or trusted contributors (never with public PRs from forks).

### 3.9 Reading a failed run

1. PR or commit shows a red X -> **Details**.
2. Open the failed job, expand the red step, scroll to pytest's short summary:
   `FAILED tests/test_cli.py::test_tool_is_fast - AssertionError: took 6.2s`.
3. Download the **artifact** (HTML report, logs, screenshots) from the run summary page.
4. Reproduce locally with the **same** command, environment and Python version.
5. Fix, commit, push to the same branch - the checks run again automatically.
6. Is it flaky? Re-run the failed job once ("Re-run failed jobs"), but open a ticket - flaky
   tests must be fixed, not ignored.

### Common mistakes (CI)

* Workflow file not in `.github/workflows/` or wrong extension -> nothing happens.
* Tabs or wrong indentation in YAML.
* Forgetting `actions/checkout` -> "file not found" for everything.
* Upload step without `if: always()` -> no report when tests fail.
* Same artifact name in every matrix job -> upload conflict.
* Expecting Windows desktop tests to run on `ubuntu-latest` or hosted `windows-latest`.
* Cron written in local time instead of UTC.
* Printing secrets or storing them in `config.yaml`.
* Running the self-hosted runner as a service -> UI tests see no windows.

### Try it yourself (CI)

1. Copy `examples/github_actions/01_hello_world.yml` to `.github/workflows/` of a test repo,
   push, and watch it run.
2. Add `workflow_dispatch` with a `choice` input and print the chosen value.
3. Change the course workflow's matrix to add Python 3.14 for Windows only (`include:`).
4. Make a test fail on a branch and inspect the artifact of the failed run.

### Summary (CI)

CI runs your tests automatically on events (push, PR, schedule, manual). A GitHub Actions
workflow is YAML with jobs made of steps on runners. For Python: checkout, setup-python with pip
cache, install requirements, pytest with markers and HTML report, upload artifacts with
`if: always()`. CLI tests run on Linux and Windows via a matrix; Windows desktop tests need a
self-hosted Windows 10/11 runner with an interactive session.

---

## 4. Desktop & CLI automation best practices

### 4.1 Desktop vs CLI vs system automation

| Type | Typical targets | Python tools | Speed / stability | CI |
|---|---|---|---|---|
| Desktop UI | Calculator, Notepad, thick-client ERP, installers' GUIs | pywinauto (UIA backend), pyautogui/OpenCV as last resort | slow, most fragile | Windows desktop session |
| CLI | own tools (`sysinfo_cli.py`), `git`, installers with silent flags | `subprocess`, framework `run_command()` | fast, stable | any OS |
| System | files, logs, services, disk, environment, scheduled jobs | `pathlib`, `shutil`, `os`, `platform`, `zipfile` | fast | any OS (OS-specific parts aside) |

Use the **test pyramid**: many fast CLI/unit/file checks, fewer UI end-to-end tests. Verify
through the fastest reliable interface; use the UI to check what the user actually does.

### 4.2 UI object identification and synchronization

Locator priority:

1. **auto_id** (AutomationId) - set by developers, language-independent:
   `child_window(auto_id="num7Button", control_type="Button")`
2. **name/title + control_type** - readable, but changes with language and text:
   `child_window(title="Seven", control_type="Button")`
3. **control_type + index** - `child_window(control_type="Document")`, `found_index=0`;
   breaks when the layout changes.
4. **Image matching / coordinates** - last resort; breaks with DPI, theme, resolution.

Tools: `window.print_control_identifiers()`, Accessibility Insights for Windows, Inspect.exe.
Keep all locators in **page objects** (`pages/calculator_page.py` has a dictionary of button
auto_ids), so a UI change means one edit.

Synchronization - never guess time:

```python
time.sleep(3)                                     # BAD: flaky and slow

win.wait("visible", timeout=15)                   # pywinauto: visible / exists / ready / enabled
control.wait("exists", timeout=10)

from core.waits import wait_until                 # framework: poll any condition
wait_until(lambda: calculator.display_text().endswith(" 0"),
           timeout=10, message="display to reset to 0")
```

`examples/best_practices/01_sleep_vs_wait_before.py` fails randomly with a fixed sleep;
`01_sleep_vs_wait_after.py` always passes and never waits longer than needed.

### 4.3 Native dialogs and controls

* **Message boxes** ("Do you want to save changes?"): wait for the dialog explicitly, then
  click its button by title/auto_id. Better: **avoid** them - save before closing (our
  `NotepadPage.close_tab()` saves first if the title starts with `*`).
* **Save As / Open / file pickers**: common file dialogs contain a *File name* edit box - type
  the full path, press Enter or click *Save*, and handle "already exists - replace?".
  Verify the auto_ids on your machine with `print_control_identifiers()`.
* **Avoid dialogs when possible**: open files through the command line (`notepad.exe <path>`),
  work on files that already exist so Ctrl+S saves silently, use CLI flags or config files.
* **Unexpected dialogs** (update prompts, crash reporters): always use timeouts so the test
  fails fast with a screenshot instead of hanging.

```python
dlg = app.window(title_re="Save as|Save As")
dlg.wait("visible", timeout=10)
dlg.child_window(auto_id="1001", control_type="Edit").set_edit_text(str(target))
dlg.child_window(title="Save", control_type="Button").invoke()
```

### 4.4 Never assume a clean application state

Windows 11 Notepad **restores the user's previous tabs** at start-up and opens new files as
additional tabs in the same window. A script that connects to "the Notepad window" and types
could type into a colleague's unsaved document; calling `.close()` on the window closes
**all** their tabs.

The safe pattern (implemented in `pages/notepad_page.py`):

1. Create **your own** file (pytest `tmp_path`, unique name).
2. Open exactly that file: `notepad.exe <path>`.
3. Connect by title regex `\*?<filename> - Notepad` (the `*` appears when unsaved).
4. Type into `child_window(control_type="Document")` with
   `type_keys(text, with_spaces=True, pause=0.05)` and verify the editor text.
5. Save with `^s` (no dialog: the file exists) and close **only your tab** with `^w`.
6. **Never** call `.close()` on the Notepad window.
7. Verify the saved content **from disk** - the real oracle.

The same lesson applies to any application that remembers state: last opened files, window
positions, "remember me" logins, user settings. Set up the state you need; do not assume it.

### 4.5 Reliability and failure recovery

**Retries - for transient problems only**

```python
from core.waits import retry, WaitTimeoutError

@retry(times=3, delay=1.0, backoff=2.0, exceptions=(WaitTimeoutError,))
def open_calculator(config):
    return CalculatorPage(config).open()
```

* Retry idempotent steps (safe to repeat): launching, connecting, `calculate()` (it clears first).
* Never retry an assertion to make a real bug disappear. Log each retry and watch the numbers.

**Cleanup that always runs** - fixtures with `yield`, `try/finally`, context managers:

```python
@pytest.fixture
def notepad(config, tmp_path):
    test_file = tmp_path / "automation_note.txt"
    test_file.write_text("", encoding="utf-8")
    page = NotepadPage(config).open_file(test_file)
    yield page                  # the test runs here
    page.close_tab()            # teardown - runs even when the test failed
```

**Kill leftover processes - only your own**: keep the `Popen` object / PID you started and
`terminate()` then `kill()` it. Never `taskkill /IM notepad.exe /F` on a shared machine.
Store apps (Win11 Calculator/Notepad) are launched via a stub, so close them through the UI
(e.g. `close_tab()`) or via the PID of *your* window. See
`examples/best_practices/04_kill_leftover_process.py`.

**Evidence on failure**: the framework's `conftest.py` hook takes a screenshot when a desktop
test fails and embeds it in the pytest-html report; the logger writes a timestamped log file
per run. Upload both as CI artifacts.

**Isolate test data**: every test creates its own files in `tmp_path`, uses unique names, and
never depends on another test's output. Tests must pass in any order and alone.

**Fail fast and clearly**: specific exceptions, meaningful assertion messages
(`assert result == 15, f"{case_id}: got {result}"`), timeouts everywhere.

### 4.6 Cross-platform challenges

| Challenge | Example problem | Solution |
|---|---|---|
| Paths | `"C:\\Users\\ravi\\data.csv"`, `"reports\\" + name` | `pathlib.Path`, relative to `Path(__file__)`; framework `core/paths.py` |
| Line endings | `"a\r\nb" != "a\nb"` | compare `splitlines()`, normalise `\r\n`, `.gitattributes` |
| Shells | `dir` vs `ls`, `%VAR%` vs `$VAR`, quoting | `subprocess.run([...])` with a list, no `shell=True`; `shell: bash` in CI |
| OS tools | `ping -n` vs `ping -c`, `tasklist` vs `ps` | Python APIs (`shutil`, `platform`, `os`) or explicit `if sys.platform` branches |
| Python executable | `python` vs `python3` vs venv | `sys.executable` |
| Encodings | cp1252 default on Windows | always `encoding="utf-8"` |
| DPI / resolution | coordinates and images shift at 125% scaling | locators instead of coordinates; fixed 100% DPI on runners |
| Case sensitivity | `Test_Data.csv` vs `test_data.csv` works on Windows only | use exact names |

Demos: `examples/best_practices/02_hardcoded_paths_before.py` / `_after.py` and
`05_cross_platform_commands.py`.

### Common mistakes (best practices)

* `time.sleep()` everywhere; increasing it every time a test fails.
* Recording coordinates or images when an auto_id exists.
* Grabbing "whatever window is open" and closing the whole application.
* Cleanup code at the end of the test body (never runs after a failure).
* Tests that depend on the previous test's data or state.
* Broad `except Exception: pass` that hides the real failure.
* Hard-coded personal paths and environment URLs.

### Try it yourself (best practices)

1. Run every file in `examples/best_practices/` and read the output.
2. Run `01_sleep_vs_wait_before.py` three times - count the failures.
3. Do Lab 3: refactor `hands_on/lab3_starter/flaky_report_check.py`.

### Summary (best practices)

Automate through the fastest reliable interface. Identify UI elements by auto_id, synchronise
with explicit waits, avoid or explicitly handle dialogs, and never assume the application starts
clean. Make tests reliable with targeted retries, guaranteed cleanup, stopping only your own
processes, isolated data and rich failure evidence. Write code that runs on Windows and Linux:
pathlib, list-based subprocess calls, explicit encodings, normalised line endings.

---

## 5. Mini project overview

The capstone (details in `hands_on/Mini_Project.md`) extends `automation_framework/` with:

* **(A) Desktop end-to-end workflow** - read expressions from test data, compute each one with
  `CalculatorPage.calculate()`, type a report into a Notepad temp file that the test owns, save
  it, and verify the file content from disk.
* **(B) CLI / system task** - `tools/log_archiver_cli.py` collects system information and
  archives log files (`collect`, `archive --keep N`), tested with `pytest -m cli`.
* **(C) Configuration-driven execution** - a `mini_project:` block per environment in
  `config/config.yaml`; `--env dev` and `--env qa` use different data and settings.
* **(D) Quality** - logging, screenshot on failure, HTML report, CI workflow, Git hygiene.

A starter kit (`hands_on/mini_project_starter/`) and a reference solution
(`hands_on/mini_project_solution/`) are provided.

---

## 6. Best-practices checklist

Use this before every Pull Request.

**Repository**
- [ ] `.gitignore` covers reports, logs, screenshots, caches, venv, `.env`
- [ ] No secrets, tokens, personal paths in code or config
- [ ] README explains setup, run commands, markers, environments
- [ ] `requirements.txt` updated for any new package
- [ ] Small, focused commits with meaningful messages; work on a feature branch
- [ ] Release tagged when the framework version changes

**Tests**
- [ ] Locators in page objects, auto_id first
- [ ] No `time.sleep()` for synchronization - explicit waits with timeouts
- [ ] Test creates its own data (tmp_path) and cleans up in a fixture/finally
- [ ] Only closes/kills what it opened/started (own Notepad tab, own process)
- [ ] Independent: passes alone and in any order
- [ ] Correct markers (`smoke`, `regression`, `desktop`, `cli`)
- [ ] Clear assertion messages; verifies the real outcome (file on disk, exit code, stdout)
- [ ] Data and settings come from `test_data/` and `config.yaml`, not hard-coded
- [ ] Runs on Windows and Linux where applicable (pathlib, `sys.executable`, encoding)

**CI**
- [ ] Workflow YAML validated; triggers correct (push/PR/schedule/dispatch)
- [ ] pip cache enabled; job `timeout-minutes` set
- [ ] Reports/logs/screenshots uploaded with `if: always()`
- [ ] CLI tests on a Linux + Windows matrix; desktop tests on a Windows desktop runner
- [ ] Secrets only via `${{ secrets.* }}`
- [ ] `main` protected: PR + green checks required

---

## 7. Common mistakes (all topics)

| Mistake | Consequence | Better |
|---|---|---|
| Committing reports/logs | Huge repo, merge conflicts | `.gitignore` from day one |
| Password in config.yaml | Security incident | GitHub Secrets + env vars; rotate leaked secrets |
| Direct commits to main | Broken main, no review | feature branch + PR + required checks |
| Leaving conflict markers | SyntaxError / YAML error | search for `<<<<<<<` before committing |
| No `if: always()` on artifacts | No report for failed runs | always upload evidence |
| Desktop tests on ubuntu-latest | Cannot run at all | self-hosted Windows runner, skip on Linux |
| Cron in local time | Runs at the wrong hour | cron is UTC |
| `time.sleep(5)` | Flaky and slow | `wait_until`, `.wait()` |
| Typing into "any Notepad" | Damages user data | own temp file, own tab, Ctrl+W |
| Killing by image name | Kills colleagues' apps | stop only your own PID |
| Cleanup at end of test body | Dirty state after failures | fixture teardown / finally |
| `"dir\\file"` strings | Breaks on Linux | `pathlib` |

---

## 8. Questions and answers

**Q1. What is the difference between Git and GitHub?**
Git is a distributed version control tool that runs locally. GitHub is a hosting platform for
Git repositories that adds collaboration features (Pull Requests, reviews, issues) and CI/CD via
GitHub Actions.

**Q2. Explain the working directory, staging area and repository.**
The working directory holds the files you edit. `git add` copies selected changes into the
staging area (index), which defines the next commit. `git commit` stores the staged snapshot
permanently in the local repository (`.git`). `git push` sends commits to a remote.

**Q3. What is the difference between `git fetch` and `git pull`?**
`fetch` downloads new commits from the remote and updates remote-tracking branches
(`origin/main`) without touching your working files. `pull` is `fetch` followed by a merge (or
rebase with `--rebase`) into your current branch, so it can create conflicts.

**Q4. Merge vs rebase - when would you use each?**
Merge combines branches with a merge commit and preserves true history; it is safe for shared
branches. Rebase replays your commits on top of another branch, giving a linear history but
creating new commit hashes; use it only on your own branches that nobody else has pulled.

**Q5. How do you resolve a merge conflict?**
Run `git status` to see conflicted files, open each file, decide the correct content between
the `<<<<<<<`, `=======`, `>>>>>>>` markers, remove the markers, `git add` the file, and
`git commit` to complete the merge. Then run the tests. `git merge --abort` cancels.

**Q6. Which branching strategy would you choose for a test automation repository and why?**
A feature branch workflow with Pull Requests into a protected `main`: each change is isolated,
reviewed and validated by CI, and branches are short-lived. GitFlow is usually too heavy for
test code; trunk-based development is great if the team integrates daily and has strong CI.

**Q7. What should never be committed to an automation repository?**
Secrets (passwords, tokens, keys), generated output (reports, logs, screenshots), virtual
environments, caches (`__pycache__`, `.pytest_cache`) and personal IDE settings. Use
`.gitignore`, environment variables and GitHub Secrets.

**Q8. What is CI/CD?**
Continuous Integration: every change is integrated frequently and automatically built and
tested. Continuous Delivery: every green build is releasable on demand. Continuous Deployment:
every green build is released automatically.

**Q9. Explain workflows, jobs, steps, runners and actions in GitHub Actions.**
A workflow is a YAML file in `.github/workflows/` triggered by events. It contains jobs; each job
runs on a runner (a machine) and consists of ordered steps. A step either runs a shell command
(`run:`) or uses an action (`uses:`), a reusable packaged step such as `actions/checkout`.

**Q10. How do you make sure the test report is available when tests fail in CI?**
Generate it with `pytest --html=reports/report.html --self-contained-html` and upload it with
`actions/upload-artifact` using `if: always()`, so the upload step runs even after the test step
failed. Include logs and screenshots.

**Q11. Can you run pywinauto desktop tests on an Ubuntu runner? On windows-latest?**
Not on Ubuntu - there is no Windows desktop or Windows applications. GitHub-hosted
`windows-latest` is a Windows Server VM without Store Calculator/Windows 11 Notepad and without
an interactive logged-in desktop, so it is not reliable for UI tests. Use a self-hosted Windows
10/11 runner started interactively in an unlocked session. Run CLI tests on Ubuntu.

**Q12. What does "headless" mean for desktop automation?**
Headless means executing without a person watching and often without a physical display. CLI
tests are inherently headless; Linux GUI apps can use a virtual display (Xvfb). Windows UI
Automation still needs a real interactive session - it can be an unattended VM, but it must be
logged in and unlocked.

**Q13. How do you schedule a nightly regression in GitHub Actions?**
Add `on: schedule: - cron: "30 20 * * *"`. Cron uses UTC (this is 02:00 IST). Scheduled runs use
the default branch. Add `workflow_dispatch` to also allow manual runs.

**Q14. What is a matrix build and why is it useful?**
`strategy.matrix` runs the same job for every combination of values, e.g. `os: [ubuntu-latest,
windows-latest]` x `python: ["3.12", "3.13"]` = 4 jobs. It proves the code works on every
supported platform and version with one job definition.

**Q15. Why avoid `time.sleep()` in UI automation, and what do you use instead?**
A fixed sleep is either too short (flaky failures on slow machines) or too long (wasted time).
Use explicit waits that poll a condition with a timeout: pywinauto `wait("visible")`,
`wait("exists")`, or a helper like `wait_until(condition, timeout)`.

**Q16. In what order do you prefer locators for desktop UI elements?**
auto_id first (stable, language-independent), then name/title with control_type, then
control_type with index, and image matching or coordinates only as a last resort.

**Q17. A desktop test fails and all following tests fail too. What is likely wrong and how do you fix it?**
The failing test left the application in a bad state (dialog open, app not closed, file locked)
because cleanup lived at the end of the test body. Move cleanup into fixture teardown or
`finally`, start each test from a known state, and kill only processes the test started.

**Q18. How do you write automation that works on both Windows and Linux?**
Use `pathlib` with paths relative to the project, pass commands to `subprocess` as lists without
`shell=True`, use `sys.executable`, specify `encoding="utf-8"`, normalise line endings when
comparing text, prefer Python APIs over OS commands, and test on both OSes in a CI matrix.

**Q19. When is a retry appropriate in a test framework?**
For transient, environmental problems on idempotent steps - an application slow to start, a busy
resource. Retries must be limited, logged, and must never wrap assertions that detect real bugs.

---

## 9. Day 5 summary

* **Git**: edit -> `add` -> `commit` -> `push`; `fetch`/`pull` to sync; branches + PRs; resolve
  conflicts by editing, `add`, `commit`; keep the repo clean and secret-free; tag releases.
* **GitHub Actions**: workflows (YAML) triggered by events run jobs of steps on runners; use
  setup-python + pip cache + pytest + upload-artifact (`if: always()`); schedule with UTC cron;
  manual runs with `workflow_dispatch`; CLI tests on a Linux/Windows matrix, desktop tests on a
  self-hosted Windows desktop runner.
* **Best practices**: auto_id locators, explicit waits, avoid/handle dialogs, never assume clean
  state, targeted retries, guaranteed cleanup, stop only your own processes, isolated data,
  evidence on failure, cross-platform code.
* **Mini project**: an end-to-end, configuration-driven desktop + CLI suite with logging, HTML
  reports and CI - the portfolio piece of this course.
