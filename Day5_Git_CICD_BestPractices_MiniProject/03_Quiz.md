# Day 5 Quiz - Git, CI/CD with GitHub Actions, Best Practices

20 multiple-choice questions. Choose **one** answer per question.
Pass mark: 14 / 20 (70%). Time: 20 minutes.

---

**1.** Which command moves changes from the working directory to the staging area?

- A) `git commit`
- B) `git add`
- C) `git push`
- D) `git stash`

**2.** You want to see changes that are **staged** but not yet committed. Which command?

- A) `git diff`
- B) `git log -p`
- C) `git diff --staged`
- D) `git status --ignored`

**3.** What does `git fetch origin` do?

- A) Downloads new commits and merges them into your current branch
- B) Downloads new commits and updates `origin/*` branches without changing your working files
- C) Uploads your commits to the remote
- D) Deletes local branches that no longer exist on the remote

**4.** A colleague already pulled your branch `feature/x`. You want to update it with the latest `main`. What is the safest choice?

- A) `git rebase main` and `git push --force`
- B) `git merge main` into `feature/x`
- C) `git reset --hard origin/main`
- D) Delete the branch and create it again

**5.** After `git merge feature/timeout-qa` Git reports a conflict in `config.yaml`. What is the correct sequence to finish?

- A) `git commit` immediately
- B) Edit the file and remove the markers, `git add config.yaml`, `git commit`
- C) `git push --force`
- D) `git merge --continue` without editing

**6.** Which of these should be listed in the `.gitignore` of an automation repository?

- A) `tests/`
- B) `requirements.txt`
- C) `reports/`, `logs/`, `screenshots/`, `.venv/`
- D) `config/config.yaml`

**7.** You accidentally pushed an API token to GitHub. What is the **first** thing to do?

- A) Delete the file in a new commit
- B) Revoke/rotate the token
- C) Make the repository private
- D) Rewrite history with `git rebase -i`

**8.** Which branching strategy has everyone integrating into `main` at least daily with very short-lived branches?

- A) GitFlow
- B) Trunk-based development
- C) Release branching
- D) Forking workflow

**9.** In GitHub Actions, where must workflow files be stored?

- A) `/workflows/` at the repository root
- B) `.github/actions/`
- C) `.github/workflows/`
- D) Anywhere, as long as the extension is `.yml`

**10.** Which statement about jobs and steps is TRUE?

- A) All steps of a workflow share one machine, even across jobs
- B) Jobs run in parallel by default; steps within a job run in order on the same runner
- C) Steps run in parallel; jobs always run in sequence
- D) A job can only contain one step

**11.** Why is `if: always()` added to the `actions/upload-artifact` step?

- A) To upload the report even when the test step failed
- B) To make the upload faster
- C) To retry the upload 3 times
- D) It is required syntax for every `uses:` step

**12.** What does `cache: pip` in `actions/setup-python@v5` do?

- A) Installs pip on the runner
- B) Caches downloaded packages between runs to speed up `pip install`
- C) Caches test results so passed tests are skipped
- D) Stores the virtual environment as an artifact

**13.** The cron expression `"30 20 * * *"` in a GitHub Actions schedule means:

- A) Every 30 minutes, 20 times a day
- B) 20:30 in the runner's local time zone, Mondays only
- C) Every day at 20:30 **UTC**
- D) On the 20th of every month at 00:30

**14.** Which trigger adds a "Run workflow" button (with optional inputs) to the Actions tab?

- A) `push`
- B) `schedule`
- C) `repository_dispatch`
- D) `workflow_dispatch`

**15.** Your suite has CLI tests and Windows 11 Calculator/Notepad (pywinauto) tests. Which CI setup is most appropriate?

- A) Everything on `ubuntu-latest`
- B) Everything on GitHub-hosted `windows-latest`
- C) CLI tests on an ubuntu + windows matrix; desktop tests on a self-hosted Windows 10/11 runner with an interactive logged-in session
- D) Desktop tests on `ubuntu-latest` using Xvfb

**16.** What is Xvfb used for in CI?

- A) Running Windows desktop apps on Linux
- B) Providing a virtual display so **Linux** GUI apps can run without a monitor
- C) Encrypting secrets
- D) Recording videos of Windows tests

**17.** Which locator is generally the MOST stable for a Windows desktop control?

