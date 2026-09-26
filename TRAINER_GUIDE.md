# Trainer Guide - Python Desktop Application Automation Testing

**Duration:** 5 days × 8 hours (09:00-17:00, 2 tea breaks + lunch) · **Audience:** manual testers / freshers, no Python required · **Batch size:** 10-20

---

## 1. How to use this kit

| Before the course | During each day | After each day |
|---|---|---|
| Run the setup checklist (section 3) on the **training machine** | Present `01_Presentation.md` and read the trainer notes in the slide notes | Assign `02_Reading_Material.md` sections + `03_Quiz.md` |
| Export decks to PPTX/PDF (see README) | Run the demos from `examples/` exactly where the notes say so | Review lab solutions from `hands_on/solutions/` |
| Share `02_Reading_Material.md`, `hands_on/Lab_Guide.md` and `starter/` with trainees. **Keep `solutions/` for yourself** until each lab ends | Labs: trainees follow `Lab_Guide.md` using `starter/` files | Collect questions for the next morning's recap |

**Teaching pattern for every topic:** concept (slide) → live demo (example script) → trainees try it (lab) → discuss the solution.

---

## 2. Five-day schedule at a glance

| Day | Morning | Afternoon | Labs | Assessment |
|---|---|---|---|---|
| 1 | Python intro, setup, syntax, data types, operators, conditions, loops, functions | OOP (class, `__init__`, inheritance, encapsulation), debugging, exceptions | Calculator with functions · PyBank OOP · 5 buggy scripts | Day 1 quiz |
| 2 | How desktop apps work, app types, UI elements, element vs image automation, pywinauto, pyautogui | Focus/windows/dialogs, CLI tools, `sys.argv`, `argparse`, reusable utilities, `subprocess` | Calculator · safe Notepad · log analyzer CLI · calc_cli with arguments | Day 2 quiz |
| 3 | CSV, JSON, YAML, env configs, data-driven desktop automation | Linux filesystem and commands, permissions, venv, subprocess, config-driven runners | Data-driven Calculator · Linux commands · system tasks · config CLI · shell and permissions labs | Day 3 quiz |
| 4 | Modular framework design, config, environments, logging | PyTest (fixtures, parametrize, markers, HTML report, screenshot on failure), AI basics | Logging mini framework · PyTest + reports · AI-assisted refactor | Day 4 quiz |
| 5 | Git, branching, GitHub Actions | Best practices, **mini project (3 h)**, demos, review | Git · CI pipeline · flaky-script refactor · capstone | Day 5 quiz + mini project (100 marks) |

Detailed minute-by-minute agendas are on slide 2 of each deck.

**Certification suggestion:** average quiz score ≥ 70% **and** mini project ≥ 60/100.

---

## 3. Setup checklist (training machine: do this the day before)

- [ ] Python 3.12+ on PATH: `python --version`
- [ ] `pip install -r requirements.txt` succeeds
- [ ] Node.js LTS installed and `npm install` run in the project root (Allure 3 report generator, no Java needed)
- [ ] Git + Git Bash: `git --version`
- [ ] VS Code + Python extension (+ Marp extension for slides)
- [ ] `cd automation_framework && pytest` → **30 passed** (8 Calculator + 4 Notepad + 9 Excel + 9 CLI, about 1 min). Excel tests need Microsoft Excel installed; without it they are skipped
- [ ] `python run_tests.py` asks which application to test. Press Enter to test all
- [ ] `python run_tests.py` builds `allure-report/index.html` and `reports/test_report.pdf`. Open both once before class
- [ ] Day 2 `examples\02_calculator_pywinauto.py` and `03_notepad_safe_automation.py` run with PASS
- [ ] Day 2 `examples\06_image_based_click.py --capture`, then run it without the flag. The reference image depends on your **display scaling and theme**, so capture it on the presenting machine
- [ ] Accessibility Insights for Windows installed (object inspection demo, Day 2)
- [ ] Trainees have GitHub accounts (Day 5)
- [ ] Projector: keep display scaling unchanged between capturing images and presenting

**Verified environment:** Windows 11 (build 26200), Python 3.14, pywinauto 0.6.9, pytest 9.1, pytest-html 4.2. Every script in `examples/` and `hands_on/solutions/` was run, including the GUI scripts driving the real Calculator and Notepad.

---

## 4. Syllabus coverage checklist

Every bullet of the official course outline, and where it is taught.

