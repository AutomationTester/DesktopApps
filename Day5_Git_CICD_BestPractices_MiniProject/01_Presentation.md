---
marp: true
theme: default
paginate: true
style: |
  /* Denser layouts for content-heavy slides: add "_class: compact" or "_class: tight" */
  section.compact { font-size: 24px; padding: 48px 64px 40px; }
  section.compact h1 { margin-top: 0; margin-bottom: 0.3em; }
  section.tight { font-size: 20px; padding: 36px 56px 32px; }
  section.tight h1 { margin-top: 0; margin-bottom: 0.25em; }
  section.tight pre { margin: 0.4em 0; }
---

# Day 5
## Git, CI/CD with GitHub Actions, Best Practices & Mini Project

Python Desktop Application Automation Testing - 5-Day Program

*From "it works on my machine" to "it runs every night, on every commit, for the whole team"*

<!-- Trainer notes: Welcome everyone to the final day. Today we take the framework we built on Day 4 and make it a team asset: version-controlled in Git, executed automatically by GitHub Actions, hardened with best practices, and extended in a capstone mini project. Check that everyone has a GitHub account and Git installed (git --version) before the first lab. -->

---

<!-- _class: compact -->
# Day 5 Agenda (09:00 - 17:00)

| Time | Session |
|---|---|
| 09:00 - 09:15 | Welcome, Day 4 recap |
| 09:15 - 10:05 | **Module 1:** Version control with Git |
| 10:05 - 10:30 | **Lab 1:** Git hands-on (local repo -> GitHub) |
| 10:30 - 10:45 | *Break* |
| 10:45 - 11:25 | **Module 2:** CI/CD using GitHub Actions |
| 11:25 - 11:50 | **Lab 2:** Run the framework in GitHub Actions |
| 11:50 - 12:35 | **Module 3:** Desktop & CLI automation best practices |
| 12:35 - 13:15 | *Lunch* |
| 13:15 - 13:35 | **Lab 3:** Refactor a flaky script |
| 13:35 - 16:35 | **Mini Project** (brief, build, 10-min break, stabilise, demos, review) |
| 16:35 - 17:00 | Course recap, certification & next steps, Q&A |

<!-- Trainer notes: The mini project gets the biggest block (3 hours) - protect it. If Module 1 overruns, shorten Lab 1 by skipping the rebase task; if Module 2 overruns, do Lab 2 Task 5 (schedule) as a demo. -->

---

# Where we are in the course

```
Day 1  Python, OOP, debugging            -> write clean code
Day 2  pywinauto desktop + CLI automation -> drive Calculator, Notepad, CLIs
Day 3  CSV/JSON/YAML, Linux, subprocess   -> data + system automation
Day 4  Framework, logging, PyTest, AI     -> automation_framework/
Day 5  Git + CI/CD + best practices       -> team-ready, automated, reliable
```

Today's outcome: **your framework in your own GitHub repo, tested automatically by CI, extended with an end-to-end project.**

<!-- Trainer notes: Quickly ask 2-3 recap questions about Day 4: What does conftest.py do? What is a marker? How do we choose the environment (--env)? This warms up the room and connects to today's CI commands. -->

---

# Quick recap: our framework

```
automation_framework/
  pytest.ini            markers: smoke, regression, desktop, cli
  config/config.yaml    environments: dev, qa  ->  pytest --env qa
  core/                 config_reader, logger, waits (wait_until, @retry),
                        base_window (BaseWindow), cli_runner (run_command)
  pages/                CalculatorPage, NotepadPage
  tools/sysinfo_cli.py  CLI "application under test"
  test_data/            csv / json / yaml
  tests/                conftest.py + test_calculator / test_notepad / test_cli
```

<!-- Trainer notes: Open the folder in VS Code and show it live. Point out that there is also requirements.txt at the repo root and .github/workflows/automation-ci.yml - we will explain both today. -->

---

<!-- _class: lead -->
# Module 1
## Version Control with Git

<!-- Trainer notes: Ask: "Who has ever had a file named final_v2_REALLY_final.py?" Git solves exactly that, plus team collaboration. -->

---

# Why version control for test automation?

- **History**: who changed which locator, when and why
- **Undo**: go back to the last working version in seconds
- **Collaboration**: many testers work on one framework in parallel
- **Review**: changes are checked before they reach `main`
- **Automation trigger**: every push can start the CI pipeline
- Test code **is** code - treat it like production code

<!-- Trainer notes: Emphasise the last bullet. Automation repos rot quickly when they are shared via email or network drives. Git is also the entry ticket for CI/CD - no Git, no GitHub Actions. -->

---

# Git vs GitHub

| Git | GitHub |
|---|---|
| Version control **tool** | **Hosting service** for Git repositories |
| Runs locally on your PC | Website + cloud |
| `git commit`, `git branch` ... | Pull Requests, code review, Issues |
| Works offline | GitHub **Actions** = CI/CD |

Alternatives to GitHub: GitLab, Bitbucket, Azure DevOps - Git commands are identical.

<!-- Trainer notes: Many freshers mix these up. Git is the engine, GitHub is one of the garages. Everything in Module 1 works without internet except push/pull/fetch/clone from GitHub. -->

---

# The three areas of Git

