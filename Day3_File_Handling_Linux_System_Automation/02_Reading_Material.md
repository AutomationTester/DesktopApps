# Day 3 - Trainee Handbook
## File Handling, Configuration Management, Linux Basics & CLI Automation

*Python Desktop Application Automation Testing - Day 3 of 5*

Prerequisites: Day 1 (Python and OOP), Day 2 (pywinauto desktop automation, argparse, subprocess basics).
Companion files: `examples/` (runnable demos), `hands_on/Lab_Guide.md` (labs), `03_Quiz.md` (self-check).

---

## Table of Contents

1. [Working with files in Python - the essentials](#1-working-with-files-in-python---the-essentials)
2. [Reading and writing CSV files](#2-reading-and-writing-csv-files)
3. [Reading and writing JSON files](#3-reading-and-writing-json-files)
4. [Introduction to YAML for configuration](#4-introduction-to-yaml-for-configuration)
5. [CSV vs JSON vs YAML](#5-csv-vs-json-vs-yaml)
6. [Managing test data and environment configs](#6-managing-test-data-and-environment-configs)
7. [Data-driven desktop automation](#7-data-driven-desktop-automation)
8. [Linux filesystem structure](#8-linux-filesystem-structure)
9. [Common shell commands](#9-common-shell-commands)
10. [File permissions and execution rights](#10-file-permissions-and-execution-rights)
11. [Running Python scripts in Linux](#11-running-python-scripts-in-linux)
12. [Virtual environments basics](#12-virtual-environments-basics)
13. [Executing Linux commands using Python](#13-executing-linux-commands-using-python)
14. [Automating CLI-based tools](#14-automating-cli-based-tools)
15. [Handling command outputs and errors](#15-handling-command-outputs-and-errors)
16. [Configuration-driven execution using JSON/YAML](#16-configuration-driven-execution-using-jsonyaml)
17. [Automating system-level tasks](#17-automating-system-level-tasks)
18. [Common mistakes](#18-common-mistakes)
19. [Questions and answers](#19-questions-and-answers)
20. [Day 3 summary](#20-day-3-summary)

---

## 1. Working with files in Python - the essentials

Before touching CSV/JSON/YAML, three habits save hours of debugging.

**Habit 1 - always use `with`.** It closes the file even if an exception happens.

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("first line\n")
```

**Habit 2 - always pass `encoding="utf-8"`.** On Windows the default encoding is often `cp1252`; on Linux it is `utf-8`. The same script can then read a file differently on two machines.

**Habit 3 - build paths from the script's location**, not from the current working directory:

```python
from pathlib import Path

HERE = Path(__file__).resolve().parent        # folder containing this .py file
data_file = HERE / "data" / "calculator_tests.csv"
```

`pathlib` uses the right separator on each OS (`\` on Windows, `/` on Linux), so you never hard-code either.

| Mode | Meaning | If file exists | If missing |
|------|---------|----------------|------------|
| `"r"` | read (default) | read it | `FileNotFoundError` |
| `"w"` | write | **erased** | created |
| `"a"` | append | add to end | created |
| `"x"` | exclusive create | `FileExistsError` | created |
| `"rb"`/`"wb"` | binary read/write | - | - |

Useful `pathlib` helpers: `p.exists()`, `p.is_file()`, `p.mkdir(parents=True, exist_ok=True)`, `p.glob("*.log")`, `p.read_text(encoding="utf-8")`, `p.write_text(...)`, `p.stat().st_size`, `p.stat().st_mtime`, `p.unlink()`.

---

## 2. Reading and writing CSV files

CSV (Comma-Separated Values) is a plain-text table. The first row is usually a header. It opens in Excel, which is why business analysts and manual testers love it - and why it is the most common format for **test data**.

```
test_id,username,password,expected
TC001,admin,admin123,success
TC004,"o'brien, john",pa$$,failure
```

Note the quotes around `o'brien, john`: a value containing a comma must be quoted. This is why you should never parse CSV with `line.split(",")` - use the `csv` module, which handles quoting for you.

### 2.1 csv.reader and csv.writer (rows as lists)

```python
import csv

# Write
rows = [["test_id", "username", "expected"],
        ["TC001", "admin", "success"]]
with open("tests.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)

# Read
with open("tests.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)          # first row
    for row in reader:             # ['TC001', 'admin', 'success']
        print(row[0], row[1])
```

**Why `newline=""`?** The csv module writes its own line endings. Without `newline=""` on Windows you get an extra blank line between every row.

### 2.2 csv.DictReader and csv.DictWriter (rows as dictionaries)

For test data, prefer the dictionary versions. You access columns by name, so inserting a new column in Excel does not break your script.

```python
with open("login_testdata.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    required = {"test_id", "username", "password", "expected"}
    missing = required - set(reader.fieldnames or [])
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    for row in reader:
        print(row["test_id"], row["username"])
```

Writing a results report:

```python
fields = ["test_id", "expected", "actual", "status"]
with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(results)          # list of dicts
```

### 2.3 Everything is a string

CSV has no data types. `"1.25"` is a string, an empty cell is `""` (not `None`), and `bool("False")` is `True` because the string is not empty. Convert explicitly:

```python
duration = float(row["duration"])
retries = int(row["retries"])
enabled = row["enabled"].strip().lower() in ("yes", "true", "1")
```

**Demo:** `examples/01_csv_read_write.py`, `examples/02_csv_dictreader_testdata.py`

> **Try it yourself:** Add a column `priority` to `sandbox/login_testdata.csv` produced by example 02 and change the script to run only `high` priority rows.

---

## 3. Reading and writing JSON files

JSON (JavaScript Object Notation) stores nested, typed data. It is the language of REST APIs and many CLI tools (`--output json`).

| JSON | Python |
|------|--------|
| object `{"a": 1}` | `dict` |
| array `[1, 2]` | `list` |
| string `"text"` | `str` |
| number `3`, `2.5` | `int`, `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

**Syntax rules:** keys and strings use **double quotes**; **no trailing commas**; **no comments**.

### The four functions

| Function | Direction |
|----------|-----------|
| `json.load(f)` | file -> Python |
| `json.dump(obj, f, indent=2)` | Python -> file |
| `json.loads(text)` | string -> Python |
| `json.dumps(obj)` | Python -> string |

(The `s` stands for *string*.)

```python
import json

with open("test_suite.json", encoding="utf-8") as f:
    suite = json.load(f)

enabled = [t["id"] for t in suite["tests"] if t["enabled"]]
timeout = suite.get("timeout", 30)          # optional key with default

suite["max_retries"] = 3                    # modify
with open("test_suite.json", "w", encoding="utf-8") as f:
    json.dump(suite, f, indent=2)           # write the WHOLE file back
```

JSON files cannot really be "appended to" - you read, modify and rewrite. For large logs of records use JSON Lines (one JSON object per line) or CSV.

### Handling invalid JSON

```python
try:
    data = json.loads("{'name': 'demo',}")
except json.JSONDecodeError as e:
    print(e.msg, e.lineno, e.colno)
```

**Demo:** `examples/03_json_read_write.py`

> **Try it yourself:** Run `python -c "import json,sys; print(json.dumps({'ok': True}))"` and parse its output with `json.loads` in another script.

---

## 4. Introduction to YAML for configuration

YAML ("YAML Ain't Markup Language") is a human-friendly superset of JSON used for configuration: GitHub Actions, Azure Pipelines, Docker Compose, Kubernetes, Ansible, pytest plugins and more.

```yaml
# comments are allowed
project: Calculator Automation
version: "1.10"            # quoted -> string
app:                       # nested mapping (dict)
  path: calc.exe
  launch_timeout: 10
headless: false            # boolean
test_groups:               # list
  - smoke
  - regression
browsers: [chrome, edge]   # inline list also works
description: |
  multi-line text
  keeps line breaks
```

Structure comes from **indentation with spaces** (never tabs). A `key: value` pair is a dict entry; a line starting with `- ` is a list item.

### YAML in Python

Install once: `pip install pyyaml` (the import name is `yaml`).

```python
import yaml

with open("config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)            # normal dict / list / str / int / bool

with open("out.yaml", "w", encoding="utf-8") as f:
    yaml.safe_dump(config, f, sort_keys=False)
```

Always use **`yaml.safe_load`**. The older `yaml.load` with an unsafe loader can construct arbitrary Python objects from a malicious file.

### YAML gotchas

| You write | You get | Fix |
|-----------|---------|-----|
| `answer: yes` | `True` | `answer: "yes"` |
| `country: NO` | `False` | `country: "NO"` |
| `zip: 01234` | `668` (octal!) | `zip: "01234"` |
| `version: 1.10` | `1.1` (float) | `version: "1.10"` |
| `empty:` | `None` | give a value |
| tab indentation | `yaml.YAMLError` | use spaces |

**Demo:** `examples/04_yaml_config.py`

---

## 5. CSV vs JSON vs YAML

| Feature | CSV | JSON | YAML |
|---------|-----|------|------|
| Structure | flat table | nested | nested |
| Data types | strings only | str, number, bool, null | str, number, bool, null, dates... |
| Comments | no | no | yes |
| Human editing | easy (Excel) | OK | very easy |
| Typical use in testing | test data tables | tool/API input and output, structured test data | configuration, CI pipelines |
| Python module | `csv` (built in) | `json` (built in) | `yaml` (`pip install pyyaml`) |
| Main risk | Excel changes data (leading zeros, dates) | trailing commas, single quotes | indentation, implicit types |
| Safe read | `csv.DictReader` | `json.load` | `yaml.safe_load` |

Rule of thumb: **CSV for rows of test data, JSON for machine-to-machine data, YAML for configuration humans edit.**

---

## 6. Managing test data and environment configs

### 6.1 Test data

- Keep data **out of code** in a `data/` folder; keep it in **git** next to the tests.
- Give every row a unique **test_id** so failures are traceable.
- Cover **positive, negative and boundary** values (0, negative numbers, very large numbers, decimals, divide by zero, empty input).
- **Validate** data files before running (required columns, types, allowed values) and fail fast with a clear message.
- Use **synthetic data**, never real customer data (privacy laws like GDPR apply to test systems too).

```
project/
  tests/             test code
  data/              calculator_tests.csv, login.json
  config/            dev.yaml, qa.yaml, prod.yaml
  reports/           generated results (in .gitignore)
  requirements.txt
  .gitignore         .venv/, reports/, .env
```

### 6.2 Environment configs

The same tests usually run against several environments. Keep **one file per environment with the same keys**:

```yaml
# config/qa.yaml
env_name: qa
base_url: https://qa.example.internal
db:
  host: qa-db.example.internal
  user: qa_automation
  password_env_var: APP_DB_PASSWORD    # NAME of the variable, not the password
retries: 2
```

Select the environment at run time with a command-line option or an environment variable, and allow single values to be overridden. Typical priority:

**command line > environment variable > config file > default in code**

### 6.3 Environment variables

| Shell | Set for the session | Set for one command | Read |
|-------|--------------------|--------------------|------|
| Linux / macOS / Git Bash | `export TEST_ENV=qa` | `TEST_ENV=qa python3 run.py` | `echo $TEST_ENV` |
| PowerShell | `$env:TEST_ENV = "qa"` | - | `$env:TEST_ENV` |
| cmd.exe | `set TEST_ENV=qa` | - | `echo %TEST_ENV%` |

In Python: `os.environ.get("TEST_ENV", "dev")`. Environment variables are **always strings** - convert with `int()` etc. Changing `os.environ` inside Python affects only that process and the child processes it starts.

### 6.4 Secrets are never in code

Passwords, API tokens and keys must never be in `.py`, `.yaml` or `.json` files that go into git - git history keeps them forever, and bots scan public repositories within minutes.

- The config stores only the **name** of the variable holding the secret.
- Locally: set the env var, or use a `.env` file that is listed in `.gitignore` (commit a `.env.example` containing only names).
- In CI: use the pipeline's **secret variables** (GitHub Actions secrets, Azure DevOps variable groups, Jenkins credentials).
- In enterprises: a vault (Azure Key Vault, HashiCorp Vault, AWS Secrets Manager).
- **Mask** secrets in logs and reports (`"****"`).

```python
secret_var = config["db"]["password_env_var"]
password = os.environ.get(secret_var)
if not password:
    raise RuntimeError(f"Please set {secret_var}")
```

**Demo:** `examples/05_env_configs.py` with `examples/config/dev.yaml`, `qa.yaml`, `prod.yaml`:

```
python 05_env_configs.py --env qa
TEST_ENV=prod python 05_env_configs.py          # Git Bash / Linux
python 05_env_configs.py --env prod --demo-overrides
```

---

## 7. Data-driven desktop automation

**Data-driven testing (DDT)** means: one test script, many rows of data. A new test case is a new row, not new code.

### 7.1 The Calculator example

`examples/data/calculator_tests.csv`:

```
test_id,num1,operator,num2,expected,description
CALC-001,7,+,8,15,simple addition
CALC-004,9,/,4,2.25,division with decimal result
CALC-007,8,/,0,Cannot divide by zero,divide by zero error message
CALC-009,2,+,2,5,DELIBERATELY WRONG expected value - should FAIL
```

The GUI part uses what you learned on Day 2 (Windows 11 Calculator, UIA backend):

```python
subprocess.Popen("calc.exe")
win = Desktop(backend="uia").window(title="Calculator")
win.wait("visible", timeout=10)
win.child_window(auto_id="num7Button", control_type="Button").invoke()
win.child_window(auto_id="plusButton", control_type="Button").invoke()
win.child_window(auto_id="num8Button", control_type="Button").invoke()
win.child_window(auto_id="equalButton", control_type="Button").invoke()
win.child_window(auto_id="CalculatorResults").window_text()   # "Display is 15"
```

Other buttons: `num0Button`..`num9Button`, `minusButton`, `multiplyButton`, `divideButton`, `clearButton`. Strip `"Display is "` and thousands separators (`,`) before comparing.

### 7.2 Layered design

`examples/06_data_driven_calculator.py` is split into layers:

| Layer | Responsibility | Knows about GUI? |
|-------|----------------|------------------|
| Data | `load_test_cases()` reads CSV or JSON into a list of dicts | no |
| Driver | `MockCalculator` / `GuiCalculator` with `calculate(num1, op, num2)` | only GuiCalculator |
| Test | `run_suite()` loops, compares, sets PASS/FAIL/ERROR | no |
| Report | `write_results()` writes a CSV | no |

Both drivers have the same method, so `run_suite()` works with either (polymorphism from Day 1). Benefits:

- `--dry-run` validates data files and reporting in seconds on any machine (even Linux CI without a desktop).
- The GUI driver can change (new app version, new auto_ids) without touching data code.
- One broken row is caught with `try/except` and reported as `ERROR`, the rest still run.
- A non-zero exit code when anything fails makes CI builds turn red.

```
python 06_data_driven_calculator.py --dry-run
python 06_data_driven_calculator.py --dry-run --data data/calculator_tests.json
```

Always include at least one row that is **expected to fail**, to prove your test can actually detect a failure.

> **Try it yourself:** Add three boundary rows to the CSV (very large numbers, decimals like `0.1 + 0.2`, negative input) and run the dry-run again. What does `0.1 + 0.2` give, and how does `results_match()` handle it?

---

## 8. Linux filesystem structure

Linux has **one tree** starting at `/` (root). There are no drive letters.

| Path | Contains | Windows analogy |
|------|----------|-----------------|
| `/` | root of everything | `C:\` |
| `/home/<user>` (`~`) | your personal files | `C:\Users\<user>` |
| `/root` | home of the administrator (root user) | - |
| `/bin`, `/usr/bin` | programs (`ls`, `grep`, `python3`) | `C:\Windows\System32` |
| `/etc` | system configuration files | registry / `ProgramData` |
| `/var/log` | log files | Event Viewer logs |
| `/tmp` | temporary files, often cleared on reboot | `%TEMP%` |
| `/opt` | optional third-party software | `C:\Program Files` |
| `/dev`, `/proc` | devices and running processes (virtual) | Device Manager / Task Manager |
| `/mnt`, `/media` | mounted drives (WSL: `/mnt/c` is `C:\`) | other drive letters |

Important differences from Windows:
- Separator is `/`, not `\`.
- Names are **case-sensitive**: `Report.txt` and `report.txt` are different files.
- Files starting with `.` are hidden (`.gitignore`, `.env`, `.venv`).
- Special path symbols: `~` home, `.` current directory, `..` parent, `-` previous directory (with `cd`).
- In Git Bash, `C:\Users\me` appears as `/c/Users/me`.

**Where to practise:** Git Bash (comes with Git for Windows), WSL (`wsl --install` from an admin PowerShell - gives a real Ubuntu), a Linux VM (VirtualBox/Hyper-V), or a browser-based cloud shell (GitHub Codespaces, Azure Cloud Shell, Google Cloud Shell).

---

## 9. Common shell commands

### 9.1 Cheat-sheet

| Command | Purpose | Useful options | Example | Windows cmd |
|---------|---------|----------------|---------|-------------|
| `pwd` | print working directory | | `pwd` | `cd` |
| `ls` | list directory | `-l` long, `-a` hidden, `-h` sizes, `-R` recursive, `-t` by time | `ls -la /var/log` | `dir` |
| `cd` | change directory | `..`, `~`, `-` | `cd ../logs` | `cd` |
| `mkdir` | make directory | `-p` parents | `mkdir -p data/in` | `mkdir` |
| `touch` | create empty file / update time | | `touch notes.txt` | `type nul > f` |
| `cp` | copy | `-r` folders, `-i` confirm, `-p` keep times | `cp -r data backup` | `copy`, `xcopy` |
| `mv` | move or rename | `-i` confirm | `mv a.csv old.csv` | `move`, `ren` |
| `rm` | remove | `-r` folders, `-f` force, `-i` confirm | `rm -r tmpdir` | `del`, `rmdir /s` |
| `cat` | print file | `-n` line numbers | `cat app.log` | `type` |
| `head` / `tail` | first / last lines | `-n 20`, `tail -f` follow | `tail -f app.log` | - |
| `grep` | search text | `-i`, `-n`, `-c`, `-v`, `-r`, `-E`, `-q` | `grep -in error app.log` | `findstr` |
| `find` | find files | `-name`, `-type f/d`, `-mtime`, `-size`, `-exec`, `-delete` | `find . -name "*.log" -mtime +7` | `dir /s` |
| `wc` | count lines/words | `-l` | `wc -l app.log` | `find /c /v ""` |
| `chmod` | change permissions | `+x`, `755`, `-R` | `chmod +x run.sh` | `icacls` |
| `echo` | print text | `>` overwrite, `>>` append | `echo hi > f.txt` | `echo` |
| `which` | locate a command | | `which python3` | `where` |
| `du` / `df` | folder size / disk free | `-sh` / `-h` | `du -sh logs` | - |
| `ps` / `pgrep` | processes | `ps aux`, `pgrep -x name` | `pgrep -x sshd` | `tasklist` |

### 9.2 Examples in context

```bash
cd ~/project
ls -l logs                         # what logs do we have?
grep -c "ERROR" logs/app.log       # how many errors?
grep -n "Timeout" logs/*.log       # where exactly?
find . -name "*.log" -mtime +7     # logs older than a week
cp -r data data_backup             # backup before a destructive test
mv results.csv results_$(date +%Y%m%d).csv
rm -r data_backup                  # careful - there is no recycle bin
```

### 9.3 Redirection, pipes and exit codes

```bash
echo "INFO start" >  app.log         # overwrite
echo "ERROR fail" >> app.log         # append
python3 run.py > out.txt 2> err.txt  # stdout and stderr to different files
python3 run.py > all.txt 2>&1        # both into one file
cat app.log | grep -i error | wc -l  # pipe: output -> input
echo $?                              # exit code of the last command (0 = OK)
```

`grep` exit codes: `0` found, `1` not found, `2` error. Automation scripts rely on these codes.

**Demo:** `examples/linux_commands_practice.sh` - run with `bash linux_commands_practice.sh`. It creates `examples/sandbox/linux_practice/` and demonstrates every command above with comments.

> **Try it yourself:** Do Lab 5 in `hands_on/Lab_Guide.md` - 22 commands to type, each with the expected result.

---

## 10. File permissions and execution rights

### 10.1 Reading `ls -l`

```
-rwxr-xr--  1 tester qa  220 Sep 26 10:00 deploy.sh
^\_/\_/\_/    ^      ^
| |  |  |     owner  group
| |  |  +-- others: r--
| |  +----- group : r-x
| +-------- owner : rwx
+---------- type  : - file, d directory, l symbolic link
```

| Letter | On a file | On a directory |
|--------|-----------|----------------|
| `r` read | read the contents | list the names inside |
| `w` write | modify the file | create / delete / rename files inside |
| `x` execute | run it as a program | enter it (`cd`) and access files inside |

### 10.2 Octal notation

Each group is a sum of **r = 4, w = 2, x = 1**.

| Octal | rwx | Meaning / typical use |
|-------|-----|----------------------|
| 7 | `rwx` | read, write, execute |
| 6 | `rw-` | read, write |
| 5 | `r-x` | read, execute |
| 4 | `r--` | read only |
| 0 | `---` | nothing |

**Common permission sets:**

| Mode | String | Typical use |
|------|--------|-------------|
| 755 | `rwxr-xr-x` | scripts and programs, directories |
| 644 | `rw-r--r--` | normal files (data, config) |
| 600 | `rw-------` | secrets, `.env`, SSH private keys |
| 700 | `rwx------` | private scripts / folders |
| 750 | `rwxr-x---` | scripts shared with your team only |
| 444 | `r--r--r--` | read-only baseline files |
| 777 | `rwxrwxrwx` | everyone can do everything - **avoid** |

### 10.3 chmod

```bash
chmod +x run_tests.sh      # add execute for all
chmod u+x run_tests.sh     # owner only   (u user, g group, o others, a all)
chmod go-w config.yaml     # remove write from group and others
chmod u=rw,go=r file.txt   # set exactly (= 644)
chmod 755 run_tests.sh     # octal
chmod -R 755 scripts/      # recursive
```

`chown user:group file` changes the owner (usually needs `sudo`). `sudo` runs one command as the administrator - use it sparingly.

> **Note:** In Git Bash on Windows, NTFS does not store Linux permissions, so `chmod` mostly has no visible effect. Use WSL or a Linux VM for permission exercises (Lab 6). From Python on Windows, `os.chmod` can only toggle the read-only flag.

### 10.4 Execution rights and the shebang

A file needs the `x` permission **and** a shebang line to run as `./script`:

```python
#!/usr/bin/env python3
print("Hello from Linux")
```

```bash
python3 hello.py     # works without x - python just reads the file
./hello.py           # Permission denied
chmod +x hello.py
./hello.py           # works - the kernel reads the shebang and starts python3
```

- `#!/usr/bin/env python3` is preferred over `#!/usr/bin/python3` because it finds `python3` on the PATH (including inside an activated venv).
- Save scripts with **LF** line endings. With Windows CRLF you get `/usr/bin/env: 'python3\r': No such file or directory`. In VS Code click "CRLF" in the status bar and choose "LF"; in projects add `*.sh text eol=lf` to `.gitattributes`.

From Python: `os.access(path, os.X_OK)`, `stat.filemode(path.stat().st_mode)`, `os.chmod(path, 0o755)` - see `hands_on/solutions/lab6_permissions_check.py`.

---

## 11. Running Python scripts in Linux

```bash
python3 --version                   # on many distros 'python' does not exist
which python3                       # /usr/bin/python3
python3 run_tests.py --env qa       # argparse works the same as on Windows
./run_tests.py --env qa             # with shebang + chmod +x
TEST_ENV=qa python3 run_tests.py    # env var just for this command
python3 run_tests.py > run.log 2>&1 &   # background, output to a log file
nohup python3 run_tests.py &        # keeps running after you log out
echo $?                             # exit code of the last command
```

- **Exit codes:** end your scripts with `sys.exit(0)` on success and a non-zero value on failure. Cron, CI servers and shell scripts use this to decide whether the run failed.
- **Scheduling:** `crontab -e` and add `0 2 * * * /usr/bin/python3 /opt/tests/nightly.py >> /var/log/nightly.log 2>&1` (runs every day at 02:00). Windows equivalent: Task Scheduler.
- **Paths:** use `pathlib` and `Path(__file__)`; never hard-code `C:\...`.
- **Windows names:** on Windows you usually run `python`; `python3` may open the Microsoft Store stub.

---

## 12. Virtual environments basics

A **virtual environment (venv)** is a private folder containing its own Python interpreter link and installed packages. Each project gets its own, so package versions do not clash between projects, and the setup can be recreated anywhere.

| Step | Linux / macOS / WSL | Windows PowerShell | Windows cmd | Git Bash (Windows) |
|------|--------------------|--------------------|-------------|--------------------|
| Create | `python3 -m venv .venv` | `python -m venv .venv` | `python -m venv .venv` | `python -m venv .venv` |
| Activate | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` | `.venv\Scripts\activate.bat` | `source .venv/Scripts/activate` |
| Verify | `which python` | `where python` / `Get-Command python` | `where python` | `which python` |
| Deactivate | `deactivate` | `deactivate` | `deactivate` | `deactivate` |

After activation, the prompt shows `(.venv)` and `pip install` goes into the venv.

```bash
pip install pyyaml pytest
pip freeze > requirements.txt       # save exact versions
pip install -r requirements.txt     # recreate on another machine / CI agent
pip list                            # what is installed?
```

Example `requirements.txt`:

```
pyyaml==6.0.3
pytest>=8.0
pywinauto==0.6.9 ; sys_platform == "win32"    # only installed on Windows
```

Tips:
- Commit `requirements.txt`, **never** commit `.venv/` (add it to `.gitignore`).
- PowerShell blocks `Activate.ps1`? Run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- Ubuntu/Debian may need `sudo apt install python3-venv`.
- Linux uses `bin/`, Windows uses `Scripts/` - the most common confusion.

---

## 13. Executing Linux commands using Python

### 13.1 subprocess.run

```python
import subprocess

result = subprocess.run(
    ["ls", "-l", "/tmp"],     # command + arguments as a LIST
    capture_output=True,      # collect stdout and stderr
    text=True,                # decode bytes to str
    timeout=30,               # never wait forever
)
result.returncode   # 0 = success
result.stdout       # normal output (str)
result.stderr       # error output (str)
```

Other useful arguments: `cwd="some/folder"` (run in a folder), `env={**os.environ, "TEST_ENV": "qa"}` (extra environment variables), `check=True` (raise on non-zero exit), `input="text"` (send to stdin).

`subprocess.run` **waits** for the command to finish. `subprocess.Popen` starts a process and returns immediately - used on Day 2 for GUI apps such as `calc.exe`, and for long-running processes.

### 13.2 List form, shlex and shell=True

- **List form** `["grep", "-i", "error", "app.log"]` - no shell involved, spaces inside arguments are safe, no shell injection. Preferred.
- **`shlex.split(string)`** converts a command line into that list correctly, respecting quotes: `shlex.split("grep -i 'error code' log.txt")` -> `['grep', '-i', 'error code', 'log.txt']`. `str.split()` would break the quoted part.
- **`shlex.quote(value)`** safely quotes a value if you must build a shell string.
- **`shell=True`** runs the string through the shell (`/bin/sh` or `cmd.exe`). Needed only for shell built-ins (Windows `dir`, `echo`), pipes (`|`), wildcards (`*.log`) and redirection. Never combine `shell=True` with untrusted input: `f"ls {name}"` with `name = "x; rm -rf ~"` is a disaster.

### 13.3 Cross-platform considerations

```python
import platform, shutil, sys

if platform.system() == "Windows":           # "Windows", "Linux", "Darwin"
    result = subprocess.run('dir /b', shell=True, capture_output=True, text=True)
else:
    result = subprocess.run(["ls", "-1"], capture_output=True, text=True)

shutil.which("grep")     # full path, or None if not installed
sys.executable           # the Python running now - exists on every OS
```

| Area | Windows | Linux | Portable approach |
|------|---------|-------|-------------------|
| List files | `dir` (built-in, needs shell) | `ls` | `Path.iterdir()` |
| Search text | `findstr` | `grep` | read file in Python |
| Copy | `copy`/`xcopy` | `cp` | `shutil.copy2` / `copytree` |
| Processes | `tasklist` | `ps`, `pgrep` | subprocess with OS check |
| Python | `python` | `python3` | `sys.executable` |
| Paths | `\` | `/` | `pathlib.Path` |
| Line endings | `\r\n` | `\n` | `str.splitlines()` |

Often the best cross-platform solution is to **not shell out at all** and use Python's `shutil`, `pathlib` and `os` modules.

**Demo:** `examples/07_subprocess_linux_commands.py`

---

## 14. Automating CLI-based tools

Many products ship a command-line interface, and testers also drive tools like `git`, `docker`, database clients, installers and the application's own CLI. The pattern:

1. Build the command (list form) with the arguments of the test case.
2. Run it with a timeout.
3. Check the **exit code**, then **stdout/stderr**.
4. Parse the output and assert.
5. Record the result.

```python
r = subprocess.run([sys.executable, "--version"], capture_output=True, text=True, timeout=10)
assert r.returncode == 0
assert r.stdout.startswith("Python 3")
```

Parsing text output:

```python
status = {}
for line in r.stdout.splitlines()[1:]:     # skip header
    name, state = line.split()
    status[name] = state
assert status["db"] == "RUNNING"
```

If the tool can print JSON (`--json`, `--output json`, `--format json`), use it and parse with `json.loads(r.stdout)` - much more robust than splitting text columns.

Remember: some tools use exit codes with special meanings - `grep` returns 1 for "no match", `diff` returns 1 for "files differ". Read the tool's documentation before treating every non-zero code as a crash.

---

## 15. Handling command outputs and errors

| Situation | What Python does | How to handle |
|-----------|------------------|---------------|
| Tool ran but failed | `returncode != 0`, message in `stderr` | check `result.returncode`, log `result.stderr` |
| Same, with `check=True` | raises `subprocess.CalledProcessError` (`e.returncode`, `e.stdout`, `e.stderr`) | `try/except CalledProcessError` |
| Tool hangs | with `timeout=N`: raises `subprocess.TimeoutExpired` and kills the process | always pass a timeout |
| Tool not installed / not on PATH | raises `FileNotFoundError` | `shutil.which()` first, or catch it |
| File not executable | raises `PermissionError` | `chmod +x`, or catch it |
| Output as bytes | `stdout` is `b'...'` without `text=True` | pass `text=True` or `.decode()` |

```python
try:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=True)
    print(r.stdout)
except subprocess.CalledProcessError as e:
    print(f"FAILED rc={e.returncode}: {e.stderr.strip()}")
except subprocess.TimeoutExpired as e:
    print(f"HUNG > {e.timeout}s")
except FileNotFoundError:
    print(f"Not installed: {cmd[0]}")
```

A reusable helper that never raises (you build it in Lab 2):

```python
def run_command(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"ok": r.returncode == 0, "returncode": r.returncode,
                "stdout": r.stdout.strip(), "stderr": r.stderr.strip(), "error": ""}
    except subprocess.TimeoutExpired:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": "",
                "error": f"timeout after {timeout}s"}
    except FileNotFoundError:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": "",
                "error": "command not found"}
```

**Demo:** `examples/08_command_output_errors.py`

---

## 16. Configuration-driven execution using JSON/YAML

Instead of hard-coding which commands to run and what to expect, describe them in a config file. Testers can then add checks without touching Python.

```yaml
# examples/config/commands.yaml (excerpt)
settings:
  default_timeout: 15
checks:
  - name: Python is installed
    command: "{python} --version"        # {python} -> sys.executable
    expect_stdout_contains: "Python 3"
    tags: [smoke]
  - name: Tool reports a controlled failure
    command: ["{python}", "-c", "import sys; sys.stderr.write('invalid license'); sys.exit(4)"]
    expected_returncode: 4
    expect_stderr_contains: "invalid license"
  - name: List directory (Linux)
    command: "ls -la"
    os: linux                             # skipped on Windows
```

The runner (`examples/09_config_driven_runner.py`):

1. loads YAML or JSON (chosen by file extension),
2. filters by OS and `--tag`,
3. runs each command with a timeout,
4. compares return code, stdout and stderr with the expectations,
5. prints PASS/FAIL/SKIP, writes a JSON report and exits 0/1.

```
python 09_config_driven_runner.py
python 09_config_driven_runner.py --tag smoke
python 09_config_driven_runner.py --config config/commands.json
```

The same idea powers real tools: CI pipelines (YAML), Ansible playbooks (YAML), and test frameworks that read suites from files. Lab 4 extends it into a full configuration CLI with `show/get/set/validate/run` sub-commands.

---

## 17. Automating system-level tasks

| Task | Python | Linux shell equivalent |
|------|--------|------------------------|
| Disk space | `shutil.disk_usage(path)` -> total, used, free | `df -h` |
| Folder size | `sum(f.stat().st_size for f in p.rglob("*") if f.is_file())` | `du -sh folder` |
| Old files | `f.stat().st_mtime < time.time() - days*86400` | `find . -mtime +7` |
| Archive | `shutil.make_archive(base, "zip" or "gztar", root_dir)` | `tar -czf a.tar.gz dir` |
| Delete | `Path.unlink()`, `shutil.rmtree()` | `rm`, `rm -r` |
| Backup | `shutil.copytree(src, dst)`, `shutil.copy2` | `cp -r`, `rsync -a` |
| Process running? | `tasklist /FI "IMAGENAME eq x.exe"` / `pgrep -x x` | `ps aux \| grep x`, `pgrep` |
| Service active? | `subprocess.run(["systemctl", "is-active", "ssh"])` rc 0 | `systemctl status ssh` |

**Safety rules for scripts that delete things:**
1. Offer `--dry-run` and use it first.
2. Check the target is inside an allowed folder before deleting (`assert_in_sandbox`).
3. Log every deleted file.
4. Archive before deleting when logs may be needed for bug reports.

**Demo:** `examples/10_system_tasks.py` (disk report, archive old logs, cleanup files older than N days, folder backup with verification, process check - all inside `examples/sandbox/system_tasks/`).

---

## 18. Common mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Opening CSV without `newline=""` | blank rows in Excel on Windows | `open(f, "w", newline="", encoding="utf-8")` |
| Parsing CSV with `split(",")` | broken rows when a value contains a comma | use `csv` module |
| Forgetting CSV values are strings | `"2" + "3" == "23"`, `bool("False") is True` | convert with `int()`, `float()`, explicit checks |
| Opening results file with `"w"` inside a loop | only the last row survives | open once before the loop, or use `"a"` |
| Single quotes / trailing commas in JSON | `JSONDecodeError` | double quotes, no trailing commas |
| `yaml.load()` without safe loader | security risk | `yaml.safe_load()` |
| Tabs or mixed indentation in YAML | `YAMLError` | spaces only |
| Unquoted `yes`, `NO`, `01234`, `1.10` in YAML | wrong types | quote them |
| Password in config/code | leaked in git history | env vars / secret store |
| Relative paths depending on the current folder | `FileNotFoundError` when run from elsewhere | `Path(__file__).resolve().parent` |
| `rm -rf` with a wrong/empty variable | deleted the wrong files | double-check, `set -u`, sandbox checks, `--dry-run` |
| Expecting `chmod` to work in Git Bash | permissions do not change | use WSL / Linux |
| Script saved with CRLF endings | `python3\r: No such file` | save as LF |
| Activating venv with `bin` on Windows | "not found" | Windows uses `Scripts` |
| Command as a single string without `shell=True` | `FileNotFoundError` | pass a list or `shlex.split()` |
| `shell=True` with user input | shell injection | list form |
| No `timeout` | suite hangs forever | always pass `timeout=` |
| Treating every non-zero code as crash | false failures (`grep` = 1) | know the tool's exit codes |
| Ignoring `stderr` | no clue why a command failed | log `stderr` in reports |
| `dir` without `shell=True` | `FileNotFoundError` | `dir` is a cmd built-in |

---

## 19. Questions and answers

**Q1. What is the difference between `csv.reader` and `csv.DictReader`?**
`csv.reader` returns each row as a list (access by index). `csv.DictReader` returns each row as a dictionary keyed by the header row (access by column name), which is more readable and does not break when columns are reordered.

**Q2. Why do we pass `newline=""` when opening CSV files?**
The csv module manages line endings itself. Without `newline=""`, Windows translates `\n` again, producing `\r\r\n` and blank rows between records.

**Q3. What is the difference between `json.load` and `json.loads`?**
`json.load` reads from a file object; `json.loads` parses a string. Likewise `json.dump` writes to a file and `json.dumps` returns a string.

**Q4. Why use `yaml.safe_load` instead of `yaml.load`?**
`yaml.load` with the full/unsafe loader can instantiate arbitrary Python objects described in the file, which can execute code. `safe_load` only builds basic types (dict, list, str, numbers, bool, None).

**Q5. When would you choose CSV, JSON or YAML?**
CSV for flat tabular test data edited in spreadsheets; JSON for nested, typed data exchanged with tools and APIs; YAML for human-edited configuration that benefits from comments and readability.

**Q6. How do you manage different environments (dev/qa/prod) in an automation framework?**
One config file per environment with the same keys, selected at run time via a CLI option or an environment variable (`TEST_ENV`), with environment-variable overrides for individual values and secrets injected from the environment or a vault.

**Q7. How do you keep secrets out of your test code?**
Never hard-code them. Store only the variable name in config, read the value from environment variables (set locally or by CI secret variables) or a secrets vault, keep `.env` files in `.gitignore`, and mask secrets in logs.

**Q8. What is data-driven testing and what are its benefits?**
Separating test logic from test data so one script runs against many data rows. Benefits: new cases without code changes, non-programmers can add data, better coverage of boundaries, less duplicated code.

**Q9. How did you design the data-driven Calculator test so it can run without a GUI?**
By separating layers: a data loader, a driver interface (`calculate()`), a test runner and a report writer. A `MockCalculator` implements the same interface in pure Python, selected with `--dry-run`, so the data and reporting logic can be validated anywhere, including headless CI.

**Q10. Explain the permission string `-rwxr-x---` and its octal value.**
A regular file; owner has read/write/execute (7), group has read/execute (5), others have nothing (0): **750**.

**Q11. What does `chmod +x script.py` do and why is a shebang needed?**
It adds execute permission. When you run `./script.py`, the kernel reads the first line (`#!/usr/bin/env python3`) to know which interpreter to start; without it, the shell does not know the file is a Python script.

**Q12. What is a virtual environment and how do you activate it on Linux and Windows?**
An isolated Python environment with its own packages. Create with `python -m venv .venv`; activate with `source .venv/bin/activate` on Linux/macOS, `.venv\Scripts\Activate.ps1` in PowerShell, or `.venv\Scripts\activate.bat` in cmd. `requirements.txt` records the packages to reinstall with `pip install -r`.

**Q13. What is the difference between `subprocess.run` and `subprocess.Popen`?**
`run` starts a command, waits for it to finish and returns a `CompletedProcess` with returncode/stdout/stderr. `Popen` starts the process and returns immediately, giving you control over a still-running process - used for GUI apps and long-running or interactive processes.

**Q14. Why is `shell=True` risky, and when is it needed?**
It passes the command through a shell, so special characters in untrusted input can inject extra commands. It is needed only for shell features: built-ins (`dir`), pipes, wildcards, redirection. Prefer the list form.

**Q15. How do you handle a command that might hang, fail, or not exist?**
Pass `timeout=` and catch `subprocess.TimeoutExpired`; check `returncode` (or use `check=True` and catch `CalledProcessError`) and log `stderr`; catch `FileNotFoundError` (or check `shutil.which()` first) for missing tools.

**Q16. How would you make a Python automation script work on both Windows and Linux?**
Use `pathlib` for paths, `sys.executable` for Python, `platform.system()` to choose OS-specific commands, `shutil.which()` to check tool availability, `splitlines()` for output, and prefer pure-Python modules (`shutil`, `os`) over shell commands.

**Q17. How would you find and delete log files older than 7 days on Linux, and in Python?**
Shell: `find /path -name "*.log" -mtime +7` (preview), then add `-delete`. Python: loop over `Path(...).glob("*.log")`, compare `stat().st_mtime` with `time.time() - 7*86400`, and `unlink()` - with a dry-run option and a check that the path is inside the allowed folder.

**Q18. What is the meaning of exit code 0, and why should test scripts return non-zero on failure?**
0 means success; any other value means failure (tool-specific). CI servers, cron and shell scripts use the exit code to decide whether a step failed, so a test script must `sys.exit(1)` when tests fail.

---

## 20. Day 3 summary

- **Files:** use `with`, `encoding="utf-8"`, `pathlib`, and paths based on `__file__`.
- **CSV:** `csv.DictReader` / `DictWriter`, `newline=""`, convert types.
- **JSON:** `load/dump` for files, `loads/dumps` for strings, strict syntax, `JSONDecodeError`.
- **YAML:** `pip install pyyaml`, `yaml.safe_load`, spaces only, quote ambiguous values.
- **Configs:** one file per environment, env var overrides, secrets from the environment, masked in output.
- **Data-driven automation:** one script, many rows; layered design with a mock driver and `--dry-run`; PASS/FAIL/ERROR results in CSV; exit code for CI.
- **Linux:** single `/` tree, case-sensitive, `ls cd pwd cp mv rm cat grep find`, redirection and pipes, exit codes.
- **Permissions:** `rwx` for owner/group/others, octal 755/644/600, `chmod`, shebang + `chmod +x` to run `./script.py`, LF line endings.
- **venv:** `python -m venv .venv`, `bin` vs `Scripts`, `requirements.txt`.
- **CLI automation:** `subprocess.run([...], capture_output=True, text=True, timeout=...)`, `shlex`, cross-platform checks, handle `returncode`, `stderr`, `CalledProcessError`, `TimeoutExpired`, `FileNotFoundError`.
- **Config-driven execution:** commands and expectations in YAML/JSON, runner reports PASS/FAIL.
- **System tasks:** `shutil.disk_usage`, `make_archive`, `copytree`, age-based cleanup with dry-run and sandbox checks, process checks.

Next: Day 4 builds on today's data-driven and config-driven design with test frameworks, reporting and CI.