### Day 1 - Python Fundamentals, OOPs & Debugging  (`Day1_Python_Fundamentals_OOP_Debugging/`)

| Syllabus topic | Example(s) | Lab |
|---|---|---|
| Introduction to Python and automation use cases | `01_first_program.py` | - |
| Desktop & CLI automation overview | `02_cli_automation_preview.py` | - |
| Python installation and IDE setup (VS Code / PyCharm) | slides + reading ch. "Setup" | - |
| Python syntax and first program | `01_first_program.py` | - |
| Variables and data types | `03_variables_datatypes.py` | Lab 4 |
| Operators (arithmetic, logical, comparison) | `04_operators.py` | Lab 1 |
| Conditional statements | `05_conditionals.py` | Lab 1 |
| Loops (for, while) | `06_loops.py` | Lab 4 |
| Functions and reusability | `07_functions.py` | **Lab 1 - Calculator using functions** |
| Why OOP is critical for automation frameworks | `12_automation_oop_example.py` | - |
| Class and Object | `08_classes_objects.py` | Lab 2 |
| Constructor (`__init__`) | `09_constructor_methods_attributes.py` | Lab 2 |
| Methods and attributes | `09_constructor_methods_attributes.py` | Lab 2 |
| Inheritance (basic) | `10_inheritance.py` | Lab 2 |
| Encapsulation (basic) | `11_encapsulation.py` | **Lab 2 - OOP business logic (PyBank)** |
| Automation-oriented OOP examples | `12_automation_oop_example.py` | - |
| Common Python and automation errors | `13_common_errors.py` | Lab 3 |
| Print-based debugging | `14_print_debugging.py` | Lab 3 |
| IDE debugging (breakpoints, step-in/step-over) | `15_ide_debugging_walkthrough.py`, `17_debugging_demo_buggy.py` / `_fixed.py` | **Lab 3 - Debugging faulty scripts** |
| Exception handling (try, except, finally) | `16_exception_handling.py` | Lab 5 |

### Day 2 - Desktop Application Automation & CLI Automation  (`Day2_Desktop_and_CLI_Automation/`)

| Syllabus topic | Example(s) | Lab |
|---|---|---|
| How desktop applications work | `01_list_running_windows.py` | Lab 0 (inspect) |
| Types of desktop applications (Win32, WPF, Electron, UWP) | slides + reading, `01_list_running_windows.py` | - |
| Desktop UI elements and states | `04_print_control_identifiers.py`, `07_handle_dialogs_focus.py` | Lab 0 |
| Desktop automation challenges | reading + slides (Notepad tab restore, duplicate Calculator windows) | Lab 2 |
| Element-based vs image-based automation | `02_calculator_pywinauto.py` vs `06_image_based_click.py` | - |
| Mouse and keyboard automation | `05_mouse_keyboard_pyautogui.py` | - |
| Handling focus, windows, dialogs | `07_handle_dialogs_focus.py` | Lab 2 |
| Introduction to CLI tools and automation use cases | slides, `10_subprocess_demo.py` | - |
| Running Python scripts from command line | `08_sys_argv_demo.py` | Lab 4 |
| Command-line arguments (`sys.argv`, `argparse`) | `08_sys_argv_demo.py`, `09_argparse_demo.py` | **Lab 4 - Passing arguments** |
| Writing reusable utility scripts | `11_reusable_cli_utility.py` | **Lab 3 - Reusable CLI utility (log analyzer)**, Lab 5 |
| Automating system commands using Python | `10_subprocess_demo.py` | Lab 5 |
| Hands-on: Automating Notepad / Calculator | `02_calculator_pywinauto.py`, `03_notepad_safe_automation.py` | **Labs 1 & 2** |

### Day 3 - File Handling, Linux Basics & System Automation  (`Day3_File_Handling_Linux_System_Automation/`)

