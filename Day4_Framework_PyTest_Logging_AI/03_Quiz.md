# Day 4 Quiz - Framework Design, PyTest, Logging & AI Basics

20 questions, one correct answer each. Time: 20 minutes. Answer key at the bottom.

---

**1. In a layered automation framework, where should the locator `auto_id="num7Button"` live?**
- A) In every test that clicks button 7
- B) In the page/window object class for the Calculator
- C) In `conftest.py`
- D) In `pytest.ini`

**2. What is the main benefit of a configuration-driven framework?**
- A) Tests run faster
- B) Environment-specific values (timeouts, URLs, paths) change without editing code
- C) It removes the need for assertions
- D) It makes logging unnecessary

**3. In `automation_framework`, which value wins if all three are set?**
`--env qa` on the command line, `TEST_ENV=dev`, `default_env: dev` in config.yaml
- A) `default_env`
- B) `TEST_ENV`
- C) `--env qa`
- D) pytest raises an error

**4. Which of these is the correct order of Python log levels, from lowest to highest severity?**
- A) INFO < DEBUG < WARNING < ERROR < CRITICAL
- B) DEBUG < INFO < WARNING < ERROR < CRITICAL
- C) DEBUG < WARNING < INFO < ERROR < CRITICAL
- D) TRACE < DEBUG < INFO < ERROR < FATAL

**5. A logger is set to `INFO`. Which call produces NO output?**
- A) `log.info("Calculator opened")`
- B) `log.warning("Retrying click")`
- C) `log.debug("Button rectangle: ...")`
- D) `log.error("Result mismatch")`

**6. Why is `logging` preferred over `print()` in an automation framework?**
- A) `print()` does not work on Windows
- B) Logging gives levels, timestamps, formats and multiple destinations (console + file) that can be switched without code changes
- C) Logging is faster than print in all cases
- D) pytest cannot capture print output

**7. Which handler starts a new log file when the current one reaches a size limit?**
- A) `FileHandler`
- B) `StreamHandler`
- C) `RotatingFileHandler`
- D) `TimedRotatingFileHandler`

**8. Which file names does pytest discover as tests by default?**
- A) Any `.py` file
- B) `test_*.py` or `*_test.py`
- C) Only files inside a folder called `tests`
- D) Files listed in `requirements.txt`

**9. What does code after `yield` in a pytest fixture do?**
- A) Nothing, it is never executed
- B) It runs as teardown after the test, even if the test fails
- C) It runs before the test
- D) It runs only when the test passes

**10. A fixture that starts Calculator is slow. Which scope shares ONE instance across all tests in a single test file?**
- A) `function`
- B) `class`
- C) `module`
- D) `session`

**11. Where should fixtures used by many test files be placed?**
- A) `pytest.ini`
- B) `conftest.py`
- C) `__init__.py`
- D) In each test file separately

**12. What does this produce?**
```python
@pytest.mark.parametrize("a,b,expected", [(2, 3, 5), (10, 5, 15), (1, 1, 3)])
def test_add(a, b, expected):
    assert a + b == expected
```
- A) 1 test, fails
- B) 3 tests: 2 pass, 1 fails
- C) 3 tests, all pass
- D) A syntax error

**13. With `--strict-markers` in `pytest.ini`, what happens if a test uses `@pytest.mark.smok` (typo)?**
- A) The test is silently skipped
- B) pytest raises an error because the marker is not registered
- C) The marker is treated as `smoke`
- D) Nothing, markers are optional

**14. Which command runs only tests marked `desktop` that are NOT marked `regression`?**
- A) `pytest -k "desktop not regression"`
- B) `pytest -m "desktop and not regression"`
- C) `pytest --markers desktop -regression`
- D) `pytest -m desktop,regression`

