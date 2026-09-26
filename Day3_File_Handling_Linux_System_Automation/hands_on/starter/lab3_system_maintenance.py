"""
Lab 3 - STARTER - Automating system-level tasks
===============================================
Build a small "test machine housekeeping" tool with sub-tasks:

  report   - disk usage + size of each sandbox folder        (DONE for you)
  archive  - zip *.log files older than N days into sandbox/lab3/archive/
  cleanup  - delete *.log files older than N days (supports --dry-run)
  backup   - copy sandbox/lab3/results/ to sandbox/lab3/backup/results_<timestamp>/
  process  - check whether given processes are running
  all      - everything above

SAFETY: only ever touch files under sandbox/lab3/ - use safe(path) before
deleting anything.

Run:
  python lab3_system_maintenance.py report
  python lab3_system_maintenance.py all --days 7
  python lab3_system_maintenance.py cleanup --days 3 --dry-run
Search for "# TODO". See hands_on/Lab_Guide.md, Lab 3.
"""

import argparse
import os
import platform
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE / "sandbox" / "lab3"
LOGS = ROOT / "logs"
RESULTS = ROOT / "results"
ARCHIVE = ROOT / "archive"
BACKUP = ROOT / "backup"
DAY = 86400


def safe(path):
    """Guard: only allow paths inside ROOT. (DONE)"""
    path = Path(path).resolve()
    if ROOT.resolve() not in path.parents:
        raise RuntimeError(f"Path outside sandbox: {path}")
    return path


def setup():
    """Create fake logs with different ages. (DONE)"""
    for d in (LOGS, RESULTS, ARCHIVE, BACKUP):
        d.mkdir(parents=True, exist_ok=True)
    now = time.time()
    for i, age in enumerate([0, 2, 4, 6, 9, 12, 20, 45]):
        f = LOGS / f"run_{i + 1:02d}.log"
        f.write_text(f"test run log, age {age} days\n" * 100, encoding="utf-8")
        os.utime(f, (now - age * DAY, now - age * DAY))
    (RESULTS / "results_latest.csv").write_text("test_id,status\nT1,PASS\nT2,FAIL\n", encoding="utf-8")
    (RESULTS / "summary.json").write_text('{"total": 2, "passed": 1}\n', encoding="utf-8")
    print(f"[setup] sample data created in {ROOT.relative_to(HERE)}")


def human(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


def task_report(args):
    """(DONE) - read it to see shutil.disk_usage in action."""
    total, used, free = shutil.disk_usage(ROOT)
    pct = used * 100 / total
    print(f"[report] disk: {human(used)} used of {human(total)} ({pct:.1f}%), free {human(free)}")
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        files = [f for f in d.rglob("*") if f.is_file()]
        print(f"[report]   {d.name:<8} {len(files):>3} files {human(sum(f.stat().st_size for f in files)):>9}")


def old_logs(days):
    # TODO 1: return a sorted list of *.log files in LOGS whose st_mtime is
    #         older than (time.time() - days * DAY)
    raise NotImplementedError("TODO 1: old_logs")


def task_archive(args):
    # TODO 2: copy old_logs(args.days) into a staging folder inside ROOT,
    #         shutil.make_archive(str(ARCHIVE / "logs_<timestamp>"), "zip", root_dir=staging)
    #         then remove the staging folder (shutil.rmtree(safe(staging)))
    raise NotImplementedError("TODO 2: task_archive")


def task_cleanup(args):
    # TODO 3: for each old log: if args.dry_run print "would delete", else safe(f).unlink()
    #         print how many files matched and how many bytes were freed
    raise NotImplementedError("TODO 3: task_cleanup")


def task_backup(args):
    # TODO 4: shutil.copytree(RESULTS, BACKUP / f"results_{timestamp}")
    #         verify: same file names and sizes in source and copy -> print PASS/FAIL
    raise NotImplementedError("TODO 4: task_backup")


def process_running(name):
    # TODO 5: Windows -> tasklist /FI "IMAGENAME eq name.exe" /NH and look for the name
    #         Linux   -> pgrep -x name  (returncode 0 means running)
    raise NotImplementedError("TODO 5: process_running")


def task_process(args):
    for n in args.names:
        print(f"[process] {n:<15} {'RUNNING' if process_running(n) else 'NOT RUNNING'}")


TASKS = {"report": task_report, "archive": task_archive, "cleanup": task_cleanup,
         "backup": task_backup, "process": task_process}


def main():
    parser = argparse.ArgumentParser(description="Lab 3 - system maintenance")
    parser.add_argument("task", choices=list(TASKS) + ["all"])
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--names", nargs="+",
                        default=["python", "explorer"] if platform.system() == "Windows" else ["python3", "bash"])
    args = parser.parse_args()

    if not LOGS.exists():
        setup()
    for name in (TASKS if args.task == "all" else [args.task]):
        try:
            TASKS[name](args)
        except NotImplementedError as todo:
            print(f"[{name}] not finished yet -> {todo}")


if __name__ == "__main__":
    main()
