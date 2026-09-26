# Day 3 Quiz
## File Handling, Configuration Management, Linux Basics & CLI Automation

20 multiple-choice questions. Choose **one** answer per question. Answer key with explanations at the end.
Suggested time: 20 minutes.

---

**1.** Why should you pass `newline=""` when opening a file for the `csv` module?

- A) It makes the file open faster
- B) It prevents extra blank lines between rows on Windows because the csv module handles line endings itself
- C) It removes the header row
- D) It is required to read UTF-8 files

**2.** What does `csv.DictReader` return for each data row?

- A) A list of strings
- B) A tuple
- C) A dictionary keyed by the header row
- D) A JSON string

**3.** A CSV cell contains `False`. What does `bool(row["enabled"])` return?

- A) `False`
- B) `True`
- C) `None`
- D) It raises `ValueError`

**4.** Which function parses a JSON **string** (for example, the stdout of a CLI tool)?

- A) `json.load()`
- B) `json.dump()`
- C) `json.loads()`
- D) `json.dumps()`

**5.** Which of these is **valid** JSON?

- A) `{'name': 'demo'}`
- B) `{"name": "demo",}`
- C) `{"name": "demo", "active": true, "owner": null}`
- D) `{"name": "demo"} // test suite`

**6.** What will `yaml.safe_load("zip: 01234")` most likely give for `zip`?

- A) `"01234"`
- B) `1234`
- C) `668` (interpreted as an octal number)
- D) A `YAMLError`

**7.** Why is `yaml.safe_load` recommended over `yaml.load` with the unsafe loader?

- A) It is faster
- B) It supports comments
- C) It only constructs basic types, so a malicious file cannot create arbitrary Python objects
- D) It preserves key order

**8.** Your QA database password must be available to the test framework. What is the best practice?

- A) Put it in `config/qa.yaml` and commit it
- B) Hard-code it in the test script but make the repo private
- C) Store only the variable name in the config and read the value from an environment variable / CI secret
- D) Put it in the test data CSV

**9.** In the data-driven Calculator example, what is the main benefit of the `MockCalculator` + `--dry-run` design?

- A) It makes the GUI faster
- B) Data loading, comparison and reporting can be tested anywhere without launching the GUI
- C) It removes the need for test data
- D) It lets pywinauto work on Linux

**10.** Which Linux directory usually contains system log files?

- A) `/etc`
- B) `/home`
- C) `/var/log`
- D) `/bin`

**11.** Which command shows **hidden** files in long format?

- A) `ls -l`
- B) `ls -la`
- C) `ls -R`
- D) `dir /h`

**12.** Which command counts the lines containing "error" in `app.log`, **ignoring case**?

- A) `grep -c -i error app.log`
- B) `grep -v error app.log`
- C) `find app.log -name error`
- D) `cat -n error app.log`

**13.** Which command finds `.log` files modified **more than 7 days ago** under the current directory?

- A) `find . -name "*.log" -mtime -7`
- B) `find . -name "*.log" -mtime +7`
- C) `grep -r "*.log" --days 7`
- D) `ls -t *.log | head -7`

**14.** What is the octal value of `rwxr-x---`?

- A) 755
- B) 750
- C) 740
- D) 640

**15.** You run `./check.py` on Linux and get `Permission denied`. The file starts with `#!/usr/bin/env python3`. What fixes it?

- A) `chmod +x check.py`
- B) `chmod 600 check.py`
- C) Rename it to `check.sh`
- D) `rm check.py`

**16.** How do you activate a venv named `.venv` in **Windows PowerShell**?

- A) `source .venv/bin/activate`
- B) `.venv\Scripts\Activate.ps1`
- C) `activate .venv`
- D) `pip activate .venv`

**17.** Which call is the safest way to run `grep` with a pattern that contains spaces?

- A) `subprocess.run("grep " + pattern + " app.log", shell=True)`
- B) `subprocess.run(["grep", pattern, "app.log"], capture_output=True, text=True)`
- C) `os.system("grep " + pattern)`
- D) `subprocess.run("grep", pattern, "app.log")`

