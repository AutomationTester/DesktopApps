"""
Lab 2 - SOLUTION - Executing Linux commands via Python scripts
==============================================================
1. Detect the OS and pick the right command for each "check"
2. Run each command with a safe helper (timeout, no exceptions escape)
3. Parse output (count files, find ERROR lines, read python version)
4. Save everything to sandbox/lab2_command_log.csv

Run:  python lab2_run_commands.py
"""

import csv
import platform
import shlex
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox"
IS_WINDOWS = platform.system() == "Windows"


def run_command(cmd, timeout=10, shell=False):
    """Run a command; ALWAYS return a dict (never raise)."""
    if isinstance(cmd, str) and not shell:
        cmd = shlex.split(cmd)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=shell)
        return {"returncode": r.returncode, "stdout": r.stdout, "stderr": r.stderr, "error": ""}
    except subprocess.TimeoutExpired:
        return {"returncode": None, "stdout": "", "stderr": "", "error": f"timeout after {timeout}s"}
    except FileNotFoundError:
        return {"returncode": None, "stdout": "", "stderr": "", "error": "command not found"}


def prepare_sandbox():
    """Create a few files to run commands against."""
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
    if IS_WINDOWS:
        checks += [
            ("list files", f'dir /b "{work}"', True),            # dir is a cmd built-in
            ("find ERROR lines", ["findstr", "ERROR", log], False),
            ("current user", ["whoami"], False),
        ]
    else:
        checks += [
            ("list files", ["ls", "-1", str(work)], False),
            ("find ERROR lines", ["grep", "ERROR", log], False),
            ("current user", ["whoami"], False),
        ]
    # Linux tools also available on Windows via Git Bash? Use them as a bonus.
    if IS_WINDOWS and shutil.which("grep"):
        checks.append(("grep via Git Bash", ["grep", "-c", "ERROR", log], False))
    checks.append(("missing tool (negative test)", ["no_such_tool_123"], False))
    return checks


def main():
    work = prepare_sandbox()
    print(f"OS detected: {platform.system()}\n")
    log_rows = []
    for name, cmd, shell in build_checks(work):
        res = run_command(cmd, shell=shell)
        out_lines = res["stdout"].splitlines()
        status = "OK" if res["returncode"] == 0 else "FAILED"

        # --- parse output depending on the check ---------------------------
        detail = res["error"] or (out_lines[0] if out_lines else res["stderr"].strip())
        if name == "list files" and status == "OK":
            detail = f"{len(out_lines)} files: {', '.join(out_lines)}"
        elif name == "find ERROR lines" and status == "OK":
            detail = f"{len(out_lines)} ERROR lines (unique: {sorted(set(out_lines))})"

        print(f"[{status:<6}] {name:<30} rc={res['returncode']}  {detail}")
        log_rows.append({"timestamp": datetime.now().isoformat(timespec="seconds"),
                         "check": name,
                         "command": cmd if isinstance(cmd, str) else " ".join(Path(c).name if c == sys.executable else c for c in cmd),
                         "returncode": res["returncode"], "status": status, "detail": detail})

    out = SANDBOX / "lab2_command_log.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(log_rows[0].keys()))
        writer.writeheader()
        writer.writerows(log_rows)
    print(f"\nLog written to {out.relative_to(HERE)}")


if __name__ == "__main__":
    main()
