# AI Prompt Examples for Test Automation

These prompts work with any AI coding assistant such as GitHub Copilot Chat, ChatGPT or Claude.
The responses shown are **representative summaries**. Real answers vary between tools and between runs,
so you always have to review what comes back.

> **Golden rules before you paste anything**
> 1. Never paste passwords, API keys, tokens, connection strings, customer data, production logs with personal data, or confidential source code into a public AI tool. Use your company's approved tool and follow its policy.
> 2. Replace real names, paths and URLs with placeholders (`<APP_PATH>`, `<SERVER>`, `user@example.com`).
> 3. The AI is a junior pair-programmer. It is not the tester of record. **You** own the result.

---

## 1. Anatomy of a good prompt (R-C-T-F-C)

| Part | Meaning | Example |
|------|---------|---------|
| **R**ole | Who the AI should act as | "You are a senior Python test automation engineer." |
| **C**ontext | Tools, versions, constraints | "Windows 11, Python 3.14, pytest 9, pywinauto (uia backend)." |
| **T**ask | Exactly what you want | "Review this script for flakiness and bugs." |
| **F**ormat | Shape of the answer | "Give a numbered list of issues, then the corrected script." |
| **C**onstraints | Rules it must follow | "Standard library only. Keep function names. No time.sleep for sync." |

A weak prompt: *"fix my code"*.
A strong prompt uses all five parts (see Prompt 3 below).

---

## 2. Prompt: generate test cases from a requirement

```text
You are a senior QA engineer.
Requirement: The "Add Employee" desktop form has fields Age (integer 18-60),
Username (5-12 letters/digits) and Salary (10000.00-99999.99). Save is enabled
only when all fields are valid.
Task: Produce test cases using boundary value analysis and equivalence
partitioning. Format: a markdown table with ID, Field, Input, Expected result,
Technique. Include at least 3 negative cases per field. Do not invent fields.
```

**Typical response (summary):** a table of about 25 rows with values such as 17/18/19/59/60/61 for Age and 4/5/12/13 character usernames.
**Review:** check that every boundary appears, that no fields were invented, and that "expected results" match the real requirement. Compare it with `06_test_data_generation.py`.

---

## 3. Prompt: debug and optimise a flaky script (used in the demo)

```text
Role: You are a senior Python test automation engineer.
Context: Windows 11, Python 3.14. The script below starts a CLI export job
that writes a report file after a variable delay of 0.5 to 2 seconds, then
checks that the report contains TOTAL=42. It passes or fails randomly
and sometimes prints nothing useful.
Task:
 1. List every bug and flakiness cause, with a one-line explanation each.
 2. Rewrite the script so it is reliable and debuggable.
Constraints:
 - Standard library only.
 - No fixed time.sleep for synchronisation; wait for the process and poll for the file.
 - Use the logging module (console INFO, file DEBUG).
 - Exit code 0 on pass and 1 on fail.
 - Do not use shell=True.
Format: numbered issue list first, then one complete code block.

<paste 07_ai_debugging_before.py here>
```

**Typical response (summary):**

1. `time.sleep(1)` is a race condition, because the job takes up to 2 s. Wait for the process and poll for the file instead.
2. `except: pass` hides `FileNotFoundError`, so the test prints nothing useful.
3. The file is opened without `with`, so the handle leaks. On Windows this also locks the file.
4. `data == "TOTAL=42"` fails because the file contains `"TOTAL=42\n"`. Use `.strip()`.
5. The report from the previous run is not deleted, so the test can read stale data.
6. `shell=True` with string concatenation causes quoting problems and is a security risk. The literal `python` may not be the interpreter that is running the script. Use `[sys.executable, ...]`.
7. There is no exit code, so CI always sees success.
8. There is no logging, so failures cannot be investigated afterwards.

...followed by a rewritten script similar to `08_ai_debugging_after.py`.

---

## 4. Review checklist: never merge AI output unchecked

| # | Check | Why |
|---|-------|-----|
| 1 | Does it **run**? Execute it at least 3 times. | AI code often has small errors or wrong imports. |
| 2 | Are the APIs **real**? Check the docs for any function you do not know. | AI can "hallucinate" methods, e.g. `window.wait_until_clickable()`. |
| 3 | Did it **change behaviour** you did not ask for? | For example, it deleted an assertion to make the test "pass". |
| 4 | Did it **hide failures**? Look for broad `except`, retries around assertions, or skipped checks. | A green test that checks nothing is worse than a red one. |
| 5 | Are timeouts/retries **bounded** and configurable? | Infinite loops hang CI. |
| 6 | Is it **secure**? Look for `shell=True`, hard-coded secrets, `eval`. | Security issues come in through copied code. |
| 7 | Does it follow **our framework**: logger, config, page objects? | Consistency and maintainability. |
| 8 | Can **you explain** every line? | If not, do not commit it. |

---

## 5. More useful prompts (copy and adapt)

**Explain a failure log**
```text
Here is a pytest failure traceback and the last 30 lines of our automation log
(names anonymised). Explain the most likely root cause, rank 3 hypotheses by
likelihood, and tell me which log line supports each. Do not propose code yet.
<paste traceback + log excerpt>
```

**Convert a manual test case to pytest**
```text
Convert this manual test case into a pytest test that uses our page object
CalculatorPage (methods: open(), calculate(a, op, b) -> float, clear(), close())
and the fixture `calculator`. Use @pytest.mark.parametrize for the 4 data rows.
Add the markers smoke and desktop. Do not use time.sleep.
<paste manual steps + data>
```

**Suggest locators with fallbacks**
```text
Given this pywinauto print_control_identifiers() output (trimmed), suggest a
primary locator and two fallback locators for the "Save" button, preferring
automation_id, then title+control_type. Explain why for each.
<paste trimmed output>
```

**Improve logging**
```text
Add meaningful logging to this function: INFO for business steps, DEBUG for
locator and data details, ERROR with traceback on failure. Use lazy %s
formatting and a module logger from logging.getLogger(__name__).
```
