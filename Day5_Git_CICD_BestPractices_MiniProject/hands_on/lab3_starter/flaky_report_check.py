"""
flaky_report_check.py - Lab 3 STARTER: a FLAKY automation script. Refactor it!

It starts report_generator.py and checks that the report says "REPORT OK".
Run it 5-10 times: sometimes it passes, sometimes it fails, sometimes it
leaves a hung python.exe behind. Find and fix at least 8 problems.
(Look for the  # SMELL  hints - but not every problem is marked!)

Run (from this folder, Windows):
    python flaky_report_check.py

NOTE: a leftover hung generator is a python.exe started BY THIS SCRIPT. It is
harmless and exits by itself after 60 seconds, but a real suite would pile
these up. Your refactored version must never leave one behind.
"""
import os
import subprocess
import time

OUT = os.getcwd() + "\\output\\report.txt"          # SMELL: cwd-dependent, Windows-only path


def check_report():
    try:
        os.remove(OUT)                               # leftover from the previous run?
    except:                                          # SMELL: bare except
        pass

    # SMELL: shell=True with a string, no timeout, process handle thrown away
    subprocess.Popen("python report_generator.py --out " + OUT, shell=True)

    time.sleep(2)                                    # SMELL: fixed sleep

    try:
        f = open(OUT)                                # SMELL: no encoding, never closed
        content = f.read()
    except:
        print("FAIL - no report")                    # SMELL: print instead of logging, no detail
        return False

    if "REPORT OK" in content:
        print("PASS")
        return True
    print("FAIL - bad content")
    return False


if __name__ == "__main__":
    check_report()                                   # SMELL: exit code is always 0