```
  Working Directory        Staging Area          Local Repository        Remote (GitHub)
  (your files)             (index)               (.git folder)           (origin)
 +----------------+      +--------------+      +------------------+     +---------------+
 | edit files     | ---> | next commit  | ---> | commit history   | --> | shared history|
 |                | add  |              |commit|                  |push |               |
 |                | <--------------------------|                  | <-- |               |
 +----------------+  switch / restore          +------------------+ fetch/pull ---------+
```

- **Working directory** - files you edit
- **Staging area** - what goes into the *next* commit (`git add`)
- **Repository** - permanent snapshots (`git commit`)
- **Remote** - the team copy (`git push` / `git pull`)

<!-- Trainer notes: Draw this on the whiteboard and keep it visible all morning. The staging area is the concept most beginners find odd: explain it as a "shopping basket" - you choose exactly which changes go into this commit. -->

---

# One-time setup: git config

```bash
git --version
git config --global user.name  "Asha Tester"
git config --global user.email "asha@company.com"
git config --global init.defaultBranch main
git config --global core.autocrlf true      # Windows: CRLF on disk, LF in repo
git config --list                           # check
```

- `--global` = for your user; `--local` = only this repo
- Name/email are stamped on every commit

<!-- Trainer notes: On company laptops use the company email so commits link to the company GitHub account. core.autocrlf true on Windows avoids line-ending noise; on Linux/macOS use input. We will revisit line endings in the cross-platform section. -->

---

# Start a repository: init, status

```bash
mkdir my-automation-repo && cd my-automation-repo
git init                 # creates the hidden .git folder
git status               # what changed? what is staged?
```

```
On branch main
No commits yet
Untracked files:
  README.md
```

`git status` is your best friend - run it before and after every command.

<!-- Trainer notes: Show the hidden .git folder (ls -la in Git Bash). Deleting .git deletes the whole history - never do that by accident. -->

---

# add, commit

```bash
git add README.md           # stage one file
git add tests/              # stage a folder
git add .                   # stage everything (respects .gitignore)
git commit -m "feat: add calculator smoke test"
```

- A **commit** = snapshot + message + author + timestamp + parent
- Identified by a hash, e.g. `3a53131`
- Commit small, logical units: *one reason per commit*

<!-- Trainer notes: Show git status after each step: ?? (untracked) -> A (staged) -> clean. Warn about "git add ." - it's fine only if .gitignore is correct, otherwise reports and venv get committed. -->

---

# log and diff

```bash
git log --oneline --graph --decorate --all   # history as a tree
git log -p tests/test_cli.py                 # changes to one file
git diff                     # working dir vs staging  (not yet added)
git diff --staged            # staging vs last commit (about to commit)
git show HEAD                # the last commit in detail
```

```
- EXPECTED = 16
+ EXPECTED = 15
```

<!-- Trainer notes: Suggest an alias: git config --global alias.lg "log --oneline --graph --decorate --all". Explain that diff is how reviewers read your changes in a Pull Request, so learn to read + and - lines. -->

---

# Undo safely

| Situation | Command |
|---|---|
| Discard edits in a file | `git restore file.py` |
| Unstage a file | `git restore --staged file.py` |
| Fix the last commit message (not pushed) | `git commit --amend` |
| Undo a pushed commit (safe, new commit) | `git revert <hash>` |
| Throw away local commits (dangerous) | `git reset --hard <hash>` |

Rule: **never rewrite history that others already pulled** - use `revert`.

<!-- Trainer notes: reset --hard deletes uncommitted work permanently. Teach revert as the safe team option. -->

---

# Working with remotes: clone, remote, push

```bash
git clone https://github.com/acme/automation_framework.git
cd automation_framework
git remote -v                        # origin = where it came from

# existing local repo -> new empty GitHub repo
git remote add origin https://github.com/<you>/my-automation-repo.git
git push -u origin main              # first push, sets upstream
git push                             # later pushes
```

GitHub over HTTPS needs a **Personal Access Token** or Git Credential Manager login - not your password.

<!-- Trainer notes: Git for Windows ships Git Credential Manager: the first push opens a browser login. If a trainee's company blocks it, create a fine-grained PAT with Contents: read/write. -->

---

# fetch vs pull

```bash
git fetch origin           # download new commits, do NOT change my files
git status -sb             # ## main...origin/main [behind 2]
git log main..origin/main  # what is new?
git pull                   # = fetch + merge   (or --rebase)
```

```
 Remote   A---B---C---D        fetch: updates origin/main only
 Local    A---B                pull : moves main to D as well
```

Habit: **pull before you start work, push when you finish**.

<!-- Trainer notes: fetch is the "look before you leap" command. Pull can create conflicts, fetch never does. -->

---

# Everyday Git workflow

```
   git pull            (get team changes)
       |
   git switch -c feature/notepad-save-test
       |
   edit -> git status -> git diff -> git add -> git commit   (repeat)
       |
   pytest -m smoke     (run tests locally BEFORE pushing)
       |
   git push -u origin feature/notepad-save-test
       |
   open Pull Request -> CI runs -> review -> merge to main
```

<!-- Trainer notes: This is the loop they will use every day in a real team. Stress "run tests before pushing" - CI is a safety net, not a replacement for local runs. -->

---

# Branching basics

```bash
git branch                        # list branches
git switch -c feature/login-test  # create + switch  (old: checkout -b)
git switch main                   # go back
git merge feature/login-test      # bring changes into main
git branch -d feature/login-test  # delete merged branch
```

- A branch is just a **movable pointer** to a commit - cheap to create
- `main` should always be **green** (tests pass)

