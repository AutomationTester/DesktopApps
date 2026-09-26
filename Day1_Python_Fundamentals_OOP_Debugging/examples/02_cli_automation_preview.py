"""
Example 02 - Desktop & CLI Automation Preview
==============================================
Day 1 | Topic: Introduction to Python and automation use cases,
               Desktop & CLI automation overview

How to run:
    python 02_cli_automation_preview.py

What this shows:
    * Python can talk to the operating system (OS) using the
      standard library - no extra installation needed.
    * CLI automation = running command-line tools from a script and
      checking their output automatically (exactly what a tester does
      by hand in a terminal).
    * This is SAFE: it only reads information and runs "python --version".
      It does NOT open any window or move the mouse.

Desktop GUI automation (pywinauto, pyautogui) is covered from Day 2 onwards.
"""

import os            # operating-system helpers (folders, environment)
import platform      # information about the machine
import subprocess    # run other programs / commands
import sys           # information about the running Python
from datetime import datetime

print("=" * 55)
print(" AUTOMATION PREVIEW - collecting test environment info")
print("=" * 55)

# ---------------------------------------------------------------
# 1. Environment details - testers put these in every test report
# ---------------------------------------------------------------
print("Run started at   :", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("Operating system :", platform.system(), platform.release())
print("Machine name     :", platform.node())
print("Python version   :", platform.python_version())
print("Current folder   :", os.getcwd())

# ---------------------------------------------------------------
# 2. CLI automation - run a command and CHECK its result
#    Manual tester: opens terminal, types "python --version", reads output.
#    Automation   : the script does the same and verifies it.
# ---------------------------------------------------------------
print()
print("CLI TEST: 'python --version' should succeed and mention 'Python'")

# sys.executable = full path of the python that is running this script
result = subprocess.run(
    [sys.executable, "--version"],   # the command and its argument
    capture_output=True,             # collect what the command prints
    text=True,                       # give us normal strings, not bytes
)

output = (result.stdout or result.stderr).strip()
print("  Exit code :", result.returncode)   # 0 means success on all OSes
print("  Output    :", output)

if result.returncode == 0 and "Python" in output:
    print("  Result    : PASS")
else:
    print("  Result    : FAIL")

# ---------------------------------------------------------------
# 3. File-system automation - list the demo scripts in this folder
# ---------------------------------------------------------------
print()
this_folder = os.path.dirname(os.path.abspath(__file__))
scripts = [name for name in sorted(os.listdir(this_folder)) if name.endswith(".py")]
print(f"Found {len(scripts)} Python demo scripts in the examples folder.")
print("First three:", scripts[:3])

print()
print("Where Python automation is used in testing:")
use_cases = [
    "Desktop GUI testing   (pywinauto, pyautogui)",
    "CLI / batch testing   (subprocess)",
    "Test data generation  (csv, json, random)",
    "Log and report checks (file reading, re)",
    "API and web testing   (requests, selenium, playwright)",
]
for number, case in enumerate(use_cases, start=1):
    print(f"  {number}. {case}")
