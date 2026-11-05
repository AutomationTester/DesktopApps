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

# Day 3
## File Handling, Configuration Management, Linux Basics & CLI Automation

**Python Desktop Application Automation Testing**
5-Day Corporate Training

<!-- Trainer notes: Welcome back. Quick recap question to warm up: "Yesterday we launched Notepad with pywinauto and ran commands with subprocess - where did the test inputs come from?" (Answer: hard-coded in the script.) Today we fix that: data and configuration move OUT of the code, and we learn the Linux skills needed to run automation on servers/CI agents. -->

---

## Where we are in the course

| Day | Topic |
|-----|-------|
| 1 | Python & OOP foundations |
| 2 | Desktop automation (pywinauto) + CLI (argparse, subprocess) |
| **3** | **File handling, configs, Linux basics, CLI automation** |
| 4 | Framework design, PyTest, logging, AI basics |
| 5 | Git, GitHub Actions CI/CD, best practices, mini project |

<!-- Trainer notes: Position today as the "glue" day - the Day 4 framework depends on reading test data and configs, and Day 5 CI runs the tests on Linux build agents. -->

---

## Learning objectives

By the end of today you will be able to:

- Read and write **CSV**, **JSON** and **YAML** files from Python
- Manage **dev / qa / prod** configs, environment variables and secrets
- Build a **data-driven** desktop test (Windows Calculator)
- Navigate Linux, use `ls cd pwd cp mv rm cat grep find`, set **permissions**
- Run Python scripts on Linux and use **virtual environments**
- Run commands from Python, handle **output and errors**, drive runs from **config files**

<!-- Trainer notes: Read these out, then say: "Each objective has a lab. By 5 pm you will have four small tools you can reuse at work." -->

---

## Agenda (8 hours)

| Time | Session |
|------|---------|
| 09:00 - 09:15 | Recap Day 2, objectives |
| 09:15 - 10:30 | CSV and JSON file handling (demos 01-03) |
| 10:30 - 10:45 | **Break** |
| 10:45 - 11:30 | YAML, environment configs, secrets (demos 04-05) |
| 11:30 - 12:30 | Data-driven desktop automation + **Lab 1** |
| 12:30 - 13:15 | **Lunch** |
| 13:15 - 14:15 | Linux basics: filesystem, commands, permissions + **Lab 5 / 6** |
| 14:15 - 14:45 | Running Python on Linux, virtual environments |
| 14:45 - 15:00 | **Break** |
| 15:00 - 16:00 | Automating CLI tools, outputs & errors, config-driven runs (demos 07-09) + **Lab 2** |
| 16:00 - 16:50 | System tasks + CLI config automation: **Lab 3 / Lab 4** |
| 16:50 - 17:00 | Recap, quiz, Q&A |

<!-- Trainer notes: The day is dense. If the group is slow, move Lab 4 to homework and do Lab 3 only. Labs 7 and 8 in the lab guide are extras/homework. Quiz (03_Quiz.md) can be done in the last 10 min or as homework. -->

---

## Why files and configs matter in testing

- Hard-coded inputs -> change code for every new test case
- Business analysts give you **Excel/CSV** test data
- Tools and APIs speak **JSON**
- CI systems and frameworks use **YAML** configs
- Same test must run on **dev, qa, prod** -> different URLs, users, timeouts

> Rule of thumb: **code = how to test**, **files = what to test and where**

<!-- Trainer notes: Ask: "In your current manual testing, where do test cases live?" (Excel, TestRail, Jira...). Those tables become CSV files. Make the point that a tester who can maintain data files without touching code is very valuable. -->

---

# Part 1
## File Handling & Configuration Management

<!-- Trainer notes: Section divider. ~2.5 hours including Lab 1. -->

---

## File handling refresher

```python
from pathlib import Path

HERE = Path(__file__).resolve().parent      # folder of THIS script
data_file = HERE / "data" / "users.csv"     # works on Windows and Linux

with open(data_file, "r", encoding="utf-8") as f:   # auto-closes
    text = f.read()
```

| Mode | Meaning |
|------|---------|
| `"r"` | read (default) |
| `"w"` | write - **overwrites** |
| `"a"` | append |
| `"x"` | create, fail if exists |

<!-- Trainer notes: Emphasise three habits: (1) always use `with`, (2) always pass encoding="utf-8" (Windows default is cp1252), (3) build paths from __file__ so scripts work from any working directory - the #1 "works on my machine" issue in labs. -->

---

## CSV - Comma-Separated Values

```
test_id,username,password,expected
TC001,admin,admin123,success
TC002,admin,wrong,failure
```

- Plain text table, first row is usually the **header**
- Opens in Excel -> ideal for testers and BAs
- Only strings - **no types, no nesting**
- Values containing commas are wrapped in quotes: `"o'brien, john"`

<!-- Trainer notes: Show a CSV in Notepad and in Excel side by side. Point out that Excel may silently change data (leading zeros in 01234, long numbers become 1.2E+10, dates reformatted). Recommend editing CSV in VS Code for test data. -->

---

## Reading CSV with `csv.reader`

```python
import csv

with open("login_tests.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)           # skip / keep the header
    for row in reader:              # row is a LIST of strings
        test_id, user, pwd, expected = row
        print(test_id, user)
```

- `newline=""` -> required by the csv module (no blank lines on Windows)
- Never use `line.split(",")` - breaks on quoted commas

<!-- Trainer notes: Demo examples/01_csv_read_write.py. Highlight the "o'brien, john" row being handled correctly. Common question: "Why newline=''?" - the csv module handles line endings itself; without it you get \r\r\n on Windows and blank rows in Excel. -->

---

## Writing CSV with `csv.writer`

```python
rows = [
    ["test_id", "username", "password", "expected"],
    ["TC001", "admin", "admin123", "success"],
]
with open("login_tests.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)          # many rows
    writer.writerow(["TC002", "admin", "x", "failure"])   # one row

# Append later without rewriting:
with open("login_tests.csv", "a", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(["TC003", "guest", "guest", "success"])
```