<!-- Trainer notes: Show that creating a branch is instant - nothing is copied. HEAD points to the current branch. -->

---

# Branching strategies

**Feature branch workflow** (most teams, recommended for automation repos)
- one branch per task: `feature/`, `fix/`, `test/`, `chore/`
- merged to `main` via Pull Request

**GitFlow** - `main` (releases), `develop`, `feature/*`, `release/*`, `hotfix/*`
- good for versioned products with scheduled releases; heavier process

**Trunk-based development** - everyone commits to `main` (or very short-lived branches, < 1 day)
- needs strong CI and feature flags; fastest feedback

<!-- Trainer notes: For a test automation repo, feature branches + PRs is the sweet spot. GitFlow is often overkill for test code; trunk-based requires excellent automated tests - which is ironically what we are building. -->

---

# GitFlow vs trunk-based (diagram)

```
GitFlow
main     o---------------------o-----------o   (v1.0)      (v1.1)
          \                   /           /
develop    o---o-------o-----o-----o-----o
                \     /       \       /
feature/x        o---o         o-----o feature/y

Trunk-based
main     o--o--o--o--o--o--o--o--o      (tiny branches merged same day)
             \/    \/    \/
```

<!-- Trainer notes: Ask the room which one their project uses. Often the answer is "some mix". The important principle: short-lived branches cause fewer conflicts. -->

---

# Pull Requests & code review

1. Push your branch -> GitHub shows **"Compare & pull request"**
2. Describe: *what, why, how tested* (link the test case / ticket)
3. **CI checks run automatically** on the PR
4. Reviewer comments, you push fixes to the same branch
5. Approve -> **merge** -> delete branch

Review checklist for automation code: stable locators? explicit waits? cleanup? no secrets? tests independent? readable names?

<!-- Trainer notes: Protect main in GitHub settings: Settings -> Branches -> require PR + passing status checks. This turns CI from "nice to have" into a gate. -->

---

# Merge vs rebase

```
Before:        main  A---B---C
                          \
               feature     D---E

merge:         A---B---C-------M       keeps real history, extra merge commit
                        \     /
                         D---E

rebase:        A---B---C---D'--E'      linear history, commits get NEW hashes
```

- `git merge feature` - safe, default
- `git rebase main` (while on feature) - tidy, **only for your own, unpushed / unshared branches**

<!-- Trainer notes: The golden rule of rebase: never rebase commits that others have based work on. For beginners: merge by default, rebase your local feature branch onto main to update it if the team prefers linear history. -->

---

# Merge conflicts: why they happen

Two branches changed **the same lines** of the same file:

```
<<<<<<< HEAD
    timeout: 15
=======
    timeout: 30
>>>>>>> feature/timeout-qa
```

- `HEAD` = your current branch, below `=======` = the incoming branch
- Git cannot guess - **a human decides**

<!-- Trainer notes: Conflicts are normal, not errors. They are more frequent in shared files like config.yaml, conftest.py and test data. Small, frequent merges keep them small. -->

---

# Resolving a merge conflict

```bash
git merge feature/timeout-qa        # CONFLICT (content) in config.yaml
git status                          # both modified: config.yaml
# 1. open file (VS Code: Accept Current / Incoming / Both / Compare)
# 2. keep the right content, DELETE all <<<<<<< ======= >>>>>>> lines
git add config.yaml                 # mark as resolved
git commit                          # completes the merge
pytest -m smoke                     # verify nothing broke!
```

Panic button: `git merge --abort` (back to before the merge)

<!-- Trainer notes: Live demo with examples/git_practice.sh - it creates a real conflict in examples/sandbox_repo and resolves it. Then open the sandbox in VS Code to show the merge editor. -->

---

# Demo: examples/git_practice.sh

```bash
cd Day5_Git_CICD_BestPractices_MiniProject/examples
bash git_practice.sh           # init, commits, branch, conflict, resolve, tag
bash git_practice.sh --clean   # remove the sandbox
```

```
*   12e927b (HEAD -> main, tag: v1.0.0) merge: support formal and casual greetings
|\
| * cbbfe2d feat: formal greeting
* | cedf34e feat: casual greeting
|/
* 5ccbc94 feat: add farewell() helper
```

<!-- Trainer notes: The script only touches examples/sandbox_repo and uses local git config, so it is safe on any laptop. Run it, then scroll through the output step by step. -->

---

# Best practices for automation repositories (1/3)

**.gitignore** - commit source, never output

```gitignore
reports/
logs/
screenshots/
__pycache__/
.pytest_cache/
.venv/
.env
```

- Generated files bloat the repo and cause pointless conflicts
- See `examples/sample.gitignore`

<!-- Trainer notes: Show git status --ignored. The course repo's root .gitignore already ignores automation_framework/logs, reports and screenshots. -->

---

# Best practices for automation repositories (2/3)

**Never commit secrets**
- Passwords, tokens, API keys -> environment variables / GitHub **Secrets**
- Commit a `.env.example` with fake values, ignore `.env`
- Leaked a secret? **Rotate it immediately** - deleting the commit is not enough (history, forks, clones)

**Commit messages**
```
feat(calculator): add division by zero test
fix(notepad): wait for title without '*' after save
chore: bump pytest-html to 4.1
```
Imperative, short subject (< 72 chars), *why* in the body.

<!-- Trainer notes: The type(scope): subject style is "Conventional Commits". Bad examples: "update", "fix", "asdf". A good message saves the reviewer 5 minutes. GitHub also runs secret scanning / push protection on many repos. -->