**18.** `subprocess.run(["no_such_tool"])` is executed and the tool is not installed. What happens?

- A) `returncode` is 127 and no exception
- B) `subprocess.TimeoutExpired` is raised
- C) `FileNotFoundError` is raised
- D) `subprocess.CalledProcessError` is raised

**19.** `subprocess.run(cmd, check=True)` runs a command that exits with code 2. What happens?

- A) Nothing, you must inspect `returncode`
- B) `subprocess.CalledProcessError` is raised with `returncode == 2`
- C) `FileNotFoundError` is raised
- D) The command is retried twice

**20.** In a config-driven command runner, a check has `expected_returncode: 4` and the command exits with 4. What should the runner report?

- A) FAIL, because the return code is non-zero
- B) PASS, because the actual return code matches the expected one
- C) SKIP
- D) ERROR

---

## Answer Key

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | **B** | The csv module writes `\r\n` itself; without `newline=""` Windows adds another translation, which shows up as blank rows. |
| 2 | **C** | `DictReader` maps each row to a dict using the header, so you access `row["username"]`. `csv.reader` gives lists. |
| 3 | **B** | CSV values are strings. Any non-empty string is truthy, so `bool("False")` is `True`. Convert explicitly, e.g. `value.lower() == "true"`. |
| 4 | **C** | `loads` = load **s**tring. `load` reads a file object; `dump`/`dumps` go the other direction. |
| 5 | **C** | JSON needs double quotes (A is wrong), no trailing commas (B), and no comments (D). `true` and `null` are valid JSON literals. |
| 6 | **C** | PyYAML (YAML 1.1) treats a leading-zero number as octal: `01234` becomes `668`. Quote values like zip codes and IDs. |
| 7 | **C** | The unsafe loader can instantiate arbitrary objects (possible code execution). `safe_load` builds only dict, list, str, numbers, bool, None. |
| 8 | **C** | Secrets never go into code, config or data files in git. The config names the env var (e.g. `APP_DB_PASSWORD`); the value comes from the environment or CI secret store. |
| 9 | **B** | Both drivers share `calculate()`. The mock lets you validate data files, comparisons and reports quickly on any machine or headless CI. It does not make pywinauto work on Linux. |
| 10 | **C** | `/var/log` holds logs. `/etc` = configuration, `/home` = user files, `/bin` = programs. |
| 11 | **B** | `-l` = long format, `-a` = all including hidden (dot) files. `-R` is recursive. |
| 12 | **A** | `-c` counts matching lines, `-i` ignores case. `-v` inverts the match. |
| 13 | **B** | `-mtime +7` = more than 7 days ago; `-mtime -7` = within the last 7 days. |
| 14 | **B** | rwx = 4+2+1 = 7, r-x = 4+1 = 5, --- = 0, so 750. |
| 15 | **A** | The script needs execute permission. The shebang is already present. `chmod 600` would remove execute rights for everyone. |
| 16 | **B** | Windows venvs use the `Scripts` folder; PowerShell runs `Activate.ps1`. `source .venv/bin/activate` is Linux/macOS. |
| 17 | **B** | List form passes the pattern as one argument with no shell parsing, so spaces are safe and injection is impossible. A and C build shell strings from input. D passes arguments incorrectly. |
| 18 | **C** | Without a shell, Python cannot start a non-existent executable and raises `FileNotFoundError`. (Return code 127 is what a *shell* reports with `shell=True` on Linux.) |
| 19 | **B** | `check=True` turns a non-zero exit into `CalledProcessError`, which carries `returncode`, `stdout` and `stderr`. |
| 20 | **B** | A test passes when actual behaviour matches expected behaviour. Negative tests often expect a specific non-zero code. |

**Scoring:** 18-20 excellent, 14-17 good - review the topics you missed, below 14 - re-read `02_Reading_Material.md` and redo the labs.