<!-- Trainer notes: Ask what happens if you use "w" instead of "a" for the append - file is wiped. Classic bug when writing results in a loop: opening with "w" inside the loop keeps only the last row. -->

---

## Everything in CSV is a string

```python
for test_id, duration, retries in reader:
    total += duration          # BUG: "1.25" + "3.50" -> TypeError / concat
    total += float(duration)   # correct
    if int(retries) > 1: ...
```

- Convert explicitly: `int()`, `float()`, `value == "true"`
- Strip spaces: `value.strip()` (Excel users add them)
- Empty cell -> `""` not `None`

<!-- Trainer notes: Run the type_conversion_demo part of example 01. Ask: "What does bool('False') return?" - True! Any non-empty string is truthy. Convert with value.lower() == "true". -->

---

## `csv.DictReader` - rows as dictionaries

```python
with open("login_testdata.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)            # ['test_id', 'username', ...]
    for row in reader:
        print(row["test_id"], row["username"])
```

- Access by **column name**, not position
- Column order can change without breaking your code
- Validate required columns early:

```python
missing = {"test_id", "expected"} - set(reader.fieldnames)
if missing: raise ValueError(f"Missing columns: {missing}")
```

<!-- Trainer notes: Demo examples/02_csv_dictreader_testdata.py. This is the pattern for test data - recommend DictReader by default. Ask: "What if a BA renames 'username' to 'user'?" -> fail fast with a clear error rather than a KeyError deep in the test. -->

---

## `csv.DictWriter` - writing result reports

```python
fields = ["test_id", "expected", "actual", "status"]
with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerow({"test_id": "TC001", "expected": "success",
                     "actual": "success", "status": "PASS"})
```

- Keys must match `fieldnames` (extra key -> `ValueError`)
- Use `extrasaction="ignore"` to drop extra keys

<!-- Trainer notes: Show sandbox/login_results.csv produced by example 02 and open it in Excel. Managers love a results CSV they can filter by status. -->

---

## JSON - JavaScript Object Notation

```json
{
  "suite_name": "Notepad Smoke Tests",
  "retry_on_failure": true,
  "max_retries": 2,
  "owner": null,
  "tests": [
    {"id": "NP-01", "action": "type_text", "data": "Hello"}
  ]
}
```

- Nested objects `{}` and arrays `[]`
- Real types: string, number, true/false, null
- Language of REST APIs and many CLI tools (`--output json`)

<!-- Trainer notes: Relate to Day 1 - JSON object = Python dict, JSON array = Python list. Mention that many CLI tools (az, kubectl, docker inspect, gh) can print JSON, which is much easier to parse than text tables. -->

---

## JSON <-> Python types

| JSON | Python |
|------|--------|
| object `{}` | `dict` |
| array `[]` | `list` |
| string `"a"` | `str` |
| number `1`, `2.5` | `int`, `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

JSON rules: **double quotes only**, **no trailing commas**, **no comments**

<!-- Trainer notes: The three rules cause 90% of "invalid JSON" errors. Example 03 deliberately writes a broken file to show json.JSONDecodeError with line/column. -->

---

## Reading and writing JSON

```python
import json

with open("test_suite.json", encoding="utf-8") as f:
    suite = json.load(f)                 # file -> Python
enabled = [t["id"] for t in suite["tests"] if t["enabled"]]
timeout = suite.get("timeout", 30)       # optional key with default

suite["max_retries"] = 3
with open("test_suite.json", "w", encoding="utf-8") as f:
    json.dump(suite, f, indent=2)        # Python -> file (pretty)

data = json.loads('{"status": "ok"}')   # string -> Python
text = json.dumps(data)                  # Python -> string
```

`load/dump` = files, `loads/dumps` = **s**trings

<!-- Trainer notes: Demo examples/03_json_read_write.py. Common question: "Can I append to a JSON file?" - Not really; read, modify, write the whole file. For logs of many records, use JSON Lines (one JSON object per line) or CSV. -->

---

## Handling bad JSON

```python
try:
    with open("broken.json", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e.msg} at line {e.lineno}, col {e.colno}")
except FileNotFoundError:
    print("File missing")
```

- Fail **early** with a clear message
- Tip: VS Code highlights JSON syntax errors

<!-- Trainer notes: Show the output of broken_json_demo in example 03. Link to testing: a malformed data file should fail the setup step, not produce 50 confusing test failures. -->

---

## YAML - for humans

```yaml
# Test run configuration (comments allowed!)
project: Calculator Automation
app:
  path: calc.exe
  launch_timeout: 10
headless: false
test_groups:
  - smoke
  - regression
```

- Indentation (spaces!) defines structure
- Superset of JSON, much more readable
- Used by GitHub Actions, Azure Pipelines, Docker Compose, Kubernetes, Ansible

<!-- Trainer notes: Show a real GitHub Actions workflow if you have one. Point out the trainees will see YAML again on Day 4 (framework config) and Day 5 (GitHub Actions CI). -->

---

## YAML in Python (PyYAML)

```python
# pip install pyyaml
import yaml

with open("config.yaml", encoding="utf-8") as f:
    config = yaml.safe_load(f)            # -> dict
print(config["app"]["launch_timeout"])    # 10 (int)

with open("out.yaml", "w", encoding="utf-8") as f:
    yaml.safe_dump(config, f, sort_keys=False)