---

# Best practices for automation repositories (3/3)

- **README.md** - purpose, setup, how to run, markers, environments
- **requirements.txt** - pinned/minimum versions -> `pip install -r requirements.txt`
- **Clear folder structure** - config / core / pages / tests / test_data / tools
- **Tag releases** of the framework:

```bash
git tag -a v1.2.0 -m "Adds Notepad regression suite"
git push origin v1.2.0        # tags are not pushed by default
```

- Small PRs, green `main`, delete merged branches

<!-- Trainer notes: Tags let you say "production release 5.3 was verified with automation v1.2.0" - very useful for audits and reproducing old results. -->

---

# Git cheat sheet (keep this slide)

| Goal | Command |
|---|---|
| Start / copy | `git init` / `git clone <url>` |
| What changed | `git status` / `git diff` / `git diff --staged` |
| Save | `git add <f>` -> `git commit -m "msg"` |
| History | `git log --oneline --graph` |
| Branch | `git switch -c feature/x` / `git switch main` |
| Combine | `git merge feature/x` / `git rebase main` |
| Sync | `git fetch` / `git pull` / `git push` |
| Release | `git tag -a v1.0.0 -m "..."` |

<!-- Trainer notes: The full cheat sheet is in the reading material. Transition: now let's do it ourselves - Lab 1. -->

---

# Lab 1 - Git hands-on (25 min)

`hands_on/Lab_Guide.md` -> **Lab 1**

1. `git init`, config, README, .gitignore, requirements.txt
2. First commits, `git diff`, `git log`
3. Feature branch + merge
4. Create **and resolve** a merge conflict
5. (Optional) rebase a short branch, tag `v1.0.0`
6. Push to **your own** GitHub repository

<!-- Trainer notes: Walk around and check that everyone completes the conflict task - that is the skill they will need most. Solution: hands_on/solutions/lab1_git_solution.sh. -->

---

<!-- _class: lead -->
# Module 2
## CI/CD using GitHub Actions

<!-- Trainer notes: Transition: our code is on GitHub. Now let's make GitHub run our tests for us - on every change and every night. -->

---

# CI/CD fundamentals

- **Continuous Integration (CI)**: every change is merged often and **automatically built and tested**
- **Continuous Delivery**: every green build *can* be released (button)
- **Continuous Deployment**: every green build *is* released automatically

Why testers care:
- Tests run on **every push / PR** -> bugs found in minutes, not weeks
- Same clean environment every time -> no "works on my machine"
- **Nightly regression** without anyone staying late
- Reports and evidence stored automatically

<!-- Trainer notes: As automation engineers you own the "T" in CI. A CI pipeline without good tests just builds broken software faster. -->

---

# The CI pipeline for our framework

```
 developer                GitHub                          runners
+----------+  git push  +---------+  event   +---------------------------------+
| laptop   | ---------> | repo    | -------> | workflow: Automation CI         |
+----------+  / PR      +---------+          |                                 |
                  cron (nightly) --------->  |  job cli-tests (matrix x4)      |
                  manual (dispatch) ------>  |   ubuntu/windows x py3.12/3.13  |
                                             |   checkout -> python -> pip ->  |
                                             |   pytest -m cli -> artifact     |
                                             |            | needs              |
                                             |  job desktop-tests              |
                                             |   self-hosted Windows 10/11     |
                                             |   pytest -m desktop -> artifact |
                                             +---------------------------------+
                                                   |  red/green status on commit/PR
                                                   v  + downloadable HTML reports
```

<!-- Trainer notes: This is the exact shape of .github/workflows/automation-ci.yml in the course repo. Keep the diagram up while explaining the building blocks on the next slides. -->

---

# GitHub Actions vocabulary

| Term | Meaning |
|---|---|
| **Workflow** | YAML file in `.github/workflows/` - the whole pipeline |
| **Event** | What triggers it: `push`, `pull_request`, `schedule`, `workflow_dispatch` |
| **Job** | Group of steps on **one runner**; jobs run in parallel unless `needs:` |
| **Step** | A shell command (`run:`) or an action (`uses:`) |
| **Runner** | Machine that executes a job: GitHub-hosted or self-hosted |
| **Action** | Reusable step, e.g. `actions/checkout@v4` |
| **Secret** | Encrypted value, `${{ secrets.NAME }}`, masked in logs |
| **Artifact** | Files kept after the run (reports, logs, screenshots) |

<!-- Trainer notes: Everything in GitHub Actions is one of these eight things. Make sure trainees can explain "job vs step": different jobs = different machines, steps in a job share the same file system. -->

---

# Workflow YAML structure

```yaml
name: Automation CI                 # shown in the Actions tab
on:                                 # EVENTS
  push:
    branches: [main]
  pull_request:
jobs:                               # JOBS
  cli-tests:                        # job id
    runs-on: ubuntu-latest          # RUNNER
    steps:                          # STEPS (in order)
      - uses: actions/checkout@v4   # ACTION
      - run: pytest -m cli          # SHELL COMMAND
```

YAML: indentation with **spaces** (never tabs), `key: value`, lists with `-`.

<!-- Trainer notes: 90% of beginner CI failures are YAML indentation mistakes. VS Code with the "GitHub Actions" extension validates workflow files. Fun fact: PyYAML reads the key on as the boolean True - GitHub uses its own parser, so it works. -->

