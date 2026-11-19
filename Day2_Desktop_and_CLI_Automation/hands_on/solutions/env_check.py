"""
Lab 5 (extra) - SOLUTION: env_check.py - pre-test environment check with subprocess

Before a test run, a CI job should confirm the machine is ready.

    python env_check.py
    python env_check.py --min-python 3.10 --tools python where notepad.exe
    python env_check.py --report env_report.txt
    python env_check.py --tools git nosuchtool          (-> FAIL, exit 1)

Checks
    1. Python version >= --min-python        (subprocess: python --version)
    2. Every tool in --tools is on the PATH   (subprocess: where <tool>)
    3. pip packages importable                (subprocess: python -c "import x")
    4. Network info collected as evidence     (subprocess: ipconfig)
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run(cmd: list, timeout: int = 30) -> subprocess.CompletedProcess:
    """Run a command, never raise for non-zero exit; raise only on timeout."""
    return subprocess.run(cmd, capture_output=True, text=True,
                          timeout=timeout, errors="replace")


def check_python(min_version: str) -> tuple:
    result = run([sys.executable, "--version"])
    version_text = (result.stdout or result.stderr).strip()        # 'Python 3.14.7'
    current = tuple(int(p) for p in version_text.split()[1].split(".")[:2])
    wanted = tuple(int(p) for p in min_version.split(".")[:2])
    return current >= wanted, f"{version_text} (need >= {min_version})"


def check_tool(tool: str) -> tuple:
    try:
        result = run(["where", tool])
    except FileNotFoundError:
        return False, "'where' command not available"
    if result.returncode == 0:
        return True, result.stdout.splitlines()[0]
    return False, "not found on PATH"


def check_package(package: str) -> tuple:
    result = run([sys.executable, "-c", f"import {package}"])
    return result.returncode == 0, "importable" if result.returncode == 0 else "NOT installed"


def collect_ipv4() -> str:
    try:
        result = run(["ipconfig"])
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "(ipconfig unavailable)"
    ips = [l.split(":", 1)[1].strip() for l in result.stdout.splitlines() if "IPv4" in l]
    return ", ".join(ips) or "(none)"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check that this machine is ready for testing.")
    parser.add_argument("--min-python", default="3.10", help="minimum Python version (default 3.10)")
    parser.add_argument("--tools", nargs="+", default=["python", "notepad.exe", "calc.exe"],
                        help="executables that must be on the PATH")
    parser.add_argument("--packages", nargs="+", default=["pywinauto", "pyautogui"],
                        help="Python packages that must be importable")
    parser.add_argument("--report", type=Path, help="also write the report to this file")
    args = parser.parse_args(argv)

    lines = [f"Environment check - {datetime.now():%Y-%m-%d %H:%M:%S}"]
    all_ok = True

    def record(ok: bool, name: str, detail: str) -> None:
        nonlocal all_ok
        all_ok &= ok
        lines.append(f"[{'PASS' if ok else 'FAIL'}] {name:<22} {detail}")

    ok, detail = check_python(args.min_python)
    record(ok, "python version", detail)
    for tool in args.tools:
        ok, detail = check_tool(tool)
        record(ok, f"tool: {tool}", detail)
    for package in args.packages:
        ok, detail = check_package(package)
        record(ok, f"package: {package}", detail)
    lines.append(f"[INFO] IPv4 addresses         {collect_ipv4()}")
    lines.append("OVERALL: " + ("PASS" if all_ok else "FAIL"))

    report = "\n".join(lines)
    print(report)
    if args.report:
        args.report.write_text(report + "\n", encoding="utf-8")
        print(f"Report written to {args.report}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