| Syllabus topic | Example(s) | Lab |
|---|---|---|
| Reading and writing CSV files | `01_csv_read_write.py`, `02_csv_dictreader_testdata.py` | Lab 1 |
| Reading and writing JSON files | `03_json_read_write.py` | Lab 1 |
| Introduction to YAML for configuration | `04_yaml_config.py` | Lab 4 |
| Managing test data and environment configs | `05_env_configs.py` + `config/dev.yaml, qa.yaml, prod.yaml` | Lab 4 |
| Data-driven desktop automation | `06_data_driven_calculator.py` (+ `--dry-run`) | **Lab 1 - Data-driven Calculator** |
| Linux filesystem structure | slides + reading | Lab 5 |
| Shell commands: ls, cd, pwd, cp, mv, rm, cat, grep, find | `linux_commands_practice.sh` | **Lab 5 - 22 shell commands** |
| File permissions and execution rights | slides + reading | **Lab 6 - Permissions** (use WSL/Linux) |
| Running Python scripts in Linux | slides (shebang, `chmod +x`) | Lab 6 |
| Virtual environments basics | slides + reading | Lab 7 |
| Executing Linux commands using Python | `07_subprocess_linux_commands.py` | **Lab 2** |
| Automating CLI-based tools | `09_config_driven_runner.py` | Lab 2 |
| Handling command outputs and errors | `08_command_output_errors.py` | Lab 2 |
| Configuration-driven execution using JSON/YAML | `09_config_driven_runner.py` + `config/commands.yaml/json` | **Lab 4 - Config CLI** |
| Automating system-level tasks | `10_system_tasks.py` | **Lab 3 - System maintenance** |

### Day 4 - Framework Design, PyTest, Logging & AI Basics  (`Day4_Framework_PyTest_Logging_AI/` + `automation_framework/`)

| Syllabus topic | Example(s) | Lab |
|---|---|---|
| Modular framework design | `automation_framework/` (README architecture) | **Lab 1 - mini framework** |
| Reusable utilities and helpers | `automation_framework/core/`, `utils/` | Lab 1 |
| Configuration-driven frameworks | `03_logger_config_from_yaml.py`, `automation_framework/config/config.yaml` | Lab 1 |
| Environment handling | `--env` / `TEST_ENV` in `automation_framework/tests/conftest.py` | Lab 2 |
| Importance of logging / Python logging module | `01_logging_basics.py` | Lab 1 |
| Log levels and formats | `01_logging_basics.py`, `03_logger_config_from_yaml.py` | Lab 1 |
| Log file management | `02_logging_handlers_rotation.py`, `automation_framework/core/logger.py` | Lab 1 |
| Using logs for debugging failures | `07_ai_debugging_before.py` / `08_ai_debugging_after.py` | Lab 3 |
| Why PyTest / test structure and execution flow | `pytest_demo/test_basics.py`, `test_fixtures.py` | **Lab 2** |
| Assertions and validations | `pytest_demo/test_basics.py` | Lab 2 |
| Parameterization (basic) | `pytest_demo/test_parametrize.py` (+ CSV) | Lab 2 |
| Markers | `pytest_demo/test_markers.py`, `pytest.ini` | Lab 2 |
| HTML reports | `pytest --html=reports/report.html --self-contained-html` | Lab 2 |
| Allure report + PDF export (extension) | `automation_framework/run_tests.py`, `allurerc.mjs`, `core/reporting.py`, `tools/allure_pdf_report.py` | Lab 2 stretch (section 8) |
| Screenshot and log capture on failure | `pytest_demo/test_failure_capture.py` (`-m demo_fail`), framework `conftest.py` | Lab 2 |
| POM-style design for desktop | `automation_framework/pages/`, `core/base_window.py` | Lab 1 |
| Role of AI in automation / AI-assisted script design | slides, `examples/ai_prompt_examples.md` | Lab 3 |
| Smart retries and synchronization logic | `04_retry_and_wait.py`, `05_self_healing_locator_concept.py` | Lab 3 |
| AI-based test data generation (conceptual) | `06_test_data_generation.py` | - |
| Demo: AI-assisted debugging and optimization | `07_ai_debugging_before.py` → `08_ai_debugging_after.py` | **Lab 3 - AI-assisted improvement** |

### Day 5 - Git, GitHub Actions CI/CD & Mini Project  (`Day5_Git_CICD_BestPractices_MiniProject/`)

