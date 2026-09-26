"""
10_system_tasks.py
==================
Day 3 - Automating system-level tasks (the daily chores of an automation
engineer on a test machine / CI agent / Linux server).

Tasks
-----
  1. Disk usage report            shutil.disk_usage + folder size walk
  2. Archive old logs             shutil.make_archive (zip / tar.gz)
  3. Clean up files older than N days (with --dry-run preview)
  4. Back up a folder             shutil.copytree into a timestamped folder
  5. Check whether a process is running   (tasklist on Windows, ps on Linux)

SAFETY: everything happens inside  examples/sandbox/system_tasks/  which this
script creates and fills with fake log files. Nothing outside that folder is
ever modified or deleted. Deletion code double-checks the path is inside
the sandbox before removing anything.

Run:
  python 10_system_tasks.py              (all tasks)
  python 10_system_tasks.py --days 5     (treat files older than 5 days as old)
  python 10_system_tasks.py --dry-run    (show what WOULD be deleted)
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
SANDBOX = HERE / "sandbox" / "system_tasks"
LOG_DIR = SANDBOX / "logs"
DATA_DIR = SANDBOX / "test_data"
ARCHIVE_DIR = SANDBOX / "archives"
BACKUP_DIR = SANDBOX / "backups"
DAY = 24 * 60 * 60


def assert_in_sandbox(path):
    """Refuse to touch anything outside the sandbox - a cheap safety net."""
    path = Path(path).resolve()
    if SANDBOX.resolve() not in path.parents and path != SANDBOX.resolve():
        raise RuntimeError(f"Refusing to modify path outside sandbox: {path}")


def human(n_bytes):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n_bytes < 1024:
            return f"{n_bytes:.1f} {unit}"
        n_bytes /= 1024
    return f"{n_bytes:.1f} PB"


def setup_sample_files():
    """Create fake log files with different ages (by changing modified time)."""
    for d in (LOG_DIR, DATA_DIR, ARCHIVE_DIR, BACKUP_DIR):
        d.mkdir(parents=True, exist_ok=True)
    now = time.time()
    for age_days in (0, 1, 3, 8, 15, 30):
        f = LOG_DIR / f"app_{age_days:02d}d_old.log"
        f.write_text(f"fake log written {age_days} days ago\n" * 200, encoding="utf-8")
        mtime = now - age_days * DAY
        os.utime(f, (mtime, mtime))          # set access & modified time
    (DATA_DIR / "users.csv").write_text("id,name\n1,alice\n2,bob\n", encoding="utf-8")
    (DATA_DIR / "config.yaml").write_text("env: qa\n", encoding="utf-8")
    print(f"[SETUP] Sample files created under {SANDBOX.relative_to(HERE)}")


# ---------------------------------------------------------------------------
def disk_usage_report(threshold_pct=90):
    print("\n=== 1. Disk usage report ===")
    total, used, free = shutil.disk_usage(HERE)   # drive/partition containing this folder
    pct = used / total * 100
    print(f"Drive of {HERE.anchor or '/'}: total={human(total)} used={human(used)} "
          f"free={human(free)} ({pct:.1f}% used)")
    status = "WARNING" if pct >= threshold_pct else "OK"
    print(f"Threshold {threshold_pct}% -> {status}")

    # Size of each sandbox sub-folder (like 'du -sh *' on Linux)
    for folder in sorted(p for p in SANDBOX.iterdir() if p.is_dir()):
        size = sum(f.stat().st_size for f in folder.rglob("*") if f.is_file())
        print(f"  {folder.name:<12} {human(size):>10}")


def find_old_files(folder, days, pattern="*.log"):
    cutoff = time.time() - days * DAY
    return sorted(f for f in folder.glob(pattern) if f.is_file() and f.stat().st_mtime < cutoff)


def archive_old_logs(days):
    print(f"\n=== 2. Archive logs older than {days} days ===")
    old = find_old_files(LOG_DIR, days)
    if not old:
        print("Nothing to archive.")
        return None
    # Copy old logs to a staging folder, then zip that folder
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    staging = SANDBOX / f"staging_{stamp}"
    staging.mkdir()
    for f in old:
        shutil.copy2(f, staging / f.name)    # copy2 keeps timestamps
    archive = shutil.make_archive(str(ARCHIVE_DIR / f"old_logs_{stamp}"), "zip", root_dir=staging)
    assert_in_sandbox(staging)
    shutil.rmtree(staging)
    print(f"Archived {len(old)} files -> {Path(archive).relative_to(HERE)}")
    # On Linux you would often use "gztar" -> .tar.gz
    return old


def cleanup_old_files(days, dry_run):
    print(f"\n=== 3. Clean up logs older than {days} days {'(DRY RUN)' if dry_run else ''} ===")
    old = find_old_files(LOG_DIR, days)
    for f in old:
        age = (time.time() - f.stat().st_mtime) / DAY
        if dry_run:
            print(f"  would delete {f.name}  ({age:.0f} days old)")
        else:
            assert_in_sandbox(f)
            f.unlink()
            print(f"  deleted {f.name}  ({age:.0f} days old)")
    remaining = [f.name for f in LOG_DIR.glob("*.log")]
    print(f"Remaining logs: {remaining}")


def backup_folder():
    print("\n=== 4. Back up the test_data folder ===")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = BACKUP_DIR / f"test_data_{stamp}"
    shutil.copytree(DATA_DIR, target)
    copied = [p.name for p in target.iterdir()]
    print(f"Copied {len(copied)} files -> {target.relative_to(HERE)}  {copied}")
    # Verify the backup: same file names and sizes
    ok = all((target / f.name).stat().st_size == f.stat().st_size for f in DATA_DIR.iterdir())
    print(f"Backup verification: {'PASS' if ok else 'FAIL'}")


def is_process_running(name):
    """Return True if a process with this name is running. Cross-platform."""
    if platform.system() == "Windows":
        # tasklist /FI "IMAGENAME eq python.exe" /NH  -> one line per process
        r = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {name}", "/NH"],
                           capture_output=True, text=True)
        return name.lower() in r.stdout.lower()
    # Linux/macOS: 'ps -e -o comm=' lists just the command names
    r = subprocess.run(["ps", "-e", "-o", "comm="], capture_output=True, text=True)
    return any(Path(line.strip()).name == name for line in r.stdout.splitlines())


def check_processes():
    print("\n=== 5. Check processes / services ===")
    if platform.system() == "Windows":
        names = ["python.exe", "explorer.exe", "notarealapp.exe"]
    else:
        names = ["python3", "bash", "notarealapp"]
    for n in names:
        print(f"  {n:<18} {'RUNNING' if is_process_running(n) else 'NOT RUNNING'}")
    print("  (Linux services: 'systemctl is-active sshd' returns 0 when active)")


def main():
    parser = argparse.ArgumentParser(description="System-level automation tasks")
    parser.add_argument("--days", type=int, default=7, help="age threshold in days")
    parser.add_argument("--dry-run", action="store_true", help="preview cleanup only")
    args = parser.parse_args()

    setup_sample_files()
    disk_usage_report()
    archive_old_logs(args.days)
    cleanup_old_files(args.days, args.dry_run)
    backup_folder()
    check_processes()
    print("\nAll tasks finished. Inspect examples/sandbox/system_tasks/ to see the results.")


if __name__ == "__main__":
    main()
