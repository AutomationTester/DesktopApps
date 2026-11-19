"""
Lab 3 - STARTER: log_analyzer.py - a reusable CLI utility

Target usage (when finished):
    python log_analyzer.py --file app.log
    python log_analyzer.py --file app.log --level ERROR
    python log_analyzer.py --file app.log --level ERROR --count
    python log_analyzer.py --file app.log --summary
    python log_analyzer.py --file app.log --contains timeout -i        (stretch)
    python log_analyzer.py --file app.log --summary --fail-on ERROR    (stretch)

Exit codes:  0 = ok   1 = --fail-on hit   2 = usage error   3 = file error

The sample log 'app.log' is in this folder. Each line looks like:
    2026-09-21 09:00:15,102 ERROR [InvoiceModule] Validation failed: ...
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LINE_RE = re.compile(
    r"^(?P<timestamp>\S+ \S+) (?P<level>[A-Z]+) \[(?P<component>[^\]]+)\] (?P<message>.*)$"
)


def parse_line(line: str):
    """Return a dict with timestamp/level/component/message, or None."""
    match = LINE_RE.match(line.rstrip("\n"))
    return match.groupdict() if match else None


def read_entries(path: Path) -> list:
    # TODO 1: open the file (encoding="utf-8"), parse every line with
    #         parse_line() and return only the entries that are not None
    return []


def filter_entries(entries, level=None):
    # TODO 2: if level is given, keep only entries whose "level" == level
    return entries


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="log_analyzer", description="Filter and summarise application log files."
    )
    # TODO 3: add  -f/--file  (required, type=Path)
    # TODO 4: add  -l/--level (type=str.upper, choices=LEVELS)
    # TODO 5: add  -c/--count (action="store_true")
    # TODO 6: add  -s/--summary (action="store_true")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    print("Parsed:", args)          # remove once everything works

    # TODO 7: if the file does not exist -> print an error to sys.stderr, return 3
    # TODO 8: entries = read_entries(...); selected = filter_entries(...)
    # TODO 9: --summary -> print count per level (use Counter)
    #         --count   -> print only len(selected)
    #         otherwise -> print each selected line
    return 0


if __name__ == "__main__":
    sys.exit(main())
