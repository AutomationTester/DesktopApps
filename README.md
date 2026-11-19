# Python Desktop Application Automation Testing 

 Windows 11 · Python 3.12+ · pywinauto · PyTest · GitHub Actions

## Project structure

```
DesktopApps/
|-- README.md                  <- you are here
|-- requirements.txt           <- pip install -r requirements.txt
|-- package.json               <- npm install  (Allure 3 report CLI)
|-- .gitignore
|-- .github/workflows/
|   `-- automation-ci.yml      <- CI: CLI tests (Linux+Windows matrix) + desktop tests (self-hosted)
|
|-- Day1_Python_Fundamentals_OOP_Debugging/examples/
|-- Day2_Desktop_and_CLI_Automation/examples/
|-- Day3_File_Handling_Linux_System_Automation/examples/
|-- Day4_Framework_PyTest_Logging_AI/examples/
|-- Day5_Git_CICD_BestPractices_MiniProject/examples/
|
`-- automation_framework/      <- the course framework (Days 4-5, base of the mini project)
    |-- config/config.yaml     <- dev / qa environments
    |-- core/                  <- config reader, logger, waits/retry, BaseWindow, CLI runner
    |-- pages/                 <- CalculatorPage, NotepadPage (Page Object Model for desktop)
    |-- utils/                 <- CSV/JSON/YAML readers, screenshots
    |-- tools/sysinfo_cli.py   <- CLI application under test
    |-- test_data/             <- data-driven test inputs
    |-- tests/                 <- conftest.py + calculator / notepad / CLI tests
    |-- run_tests.py           <- pytest + Allure report + PDF in one command
    |-- allurerc.mjs           <- Allure report settings
    `-- tools/allure_pdf_report.py <- Allure results -> PDF
```
## Course outline

| Day | Topic | Folder |
|---|---|---|
| 1 | Python fundamentals, OOP, debugging | [Day1_Python_Fundamentals_OOP_Debugging](Day1_Python_Fundamentals_OOP_Debugging/) |
| 2 | Desktop application automation (pywinauto, pyautogui) and CLI automation (argparse, subprocess) | [Day2_Desktop_and_CLI_Automation](Day2_Desktop_and_CLI_Automation/) |
| 3 | File handling (CSV/JSON/YAML), Linux basics, system and CLI tool automation | [Day3_File_Handling_Linux_System_Automation](Day3_File_Handling_Linux_System_Automation/) |
| 4 | Framework design, logging, PyTest, HTML reports, AI basics | [Day4_Framework_PyTest_Logging_AI](Day4_Framework_PyTest_Logging_AI/) |
| 5 | Git, GitHub Actions CI/CD, best practices, mini project | [Day5_Git_CICD_BestPractices_MiniProject](Day5_Git_CICD_BestPractices_MiniProject/) |

## Setup 

1. Install **Python 3.12+** from python.org (tick *Add python.exe to PATH*), **Node.js LTS** (for the Allure report), **Git for Windows** (includes Git Bash), and **VS Code** with the *Python* extension. Optional: the *Marp for VS Code* extension to view the slides.
2. Open a terminal in this folder:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   npm install            # Allure 3 report generator - needs Node.js LTS from nodejs.org (no Java)
   ```
3. Smoke-check the installation:
   ```powershell
   cd automation_framework
   pytest -m cli          # 9 tests, no GUI
   pytest -m smoke        # includes one Calculator and one Notepad test (Windows desktop)
   python run_tests.py    # asks which app to test (Enter = all), then Allure + PDF reports
   python run_tests.py --app excel    # or choose directly: calculator | notepad | excel | cli | all
   ```

## Test reports

`python run_tests.py` (inside `automation_framework`) produces:

| Report | Location |
|---|---|
| Allure (interactive, single HTML file) | `automation_framework/allure-report/index.html` |
| PDF (summary, chart, all tests, failures with screenshots) | `automation_framework/reports/test_report.pdf` |
| pytest-html | `automation_framework/reports/report.html` |

See [automation_framework/README.md](automation_framework/README.md#reports-pytest-html-allure-and-pdf) for details.


## Safety rules built into every desktop script

- **Notepad:** Windows 11 Notepad restores your previous tabs. Scripts only open **a temp file they created** and close **only that tab** (Ctrl+W). They never type into an existing window or close the Notepad window.
- **Calculator:** every `calc.exe` launch opens *another* window, so scripts **reuse** an open Calculator and close it at the end.
- **File deletion:** scripts that delete files work only inside their own `sandbox/` folder.
- **Processes:** scripts stop only processes they started themselves.