| Syllabus topic | Example(s) | Lab |
|---|---|---|
| Git basics and workflow | `examples/git_practice.sh` | **Lab 1** Tasks 1-3 |
| Clone, add, commit, push | `git_practice.sh` | Lab 1 Tasks 2, 7, 8 |
| Branching strategies | slides (feature branch, GitFlow vs trunk-based, PRs) | Lab 1 Tasks 4-6 |
| Best practices for automation repositories | `examples/sample.gitignore` | Lab 1 Task 2 |
| CI/CD fundamentals / GitHub Actions overview | `github_actions/01_hello_world.yml` | **Lab 2** |
| Workflow YAML structure | `github_actions/02_python_tests.yml`, root `.github/workflows/automation-ci.yml` | Lab 2 |
| Running Python automation in CI | `github_actions/03_matrix_os_python.yml` | Lab 2 Tasks 2-3 |
| Headless and scheduled execution | `github_actions/04_scheduled_headless.yml` | Lab 2 Task 5 |
| Linux runner considerations for desktop & CLI | slides + `automation-ci.yml` (self-hosted desktop job) | Lab 2 questions |
| Desktop vs CLI vs system automation use cases | slides | Mini project |
| UI object identification & synchronization | `best_practices/01_sleep_vs_wait_*.py` | Lab 3 |
| Handling native dialogs and controls | slides, Day 2 `07_handle_dialogs_focus.py` | - |
| Reliability improvements and failure recovery | `best_practices/03_cleanup_finally.py`, `04_kill_leftover_process.py` | **Lab 3** |
| Cross-platform automation challenges | `best_practices/02_hardcoded_paths_*.py`, `05_cross_platform_commands.py` | Lab 3 |
| Mini project: desktop workflow + CLI/system task, config-driven, debugging and stability, final review | `hands_on/Mini_Project.md`, `mini_project_starter/`, `mini_project_solution/` | **Capstone** |

---

## 5. Real-world lessons to emphasise (they happened while building this kit)

1. **Never assume a clean application state.** Windows 11 Notepad restores the user's previous tabs. An early test script typed into a *real document* that was already open. The framework now opens only its own temp file and closes only that tab. Tell this story on Day 2.
2. **Duplicate windows break locators.** Every `calc.exe` launch opens another Calculator window, and a leftover window causes `ElementAmbiguousError: There are 2 elements that match`. The fix is to reuse or clean up. Show it live on Day 2 or Day 5.
3. **`type_keys` can drop characters.** Typing too fast lost one character. The fix is `pause=0.05` **plus** verifying the text afterwards. "Always verify, never assume the action worked."
4. **Git Bash rewrites `/` arguments** (`python calc_cli.py 10 / 4` becomes a path). Use PowerShell or `MSYS_NO_PATHCONV=1`. This is a good cross-platform lesson.
5. **Hosted CI Windows runners are Windows Server:** no Store Calculator and no interactive desktop, so desktop tests need a self-hosted runner.
6. **COM threading conflict (Excel):** importing pywinauto in the same process as win32com Office objects switches COM to another threading mode. Excel then failed with *"Object is not connected to server"*. The fix is to verify the Excel window with `win32gui` instead of pywinauto. This is a good "read the error, isolate it in a small script" debugging story.
7. **SaveAs changes the open workbook:** after `SaveAs("order.xlsx")` the open workbook *is* that file, so re-opening it returns the same object, and closing that closes ours. The fix is to close first, then re-open from disk. That's also the stronger check that the data was saved.
8. **Never leave hidden processes:** a failed Excel run left an invisible `EXCEL.EXE`. `ExcelPage.quit()` now remembers its own process ID and, if a normal quit fails, stops exactly that process.

## 6. Delivery tips

- **Pace:** Day 1 is the foundation for non-programmers. If the batch is slow, move Day 1 Lab 4-5 and Day 3 Lab 7-8 to homework.
- **Live coding:** type the first example of each topic yourself; then run the prepared example files.
- **Pairing:** pair a stronger and a weaker trainee for labs; rotate daily.
- **Morning recap (15 min):** 5 quiz questions from the previous day plus open questions.
- **Desktop demos:** don't touch the mouse or keyboard while GUI scripts run, and keep the screen unlocked. Mouse to a screen corner aborts pyautogui scripts (FAILSAFE).
- **Deliberate failures:** some demos fail on purpose, as discussion points. These include:
  - Day 1 `12_automation_oop_example.py` (CALC_04)
  - Day 3 `06_data_driven_calculator.py` (CALC-009)
  - Day 3 lab1 data (bad rows)
  - Day 4 `pytest -m demo_fail`
  - Day 5 `lab2_test_break_ci.py`

  Say so before running them.
- **Buggy scripts:** `hands_on/starter` in Day 1 Lab 3 fails on purpose. The explanations are in collapsed sections of the Lab Guide.

## 7. Resetting the kit between batches

