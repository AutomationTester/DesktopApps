# Day 3 - Hands-on Lab Guide
## File Handling, Configuration Management, Linux Basics and CLI Automation

**Course:** Python Desktop Application Automation Testing
**Day:** 3 of 5
**Total lab time:** about 3 h 30 min (spread across the day, see the agenda in `01_Presentation.md`)

---

## Before you start

| Item | Check |
|------|-------|
| Python 3 | `python --version` (Windows) / `python3 --version` (Linux) |
| PyYAML | `python -c "import yaml; print(yaml.__version__)"` - if it fails: `pip install pyyaml` |
| A Linux-like shell | **Git Bash** (installed with Git for Windows), **WSL** (`wsl --install` in an admin PowerShell, then reboot), a **Linux VM**, or a **cloud shell** (e.g. GitHub Codespaces, Azure/Google Cloud Shell) |
| Lab files | `hands_on/starter/` (you edit these) and `hands_on/solutions/` (peek only when stuck) |

**Folder layout**

```
hands_on/
  Lab_Guide.md                  <- this file
  starter/                      <- your working copies with "# TODO" markers
    data/calc_lab_tests.csv, calc_lab_tests.json
    config/app_dev.yaml, app_qa.yaml, checks.yaml
    lab1_data_driven_calculator.py
    lab2_run_commands.py
    lab3_system_maintenance.py
    lab4_config_cli.py
    lab6_permissions_check.py
  solutions/                    <- complete reference solutions (same names)
```

**Golden rule for every lab:** scripts only create or delete files inside a `sandbox/` folder next to the script. Never point a cleanup script at a real folder while you are learning.

| Lab | Topic | Time |
|-----|-------|------|
| Lab 1 | Data-driven automation using CSV/JSON (Calculator) | 45 min |
| Lab 2 | Executing Linux commands via Python scripts | 30 min |
| Lab 3 | Automating system-level tasks (logs, disk, backup, processes) | 40 min |
| Lab 4 | CLI-based configuration automation | 40 min |
| Lab 5 | Linux shell commands (type them yourself) | 30 min |
| Lab 6 | File permissions and execution rights | 20 min |
| Lab 7 (extra) | Virtual environment + requirements.txt | 15 min |
| Lab 8 (extra) | Mini project: config-driven data-driven suite | homework |

---

## Lab 1 - Data-driven automation using CSV/JSON

**Objective:** Separate test *data* from test *logic*. Read Calculator test cases from CSV or JSON, validate them, execute them through a calculator driver, and produce a CSV results file plus a JSON summary.

**Time:** 45 minutes
**File:** `starter/lab1_data_driven_calculator.py`
**Data:** `starter/data/calc_lab_tests.csv`, `starter/data/calc_lab_tests.json`

### Background
The file already contains two "drivers" with the same method `calculate(num1, op, num2)`:
- `MockCalculator` - pure Python, works anywhere. Use `--dry-run`.
- `GuiCalculator` - drives the real Windows 11 Calculator using pywinauto (auto_ids `num0Button`..`num9Button`, `plusButton`, `equalButton`, `CalculatorResults`, ...).

You write the data layer, test loop and reports. Because of the layer separation, your code works with both drivers without any change.

### Steps
1. Open `data/calc_lab_tests.csv` in VS Code. Notice the deliberately bad rows: `LAB-006` uses `%`, `LAB-007` has `abc` as a number, `LAB-008` has a wrong expected value.
2. Run the starter to see the TODO message:
   ```
   cd hands_on/starter
   python lab1_data_driven_calculator.py --dry-run
   ```
3. **TODO 1 `load_rows`** - use `csv.DictReader` for `.csv` (open with `newline=""`) and `json.load(f)["tests"]` for `.json`.
4. **TODO 2 `validate_row`** - return a message for empty fields, unsupported operators, and non-numeric numbers (`float()` inside `try/except ValueError`).
5. **TODO 3 `is_match`** - compare numerically if possible (`"2.5"` equals `"2.50"`), otherwise compare text (for `Cannot divide by zero`).
6. **TODO 4 `run_tests`** - for each row: validate, calculate, set `PASS`/`FAIL`/`ERROR`, append a result dict, print one line.
7. **TODO 5/6 `write_reports`** - write `sandbox/lab1_results.csv` with `csv.DictWriter`, then a `sandbox/lab1_summary.json`.
8. Run with both data files:
   ```
   python lab1_data_driven_calculator.py --dry-run
   python lab1_data_driven_calculator.py --dry-run --data data/calc_lab_tests.json
   ```

