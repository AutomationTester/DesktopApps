"""
log_archiver_cli - system task automation tool (mini project part B).

Collects system information and archives log files - the kind of housekeeping job
a test lab runs every night after the regression suite.

Usage:
    python tools/log_archiver_cli.py collect --output DIR
    python tools/log_archiver_cli.py archive --source DIR --dest DIR [--pattern "*.log"] [--keep N]
    python tools/log_archiver_cli.py --version

Exit codes (the tool's contract, verified by tests/test_log_archiver_cli.py):
    0 = success
    1 = nothing to do (no files matched the pattern)
    2 = usage error / source folder not found
"""
import argparse
import json
import os
import platform
import shutil
import socket
import sys
import zipfile
from datetime import datetime
from pathlib import Path

VERSION = "1.0.0"
EXIT_OK, EXIT_NOTHING_TO_DO, EXIT_USAGE = 0, 1, 2
ARCHIVE_PREFIX = "logs_"


def _timestamp():
    # microseconds -> two runs in the same second still get unique, sortable names
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def collect_system_info():
    disk = shutil.disk_usage(Path.cwd().anchor or os.sep)
    return {
        "collected_at": datetime.now().isoformat(timespec="seconds"),
        "os": platform.system(),
        "os_release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "hostname": socket.gethostname(),
        "cpu_count": os.cpu_count(),
        "disk_free_gb": round(disk.free / 1024 ** 3, 1),
    }


def cmd_collect(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    info = collect_system_info()
    target = output / f"sysinfo_{_timestamp()}.json"
    target.write_text(json.dumps(info, indent=2), encoding="utf-8")
    print(f"collected: {target}")
    return EXIT_OK


def prune_archives(dest, keep):
    """Delete the oldest archives so only the newest `keep` remain. Returns deleted names."""
    archives = sorted(dest.glob(f"{ARCHIVE_PREFIX}*.zip"))
    doomed = archives[:max(0, len(archives) - keep)]
    for old in doomed:
        old.unlink()
    return [p.name for p in doomed]


def cmd_archive(args):
    source, dest = Path(args.source), Path(args.dest)
    if not source.is_dir():
        print(f"ERROR: source folder not found: {source}", file=sys.stderr)
        return EXIT_USAGE
    if args.keep is not None and args.keep < 1:
        print("ERROR: --keep must be 1 or more", file=sys.stderr)
        return EXIT_USAGE

    files = sorted(p for p in source.glob(args.pattern) if p.is_file())
    if not files:
        print(f"WARNING: no files matching '{args.pattern}' in {source}", file=sys.stderr)
        return EXIT_NOTHING_TO_DO

    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / f"{ARCHIVE_PREFIX}{_timestamp()}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, arcname=f.name)
    print(f"archived: {len(files)} files -> {archive}")

    if args.keep is not None:
        for name in prune_archives(dest, args.keep):
            print(f"pruned: {name}")
    return EXIT_OK


def build_parser():
    parser = argparse.ArgumentParser(prog="log_archiver_cli",
                                     description="Collect system info and archive log files")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_collect = sub.add_parser("collect", help="write system information to a JSON file")
    p_collect.add_argument("--output", required=True, help="folder for sysinfo_<timestamp>.json")
    p_collect.set_defaults(func=cmd_collect)

    p_archive = sub.add_parser("archive", help="zip matching files from SOURCE into DEST")
    p_archive.add_argument("--source", required=True, help="folder that contains the logs")
    p_archive.add_argument("--dest", required=True, help="folder for logs_<timestamp>.zip")
    p_archive.add_argument("--pattern", default="*.log", help="glob pattern (default: *.log)")
    p_archive.add_argument("--keep", type=int, help="keep only the newest N archives in DEST")
    p_archive.set_defaults(func=cmd_archive)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