---

# Hello world workflow

```yaml
name: 01 Hello World
on: [push, workflow_dispatch]
jobs:
  say-hello:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello from GitHub Actions!"
      - run: echo "Branch ${{ github.ref_name }} by ${{ github.actor }}"
      - uses: actions/checkout@v4
      - run: ls -la
```

`examples/github_actions/01_hello_world.yml`

<!-- Trainer notes: ${{ }} is an expression. github.* is the context with information about the event. Without actions/checkout the runner is empty - your repository is NOT there automatically. -->

---

# Running Python automation in CI

```yaml
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip                           # reuse downloaded packages
      - run: pip install -r ../requirements.txt
      - run: pytest -m cli --env qa --html=reports/report.html --self-contained-html
      - uses: actions/upload-artifact@v4
        if: always()                           # also when tests fail!
        with:
          name: cli-report
          path: automation_framework/reports/
```

<!-- Trainer notes: pytest returns a non-zero exit code when a test fails -> the step fails -> the job is red. --self-contained-html embeds CSS so the single file opens anywhere. if: always() is the most forgotten line in CI. -->

---

# Our workflow: triggers

```yaml
on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: "30 20 * * *"     # 20:30 UTC = 02:00 IST, nightly regression
  workflow_dispatch:          # "Run workflow" button
    inputs:
      env:
        type: choice
        options: [dev, qa]
        default: qa
```

Used later as `--env ${{ inputs.env || 'qa' }}` (scheduled/push runs have no input -> `qa`).

<!-- Trainer notes: Open .github/workflows/automation-ci.yml side by side. The || operator gives a default when the input is empty. -->

---

# Our workflow: CLI job with a matrix

```yaml
  cli-tests:
    name: CLI tests (${{ matrix.os }}, py${{ matrix.python }})
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest]
        python: ["3.12", "3.13"]
    defaults:
      run:
        working-directory: automation_framework
```

2 OS x 2 Python = **4 parallel jobs** from one definition.

<!-- Trainer notes: fail-fast: false lets all combinations finish so you see whether a failure is OS-specific. Artifact names must be unique per combination, hence cli-report-${{ matrix.os }}-py${{ matrix.python }}. -->

---

# Our workflow: desktop job

```yaml
  desktop-tests:
    if: vars.DESKTOP_RUNNER_AVAILABLE == 'true'
    runs-on: [self-hosted, windows]
    needs: cli-tests
    steps:
      - uses: actions/checkout@v4
      - run: python -m pip install -r ../requirements.txt
      - run: python -m pytest -m desktop --env ${{ inputs.env || 'qa' }} --html=...
      - uses: actions/upload-artifact@v4
        if: always()     # reports/ logs/ screenshots/
```

Why self-hosted and not `windows-latest`? -> next slides.

<!-- Trainer notes: vars.* are repository variables (Settings -> Secrets and variables -> Actions -> Variables). Until someone registers a self-hosted runner and sets the variable, the job shows as skipped - the pipeline stays green. -->

---

# Secrets and variables

```yaml
    env:
      QA_API_TOKEN: ${{ secrets.QA_API_TOKEN }}   # encrypted, masked as ***
      TEST_ENV:     ${{ vars.TEST_ENV || 'qa' }}   # plain config value
```

```python
token = os.environ.get("QA_API_TOKEN")   # read in Python, never hard-code
```

- Create: *Settings -> Secrets and variables -> Actions*
- Not passed to workflows from **forks**
- Never `echo` a secret; never write it into reports/logs

<!-- Trainer notes: Sample: examples/github_actions/05_artifacts_and_secrets.yml. Mention "permissions: contents: read" for least privilege of the automatic GITHUB_TOKEN. -->

---

# Artifacts: reports, logs, screenshots

```yaml
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: desktop-report
          path: |
            automation_framework/reports/
            automation_framework/logs/
            automation_framework/screenshots/
          retention-days: 14
          if-no-files-found: ignore
```

Download: run page -> **Artifacts** section -> zip.

<!-- Trainer notes: Artifacts are the evidence for failed nightly runs - the tester's first stop in the morning. Use failure() instead of always() to upload screenshots only when something failed. -->

---

<!-- _class: compact -->
# Headless & scheduled execution

**Scheduled**: `schedule: - cron: "30 20 * * *"`
```
 +------- minute (0-59)
 | +----- hour (0-23, UTC!)
 | | +--- day of month   +-- month   +-- day of week (0=Sun)
 30 20  *  *  *
```
- Runs from the **default branch**, may be delayed at busy times

**Manual**: `workflow_dispatch` (+ inputs)

**Headless** = no person watching, often no physical screen
- CLI tests: naturally headless
- Linux GUI apps: virtual display **Xvfb**
- Windows desktop apps: still need a **real interactive desktop session**

<!-- Trainer notes: A big misconception: "headless" desktop automation on Windows does not exist the way it does for browsers. UIA needs a real, unlocked desktop. Also: GitHub disables schedules in repos without activity for 60 days. -->

---

# Linux runner considerations

- `ubuntu-latest` has **no Windows desktop apps** - no Calculator, no Notepad, no pywinauto
- Run **CLI / API / data tests on Linux** - fast and cheap
- Our `conftest.py` **skips** desktop tests on non-Windows automatically
- Linux GUI apps (Tk, Qt, GTK): `xvfb-run -a pytest ...`
- Path, shell and line-ending differences (Module 3)

