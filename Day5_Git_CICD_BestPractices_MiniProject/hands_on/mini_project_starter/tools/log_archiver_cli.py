"""
STARTER - log_archiver_cli: system task automation tool (mini project part B).

Usage (to be implemented):
    python tools/log_archiver_cli.py collect --output DIR
    python tools/log_archiver_cli.py archive --source DIR --dest DIR [--pattern "*.log"] [--keep N]
    python tools/log_archiver_cli.py --version

Exit codes (the tool's contract - your tests must verify them):
    0 = success
    1 = nothing to do (no files matched the pattern)
    2 = usage error / source folder not found

The argument parser is done for you. Implement the TODOs.
Look at tools/sysinfo_cli.py for ideas (platform, socket, shutil.disk_usage).
"""
import argparse
import json          # noqa: F401
import os            # noqa: F401
import platform      # noqa: F401
import shutil        # noqa: F401
import socket        # noqa: F401
import sys
import zipfile       # noqa: F401
from datetime import datetime
from pathlib import Path  # noqa: F401

VERSION = "1.0.0"
EXIT_OK, EXIT_NOTHING_TO_DO, EXIT_USAGE = 0, 1, 2
ARCHIVE_PREFIX = "logs_"


def _timestamp():
    # microseconds -> two runs in the same second still get unique, sortable names
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def collect_system_info():
    """Return a dict: collected_at, os, os_release, machine, python, hostname, cpu_count, disk_free_gb."""
    # TODO
    raise NotImplementedError


def cmd_collect(args):
    # TODO: create args.output folder, write sysinfo_<timestamp>.json, print "collected: <path>"
    raise NotImplementedError


def prune_archives(dest, keep):
    """Delete the oldest logs_*.zip in dest so only the newest `keep` remain. Return deleted names."""
    # TODO: hint - names contain a timestamp, so sorted() == oldest first
    raise NotImplementedError


def cmd_archive(args):
    # TODO:
    #   1. source folder missing            -> message on stderr, return EXIT_USAGE
    #   2. --keep given but < 1             -> stderr, EXIT_USAGE
    #   3. no files match args.pattern      -> "WARNING: no files matching ..." on stderr, EXIT_NOTHING_TO_DO
    #   4. zip the files into dest/logs_<timestamp>.zip (arcname = file name only)
    #   5. print "archived: <n> files -> <zip path>"
    #   6. if --keep: prune_archives and print "pruned: <name>" for each
    raise NotImplementedError


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
