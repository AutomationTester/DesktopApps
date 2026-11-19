# Lab 3 Solution: Prompt, AI Answer Review and Improvement Checklist

## Step 2: Problems found by hand (the trainee's own list comes BEFORE asking AI)

| # | Line / area | Problem | Effect |
|---|-------------|---------|--------|
| 1 | `SRC = "lab3_work/..."` | Paths are relative to the **current working directory** | The script breaks or writes elsewhere when it is started from another folder |
| 2 | `os.makedirs(SRC)` | Crashes if the folder exists. Old backup is never cleaned | The 2nd run always crashes. Stale data gives false results |
| 3 | `f = open(...)` without close, `json.load(open(...))` | File handles leak | Files can be empty or unflushed, and Windows locks them |
| 4 | `"python backup_tool.py " + SRC`, `shell=True` | String command through the shell. `python` may not be the interpreter that is running | Quoting bugs with spaces, security risk, wrong Python |
| 5 | `Popen` + `time.sleep(2)` | Fixed wait, and the process is never waited on | The tool takes 0.3 s to 2.1 s, so the result is random. The process is also left running |
| 6 | `status["files"] == "3"` | Compares an int with a str | Always False, so "Backup FAILED" even when the backup worked |
| 7 | status "running" is not handled | Reads status before the tool is done | Random FAIL |
| 8 | Only file **names** are checked | Contents are never verified | A broken copy would pass |
| 9 | `except: print("error")` | Bare except hides the real exception | No clue what failed |
| 10 | `print` only, no exit code | No log file. The script always exits 0 | Cannot debug afterwards. CI shows green |
| 11 | Magic numbers (2, 3) | Not configurable | Hard to tune for slower machines |

## Step 3: Prompt used

```text
Role: You are a senior Python test automation engineer who writes reliable,
debuggable tests for command-line tools.

Context: Windows 11, Python 3.14, standard library only. backup_tool.py is the
application under test (I cannot change it). It starts after a random delay,
writes status.json {"status": "running", "files": 0}, copies files slowly, then
writes {"status": "done", "files": <int>}. Exit code 0 on success, 2 on bad input.
The test script below gives random results and sometimes crashes on the 2nd run.

Task:
1. List every bug and flakiness cause (numbered, one line each, with the line).
2. Rewrite the test script.

Constraints:
- No time.sleep for synchronisation; wait for the process with a timeout and
  poll status.json until status == "done" (tolerate a half-written JSON file).
- pathlib paths relative to the script file; clean the work folder first.
- subprocess with sys.executable and an argument list, no shell=True.
- logging: console INFO, file DEBUG; log each failed check at ERROR.
- Verify file names AND contents. Return exit code 0 = pass, 1 = fail.
- Keep function names small and testable (a run_backup_check() -> bool).

Format: numbered list first, then ONE complete code block, then 3 bullet points
on what you would still test manually.

<paste flaky_backup_test.py here>
<paste the docstring of backup_tool.py here; do NOT paste company code or data>
```

## Step 4: Reviewing the AI answer (what we typically had to correct)

Different assistants give different answers. These are the problems trainers saw most often, and what to do about each:

| AI suggestion | Verdict | Action |
|---------------|---------|--------|
| "Increase `time.sleep(2)` to `time.sleep(5)`" | Reject. Still a race and slower | Poll with `wait_until` plus a timeout |
| Wrapped everything in `try/except Exception: pass` "for robustness" | Reject. Hides failures | Catch specific exceptions and log them |
| `@retry` around the **whole test including assertions** | Reject. It turns real bugs into passes | Retry *actions* only. Assertions run once |
| Used `status["files"] == int("3")` | Accept the idea, but compare with the parameter `file_count` | No magic numbers |
| Added `shutil.rmtree(WORK)` | Accept. Check it only deletes our own `lab3_work` folder | Path is built from `__file__` |
| Invented `subprocess.run(..., wait_for_file=...)` | Reject. The parameter does not exist (hallucination) | Check the docs |
| Changed `backup_tool.py` to write status atomically | Out of scope. We test the app, we don't change it | Log it as an improvement suggestion for developers |

## Step 5: Improvement checklist (final)

- [x] Runs 5 times in a row with `RESULT: PASS` and exit code 0
- [x] Works from any folder: `python hands_on/solutions/lab3/improved_backup_test.py`
- [x] No `time.sleep` used for synchronisation (only inside the polling loop)
- [x] No bare `except`. Every failure is logged with enough detail
- [x] `logs/improved_backup_test.log` contains the DEBUG details (command, rc, stdout)
- [x] A negative check exists (missing source gives exit code 2), see `test_backup_pytest.py`
- [x] I can explain every line to a colleague

Final script: `improved_backup_test.py`. Pytest version: `test_backup_pytest.py`.