```yaml
      - run: sudo apt-get install -y xvfb
      - run: xvfb-run -a pytest -m linux_gui
```

<!-- Trainer notes: The pytest_collection_modifyitems hook in conftest.py adds a skip marker to desktop tests when sys.platform is not win32. So even "pytest" without -m works on Linux. -->

---

# Windows desktop tests in CI

| Option | Works for Win11 Calculator/Notepad? |
|---|---|
| `ubuntu-latest` | No - no Windows at all |
| `windows-latest` (GitHub-hosted) | **Not reliably** - Windows *Server* VM, no Store Calculator / new Notepad, no interactive logged-in desktop |
| **Self-hosted Windows 10/11 runner** | **Yes** - real desktop, user logged in, screen unlocked, runner started via `run.cmd` (not as a service) |

- Disable screen lock / sleep on the runner machine; fixed resolution & 100% DPI
- Label it: `runs-on: [self-hosted, windows]`

<!-- Trainer notes: A Windows service runs in session 0, which has no desktop - UI Automation sees nothing. That is why the runner must be started interactively. Many companies use a dedicated VM with auto-logon for this. -->

---

# Matrix builds

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, windows-latest]
    python: ["3.12", "3.13"]
    include:
      - os: windows-latest
        python: "3.14"      # add one extra combination
    exclude:
      - os: ubuntu-latest
        python: "3.12"      # remove one
```

Use it to prove the **CLI tool** and framework work on every OS / Python you support.

<!-- Trainer notes: examples/github_actions/03_matrix_os_python.yml. Each combination costs runner minutes, so keep the matrix meaningful. -->

---

# Reading a CI failure

1. PR shows red X -> **Details**
2. Open the failing job -> expand the red step
3. Read pytest's summary: `FAILED tests/test_cli.py::test_x - AssertionError: ...`
4. Download the **artifact**: HTML report, log file, screenshot
5. Reproduce locally with the **same command** (`pytest -m cli --env qa`)
6. Fix -> push to the same branch -> CI re-runs

<!-- Trainer notes: Show a real failing run if you have one prepared (Lab 2 Task 6 creates one). Stress step 5: always reproduce locally with the exact same command and environment. -->

---

# Lab 2 - GitHub Actions (25 min)

`hands_on/Lab_Guide.md` -> **Lab 2**

1. Push the course `automation_framework` (+ `requirements.txt`, `.github/`) to your repo
2. Watch **Automation CI** run in the Actions tab
3. Download the HTML report artifact
4. Trigger it manually with `env = dev`
5. Add a scheduled smoke workflow
6. Break a test on a branch, open a PR, see CI fail - then fix it

<!-- Trainer notes: GitHub-hosted runner minutes are free for public repos; private repos get a monthly free quota. If the network is slow, pair trainees up. -->

---

<!-- _class: lead -->
# Module 3
## Desktop & CLI Automation Best Practices

<!-- Trainer notes: This module turns the lessons from Days 2-4 into rules. Every rule here comes from a real failure we saw or will see. -->

---

# Desktop vs CLI vs system automation

| Type | Examples | Tools | CI-friendly? |
|---|---|---|---|
| **Desktop UI** | Calculator, Notepad, ERP client | pywinauto (UIA), image matching | Needs Windows desktop |
| **CLI** | `sysinfo_cli.py`, installers with flags, `git` | subprocess, `run_command` | Any OS, headless |
| **System** | services, files, logs, disk, registry, cron | os, shutil, pathlib, psutil | Mostly headless |

**Test pyramid**: many fast CLI/API/unit checks, fewer slow UI end-to-end tests.

<!-- Trainer notes: If something can be verified through a CLI, an API, or a file, do that instead of through the UI - faster and more stable. Use the UI for what users actually do. -->

---

# UI object identification - priority

```
 1. auto_id         child_window(auto_id="num7Button")          most stable
 2. name / title    child_window(title="Seven", control_type="Button")
 3. control_type    child_window(control_type="Document")        (+ found_index)
    + index
 4. image matching  pyautogui / OpenCV                           last resort
    / coordinates
```

- Find them with `print_control_identifiers()` or Accessibility Insights
- Keep locators **in one place** (page objects: `CalculatorPage`)
- Names change with language/theme; auto_ids usually don't

<!-- Trainer notes: Titles are localised - "Seven" becomes "Sieben" on a German machine. Index-based locators break when a button is added. Images break with DPI, theme and resolution. -->

---

# Synchronization: explicit waits, not sleep

```python
# BAD - too short on slow machines, wastes time on fast ones
time.sleep(3)

# GOOD - pywinauto built-in wait
win.wait("visible", timeout=15)

# GOOD - framework helper: poll a condition
wait_until(lambda: not notepad.is_modified(), timeout=10,
           message="Notepad to finish saving")