```

- Always **`safe_load`** - plain `yaml.load` can execute arbitrary objects
- Syntax errors raise `yaml.YAMLError`

<!-- Trainer notes: Demo examples/04_yaml_config.py. Security point: yaml.load with the unsafe Loader can construct arbitrary Python objects - never use it on files you did not write. Install name is pyyaml, import name is yaml - a frequent confusion. -->

---

## YAML gotchas

```yaml
answer: yes        # -> True   (yes/no/on/off are booleans!)
country: NO        # -> False  (the "Norway problem")
zip_code: 01234    # -> 668    (octal int!)
version: 1.10      # -> 1.1    (float)
safe_zip: "01234"  # -> "01234"  quote it!
empty:             # -> None
```

- Use **spaces**, never tabs
- When in doubt, **quote strings**

<!-- Trainer notes: Run type_gotchas() from example 04 live - the 668 result always gets a reaction. Advice: quote versions, IDs, zip codes, phone numbers. -->

---

## CSV vs JSON vs YAML

| | CSV | JSON | YAML |
|--|-----|------|------|
| Best for | Tabular test data | Nested data, API/tool I/O | Configuration |
| Types | strings only | str, num, bool, null | + dates, more |
| Nesting | no | yes | yes |
| Comments | no | no | **yes** |
| Edited by | BAs in Excel | tools / devs | engineers |
| Python | `csv` (built-in) | `json` (built-in) | `yaml` (pip install pyyaml) |

<!-- Trainer notes: Common question: "When would you choose YAML over JSON?" - human-edited config with comments; JSON for machine-to-machine data. -->

---

## Managing test data

- Keep data **outside** code: `data/` folder, one file per feature
- Put data files under **version control** (git) with the tests
- Include **positive, negative and boundary** rows
- Give every row a **test_id**
- Validate files before running (required columns, types)
- Never put **real customer data** or passwords in test data

```
project/
  tests/           code
  data/            calculator_tests.csv, login.json
  config/          dev.yaml, qa.yaml, prod.yaml
  reports/         generated results (not in git)
```

<!-- Trainer notes: Discuss data privacy (GDPR) - use synthetic data. Ask the group for examples of boundary values for a Calculator (0, negative, very large numbers, decimals, divide by zero). -->

---

## Environment configs: dev / qa / prod

```yaml
# config/qa.yaml                      # config/dev.yaml
env_name: qa                          env_name: dev
base_url: https://qa.example.internal base_url: http://localhost:8080
db:                                   db:
  host: qa-db.example.internal          host: localhost
  password_env_var: APP_DB_PASSWORD     password_env_var: APP_DB_PASSWORD
retries: 2                            retries: 0
```

- **Same keys**, different values
- Choose at run time: `--env qa` or `TEST_ENV=qa`

<!-- Trainer notes: Open examples/config/dev.yaml, qa.yaml, prod.yaml side by side in VS Code (split view). Point out prod has read_only: true - automation on prod is typically limited to safe smoke checks. -->

---

## Environment variables

```python
import os
env = os.environ.get("TEST_ENV", "dev")     # default if not set
retries = int(os.environ.get("APP_RETRIES", "0"))   # always strings!
```

| Shell | Set a variable |
|-------|----------------|
| Linux / Git Bash | `export TEST_ENV=qa` |
| One command only | `TEST_ENV=qa python run.py` |
| PowerShell | `$env:TEST_ENV = "qa"` |
| cmd.exe | `set TEST_ENV=qa` |

Priority: **CLI arg > env var > config file > default**

<!-- Trainer notes: Demo: python 05_env_configs.py --env qa, then in Git Bash TEST_ENV=prod python 05_env_configs.py. Common question: "Why did my variable disappear?" - env vars set in one terminal do not affect other terminals; os.environ changes inside Python only affect that process and its children. -->

---

## Secrets are NOT in code

```python
# BAD - ends up in git history forever
DB_PASSWORD = "Sup3rS3cret!"

# GOOD - config names the variable, value comes from the environment
secret_var = config["db"]["password_env_var"]     # "APP_DB_PASSWORD"
password = os.environ.get(secret_var)
if not password:
    raise RuntimeError(f"Set {secret_var} before running")