Generated folders are git-ignored and safe to delete: `__pycache__/`, `logs/`, `reports/`, `screenshots/`, `sandbox/`, `sandbox_repo/`, `artifacts/`. Scripts recreate them. Delete Day 2 `examples/images/calc_seven.png` and capture it again on the new machine.

## 8. Allure report & PDF (Day 4 extension, about 30 min after the pytest-html topic)

**Demo flow**
1. `cd automation_framework` and `python run_tests.py -m smoke --open`. The Allure report opens in the browser.
2. Walk through Allure: *Overview* (totals, trend), grouping by **epic → feature → story**, **severity**, a test's **steps** (from the page objects) and **attachments** (CLI stdout/stderr, the Calculator display, the saved Notepad file).
3. Show where the data comes from:
   - the raw JSON files in `allure-results/`
   - the labels in `tests/test_calculator.py`
   - `core/reporting.py` (`step`, `@step_method`, `attach_*`)
   - `environment.properties` written by `conftest.py`
4. Open `reports/test_report.pdf`. It has a summary with a pie chart, results by feature, all tests, failures (message, trace, steps, screenshot), and the steps of every test.
5. Make one test fail (for example change `expected` in `test_data/calculator_data.csv`). Re-run, then show the failure in Allure and on the Failures page of the PDF, including the screenshot. Revert the change.

**Key teaching points**
- Allure = **results** (written by the pytest plugin during the run) + **report** (generated afterwards). Both the HTML report and the PDF are built from the same results.
- Allure 3 runs on Node.js (`npx allure generate`). Allure 2 needs Java; mention this because many companies still use it (`allure serve allure-results`).
- The HTML report is interactive and has no PDF export, so the framework has its own PDF generator (`reportlab`). This is a good example of a reusable utility.
- CI uploads `allure-report/` and `reports/test_report.pdf` as artifacts on every run (see `.github/workflows/automation-ci.yml`).

**Trainee exercise (stretch, Day 4 Lab 2)**
- Add `@allure.story` / `@allure.severity` / `@allure.title` to the CLI tests you wrote, and add a `with step("..."):` block inside one test.
- Generate the Allure report and the PDF with `--title "<your name> - Lab 2" --details failed`.

## 9. Choosing the application under test (`--app`)

The framework can test **Calculator, Notepad, Excel, the CLI tool, or all of them**, chosen at run time:

| Command | Behaviour |
|---|---|
| `python run_tests.py` | **Asks** the user (menu with numbers or names, Enter = default) |
| `python run_tests.py --app excel` | No question. Opens Excel and runs only the Excel tests |
| `pytest --app notepad` | Same selection directly in pytest |
| `TEST_APP=calculator pytest` (PowerShell: `$env:TEST_APP="calculator"`) | Selection via an environment variable |
| CI / no keyboard (`CI` set or input piped) | Never asks. Uses `default_app` from `config.yaml` (`all`) |

Priority: `--app` → `TEST_APP` → `default_app` in `config/config.yaml`.

**How it works (good framework-design discussion):**
- Each test file carries an **application marker** (`calculator`, `notepad`, `excel`, `cli`), registered in `pytest.ini`.
- `conftest.py` adds the `--app` option, then deselects the tests of other applications in `pytest_collection_modifyitems`. The pytest header shows `application under test: ...`.
- `--app` combines with markers: `python run_tests.py --app excel -m smoke`.
- The PDF title and the Allure environment show the selected application.

**Excel automation (COM):**
- `pages/excel_page.py` drives Excel through its object model (`win32com`). This is how Office is automated in industry. Clicking grid cells by coordinates is fragile.
- `DispatchEx` starts a **separate Excel instance**, so the user's own workbooks are never touched. `DisplayAlerts = False` stops pop-ups from blocking the run.
- The tests reuse `calculator_data.csv`, so the same data verifies two applications. They also check a `SUM` formula, `#DIV/0!`, and saving an `.xlsx` and re-opening it from disk.
- Set `excel.visible: false` in `config.yaml` (qa does this) for faster runs with Excel hidden.

**Trainee exercise:** add `word` as a fifth application. You need:
1. a `word` marker in `pytest.ini`
2. `"word"` in `SUPPORTED_APPS` and in the `run_tests.py` menu
3. `pages/word_page.py` using `DispatchEx("Word.Application")`, with `Documents.Add()`, typing with `Range.Text`, and `SaveAs2`
4. a `word` fixture, and a test that saves a `.docx` and re-opens it