```

Demo: `examples/best_practices/01_sleep_vs_wait_before.py` vs `_after.py`

<!-- Trainer notes: Run the before file: it fails randomly about half the time. Run the after file: always passes, and faster. This single demo convinces people better than any slide. -->

---

# Handling native dialogs & controls

- **Message boxes** ("Do you want to save?"): wait for them explicitly, click by auto_id/title, or **avoid** them (save before close)
- **Save As / Open / file pickers**: type the full path into the *File name* edit, press Enter; handle "already exists - replace?"
- Prefer **avoiding** dialogs: open files by command line (`notepad.exe <path>`), use existing files so Ctrl+S never shows Save As
- Always add a **timeout** - an unexpected dialog must fail fast, not hang forever

```python
dlg = app.window(title_re="Save as|Save As")
dlg.wait("visible", timeout=10)
dlg.child_window(auto_id="1001", control_type="Edit").set_edit_text(str(path))
dlg.child_window(title="Save", control_type="Button").invoke()
```

<!-- Trainer notes: auto_id 1001 is the classic File name edit on common file dialogs - verify with print_control_identifiers on your machine. Our NotepadPage avoids Save As entirely by opening an existing temp file. -->

---

# Never assume a clean app state

Windows 11 Notepad **restores the user's previous tabs** and opens new files as tabs in the same window.

A script that grabs "the Notepad window" and types may **overwrite a colleague's unsaved document**.

Safe pattern (our `NotepadPage`):
1. Create **your own** temp file (pytest `tmp_path`)
2. `notepad.exe <path>` -> connect by title `\*?<filename> - Notepad`
3. Type into `child_window(control_type="Document")` with `pause=0.05`
4. Save with `^s`, close **only your tab** with `^w`
5. **Never** `.close()` the Notepad window; verify the file **on disk**

<!-- Trainer notes: This is a real lesson from building this course - the first naive script typed into the trainer's own open notes. The same applies to any app that remembers state: browsers, IDEs, Excel. -->

---

# Reliability: retries

```python
from core.waits import retry

@retry(times=3, delay=1.0, backoff=2.0, exceptions=(WaitTimeoutError,))
def open_calculator(config):
    return CalculatorPage(config).open()
```

- Retry **transient** problems (app slow to start, busy resource)
- Only retry **idempotent** steps (safe to repeat)
- Do **not** retry assertions to hide real bugs
- Log every retry - frequent retries are a smell to investigate

<!-- Trainer notes: Retries are a seatbelt, not a steering wheel. If a test needs 3 retries every run, fix the synchronization instead. -->

---

# Reliability: cleanup & failure evidence

```python
@pytest.fixture
def notepad(config, tmp_path):
    test_file = tmp_path / "automation_note.txt"
    test_file.write_text("", encoding="utf-8")
    page = NotepadPage(config).open_file(test_file)
    yield page               # test runs here
    page.close_tab()         # ALWAYS runs - even if the test failed
```

- Cleanup in **fixtures / finally**, never at the end of the test body
- Kill **only processes you started** (keep the Popen / PID)
- On failure: **screenshot + log + HTML report** (our conftest hook)
- **Isolate test data**: temp folders, unique names, no shared files

<!-- Trainer notes: Demos: 03_cleanup_finally.py and 04_kill_leftover_process.py. Never taskkill /IM notepad.exe on a shared machine - it kills everyone's Notepad. -->

---

# Cross-platform automation challenges

| Challenge | Solution |
|---|---|
| Paths `C:\x\y` vs `/x/y` | `pathlib.Path`, paths relative to `__file__` |
| Line endings CRLF vs LF | compare with `splitlines()`, `.gitattributes` |
| Shell differences (cmd / PowerShell / bash) | `subprocess.run([...])` list, no `shell=True`; `shell: bash` in CI |
| OS-specific tools (`dir`/`ls`, `ping -n`/`-c`) | Python APIs (`shutil`, `platform`) or explicit branches |
| DPI scaling / resolution | locators not coordinates; fixed 100% DPI on runners |
| Encodings | always `encoding="utf-8"` |

Demos: `02_hardcoded_paths_*.py`, `05_cross_platform_commands.py`

<!-- Trainer notes: The CLI job runs on ubuntu and windows precisely to catch these. A classic: a test that compares output with '\n' passes on Linux and fails on Windows. -->

---

# Anti-patterns -> fixes (summary)

| Anti-pattern | Fix |
|---|---|
| `time.sleep(5)` | `wait_until` / `.wait("visible")` |
| Coordinates / image clicks | auto_id locators in page objects |
| Hard-coded paths & data | config.yaml + test_data + pathlib |
| Tests depend on each other | independent tests, own fixtures |
| Bare `except: pass` | specific exceptions, fail loudly |
| `taskkill /IM app.exe` | stop only what you started |
| `print` debugging | logging + screenshots + HTML report |

<!-- Trainer notes: Ask trainees to spot which of these they have written this week. Everyone has written at least one sleep! -->

---

# Lab 3 - Refactor a flaky script (20 min)

`hands_on/lab3_starter/flaky_report_check.py`

- Run it 5 times - random PASS/FAIL, sometimes a hung process
- Find **at least 8** problems
- Refactor: pathlib, temp dir, list command, timeout, kill own child, retry busy errors, logging, exit code
- Prove it with pytest (deterministic modes: `ok`, `busy`, `hang`)

<!-- Trainer notes: Solution: hands_on/solutions/lab3_refactored_report_check.py + test_lab3_refactored.py. Discuss the problem table in Lab_Solutions.md at the end. -->

---

<!-- _class: lead -->
# Mini Project
## End-to-end desktop + CLI automation, configuration-driven, in CI

<!-- Trainer notes: Hand out hands_on/Mini_Project.md. Form teams of 3-4. The starter kit is in hands_on/mini_project_starter. -->

---

# Mini project - what you build

```
 (A) Desktop E2E
     test_data/expressions*.csv --> CalculatorPage.calculate()
                                --> ReportNotepadPage on OWN temp file
                                --> save --> verify file ON DISK
 (B) CLI / system task
     tools/log_archiver_cli.py  collect | archive --keep N
     tested with pytest -m cli (Linux + Windows)
 (C) config.yaml mini_project block  --> pytest --env dev | qa
 (D) logging, screenshot on failure, HTML report, CI workflow