### Expected output (CSV data)
```
Running 8 tests from calc_lab_tests.csv
  LAB-001     15 + 27    expected=42      actual=42      PASS
  ...
  LAB-006      4 % 2     expected=2       actual=        ERROR unsupported operator '%'
  LAB-007    abc + 1     expected=1       actual=        ERROR num1 is not a number: 'abc'
  LAB-008     50 * 2     expected=1000    actual=100     FAIL
Summary: total=8 PASS=5 FAIL=1 ERROR=2 pass_rate=62.5%
```
The JSON data set should give 4/4 PASS. The script's exit code is `1` when anything fails (check with `echo $?` in Git Bash or `$LASTEXITCODE` in PowerShell).

### Hints
- Everything from CSV is a string. JSON numbers arrive as `int`/`float` - the starter normalises rows with `str(v).strip()`.
- `sum(r["status"] == "PASS" for r in results)` counts booleans.
- Stuck? Compare with `solutions/lab1_data_driven_calculator.py`.

### Stretch goals
- Add `--priority high` to run only rows with that priority (solution has it).
- Add a `skip` column; rows with `skip=yes` get status `SKIPPED`.
- *(Only on your own machine, with trainer permission)* run without `--dry-run` to drive the real Calculator. Keep your hands off the mouse while it runs.

---

## Lab 2 - Executing Linux commands via Python scripts

**Objective:** Run OS commands from Python safely and portably, capture output, and log the results.

**Time:** 30 minutes
**File:** `starter/lab2_run_commands.py`

### Steps
1. **TODO 1/2 `run_command`** - call `subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=shell)` and return a dict. Catch `subprocess.TimeoutExpired` and `FileNotFoundError` and return a dict with an `error` message instead of crashing.
2. **TODO 3 `build_checks`** - use `IS_WINDOWS` to choose:

   | Check | Windows | Linux |
   |-------|---------|-------|
   | list files | `dir /b "<folder>"` with `shell=True` (built-in) | `["ls", "-1", folder]` |
   | find ERROR lines | `["findstr", "ERROR", log]` | `["grep", "ERROR", log]` |
   | current user | `["whoami"]` | `["whoami"]` |
3. **TODO 4** - add a negative test with a command that does not exist.
4. **TODO 5** - improve the `detail` text: number of files, number of ERROR lines.
5. **TODO 6** - write `sandbox/lab2_command_log.csv` with `csv.DictWriter`.
6. Run: `python lab2_run_commands.py`. If you have WSL, also run it there: `wsl python3 lab2_run_commands.py` (from the starter folder).

### Expected output (Windows)
```
OS detected: Windows
[OK    ] python version                 rc=0  Python 3.x.y
[OK    ] list files                     rc=0  4 files: a.txt, b.txt, c.csv, service.log
[OK    ] find ERROR lines               rc=0  2 ERROR lines (unique: ['ERROR disk full'])
[OK    ] current user                   rc=0  mypc\me
[FAILED] missing tool (negative test)   rc=None  command not found
Log written to sandbox\lab2_command_log.csv
```

### Hints
- `grep`/`findstr` return code `1` means "no match" - not a crash.
- `dir` is not an .exe; without `shell=True` you get `FileNotFoundError`.
- `sys.executable` is the most portable command there is.

### Stretch goals
- If `shutil.which("grep")` finds Git Bash's grep on Windows, add a `grep -c ERROR` check.
- Add a `--timeout` argparse option.
- Record the duration of each command using `time.perf_counter()`.

---

## Lab 3 - Automating system-level tasks

**Objective:** Build a housekeeping tool for a test machine: disk report, log archival, cleanup of old files, folder backup, and process check.

**Time:** 40 minutes
**File:** `starter/lab3_system_maintenance.py`
The script creates `sandbox/lab3/` with 8 fake log files aged 0, 2, 4, 6, 9, 12, 20 and 45 days (using `os.utime`).

