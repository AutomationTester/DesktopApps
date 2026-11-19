# Mini Project - Starter Kit

Skeleton files for the Day 5 capstone (see `../Mini_Project.md` for the full brief).
Copy them into **your own copy** of `automation_framework/` (your personal GitHub repo),
work on a feature branch, and replace every `TODO`.

| Starter file | Copy to | State |
|---|---|---|
| `workflows/__init__.py` | `automation_framework/workflows/` | complete |
| `workflows/mini_project_settings.py` | `automation_framework/workflows/` | complete (config reader with defaults) |
| `workflows/calc_to_notepad.py` | `automation_framework/workflows/` | **TODO** - helpers + GUI steps |
| `pages/report_notepad_page.py` | `automation_framework/pages/` | **TODO** - 3 new page methods |
| `tools/log_archiver_cli.py` | `automation_framework/tools/` | **TODO** - parser done, commands to implement |
| `tests/test_workflow_helpers.py` | `automation_framework/tests/` | complete tests (test-first) - make them pass |
| `tests/test_log_archiver_cli.py` | `automation_framework/tests/` | 2 example tests, 5 **TODO** tests |
| `tests/test_e2e_calc_to_notepad.py` | `automation_framework/tests/` | **TODO** - end-to-end desktop test |
| `test_data/expressions.csv` | `automation_framework/test_data/` | complete (dev data) |
| `config/mini_project_config_snippet.yaml` | merge into `automation_framework/config/config.yaml` | **TODO** for qa |

```bash
git switch -c feature/mini-project
SOL=path/to/Day5_Git_CICD_BestPractices_MiniProject/hands_on/mini_project_starter
cp -r "$SOL/workflows" automation_framework/
cp "$SOL"/pages/*.py automation_framework/pages/
cp "$SOL"/tools/*.py automation_framework/tools/
cp "$SOL"/tests/*.py automation_framework/tests/
cp "$SOL"/test_data/*.csv automation_framework/test_data/

cd automation_framework
pytest -m cli -v                 # right now: helper tests FAIL (NotImplementedError), TODO tests SKIP
```

Your goal: `pytest -m cli --env qa` all green, `pytest -m desktop --env dev` green on a Windows
desktop, no `pytest.skip("TODO")` left, CI green on GitHub.
