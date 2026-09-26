"""
Lab 3 - SOLUTION - Automating system-level tasks
================================================
A small "test machine housekeeping" tool:

  report   - disk usage of the drive + size of each sandbox folder
  archive  - zip *.log files older than N days into sandbox/archive/
  cleanup  - delete *.log files older than N days (supports --dry-run)
  backup   - copy sandbox/results/ to sandbox/backup/results_<timestamp>/
  process  - check whether given processes are running
  all      - everything above, in order

Everything happens under  sandbox/lab3/  which the script creates with fake
data (--setup is automatic when the folder does not exist).

Run:
  python lab3_system_maintenance.py all --days 7
  python lab3_system_maintenance.py cleanup --days 3 --dry-run
  python lab3_system_maintenance.py process --names python explorer
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
    """Guard: only allow paths inside ROOT."""
    path = Path(path).resolve()
    if ROOT.resolve() not in path.parents:
        raise RuntimeError(f"Path outside sandbox: {path}")
    return path


def setup():
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


def old_logs(days):
    cutoff = time.time() - days * DAY
    return sorted(p for p in LOGS.glob("*.log") if p.stat().st_mtime < cutoff)


def task_report(args):
    total, used, free = shutil.disk_usage(ROOT)
    pct = used * 100 / total
    flag = "ALERT" if pct > args.threshold else "OK"
    print(f"[report] disk: {human(used)} used of {human(total)} ({pct:.1f}%), free {human(free)} -> {flag}")
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        files = [f for f in d.rglob("*") if f.is_file()]
        print(f"[report]   {d.name:<8} {len(files):>3} files {human(sum(f.stat().st_size for f in files)):>9}")


def task_archive(args):
    files = old_logs(args.days)
    if not files:
        print(f"[archive] no logs older than {args.days} days")
        return
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    staging = safe(ROOT / f"_staging_{stamp}")
    staging.mkdir()
    for f in files:
        shutil.copy2(f, staging)
    fmt = "zip" if platform.system() == "Windows" else "gztar"   # .zip or .tar.gz
    archive = shutil.make_archive(str(ARCHIVE / f"logs_{stamp}"), fmt, root_dir=staging)
    shutil.rmtree(staging)
    print(f"[archive] {len(files)} logs -> {Path(archive).name}")


def task_cleanup(args):
    files = old_logs(args.days)
    freed = 0
    for f in files:
        size = f.stat().st_size
        if args.dry_run:
            print(f"[cleanup] DRY RUN would delete {f.name}")
        else:
            safe(f).unlink()
            freed += size
            print(f"[cleanup] deleted {f.name}")
    print(f"[cleanup] {len(files)} file(s) matched, freed {human(freed)}"
          f"{' (nothing deleted - dry run)' if args.dry_run else ''}")


def task_backup(args):
    target = BACKUP / f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copytree(RESULTS, target)
    src = {p.name: p.stat().st_size for p in RESULTS.iterdir()}
    dst = {p.name: p.stat().st_size for p in target.iterdir()}
    print(f"[backup] {len(dst)} files -> {target.name}  verify={'PASS' if src == dst else 'FAIL'}")
    # Keep only the 3 newest backups (retention policy)
    backups = sorted(BACKUP.glob("results_*"))
    for old in backups[:-3]:
        shutil.rmtree(safe(old))
        print(f"[backup] retention: removed {old.name}")


def process_running(name):
    if platform.system() == "Windows":
        exe = name if name.lower().endswith(".exe") else name + ".exe"
        out = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {exe}", "/NH"],
                             capture_output=True, text=True).stdout
        return exe.lower() in out.lower()
    # Linux: pgrep returns 0 if a matching process exists
    return subprocess.run(["pgrep", "-x", name], capture_output=True).returncode == 0


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
    parser.add_argument("--threshold", type=float, default=90.0, help="disk usage alert %%")
    parser.add_argument("--names", nargs="+",
                        default=["python", "explorer"] if platform.system() == "Windows" else ["python3", "bash"])
    parser.add_argument("--reset", action="store_true", help="recreate sample data")
    args = parser.parse_args()

    if args.reset and ROOT.exists():
        shutil.rmtree(ROOT)
    if not LOGS.exists():
        setup()

    for name in (TASKS if args.task == "all" else [args.task]):
        TASKS[name](args)


if __name__ == "__main__":
    main()
