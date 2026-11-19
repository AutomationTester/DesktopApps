"""
Lab 3 - SOLUTION: log_analyzer.py - a reusable CLI utility

Examples
    python log_analyzer.py --file app.log
    python log_analyzer.py --file app.log --level ERROR
    python log_analyzer.py --file app.log --level ERROR --count
    python log_analyzer.py --file app.log --level WARNING --min      (WARNING and above)
    python log_analyzer.py --file app.log --summary
    python log_analyzer.py --file app.log --contains timeout -i
    python log_analyzer.py --file app.log --summary --fail-on ERROR  (CI gate)

Exit codes
    0 = ok   1 = --fail-on threshold hit   2 = usage error   3 = file error
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
# 2026-09-21 09:00:15,102 ERROR [InvoiceModule] Validation failed ...
LINE_RE = re.compile(
    r"^(?P<timestamp>\S+ \S+) (?P<level>[A-Z]+) \[(?P<component>[^\]]+)\] (?P<message>.*)$"
)


def parse_line(line: str):
    """Return a dict for a log line, or None if the line does not match."""
    match = LINE_RE.match(line.rstrip("\n"))
    return match.groupdict() if match else None


def read_entries(path: Path) -> list:
    with path.open(encoding="utf-8", errors="replace") as handle:
        return [entry for entry in map(parse_line, handle) if entry]


def filter_entries(entries, level=None, at_least=False, contains=None, ignore_case=False):
    result = entries
    if level:
        if at_least:
            allowed = set(LEVELS[LEVELS.index(level):])
            result = [e for e in result if e["level"] in allowed]
        else:
            result = [e for e in result if e["level"] == level]
    if contains:
        needle = contains.lower() if ignore_case else contains
        result = [
            e for e in result
            if needle in (e["message"].lower() if ignore_case else e["message"])
        ]
    return result


def summarize(entries) -> Counter:
    return Counter(e["level"] for e in entries)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="log_analyzer",
        description="Filter and summarise application log files.",
        epilog="Exit codes: 0 ok, 1 --fail-on hit, 2 usage error, 3 file error",
    )
    parser.add_argument("-f", "--file", required=True, type=Path, help="log file to analyse")
    parser.add_argument("-l", "--level", type=str.upper, choices=LEVELS,
                        help="show only this level (case-insensitive)")
    parser.add_argument("--min", action="store_true",
                        help="with --level: include that level AND all higher levels")
    parser.add_argument("--contains", help="show only lines whose message contains TEXT")
    parser.add_argument("-i", "--ignore-case", action="store_true",
                        help="case-insensitive --contains")
    parser.add_argument("-c", "--count", action="store_true",
                        help="print only the number of matching lines")
    parser.add_argument("-s", "--summary", action="store_true",
                        help="print a count per level")
    parser.add_argument("--fail-on", type=str.upper, choices=LEVELS,
                        help="exit 1 if any line of this level or higher exists")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.min and not args.level:
        parser.error("--min requires --level")

    if not args.file.is_file():
        print(f"ERROR: log file not found: {args.file}", file=sys.stderr)
        return 3

    entries = read_entries(args.file)
    selected = filter_entries(entries, args.level, args.min, args.contains, args.ignore_case)

    if args.summary:
        counts = summarize(selected)
        print(f"Summary for {args.file.name} ({len(selected)} lines)")
        for level in LEVELS:
            print(f"  {level:<9}{counts.get(level, 0):>5}")
    elif args.count:
        print(len(selected))
    else:
        for e in selected:
            print(f"{e['timestamp']} {e['level']:<8} [{e['component']}] {e['message']}")

    if args.fail_on:
        bad = filter_entries(entries, args.fail_on, at_least=True)
        if bad:
            print(f"FAIL: {len(bad)} line(s) at level {args.fail_on} or higher",
                  file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