### Steps
1. Run `python lab3_system_maintenance.py report` - this part is done. Read how `shutil.disk_usage()` is used.
2. **TODO 1 `old_logs(days)`** - `LOGS.glob("*.log")` + `p.stat().st_mtime < time.time() - days * DAY`.
3. **TODO 2 `task_archive`** - copy the old logs into a staging folder, `shutil.make_archive(base, "zip", root_dir=staging)`, remove the staging folder.
4. **TODO 3 `task_cleanup`** - honour `--dry-run`; call `safe(f).unlink()` only for real runs.
5. **TODO 4 `task_backup`** - `shutil.copytree(RESULTS, BACKUP / f"results_{timestamp}")`, then verify names and sizes.
6. **TODO 5 `process_running`** - Windows: `tasklist /FI "IMAGENAME eq python.exe" /NH`; Linux: `pgrep -x python3` (return code 0 = running).
7. Try:
   ```
   python lab3_system_maintenance.py cleanup --days 3 --dry-run
   python lab3_system_maintenance.py all --days 7
   python lab3_system_maintenance.py process --names python notepad
   ```
   Delete `sandbox/lab3` to start over (the solution also has `--reset`).

### Expected output (`all --days 7`, fresh data)
```
[archive] 4 logs -> logs_20260926_101500.zip
[cleanup] deleted run_05.log ... run_08.log
[cleanup] 4 file(s) matched, freed 10.4KB
[backup] 2 files -> results_20260926_101500  verify=PASS
[process] python          RUNNING
```

### Hints
- Always test cleanup with `--dry-run` first - this is what real engineers do.
- `shutil.copy2` keeps timestamps; `shutil.copy` does not.
- Use `"gztar"` instead of `"zip"` on Linux to get a `.tar.gz`.

### Stretch goals
- Retention: keep only the 3 newest backups (solution has it).
- Add `--threshold 80` and print `ALERT` when disk usage is above it.
- Linux only: check a service with `systemctl is-active ssh` (return code 0 = active).
- Schedule it: `crontab -e` on Linux (`0 2 * * * /usr/bin/python3 /path/lab3_system_maintenance.py all`) or Task Scheduler on Windows.

---

## Lab 4 - CLI-based configuration automation

**Objective:** Build a CLI (argparse sub-commands) that reads, changes, validates and uses YAML environment configs, with environment variable overrides and secrets that never touch the file.

**Time:** 40 minutes
**File:** `starter/lab4_config_cli.py`
**Config:** `starter/config/app_dev.yaml`, `app_qa.yaml`, `checks.yaml`

### Steps
1. Try the finished parts:
   ```
   python lab4_config_cli.py show --env qa
   python lab4_config_cli.py get app.launch_timeout --env dev
   ```
2. **TODO 1 `effective`** - apply `LAB_LOG_LEVEL` and `LAB_RETRIES` overrides (convert retries with `int()`).
   Test in Git Bash: `LAB_RETRIES=4 python lab4_config_cli.py show --env qa`
   Test in PowerShell: `$env:LAB_RETRIES = "4"; python lab4_config_cli.py show --env qa; Remove-Item Env:LAB_RETRIES`
3. **TODO 2 `set_dotted`** and **TODO 3 `cmd_set`** - save changes to `sandbox/lab4_config/app_<env>.yaml` (templates stay untouched). Use `yaml.safe_load(args.value)` so `"5"` becomes the int `5` and `"true"` becomes `True`.
4. **TODO 4 `validate_config`** - required keys, types, allowed log levels, retries 0..5.
   ```
   python lab4_config_cli.py set retries 9 --env qa
   python lab4_config_cli.py validate --env qa      # INVALID, exit code 1
   python lab4_config_cli.py set retries 3 --env qa
   python lab4_config_cli.py validate --env qa      # VALID, exit code 0
   ```
5. **TODO 5 `cmd_run`** - run each check in `checks.yaml`, substitute `{python}`, `{env}`, `{retries}`, pass `TEST_ENV` to the child process.
6. Set a secret and see that it is masked: Git Bash `LAB_API_TOKEN=abc123 python lab4_config_cli.py show`.

### Expected output (`run --env qa`)
```
[PASS] interpreter available                  rc=0 out='Python 3.x.y'
[PASS] child process sees TEST_ENV            rc=0 out='env=qa'
[PASS] retries value passed as argument       rc=0 out='retries 3'
[PASS] tool exits with code 3 on bad input    rc=3 out=''
4/4 checks passed for env 'qa'
```

