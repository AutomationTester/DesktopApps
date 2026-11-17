# Jenkins CI/CD demo for automation_framework

The [Jenkinsfile](Jenkinsfile) at the repo root runs the framework on a Windows agent:
**Checkout -> Setup (venv, pip, npm) -> Run tests (`run_tests.py`) -> publish JUnit results + Allure/PDF/HTML reports**.

Triggers: SCM polling every ~5 min and a nightly run. Failing tests make the build **UNSTABLE** (yellow); reports are still archived.

## 1. Install Jenkins (once, on the demo laptop)

1. Install **JDK 17 or 21** and the **Jenkins LTS** Windows installer (https://www.jenkins.io/download/). Open http://localhost:8080 and finish the setup wizard (suggested plugins).
2. Make sure **Git**, **Python 3.12+** and **Node.js LTS** are on the system `PATH`.
3. Plugins needed: *Pipeline*, *Git*, *JUnit* (all included in "suggested plugins").

## 2. Desktop tests need an interactive agent

A Jenkins *service* runs without a desktop, so Calculator/Notepad/Excel tests cannot see any window.
Two options:

| Goal | What to do |
|------|------------|
| Demo CLI tests only | Run on the built-in node: set the job parameter `AGENT_LABEL` to `built-in` (or add the label `windows` to the built-in node) and `TEST_APP` = `cli`. |
| Demo desktop tests | Create a node: *Manage Jenkins -> Nodes -> New Node* (label `windows`, remote root e.g. `C:\jenkins`, launch method *Launch agent via WebSocket*). While **logged in to Windows**, run the `agent.jar` command shown on the node page in a normal PowerShell window (not as a service) and keep the screen unlocked. |

## 3. Create the job

1. *New Item* -> name `automation-framework` -> **Pipeline** -> OK.
2. *Pipeline* section -> Definition: **Pipeline script from SCM** -> SCM: **Git** -> Repository URL of this repo, branch `*/main`, Script Path `Jenkinsfile`.
3. Save, then run **Build with Parameters** once (the first run registers the parameters and triggers).

Parameters: `AGENT_LABEL`, `TEST_ENV` (qa/dev), `TEST_APP` (cli/calculator/notepad/excel/all), `MARKER` (e.g. `smoke`).

## 4. What to show participants

- **Stage View** - the pipeline stages and timings.
- **Test Result** (JUnit trend) - pass/fail per test, history across builds.
- **Build Artifacts** - `automation_framework/reports/test_report.pdf`, `report.html`, `allure-report/index.html`, logs and failure screenshots.
- Break a test on purpose, push, and watch the next build turn yellow; fix it and watch it turn green.

Tip: Jenkins' default Content-Security-Policy blocks JavaScript in served artifacts, so open the Allure/HTML report after **downloading** the artifact (or use the PDF directly).

## Compared with GitHub Actions

[.github/workflows/automation-ci.yml](.github/workflows/automation-ci.yml) does the same job with YAML on GitHub-hosted runners. Both run the same `run_tests.py`; only the CI syntax differs.