**15. Which marker documents a KNOWN bug so the test is expected to fail and does not break the build?**
- A) `@pytest.mark.skip`
- B) `@pytest.mark.xfail(reason="BUG-101")`
- C) `@pytest.mark.parametrize`
- D) `@pytest.mark.usefixtures`

**16. Which command creates a single-file HTML report that can be emailed or uploaded as a CI artifact?**
- A) `pytest --report=html`
- B) `pytest --html=reports/report.html --self-contained-html`
- C) `pytest -v > report.html`
- D) `pytest --junitxml=report.html`

**17. Which hook is used to take a screenshot when a test fails?**
- A) `pytest_addoption`
- B) `pytest_configure`
- C) `pytest_runtest_makereport` (checking `report.when == "call"` and `report.failed`)
- D) `pytest_sessionfinish`

**18. A click sometimes fails because the button is not ready yet. Best fix?**
- A) Add `time.sleep(10)` before every click
- B) Wrap the assertion in `try/except: pass`
- C) Wait for the element state (exists/enabled) with a timeout, and retry the action with backoff if needed
- D) Mark the test `skip`

**19. An AI assistant rewrote your flaky test. The new version passes, but it removed the final `assert` and added `except Exception: pass`. What should you do?**
- A) Commit it, it passes now
- B) Reject that part: the test no longer verifies anything and hides failures. Keep real assertions and fix the synchronization issue instead
- C) Ask the AI to add more `except` blocks
- D) Mark the test `xfail`

**20. Which is acceptable when using a public AI assistant for automation work?**
- A) Pasting production passwords so it can write the login test
- B) Pasting a customer database export to generate test data
- C) Sharing an anonymised code snippet and reviewing, running and understanding the answer before using it
- D) Committing AI-generated code without running it

---

## Answer key

| Q | Answer | Explanation |
|---|---|---|
| 1 | **B** | Page objects own locators, so a UI change means editing one class, not every test. |
| 2 | **B** | The same code runs against dev/qa/prod by switching configuration. |
| 3 | **C** | `get_config`: explicit argument (`--env`) > `TEST_ENV` > `default_env`. |
| 4 | **B** | DEBUG(10) < INFO(20) < WARNING(30) < ERROR(40) < CRITICAL(50). |
| 5 | **C** | DEBUG (10) is below the INFO (20) threshold, so it is filtered out. |
| 6 | **B** | Levels, formatting, and file + console output, all controlled by configuration. |
| 7 | **C** | `RotatingFileHandler(maxBytes=..., backupCount=...)`. Timed rotation rotates by time, not size. |
| 8 | **B** | Default `python_files = test_*.py *_test.py`, functions `test_*`. |
| 9 | **B** | Everything after `yield` is teardown and runs even when the test fails. |
| 10 | **C** | `module` scope: created once per test file. |
| 11 | **B** | `conftest.py` fixtures are available automatically to all tests in that folder and below. |
| 12 | **B** | Three test cases are generated; `1 + 1 == 3` fails. |
| 13 | **B** | Strict markers turn typos into errors instead of silently selecting nothing. |
| 14 | **B** | `-m` selects by marker expression; `-k` selects by name. |
| 15 | **B** | `xfail` reports XFAIL (expected), and XPASS if the bug gets fixed. |
| 16 | **B** | pytest-html with `--self-contained-html` embeds CSS/images into one file. |
| 17 | **C** | The makereport hookwrapper sees each phase's outcome; screenshot on a failed `call`. |
| 18 | **C** | Synchronize on state, retry actions with backoff. Fixed sleeps are slow and still flaky. |
| 19 | **B** | Never accept AI output that weakens the test. You are accountable for the code. |
| 20 | **C** | Never share secrets or real customer data; always verify AI output. |

### Score guide

* 18-20: Excellent - ready to extend the framework on Day 5.
* 14-17: Good - revisit the sections you missed in `02_Reading_Material.md`.
* below 14: Re-run `examples/pytest_demo` and redo Lab 2 before Day 5.
