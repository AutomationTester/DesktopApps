"""
Day 4 - Example 07: AI-assisted debugging - the BEFORE script (buggy + flaky)
=============================================================================
Scenario: a CLI "export job" (the application under test) writes a report
file after a variable delay (0.5 - 2.0 s). The test must check the report
contains TOTAL=42.

This script "works on my machine" sometimes. It contains typical problems
that we will ask an AI coding assistant to find (see ai_prompt_examples.md):

    [ ] fixed time.sleep() instead of waiting for the job/file
    [ ] bare 'except: pass' swallows the real error
    [ ] file handle never closed
    [ ] exact comparison fails because of the trailing newline
    [ ] stale report from a previous run is not deleted (false results)
    [ ] shell=True command string, 'python' instead of sys.executable
    [ ] no logging, no exit code -> CI cannot detect failure
    [ ] magic numbers / hard-coded values

DO NOT copy this style. Run it 3-4 times and observe the inconsistent output.

Run:
    python 07_ai_debugging_before.py
"""
import os
import subprocess
import time

REPORT = os.path.dirname(os.path.abspath(__file__)) + "\\report_before.txt"

JOB = ("import time,random; time.sleep(random.uniform(0.5,2.0)); "
       "open(r'" + REPORT + "','w').write('TOTAL=42\\n')")


def run_export_test():
    subprocess.Popen('python -c "' + JOB + '"', shell=True)
    time.sleep(1)
    try:
        f = open(REPORT)
        data = f.read()
        if data == "TOTAL=42":
            print("PASS")
        else:
            print("FAIL: wrong total")
    except:
        pass
    print("Test finished")


run_export_test()
