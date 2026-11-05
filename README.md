# Python Desktop Application Automation Testing - Course Kit

**5 days · 40 hours** · Windows 11 · Python 3.12+ · pywinauto · PyTest · GitHub Actions

A complete, ready-to-deliver course: slide decks, trainee reading material, runnable examples, hands-on labs with starter and solution code, quizzes, a production-style automation framework, and a capstone mini project.

> Trainers: start with **[TRAINER_GUIDE.md](TRAINER_GUIDE.md)**. It has the delivery plan, setup checklist, and the syllabus coverage checklist.

---

## Project structure

```
DesktopApps/
|-- README.md                  <- you are here
|-- TRAINER_GUIDE.md           <- delivery plan, schedule, syllabus coverage checklist, tips
|-- requirements.txt           <- pip install -r requirements.txt
|-- package.json               <- npm install  (Allure 3 report CLI)
|-- .gitignore
|-- .github/workflows/
|   `-- automation-ci.yml      <- CI: CLI tests (Linux+Windows matrix) + desktop tests (self-hosted)
|
|-- Day1_Python_Fundamentals_OOP_Debugging/
|-- Day2_Desktop_and_CLI_Automation/
|-- Day3_File_Handling_Linux_System_Automation/
|-- Day4_Framework_PyTest_Logging_AI/
|-- Day5_Git_CICD_BestPractices_MiniProject/
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

Every **DayN** folder follows the same layout:

| Item | What it is | Audience |
|---|---|---|
| `01_Presentation.md` | Slide deck (Marp format) with trainer notes on every slide | Trainer (presenting) |
| `02_Reading_Material.md` | Handbook: explanations, examples, common mistakes, cheat sheets, questions & answers | Trainees |
| `03_Quiz.md` | 20 MCQs + answer key with explanations | Trainees / assessment |
| `examples/` | Numbered, runnable demo scripts used in the slides | Trainer demos + trainees |
| `hands_on/Lab_Guide.md` | Step-by-step labs: objective, time, tasks, expected output, hints, stretch goals | Trainees |
| `hands_on/starter/` | Lab starting files with `# TODO` markers | Trainees |
| `hands_on/solutions/` | Complete, tested solutions | Trainer |

Day 4 also has a mini framework lab (`hands_on/*/mini_framework`). Day 5 also has `hands_on/Mini_Project.md` with the starter kit and reference solution.

## Course outline

| Day | Topic | Folder |
|---|---|---|
| 1 | Python fundamentals, OOP, debugging | [Day1_Python_Fundamentals_OOP_Debugging](Day1_Python_Fundamentals_OOP_Debugging/) |
| 2 | Desktop application automation (pywinauto, pyautogui) and CLI automation (argparse, subprocess) | [Day2_Desktop_and_CLI_Automation](Day2_Desktop_and_CLI_Automation/) |
| 3 | File handling (CSV/JSON/YAML), Linux basics, system and CLI tool automation | [Day3_File_Handling_Linux_System_Automation](Day3_File_Handling_Linux_System_Automation/) |
| 4 | Framework design, logging, PyTest, HTML reports, AI basics | [Day4_Framework_PyTest_Logging_AI](Day4_Framework_PyTest_Logging_AI/) |
| 5 | Git, GitHub Actions CI/CD, best practices, mini project | [Day5_Git_CICD_BestPractices_MiniProject](Day5_Git_CICD_BestPractices_MiniProject/) |

## Setup (each trainee machine)

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

## Viewing and exporting the slides

The decks are [Marp](https://marp.app) Markdown:
- **VS Code:** install *Marp for VS Code*, open `01_Presentation.md`, and click the preview icon. Use *Export Slide Deck* to create **PPTX / PDF / HTML**.
- **Command line:** `npx @marp-team/marp-cli Day1_Python_Fundamentals_OOP_Debugging/01_Presentation.md --pptx`
- Trainer notes are HTML comments (`<!-- Trainer notes: ... -->`). Marp exports them as **speaker notes**.
- **Everything at once:** `python tools/export_materials.py` exports every `.md` file in `Day1`..`Day5` to `exports/`, keeping the Day folder structure. Slide decks become **PPTX + PDF** with speaker notes. Handbooks, quizzes and lab guides become A4 **PDF** documents. Add a filter to export one day only: `python tools/export_materials.py Day2`. Needs Node.js and Edge or Chrome. Re-run it after you edit a `.md` file.

## Safety rules built into every desktop script

- **Notepad:** Windows 11 Notepad restores your previous tabs. Scripts only open **a temp file they created** and close **only that tab** (Ctrl+W). They never type into an existing window or close the Notepad window.
- **Calculator:** every `calc.exe` launch opens *another* window, so scripts **reuse** an open Calculator and close it at the end.
- **File deletion:** scripts that delete files work only inside their own `sandbox/` folder.
- **Processes:** scripts stop only processes they started themselves.