### Hints
- `args.func(args)` - each sub-command stores its handler with `set_defaults(func=...)`.
- `isinstance(True, int)` is `True` in Python. Watch out when checking types.
- Return exit codes from `main()` and use `sys.exit(main())` so CI can react.

### Stretch goals
- Add `export` (effective config as JSON) and `reset` (delete sandbox copies) sub-commands.
- Add a `prod` environment that refuses `set` unless `--force` is passed.
- Add a `diff` sub-command that shows keys that differ between dev and qa.

---

## Lab 5 - Linux shell commands (type them yourself)

**Objective:** Get comfortable with the commands every automation engineer uses daily.

**Time:** 30 minutes
**Where:** Git Bash (right-click in a folder -> "Open Git Bash here"), WSL (`wsl` in PowerShell), a Linux VM, or a cloud shell.
**Reference script:** `examples/linux_commands_practice.sh` runs all of these automatically - but type them yourself first.

Type each command and compare with the expected result.

| # | Command | What you should see / learn |
|---|---------|-----------------------------|
| 1 | `cd ~` then `pwd` | Your home folder, e.g. `/c/Users/you` (Git Bash) or `/home/you` (Linux) |
| 2 | `mkdir -p day3lab/logs day3lab/data` | No output = success |
| 3 | `cd day3lab` then `ls` | `data  logs` |
| 4 | `echo "INFO start" > logs/app.log` | Creates the file (`>` overwrites) |
| 5 | `echo "ERROR db down" >> logs/app.log` and `echo "info done" >> logs/app.log` | Appends lines (`>>`) |
| 6 | `cat logs/app.log` | Three lines |
| 7 | `grep ERROR logs/app.log` | `ERROR db down` |
| 8 | `grep -i info logs/app.log` | Two lines (case-insensitive) |
| 9 | `grep -c -i info logs/app.log` | `2` |
| 10 | `grep FATAL logs/app.log; echo $?` | No lines, then `1` (1 = not found) |
| 11 | `printf "id,name\n1,alice\n" > data/users.csv` | Creates a CSV |
| 12 | `cp data/users.csv data/users_bak.csv` then `ls data` | `users.csv  users_bak.csv` |
| 13 | `mv data/users_bak.csv data/old.csv` then `ls data` | `old.csv  users.csv` (renamed) |
| 14 | `cp -r data data_copy` then `ls` | `data  data_copy  logs` |
| 15 | `find . -name "*.csv"` | Four CSV paths |
| 16 | `find . -type d` | `.`, `./logs`, `./data`, `./data_copy` |
| 17 | `ls -l logs` | Long listing with permissions, size, date |
| 18 | `ls -la` | Also shows `.` and `..` (and hidden files) |
| 19 | `cat logs/app.log \| grep -i error \| wc -l` | `1` - a pipe chains commands |
| 20 | `rm data/old.csv` then `rm -r data_copy` then `ls` | `data  logs` |
| 21 | `cd ..` then `pwd` | Back to the home folder |
| 22 | `rm -r day3lab` | Clean up (there is no recycle bin!) |

**Then run the reference script:**
```
cd <course folder>/Day3_File_Handling_Linux_System_Automation/examples
bash linux_commands_practice.sh
```

### Explore the Linux filesystem (WSL / Linux VM only)
```
ls /                # bin boot dev etc home lib opt proc root tmp usr var ...
ls /etc | head      # system configuration files
ls /var/log         # system logs
cat /etc/os-release # which Linux distribution?
echo $HOME; echo $PATH
which python3
```

### Stretch goals
- `head -n 1 logs/app.log`, `tail -f logs/app.log` (Ctrl+C to stop) - how would `tail -f` help while a test runs?
- `grep -rn "ERROR" .` - recursive search with line numbers.
- `find . -name "*.log" -mtime +7` - what would this find on a real server?
- `du -sh *` and `df -h` - disk usage.

---

## Lab 6 - File permissions and execution rights

**Objective:** Read and change permissions with `chmod` (symbolic and octal), understand the shebang, and check permissions from Python.

**Time:** 20 minutes
**Best in:** WSL or a Linux VM. In Git Bash on Windows, `chmod` is mostly ignored because NTFS does not store Linux permissions.

