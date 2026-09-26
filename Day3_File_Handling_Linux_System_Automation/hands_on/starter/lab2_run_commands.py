"""
Lab 2 - STARTER - Executing Linux commands via Python scripts
=============================================================
1. Detect the OS and pick the right command for each "check"
2. Run each command with a safe helper (timeout, no exceptions escape)
3. Parse output (count files, count ERROR lines)
4. Save everything to sandbox/lab2_command_log.csv

Run:  python lab2_run_commands.py
Search for "# TODO". See hands_on/Lab_Guide.md, Lab 2.
"""

import csv
import platform
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox"
IS_WINDOWS = platform.system() == "Windows"


def run_command(cmd, timeout=10, shell=False):
    """Run a command; ALWAYS return a dict (never raise).

    Return keys: returncode, stdout, stderr, error
    """
    if isinstance(cmd, str) and not shell:
        cmd = shlex.split(cmd)
    # TODO 1: call subprocess.run with capture_output=True, text=True, timeout, shell
    # TODO 2: catch subprocess.TimeoutExpired -> error "timeout after Ns", returncode None
    #         catch FileNotFoundError        -> error "command not found", returncode None
    raise NotImplementedError("TODO 1/2: run_command")


def prepare_sandbox():
    """Create a few files to run commands against. (DONE)"""
    work = SANDBOX / "lab2_work"
    work.mkdir(parents=True, exist_ok=True)
    (work / "service.log").write_text(
        "INFO start\nERROR disk full\nINFO retry\nERROR disk full\nWARN slow\n", encoding="utf-8")
    for name in ("a.txt", "b.txt", "c.csv"):
        (work / name).write_text("sample\n", encoding="utf-8")
    return work


def build_checks(work):
    """Return a list of (name, command, shell) tuples appropriate for this OS."""
    log = str(work / "service.log")
    checks = [("python version", [sys.executable, "--version"], False)]
    # TODO 3: add OS-specific checks
    #   Windows: ("list files", f'dir /b "{work}"', True)      <- dir needs shell=True
    #            ("find ERROR lines", ["findstr", "ERROR", log], False)
    #   Linux  : ("list files", ["ls", "-1", str(work)], False)
    #            ("find ERROR lines", ["grep", "ERROR", log], False)
    #   Both   : ("current user", ["whoami"], False)
    # TODO 4: add a negative test: ("missing tool (negative test)", ["no_such_tool_123"], False)
    return checks


def main():
    work = prepare_sandbox()
    print(f"OS detected: {platform.system()}\n")
    log_rows = []
    try:
        for name, cmd, shell in build_checks(work):
            res = run_command(cmd, shell=shell)
            status = "OK" if res["returncode"] == 0 else "FAILED"
            out_lines = res["stdout"].splitlines()
            detail = res["error"] or (out_lines[0] if out_lines else res["stderr"].strip())
            # TODO 5: for "list files" show how many files; for "find ERROR lines"
            #         show how many ERROR lines were found
            print(f"[{status:<6}] {name:<30} rc={res['returncode']}  {detail}")
            log_rows.append({"timestamp": datetime.now().isoformat(timespec="seconds"),
                             "check": name, "returncode": res["returncode"],
                             "status": status, "detail": detail})
    except NotImplementedError as todo:
        print(f"Not finished yet -> {todo}")
        return

    # TODO 6: write log_rows to SANDBOX / "lab2_command_log.csv" with csv.DictWriter
    print("\nTODO 6: write the CSV log")


if __name__ == "__main__":
    main()
