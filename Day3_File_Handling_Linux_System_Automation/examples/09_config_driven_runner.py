"""
09_config_driven_runner.py
==========================
Day 3 - Configuration-driven execution using JSON/YAML.

Instead of hard-coding which commands to run, we describe them in a config
file (config/commands.yaml or config/commands.json). The runner:

  1. loads the YAML/JSON file (format chosen by file extension)
  2. filters checks by OS and by --tag
  3. runs each command with subprocess (with timeout)
  4. compares return code / stdout / stderr with the expectations
  5. prints a PASS/FAIL/SKIP table and writes a JSON report

A tester can add new checks WITHOUT touching Python code.

Run:
  python 09_config_driven_runner.py
  python 09_config_driven_runner.py --config config/commands.json
  python 09_config_driven_runner.py --tag smoke
  python 09_config_driven_runner.py --report sandbox/my_report.json
Exit code: 0 if everything passed, 1 otherwise (CI friendly).
"""

import argparse
import json
import platform
import shlex
import subprocess
import sys
import time
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
DEFAULT_CONFIG = HERE / "config" / "commands.yaml"
DEFAULT_REPORT = HERE / "sandbox" / "command_report.json"
CURRENT_OS = "windows" if platform.system() == "Windows" else "linux"


def load_config(path):
    path = Path(path)
    with open(path, encoding="utf-8") as f:
        if path.suffix.lower() in (".yaml", ".yml"):
            data = yaml.safe_load(f)
        elif path.suffix.lower() == ".json":
            data = json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {path.suffix}")
    if not isinstance(data, dict) or "checks" not in data:
        raise ValueError("Config must contain a top-level 'checks' list")
    return data


def build_command(raw):
    """Accept a string or list; substitute {python}; return a list for subprocess."""
    # posix=False on Windows keeps backslashes in paths intact
    parts = shlex.split(raw, posix=(CURRENT_OS != "windows")) if isinstance(raw, str) else list(raw)
    return [p.replace("{python}", sys.executable) for p in parts]


def run_check(check, default_timeout):
    """Run one check and return a result dict with status PASS/FAIL/SKIP."""
    name = check["name"]
    target_os = check.get("os", "any")
    if target_os not in ("any", CURRENT_OS):
        return {"name": name, "status": "SKIP", "reason": f"only for {target_os}", "duration": 0}

    cmd = build_command(check["command"])
    timeout = check.get("timeout", default_timeout)
    expected_rc = check.get("expected_returncode", 0)
    start = time.perf_counter()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"name": name, "status": "FAIL", "reason": f"timed out after {timeout}s",
                "duration": round(time.perf_counter() - start, 2)}
    except FileNotFoundError:
        return {"name": name, "status": "FAIL", "reason": f"command not found: {cmd[0]}",
                "duration": round(time.perf_counter() - start, 2)}

    problems = []
    if r.returncode != expected_rc:
        problems.append(f"returncode {r.returncode} != expected {expected_rc}")
    if "expect_stdout_contains" in check and check["expect_stdout_contains"] not in r.stdout:
        problems.append(f"stdout missing '{check['expect_stdout_contains']}'")
    if "expect_stderr_contains" in check and check["expect_stderr_contains"] not in r.stderr:
        problems.append(f"stderr missing '{check['expect_stderr_contains']}'")

    return {
        "name": name,
        "status": "FAIL" if problems else "PASS",
        "reason": "; ".join(problems) or "ok",
        "returncode": r.returncode,
        "stdout": r.stdout.strip()[:200],     # keep reports small
        "stderr": r.stderr.strip()[:200],
        "duration": round(time.perf_counter() - start, 2),
    }


def main():
    parser = argparse.ArgumentParser(description="Run CLI checks described in YAML/JSON")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--tag", help="only run checks having this tag")
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = HERE / config_path
    config = load_config(config_path)
    settings = config.get("settings", {})
    default_timeout = settings.get("default_timeout", 30)
    stop_on_fail = settings.get("stop_on_first_failure", False)

    checks = config["checks"]
    if args.tag:
        checks = [c for c in checks if args.tag in c.get("tags", [])]
    print(f"Config: {config_path.name} | OS: {CURRENT_OS} | checks selected: {len(checks)}\n")

    results = []
    for check in checks:
        res = run_check(check, default_timeout)
        results.append(res)
        print(f"[{res['status']:<4}] {res['name']:<60} {res['reason']}")
        if stop_on_fail and res["status"] == "FAIL":
            print("stop_on_first_failure is set - stopping.")
            break

    summary = {s: sum(r["status"] == s for r in results) for s in ("PASS", "FAIL", "SKIP")}
    report_path = Path(args.report)
    if not report_path.is_absolute():
        report_path = HERE / report_path
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({"config": config_path.name, "os": CURRENT_OS, "summary": summary,
                   "results": results}, f, indent=2)

    print(f"\nSummary: {summary}")
    print(f"JSON report: {report_path}")
    sys.exit(0 if summary["FAIL"] == 0 else 1)


if __name__ == "__main__":
    main()