- A) Screen coordinates `(412, 305)`
- B) An image of the button
- C) `auto_id="num7Button"`
- D) `found_index=7`

**18.** Windows 11 Notepad restores the user's previous tabs. What is the safe way for a test to use Notepad?

- A) Connect to any Notepad window, select all, type, and close the window
- B) Create its own temp file, open it with `notepad.exe <path>`, work only in that tab, save with Ctrl+S, close only that tab with Ctrl+W
- C) Kill all `notepad.exe` processes first, then start a new one
- D) Use `Desktop().window(title_re=".*Notepad").close()` before each test

**19.** A test starts a helper process and sometimes fails, leaving the process running. Best fix?

- A) `taskkill /IM python.exe /F` at the start of every test
- B) Keep the `Popen` handle and terminate/kill **that** process in a fixture teardown or `finally`
- C) Add `time.sleep(10)` so the process finishes
- D) Ignore it - the OS cleans up eventually

**20.** Which code builds a report path that works on both Windows and Linux?

- A) `"reports\\" + name + ".html"`
- B) `os.getcwd() + "/reports/" + name`
- C) `Path(__file__).resolve().parent / "reports" / f"{name}.html"`
- D) `"C:/automation/reports/" + name`

---

## Answer key with explanations

| Q | Answer | Explanation |
|---|---|---|
| 1 | **B** | `git add` stages changes; `commit` records staged changes; `push` sends commits to a remote; `stash` parks work. |
| 2 | **C** | `git diff --staged` compares the staging area with the last commit. Plain `git diff` shows unstaged changes only. |
| 3 | **B** | `fetch` only downloads and updates remote-tracking branches - always safe. Downloading **and** merging is `git pull` (A). |
| 4 | **B** | Merging does not rewrite history. Rebasing + force-push (A) would break the colleague's copy; `reset --hard` (C) throws work away. |
| 5 | **B** | Resolve the content, delete all conflict markers, stage the file to mark it resolved, then commit to complete the merge. |
| 6 | **C** | Generated output and virtual environments must not be committed. Tests, requirements and the shared config are source files. |
| 7 | **B** | Once pushed, the secret must be considered leaked (clones, forks, caches). Revoke/rotate first; cleaning history is secondary. |
| 8 | **B** | Trunk-based development: very short-lived branches merged into the trunk (main) at least daily, backed by strong CI. |
| 9 | **C** | GitHub only runs workflow YAML files located in `.github/workflows/`. |
| 10 | **B** | Each job gets its own fresh runner and jobs run in parallel unless `needs:` is used; steps run sequentially and share the job's file system. |
| 11 | **A** | By default a step is skipped after an earlier failure. `if: always()` forces the upload, so the report exists precisely when tests fail. |
| 12 | **B** | setup-python can cache pip's download cache keyed on the requirements file, making installs faster. It does not skip tests. |
| 13 | **C** | Fields: minute hour day-of-month month day-of-week. GitHub cron always uses UTC (20:30 UTC = 02:00 IST). |
| 14 | **D** | `workflow_dispatch` enables manual runs, optionally with inputs such as a `choice` of environment. |
| 15 | **C** | CLI tests run anywhere (a matrix catches OS differences). Hosted `windows-latest` is Windows Server without the Store Calculator/Win11 Notepad and without an interactive desktop, and Linux cannot run Windows apps at all. |
| 16 | **B** | Xvfb (X virtual frame buffer) is a fake X server for Linux GUI apps; it does not run Windows applications. |
| 17 | **C** | auto_id is set by developers and does not change with language, theme, resolution or layout. Coordinates, images and indexes are fragile. |
| 18 | **B** | Never assume a clean state: work only on your own file and tab and never close the user's window. Killing all Notepads (C) or closing the window (A, D) can destroy someone's work. |
| 19 | **B** | Clean up only what the test started, in code that always runs. Killing by image name (A) affects other users' processes; sleeps (C) do not fix the root cause. |
| 20 | **C** | `pathlib` picks the right separator and anchoring the path to `__file__` removes the dependency on the current working directory and on a specific machine. |

### Score guide

* 18-20: Excellent - ready to own CI for an automation repo.
* 14-17: Good - review the topics you missed in `02_Reading_Material.md`.
* below 14: Re-read sections 2-4 of the reading material and redo Labs 1-3.