```

- Local: env vars or a `.env` file listed in **`.gitignore`**
- CI: pipeline **secret variables** (GitHub/Azure/Jenkins credentials)
- Enterprise: vaults (Azure Key Vault, HashiCorp Vault, AWS Secrets Manager)
- **Mask** secrets in logs and reports

<!-- Trainer notes: Demo python 05_env_configs.py --env prod --demo-overrides and point to the masked password. Story: leaked credentials in public repos are found by bots within minutes. Mention python-dotenv as an optional library but we stay with the standard library today. -->

---

## Demo: environment-aware config loader

```python
def load_config(env_name):
    with open(CONFIG_DIR / f"{env_name}.yaml", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if "APP_BASE_URL" in os.environ:                 # override
        config["base_url"] = os.environ["APP_BASE_URL"]
    secret_var = config["db"]["password_env_var"]    # secret
    config["db"]["password"] = os.environ.get(secret_var)
    return config
```

```
python 05_env_configs.py --env qa
python 05_env_configs.py --env prod --demo-overrides
```

<!-- Trainer notes: Walk through the full file examples/05_env_configs.py. Ask: "Where would you add a new environment 'uat'?" - one new YAML file and add it to VALID_ENVS. No logic changes. -->

---

## Data-driven testing (DDT)

```
 calculator_tests.csv          one test script           results.csv
 +-------------------+       +----------------+       +----------------+
 | 7 + 8 = 15        |  -->  | for row in data|  -->  | CALC-001 PASS  |
 | 9 / 4 = 2.25      |       |   automate     |       | CALC-004 PASS  |
 | 8 / 0 = error msg |       |   compare      |       | CALC-009 FAIL  |
 +-------------------+       +----------------+       +----------------+
```

- **One** script, **many** data rows
- New test case = new row, no code change
- Same idea as pytest `@pytest.mark.parametrize` (Day 4)

<!-- Trainer notes: Ask how many manual test cases for Calculator they could write in 5 minutes - each becomes one CSV row. Mention the same approach works for login screens, forms, file converters etc. -->

---

## Data file for Calculator

```
test_id,num1,operator,num2,expected,description
CALC-001,7,+,8,15,simple addition
CALC-004,9,/,4,2.25,division with decimal result
CALC-006,5,-,9,-4,negative result
CALC-007,8,/,0,Cannot divide by zero,divide by zero error message
CALC-009,2,+,2,5,DELIBERATELY WRONG expected value - should FAIL
```

Same data as JSON: `examples/data/calculator_tests.json`

<!-- Trainer notes: Open examples/data/calculator_tests.csv. Point out the deliberate FAIL row - always prove your test CAN fail (a test that never fails is worthless). -->

---

## Calculator automation recap (pywinauto)

```python
import subprocess
from pywinauto import Desktop

subprocess.Popen("calc.exe")
win = Desktop(backend="uia").window(title="Calculator")
win.wait("visible", timeout=10)

def press(auto_id):
    win.child_window(auto_id=auto_id, control_type="Button").invoke()

press("clearButton"); press("num7Button"); press("plusButton")
press("num8Button"); press("equalButton")
text = win.child_window(auto_id="CalculatorResults").window_text()
# "Display is 15"
```

<!-- Trainer notes: This is Day 2 material. Note: on Windows 11 calc.exe is only a launcher (UWP app), so we attach via Desktop(...) rather than the Popen process. Buttons: num0Button..num9Button, plusButton, minusButton, multiplyButton, divideButton, equalButton, clearButton. Display text needs "Display is " and thousands separators removed. -->

---

## Design: separate data, driver, test, report

```python
class MockCalculator:                       # runs anywhere
    def calculate(self, num1, op, num2): ...

class GuiCalculator:                        # real app via pywinauto
    def calculate(self, num1, op, num2): ...

cases   = load_test_cases("data/calculator_tests.csv")   # data layer
results = run_suite(cases, calculator)                  # test layer
write_results(results, "sandbox/calculator_results.csv")# report layer
```

- Same interface -> **polymorphism** (Day 1 OOP)
- `--dry-run` uses the mock: test the data + reporting without the GUI

<!-- Trainer notes: This is the key design lesson of the morning. Benefits: data-file bugs are found in seconds with --dry-run; the GUI part can be swapped (e.g. a different app version) without touching data code; and in CI without a desktop you can still validate data files. -->

---

## Demo: data-driven Calculator

```
python 06_data_driven_calculator.py --dry-run
python 06_data_driven_calculator.py --dry-run --data data/calculator_tests.json
```

```
Loaded 9 test cases from calculator_tests.csv
  CALC-001  7 + 8     expected=15    actual=15    PASS
  CALC-007  8 / 0     expected=Cannot divide by zero ... PASS
  CALC-009  2 + 2     expected=5     actual=4     FAIL
Total=9  PASS=8  FAIL=1  ERROR=0
```

Exit code 1 when anything fails -> CI marks the build red

<!-- Trainer notes: Run in dry-run mode. Only run the real GUI mode on your own presenter machine if appropriate (python 06_data_driven_calculator.py) and ask everyone to watch, not type. Open sandbox/calculator_results.csv afterwards. Common question: "Why compare as floats?" - "15" vs "15.0" should both pass. -->

---

## Lab 1: Data-driven automation (45 min)

`hands_on/starter/lab1_data_driven_calculator.py`

1. `load_rows()` - CSV **and** JSON
2. `validate_row()` - reject bad operators / numbers
3. `is_match()` - numeric or text comparison
4. `run_tests()` - PASS / FAIL / ERROR per row
5. `write_reports()` - `lab1_results.csv` + `lab1_summary.json`

Run with `--dry-run`. Expected: **5 PASS, 1 FAIL, 2 ERROR**

<!-- Trainer notes: Walk around; the most common issues are forgetting newline="", comparing "2.5" with "2.50" as strings, and one bad row crashing the whole loop (needs try/except). Early finishers: --priority filter and skip column stretch goals. -->

---

# Part 2
## Linux Basics for Automation Engineers

<!-- Trainer notes: Energy check after lunch. Ask: "Who has used Linux before?" Most CI agents, Docker containers and servers run Linux, so even Windows desktop testers will meet it. -->

---

## Why Linux for automation engineers?

- CI/CD agents (GitHub Actions, Jenkins, GitLab) are mostly **Linux**
- Test servers, Docker containers, cloud VMs -> Linux
- Log files you must analyse live on Linux servers
- Many CLI tools under test are Linux tools

**Where to practise today:** Git Bash (Windows), **WSL** (`wsl --install`), a Linux VM, or a cloud shell (Codespaces / Cloud Shell)

<!-- Trainer notes: Git Bash gives most commands but not a real Linux filesystem or permissions. WSL gives a real Ubuntu. If trainees lack admin rights for WSL, Git Bash is fine for today's labs; mention that permissions behave properly only in WSL/Linux. -->

---

## Linux filesystem structure

```
/                  root of everything (no C:\ drives)
|-- bin, usr/bin   programs (ls, grep, python3)
|-- etc            system configuration files
|-- home/<user>    your files  (~ is a shortcut)   ~ C:\Users\<user>
|-- root           the administrator's home
|-- tmp            temporary files (cleared on reboot)
|-- var/log        log files
|-- opt            optional / third-party software
|-- dev, proc      devices, running processes (virtual)
|-- mnt, media     mounted drives  (WSL: /mnt/c = C:\)
```

<!-- Trainer notes: Compare with Windows: one tree starting at /, forward slashes, case-sensitive names (Report.txt != report.txt). In WSL, show ls /mnt/c/Users. In Git Bash, C:\ appears as /c/. -->

---

## Paths: absolute vs relative

| Symbol | Meaning |
|--------|---------|
| `/` | root (absolute path starts here) |
| `~` | home directory |
| `.` | current directory |
| `..` | parent directory |
| `-` | previous directory (`cd -`) |

- Absolute: `/home/tester/project/data/users.csv`
- Relative: `data/users.csv`, `../logs/app.log`
- **Case-sensitive**, no spaces if you can avoid them

<!-- Trainer notes: Quick exercise: "You are in /home/tester/project/tests. What is ../data/users.csv as an absolute path?" -->

---

## Navigation: `pwd`, `ls`, `cd`

```bash
pwd                 # where am I?  /home/tester
ls                  # list names
ls -l               # long: permissions, owner, size, date
ls -la              # include hidden files (.gitignore, .env)
ls -lh /var/log     # human-readable sizes
cd project/logs     # relative
cd /tmp             # absolute
cd ..               # up one level
cd ~   (or just cd) # home
cd -                # back to previous directory
```

<!-- Trainer notes: Demo live in Git Bash. Tip: Tab completion saves typing and prevents typos; Up arrow recalls history; Ctrl+C cancels; `clear` or Ctrl+L clears the screen. -->

---

## Files: `cp`, `mv`, `rm`, `cat`

```bash
mkdir -p project/data          # create folders (-p = parents)
touch notes.txt                # empty file
cp users.csv users_bak.csv     # copy file
cp -r data data_copy           # copy folder (recursive)
mv users_bak.csv old.csv       # rename
mv old.csv archive/            # move
rm old.csv                     # delete file - NO recycle bin
rm -r data_copy                # delete folder
cat app.log                    # print file
head -n 5 app.log; tail -n 5 app.log; tail -f app.log
```

**Danger:** `rm -rf` deletes without asking. Double-check the path.

<!-- Trainer notes: Story time: rm -rf with an empty variable, e.g. rm -rf $DIR/* when DIR is unset, deletes from root. That's why our scripts use set -u and sandbox checks. tail -f is extremely useful to watch logs while a test runs. -->

---

## Searching: `grep`

```bash
grep "ERROR" app.log            # lines containing ERROR
grep -i "error" app.log         # ignore case
grep -n "ERROR" app.log         # show line numbers
grep -c "ERROR" app.log         # count matching lines
grep -v "DEBUG" app.log         # invert: lines WITHOUT DEBUG
grep -r "TODO" src/             # recursive through a folder
grep -E "ERROR|FATAL" app.log   # regular expression (either word)
cat app.log | grep -i error | wc -l      # pipes
```

Exit code: **0** = found, **1** = not found, **2** = error

<!-- Trainer notes: Testers use grep constantly to check logs after a test run. The exit code matters for automation: a script can do "if grep -q FATAL app.log; then fail". Windows equivalent: findstr. -->

---

## Finding files: `find`

```bash
find . -name "*.log"                 # by name pattern
find /var/log -name "*.gz"
find . -type d                       # only directories
find . -type f -size +10M            # files bigger than 10 MB
find . -name "*.log" -mtime +7       # modified more than 7 days ago
find . -name "*.tmp" -delete         # careful! deletes matches
find . -name "*.py" -exec grep -l "pywinauto" {} \;
```

<!-- Trainer notes: -mtime +7 is the classic log-cleanup filter we'll re-implement in Python in Lab 3. Always run find WITHOUT -delete first to preview. -->

---

<!-- _class: compact -->
## Shell command cheat-sheet

| Command | Purpose | Windows cmd equivalent |
|---------|---------|------------------------|
| `pwd` | current dir | `cd` |
| `ls -l` | list | `dir` |
| `cd` | change dir | `cd` |
| `cp` / `cp -r` | copy | `copy` / `xcopy` |
| `mv` | move/rename | `move` / `ren` |
| `rm` / `rm -r` | delete | `del` / `rmdir /s` |
| `cat` | show file | `type` |
| `grep` | search text | `findstr` |
| `find` | find files | `dir /s` |
| `mkdir -p` | create dirs | `mkdir` |

<!-- Trainer notes: Mention that PowerShell has aliases (ls, cat, cp, rm) but different options. Point to examples/linux_commands_practice.sh which runs all of these with comments: bash linux_commands_practice.sh -->

---

## Redirection and pipes

```bash
echo "INFO start" >  app.log     # write (overwrite)
echo "ERROR fail" >> app.log     # append
python run_tests.py > out.txt 2> err.txt   # stdout / stderr separately
python run_tests.py > all.txt 2>&1         # both into one file
ls -l | grep ".csv"              # pipe output into next command
echo $?                          # exit code of the last command
```

- **stdout** = normal output, **stderr** = errors - same idea as `subprocess`
- `$?` = last exit code (0 = success)

<!-- Trainer notes: This connects directly to the afternoon: result.stdout, result.stderr, result.returncode are the same three things. -->

---

## Demo: `linux_commands_practice.sh`

```bash
cd examples
bash linux_commands_practice.sh       # Git Bash / WSL / Linux
```

- Creates `examples/sandbox/linux_practice/` and runs every command
- Read the comments, then type the commands yourself (**Lab 5**)

<!-- Trainer notes: Run the script, scroll through output section by section. Then start Lab 5 (30 min, step table in Lab_Guide.md). Trainees type the commands themselves - muscle memory matters here. -->

---

## File permissions: `rwx`

```
$ ls -l
-rwxr-xr--  1 tester qa  220 Sep 26 10:00 deploy.sh
drwxr-xr-x  2 tester qa 4096 Sep 26 10:00 logs
|\_/\_/\_/
| |  |  +-- others : r--  read only
| |  +----- group  : r-x  read + execute
| +-------- owner  : rwx  read + write + execute
+---------- type   : - file, d directory, l link
```

| | File | Directory |
|--|------|-----------|
| r | read contents | list names |
| w | modify | create/delete inside |
| x | run as program | `cd` into it |

<!-- Trainer notes: Explain owner/group/others with an office analogy (you, your team, everyone else). Common question: why do directories need x? Without x you cannot cd into or access files inside, even if you can list names. -->

---

<!-- _class: compact -->
## Octal permissions

| rwx | Binary | Octal |
|-----|--------|-------|
| `rwx` | 111 | 7 |
| `rw-` | 110 | 6 |
| `r-x` | 101 | 5 |
| `r--` | 100 | 4 |
| `---` | 000 | 0 |

r = 4, w = 2, x = 1 -> add them per group

- **755** `rwxr-xr-x` scripts, folders
- **644** `rw-r--r--` normal files
- **600** `rw-------` secrets, SSH keys
- **700** `rwx------` private scripts

<!-- Trainer notes: Quick quiz: what is 750? (rwxr-x---). What is rw-rw-r--? (664). Warn against chmod 777 "to make it work" - a security smell auditors flag. -->

---

## `chmod` - changing permissions

```bash
chmod +x run_tests.sh          # add execute for everyone
chmod u+x run_tests.sh         # only owner (u=user, g=group, o=others, a=all)
chmod go-w config.yaml         # remove write from group and others
chmod 755 run_tests.sh         # octal form
chmod 600 secrets.env
chmod -R 755 scripts/          # recursive
ls -l run_tests.sh             # verify
```

- `chown user:group file` changes the owner (needs `sudo`)
- Git Bash on Windows: `chmod` mostly has no effect (NTFS) - use **WSL** to see it

<!-- Trainer notes: Do Lab 6 Part A in WSL if available. If only Git Bash is available, show it on your screen via WSL or a cloud shell. -->

---

## Execution rights & the shebang

```python
#!/usr/bin/env python3
# ^ shebang: first line, tells Linux which interpreter runs this file
print("Hello from Linux")
```

```bash
python3 hello.py        # works without x - python reads the file
./hello.py              # "Permission denied"
chmod +x hello.py
./hello.py              # works: kernel reads the shebang
```

- Use `#!/usr/bin/env python3` (finds python3 on PATH, works in venvs)
- Save with **LF** line endings - CRLF gives `python3\r: not found`

<!-- Trainer notes: The CRLF problem bites everyone who writes scripts on Windows and runs on Linux. VS Code: bottom-right "CRLF" -> click -> "LF". Add a .gitattributes with "*.sh text eol=lf" in real projects. -->

---

## Running Python scripts on Linux

```bash
python3 --version               # 'python' may not exist on Linux
python3 run_tests.py --env qa   # arguments work the same (argparse)
./run_tests.py --env qa         # with shebang + chmod +x
TEST_ENV=qa python3 run_tests.py
python3 run_tests.py > run.log 2>&1 &     # background, output to log
nohup python3 run_tests.py &    # keeps running after logout
echo $?                         # exit code of the script
```

- Scheduling: `crontab -e` -> `0 2 * * * /usr/bin/python3 /opt/tests/nightly.py`
- Windows equivalent: Task Scheduler

<!-- Trainer notes: Emphasise sys.exit(0/1) in scripts so that cron / CI knows whether the run failed. Mention `which python3` to find the interpreter path for cron. -->

---

## Virtual environments - why?

- Project A needs `pywinauto 0.6.8`, project B needs another version
- Installing everything globally -> conflicts, "works on my machine"
- A **venv** = private folder with its own Python + packages
- `requirements.txt` = list of packages to recreate the venv anywhere

```
myproject/
  .venv/              <- never commit to git
  requirements.txt    <- commit this
  tests/
```

<!-- Trainer notes: Analogy: a venv is a separate toolbox per project. CI pipelines always do "python -m venv" + "pip install -r requirements.txt" at the start. -->

---

## venv: Linux vs Windows

| Step | Linux / macOS / WSL | Windows PowerShell |
|------|---------------------|--------------------|
| Create | `python3 -m venv .venv` | `python -m venv .venv` |
| Activate | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |
| (cmd.exe) | | `.venv\Scripts\activate.bat` |
| (Git Bash) | | `source .venv/Scripts/activate` |
| Install | `pip install pyyaml pytest` | same |
| Save | `pip freeze > requirements.txt` | same |
| Restore | `pip install -r requirements.txt` | same |
| Leave | `deactivate` | same |

<!-- Trainer notes: Note bin vs Scripts - the #1 confusion. PowerShell may block Activate.ps1: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned. Ubuntu may need sudo apt install python3-venv. Lab 7 in the guide is an optional hands-on for this. -->

---

## requirements.txt

```
# requirements.txt
pyyaml==6.0.3
pytest>=8.0
pywinauto==0.6.9 ; sys_platform == "win32"
```

- `==` pin exact version (reproducible), `>=` minimum
- Environment marker: install pywinauto only on Windows
- `pip list` / `pip show pyyaml` to inspect
- `.gitignore`: `.venv/`, `__pycache__/`, `.env`, `reports/`

<!-- Trainer notes: The environment marker is a nice trick for cross-platform projects: Linux CI agents skip pywinauto. Versions shown are examples; pin what your project uses (pip freeze shows exact versions). -->

---

# Part 3
## Automating CLI Tools

<!-- Trainer notes: Section divider. Connect to Day 2 subprocess basics - now we go deeper: cross-platform, errors, and config-driven execution. -->

---

## `subprocess.run` recap

```python
import subprocess

result = subprocess.run(
    ["ls", "-l", "/tmp"],      # command as a LIST
    capture_output=True,       # collect stdout/stderr
    text=True,                 # str instead of bytes
    timeout=30,                # never hang forever
)
print(result.returncode)       # 0 = success
print(result.stdout)
print(result.stderr)
```

- `run()` waits for the command; `Popen()` does not (GUI apps, long processes)

<!-- Trainer notes: Day 2 used Popen for calc.exe because we don't want to wait for the app to close. For CLI tools, run() is almost always right. -->

---

## Command as list, `shlex`, and `shell=True`

```python
import shlex
shlex.split("grep -i 'error code' \"app log.txt\"")
# ['grep', '-i', 'error code', 'app log.txt']

subprocess.run(["grep", "-i", "error", "app.log"])     # preferred
subprocess.run("dir", shell=True)                       # Windows built-in
subprocess.run("ls *.log | wc -l", shell=True)          # pipes/wildcards
```

- List form: no shell, no quoting problems, **no injection**
- `shell=True` only for built-ins (`dir`, `echo`), pipes, wildcards
- Never `shell=True` with user input: `f"ls {user_input}"` -> `; rm -rf ~`

<!-- Trainer notes: Demo step 3 of examples/07_subprocess_linux_commands.py showing str.split vs shlex.split. shlex.quote() safely quotes a value if you must build a shell string. -->

---

<!-- _class: compact -->
## Cross-platform considerations

```python
import platform, shutil, sys

if platform.system() == "Windows":          # 'Windows' / 'Linux' / 'Darwin'
    cmd, shell = 'dir /b', True
else:
    cmd, shell = ["ls", "-1"], False

shutil.which("grep")        # path or None - is the tool installed?
sys.executable              # the running python - always exists
```

| Concern | Tip |
|---------|-----|
| Paths | `pathlib.Path`, never hard-code `\` or `/` |
| Commands | `ls`/`dir`, `grep`/`findstr`, `python3`/`python` |
| Line endings | `\n` vs `\r\n` - use `splitlines()` |
| Case | Linux file names are case-sensitive |
| Often best | do it in **pure Python** (`shutil`, `pathlib`) |

<!-- Trainer notes: Demo examples/07_subprocess_linux_commands.py. On this Windows machine Git for Windows puts ls/grep on PATH - show the "Bonus" section. Key message: prefer Python's own modules (shutil.copy, pathlib.glob) over shelling out when possible - portable and no parsing. -->

---

## Automating CLI-based tools

Typical tester tasks:
- Run the **app's CLI** with different arguments, check output/exit code
- Call tools: `git`, `docker`, `curl`, database clients, installers
- Parse output -> assert

```python
r = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
assert r.returncode == 0
assert r.stdout.startswith("Python 3")

# Prefer machine-readable output when the tool offers it
r = subprocess.run(["gh", "repo", "view", "--json", "name"], capture_output=True, text=True)
data = json.loads(r.stdout)
```

<!-- Trainer notes: Stress "--json" / "--output json" options - parsing JSON beats parsing text columns. The gh example is illustrative only (needs GitHub CLI). Ask trainees which CLI tools their products ship with. -->

---

## Parsing command output

```python
out = """service  status
db       RUNNING
cache    STOPPED"""

status = {}
for line in out.splitlines()[1:]:       # skip header
    name, state = line.split()
    status[name] = state

assert status["db"] == "RUNNING"
```

- `splitlines()` handles `\n` and `\r\n`
- `"text" in result.stdout` for simple checks
- `re` (regular expressions) for complex patterns

<!-- Trainer notes: From examples/08_command_output_errors.py section 1. Common pitfall: comparing stdout with "\n" at the end - use .strip(). -->

---

## Four ways a command can fail

| What happened | How to detect |
|---------------|---------------|
| Tool ran, reported failure | `returncode != 0`, read `stderr` |
| Tool ran, `check=True` | `subprocess.CalledProcessError` |
| Tool hangs | `timeout=` -> `subprocess.TimeoutExpired` |
| Tool not installed / wrong PATH | `FileNotFoundError` |
| No execute permission | `PermissionError` |

<!-- Trainer notes: Write these on the whiteboard. Each maps to a different bug report: product bug, product hang, environment problem, permission problem. Good automation reports which one happened. -->

---

## returncode and stderr

```python
r = subprocess.run([sys.executable, "-c",
     "import sys; sys.stderr.write('ERROR: config missing'); sys.exit(3)"],
     capture_output=True, text=True)

if r.returncode != 0:
    print(f"FAIL rc={r.returncode} stderr={r.stderr.strip()}")
```

```python
try:
    subprocess.run(cmd, capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print(e.returncode, e.stderr)
```

<!-- Trainer notes: Demo sections 2 and 3 of example 08. Note that some tools write progress to stderr even on success - check returncode first, not "stderr is empty". Also some tools (grep, diff) use return code 1 for "no difference/no match", not error. -->

---

## Timeouts and missing commands

```python
try:
    subprocess.run(["some_tool", "--sync"], capture_output=True,
                   text=True, timeout=60)
except subprocess.TimeoutExpired as e:
    print(f"Hung for more than {e.timeout}s - killed")
except FileNotFoundError:
    print("some_tool is not installed or not on PATH")
```

- **Always** set a timeout in automation
- Check first with `shutil.which("some_tool")`

<!-- Trainer notes: Demo sections 4 and 5 of example 08. A test suite that hangs overnight is worse than one that fails - timeouts turn hangs into clear failures. -->

---

## A reusable `run_command()` helper

```python
def run_command(cmd, timeout=30):
    """Never raises - always returns a dict."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"ok": r.returncode == 0, "returncode": r.returncode,
                "stdout": r.stdout.strip(), "stderr": r.stderr.strip(), "error": ""}
    except subprocess.TimeoutExpired:
        return {"ok": False, "returncode": None, "error": f"timeout {timeout}s", ...}
    except FileNotFoundError:
        return {"ok": False, "returncode": None, "error": "command not found", ...}
```

<!-- Trainer notes: Section 6 of example 08. This helper is what trainees implement in Lab 2 - encourage them to keep it in a personal "utils" module for Day 4/5. -->

---

## Configuration-driven execution

```yaml
# config/commands.yaml
settings:
  default_timeout: 15
checks:
  - name: Python is installed
    command: "{python} --version"
    expect_stdout_contains: "Python 3"
    tags: [smoke]
  - name: Tool reports a controlled failure
    command: ["{python}", "-c", "import sys; sys.exit(4)"]
    expected_returncode: 4
  - name: List directory (Linux)
    command: "ls -la"
    os: linux
```

Testers add checks by editing YAML - **no Python changes**

<!-- Trainer notes: Open examples/config/commands.yaml. Point out: {python} placeholder for portability, os filter, tags for selection, expected_returncode for negative tests. JSON version: config/commands.json - the runner picks the parser by file extension. -->

---

## Demo: config-driven runner

```
python 09_config_driven_runner.py
python 09_config_driven_runner.py --tag smoke
python 09_config_driven_runner.py --config config/commands.json
```

```
[PASS] Python is installed                         ok
[SKIP] List directory (Linux)                      only for linux
[FAIL] Hanging tool (DELIBERATE FAIL - ...)        timed out after 1s
[FAIL] Missing tool (DELIBERATE FAIL - ...)        command not found: ...
Summary: {'PASS': 4, 'FAIL': 3, 'SKIP': 1}
```

JSON report in `sandbox/command_report.json`, exit code 0/1

<!-- Trainer notes: The 3 demo_fail checks exist to show each failure type in the report. Ask: "How would you add a check that 'git --version' works?" - let a trainee edit the YAML live. -->

---

## Lab 2: Executing commands via Python (30 min)

`hands_on/starter/lab2_run_commands.py`

1. `run_command()` with timeout + error handling
2. OS-specific checks: `dir`/`ls`, `findstr`/`grep`, `whoami`
3. A negative test (missing tool)
4. Parse output: file count, ERROR line count
5. Write `sandbox/lab2_command_log.csv`

<!-- Trainer notes: If WSL is available, have trainees run the same script in WSL (wsl python3 lab2_run_commands.py) to see the Linux branch execute. -->

---

## Automating system-level tasks

| Task | Python | Linux shell |
|------|--------|-------------|
| Disk usage | `shutil.disk_usage(path)` | `df -h`, `du -sh` |
| Old files | `Path.glob` + `stat().st_mtime` | `find -mtime +7` |
| Archive | `shutil.make_archive(base, "zip", dir)` | `tar -czf`, `zip` |
| Delete | `Path.unlink()`, `shutil.rmtree()` | `rm`, `rm -r` |
| Backup | `shutil.copytree(src, dst)` | `cp -r`, `rsync` |
| Process | `tasklist` / `pgrep` via subprocess | `ps aux \| grep`, `pgrep` |
| Service | `systemctl is-active <svc>` | same |

<!-- Trainer notes: Prefer the Python column: portable and testable. Real-world uses: cleaning a test machine before a run, archiving logs after a run for bug reports, verifying the app's background service is running before GUI tests start. -->

---

## Demo: system tasks

```python
total, used, free = shutil.disk_usage(HERE)
old = [f for f in LOG_DIR.glob("*.log")
       if f.stat().st_mtime < time.time() - days * 86400]
shutil.make_archive(str(ARCHIVE_DIR / "old_logs"), "zip", root_dir=staging)
assert_in_sandbox(f); f.unlink()
shutil.copytree(DATA_DIR, BACKUP_DIR / f"test_data_{stamp}")
```

```
python 10_system_tasks.py --dry-run
python 10_system_tasks.py --days 7
```

<!-- Trainer notes: Demo examples/10_system_tasks.py. Stress the safety net: the script refuses to delete outside its sandbox, and --dry-run previews deletions. Always build deletion tools this way. -->

---

## Lab 3 & Lab 4 (80 min)

**Lab 3 - System maintenance** `lab3_system_maintenance.py`
`report | archive | cleanup | backup | process | all`, `--days`, `--dry-run`

**Lab 4 - CLI config automation** `lab4_config_cli.py`
```
python lab4_config_cli.py show --env qa
python lab4_config_cli.py set retries 3 --env qa
python lab4_config_cli.py validate --env qa
python lab4_config_cli.py run --env qa
```
Env overrides `LAB_RETRIES`, secret `LAB_API_TOKEN` (masked)

<!-- Trainer notes: Split the room if needed: faster trainees do both labs, others focus on Lab 3. Lab 4 combines argparse (Day 2), YAML, env vars, secrets and subprocess - it's the best summary of the day. -->

---

## Best practices summary

- Paths from `Path(__file__).resolve().parent`, always `encoding="utf-8"`
- CSV: `newline=""`, `DictReader`, convert types
- JSON: `indent=2`, handle `JSONDecodeError`
- YAML: `safe_load`, quote ambiguous values
- Configs per environment, env var overrides, **no secrets in code**
- `subprocess.run([...], capture_output=True, text=True, timeout=...)`
- Check `returncode`, keep `stderr`, catch `TimeoutExpired` / `FileNotFoundError`
- Deletion scripts: sandbox checks + `--dry-run`
- Exit with 0/1 so CI can react

<!-- Trainer notes: Use this as a checklist when reviewing lab code together. -->

---

<!-- _class: compact -->
## Recap

| Topic | Key takeaway |
|-------|--------------|
| CSV | Tabular data, strings only, `DictReader/DictWriter` |
| JSON | Nested, typed, `load/dump`, `loads/dumps` |
| YAML | Human config, `safe_load`, watch the gotchas |
| Env configs | dev/qa/prod files + env vars + secrets outside code |
| DDT | One script, many rows, layers + `--dry-run` |
| Linux | `/` tree, `ls cd pwd cp mv rm cat grep find` |
| Permissions | `rwx`, 755/644/600, `chmod +x`, shebang |
| venv | isolate packages, `requirements.txt` |
| CLI automation | `subprocess.run`, returncode/stderr, timeouts, config-driven |

<!-- Trainer notes: Ask 3-4 trainees to each explain one row in their own words. Then run the quiz (03_Quiz.md). -->

---

## Homework / preparation for Day 4

- Finish any open lab; compare with `hands_on/solutions/`
- Lab 7: create a venv + `requirements.txt` for your lab folder
- Lab 8 (mini project): YAML-configured suite runner
- Read `02_Reading_Material.md` sections 9-12 and the questions and answers (section 19)
- Take the quiz `03_Quiz.md`

<!-- Trainer notes: Day 4 builds on the data-driven design (pytest parametrize, fixtures reading configs, reports). Encourage trainees to bring questions from the reading material. -->

---

# Q&A

**Thank you!**

Questions about files, configs, Linux or CLI automation?

<!-- Trainer notes: Common questions to be ready for: (1) "Excel files instead of CSV?" - openpyxl/pandas can read .xlsx; CSV is simpler and diff-friendly. (2) "TOML/INI?" - Python has tomllib (read-only) and configparser built in; same concepts. (3) "Do I need to learn bash scripting?" - basics yes; complex logic is better in Python. (4) "How do CI pipelines supply secrets?" - as environment variables injected at runtime from the secret store. -->