```

<!-- Trainer notes: Part B and the unit tests can be verified on any OS and in hosted CI. Part A needs each team's Windows 11 laptop. -->

---

# Mini project - timeline (3 hours)

| Time | Activity |
|---|---|
| 13:35 - 13:45 | Brief, teams, branches (`feature/mini-project`) |
| 13:45 - 14:55 | Build: helpers + CLI tool + tests (green on `-m cli`) |
| 14:55 - 15:05 | *Break* |
| 15:05 - 16:05 | Desktop E2E, config per env, CI workflow, stabilise |
| 16:05 - 16:35 | Team demos (5 min each) + review & optimization discussion |

<!-- Trainer notes: At 14:55 every team should have pytest -m cli green. If not, give them the relevant solution file so they can still do the E2E part - the goal is learning, not suffering. -->

---

# Mini project - evaluation (100 marks)

| Area | Marks |
|---|---|
| Desktop end-to-end workflow works & verifies on disk | 25 |
| CLI tool + CLI tests (exit codes, isolation) | 20 |
| Configuration-driven (`--env dev/qa` changes behaviour) | 10 |
| Reliability: waits, retry, cleanup, no leftovers | 15 |
| Logging, screenshots, HTML report | 10 |
| CI workflow green, artifacts uploaded | 10 |
| Git hygiene: branches, commits, README, .gitignore | 10 |

<!-- Trainer notes: The detailed rubric with criteria per level is in Mini_Project.md. Share it upfront so teams know what "done" means. -->

---

# Debugging & stability during the project

- Reproduce with **one test**: `pytest tests/test_x.py::test_y -v`
- Run repeatedly to detect flakiness: loop 5x in Git Bash
  `for i in 1 2 3 4 5; do pytest -m cli -q || break; done`
- Read the **log file** in `logs/` (DEBUG level in `dev`)
- `breakpoint()` / VS Code debugger (Day 1)
- Look at the **screenshot** of a failed desktop test
- Change one thing at a time; commit when green

<!-- Trainer notes: Encourage teams to commit every time something turns green - then "git diff" shows exactly what broke it next. -->

---

# Final review & optimization discussion

- Which tests belong in **smoke** vs **regression**?
- What runs on **every PR** vs **nightly**?
- Where can a CLI/file check **replace** a slow UI check?
- Shared **module-scoped** fixtures (Calculator) vs isolation - trade-off?
- How would you run this on 3 Windows VMs in parallel? (pytest-xdist, self-hosted runner pool)
- What would you monitor over time? (duration, flaky rate, retry counts)

<!-- Trainer notes: Run this as an open discussion after the demos. Collect answers on the whiteboard; there is no single right answer. -->

---

<!-- _class: lead -->
# Course Recap

<!-- Trainer notes: Final 25 minutes: recap, next steps, certificates, Q&A. -->

---

# 5 days in one slide

| Day | You learned | You built |
|---|---|---|
| 1 | Python, OOP, debugging | clean, debuggable scripts |
| 2 | pywinauto, UIA, CLI automation | Calculator/Notepad/CLI scripts |
| 3 | CSV/JSON/YAML, Linux, subprocess | data-driven & system automation |
| 4 | Framework design, logging, PyTest, AI | `automation_framework/` |
| 5 | Git, GitHub Actions, best practices | team-ready repo, CI, E2E project |

<!-- Trainer notes: Ask each trainee to name one thing they will use at work next week. -->

---

# Key principles to take home

1. **Page objects + stable locators** (auto_id first)
2. **Explicit waits**, never blind sleeps
3. **Own your state**: own temp files, own tabs, own processes
4. **Clean up** in fixtures / finally
5. **Configuration over hard-coding** (`config.yaml`, `--env`)
6. **Evidence on failure**: logs, screenshots, HTML reports
7. **Everything in Git**, every change through **CI**

<!-- Trainer notes: These seven lines are the essence of the course. -->

---

# Certification & next steps

- **Assessment**: Day 5 quiz (20 MCQs, pass mark 70%) + mini project (pass mark 60/100)
- Course completion certificate after both
- Practise: automate one real manual regression case from your project this month
- Explore next:
  - **pytest-xdist** (parallel), **Allure** reports
  - **GitHub Actions** advanced: reusable workflows, environments, self-hosted runner pools
  - **Web automation** (Playwright / Selenium) and **API testing** (requests, pytest)
  - Vendor certifications: ISTQB Test Automation Engineer, GitHub Actions certification

<!-- Trainer notes: Adapt the assessment rules to your organisation's policy. Share links to the official docs: docs.github.com/actions, pywinauto.readthedocs.io, docs.pytest.org. -->

---

# Q & A

*Thank you - now go automate something!*

Resources in this folder:
- `02_Reading_Material.md` - handbook, cheat sheets, questions & answers
- `03_Quiz.md` - self-check
- `examples/` - Git script, workflow samples, best-practice demos
- `hands_on/` - labs, mini project starter & solution

<!-- Trainer notes: Collect feedback forms. Remind trainees that their GitHub repo with a green CI badge is a great portfolio item. -->