### Part A - shell (WSL / Linux)
```
mkdir -p ~/permlab && cd ~/permlab
printf '#!/usr/bin/env python3\nprint("hello from python")\n' > hello.py
ls -l hello.py          # -rw-r--r--  (644) - not executable
./hello.py              # Permission denied
python3 hello.py        # works - python reads the file, no x needed
chmod +x hello.py
ls -l hello.py          # -rwxr-xr-x
./hello.py              # hello from python (shebang tells Linux to use python3)
chmod 700 hello.py && ls -l hello.py     # -rwx------  only the owner
chmod u=rw,go=r hello.py && ls -l hello.py   # -rw-r--r--  symbolic form
echo "secret" > token.txt && chmod 600 token.txt && ls -l token.txt
chmod 444 token.txt && echo "x" >> token.txt   # Permission denied (read-only)
cd ~ && rm -rf ~/permlab
```

**Fill in this table (answers in the reading material):**

| Octal | rwx | Typical use |
|-------|-----|-------------|
| 755 | ? | ? |
| 644 | ? | ? |
| 600 | ? | ? |
| 700 | ? | ? |

### Part B - Python (`starter/lab6_permissions_check.py`)
1. **TODO 1** `octal_to_rwx(0o754)` should return `rwxr-xr--`.
2. **TODO 2** `rwx_to_octal("rwxr-xr--")` should return `0o754`.
3. **TODO 3/4** create files in `sandbox/lab6/`, `os.chmod` them, and audit them with `stat.filemode()` / `stat.S_IMODE()`.
4. Run on Windows *and* in WSL (`wsl python3 lab6_permissions_check.py`) and compare. On Windows only the read-only flag changes (`666` vs `444`).

### Stretch goal
Write a check that fails if any `*.env` file in a folder is readable by "others" (`mode & stat.S_IROTH`).

---

## Lab 7 (extra) - Virtual environment + requirements.txt

**Time:** 15 minutes. Work in a scratch folder **outside** the course folder, e.g. `~/venvlab`.

| Step | Windows (PowerShell) | Linux / WSL / macOS | Git Bash on Windows |
|------|----------------------|---------------------|---------------------|
| Create | `python -m venv .venv` | `python3 -m venv .venv` | `python -m venv .venv` |
| Activate | `.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` | `source .venv/Scripts/activate` |
| Check | `where python` | `which python` | `which python` |
| Install | `pip install pyyaml` | same | same |
| Freeze | `pip freeze > requirements.txt` | same | same |
| Deactivate | `deactivate` | same | same |
| Recreate elsewhere | `pip install -r requirements.txt` | same | same |

Tips: if PowerShell blocks `Activate.ps1`, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once. On Ubuntu/Debian you may need `sudo apt install python3-venv`. Never commit `.venv/` to git - add it to `.gitignore`.

**Expected:** after activation the prompt starts with `(.venv)` and `which python`/`where python` points inside `.venv`.

---

## Lab 8 (extra / homework) - Mini project

Combine everything: a YAML file lists **which data file** to run (CSV or JSON), **which environment** (dev/qa), and **which driver** (mock/gui). Write `run_suite.py` that:
1. loads `suite.yaml` (plus `--env` override and `TEST_ENV` env var),
2. runs the Lab 1 logic on each listed data file,
3. writes one combined `sandbox/suite_report.json`,
4. exits with 0/1,
5. can be run from Git Bash/WSL as `./run_suite.py --env qa` (shebang + `chmod +x`).

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'yaml'` | `pip install pyyaml` (inside your venv if one is active) |
| Blank lines between CSV rows on Windows | Open the file with `newline=""` |
| `UnicodeDecodeError` | Pass `encoding="utf-8"` to `open()` |
| `FileNotFoundError` for a data file | Build paths from `Path(__file__).resolve().parent`, not the current folder |
| `FileNotFoundError: 'dir'` | `dir` needs `shell=True` (it is a cmd built-in) |
| `python3` opens the Microsoft Store on Windows | Use `python` on Windows, `python3` on Linux |
| `bash: ./script.sh: Permission denied` | `chmod +x script.sh` or run `bash script.sh` |
| `/usr/bin/env: 'python3\r': No such file` | The script has Windows line endings. `sed -i 's/\r$//' script.py` or set VS Code to LF |
