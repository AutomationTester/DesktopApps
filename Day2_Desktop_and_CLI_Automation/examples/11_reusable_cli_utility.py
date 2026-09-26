"""
11_reusable_cli_utility.py  -  "testkit"
========================================
Day 2 - Writing a REUSABLE command-line utility (argparse sub-commands)

A small Swiss-army knife for testers. Sub-commands (like 'git commit',
'git push'):

    sysinfo   show OS / Python / machine details (evidence for bug reports)
    disk      show free disk space and FAIL if below a threshold
    search    search text (or regex) in files, e.g. find ERRORs in logs
    which     check that required tools are on the PATH (pre-test check)

TRY THESE
    python 11_reusable_cli_utility.py --help
    python 11_reusable_cli_utility.py sysinfo
    python 11_reusable_cli_utility.py disk --min-free-gb 5
    python 11_reusable_cli_utility.py search ERROR ..\\hands_on\\starter\\app.log
    python 11_reusable_cli_utility.py search "time(out|d out)" ..\\hands_on\\starter\\app.log --regex -i --count
    python 11_reusable_cli_utility.py which python notepad.exe git
    echo $LASTEXITCODE          (PowerShell - see the exit code)

WHAT MAKES A CLI UTILITY "REUSABLE"
    1. Logic lives in FUNCTIONS that return data (importable from pytest or
       other scripts: `from testkit import search_files`).
    2. main() only parses arguments and prints -> thin wrapper.
    3. Meaningful EXIT CODES so CI pipelines can react:
         0 = success / found   1 = check failed / nothing found
         2 = usage error (argparse)   3 = file problem
    4. Good --help text, sensible defaults, no hard-coded paths.
    5. `if __name__ == "__main__":` guard so importing does not run it.
"""

import argparse
import platform
import re
import shutil
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_CHECK_FAILED = 1
EXIT_USAGE = 2
EXIT_FILE_ERROR = 3


# ---------------------------------------------------------------------------
# Reusable functions (no printing, no sys.exit - easy to unit test)
# ---------------------------------------------------------------------------
def get_system_info() -> dict:
    return {
        "os": f"{platform.system()} {platform.release()} ({platform.version()})",
        "machine": platform.machine(),
        "computer": platform.node(),
        "python": platform.python_version(),
        "python_exe": sys.executable,
    }


def get_disk_usage(path: str = "C:\\") -> dict:
    usage = shutil.disk_usage(path)
    gb = 1024 ** 3
    return {
        "path": path,
        "total_gb": round(usage.total / gb, 1),
        "used_gb": round(usage.used / gb, 1),
        "free_gb": round(usage.free / gb, 1),
        "free_pct": round(usage.free / usage.total * 100, 1),
    }


def search_files(pattern: str, files: list, use_regex: bool = False,
                 ignore_case: bool = False) -> list:
    """Return a list of (file, line_number, line_text) matches.
    Raises FileNotFoundError if a file does not exist."""
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern if use_regex else re.escape(pattern), flags)
    matches = []
    for file in files:
        path = Path(file)
        with path.open(encoding="utf-8", errors="replace") as handle:
            for number, line in enumerate(handle, start=1):
                if regex.search(line):
                    matches.append((str(path), number, line.rstrip("\n")))
    return matches


def find_tools(names: list) -> dict:
    """Map each tool name to its full path, or None if not on PATH."""
    return {name: shutil.which(name) for name in names}


# ---------------------------------------------------------------------------
# Command handlers (print results, return exit code)
# ---------------------------------------------------------------------------
def cmd_sysinfo(args) -> int:
    for key, value in get_system_info().items():
        print(f"{key:<11}: {value}")
    return EXIT_OK


def cmd_disk(args) -> int:
    try:
        info = get_disk_usage(args.path)
    except OSError as exc:
        print(f"ERROR: cannot read disk '{args.path}': {exc}", file=sys.stderr)
        return EXIT_FILE_ERROR
    print(f"Drive {info['path']}  total={info['total_gb']} GB  "
          f"used={info['used_gb']} GB  free={info['free_gb']} GB ({info['free_pct']}%)")
    if args.min_free_gb is not None:
        if info["free_gb"] < args.min_free_gb:
            print(f"FAIL: free space below {args.min_free_gb} GB")
            return EXIT_CHECK_FAILED
        print(f"PASS: at least {args.min_free_gb} GB free")
    return EXIT_OK


def cmd_search(args) -> int:
    try:
        matches = search_files(args.pattern, args.files, args.regex, args.ignore_case)
    except FileNotFoundError as exc:
        print(f"ERROR: file not found: {exc.filename}", file=sys.stderr)
        return EXIT_FILE_ERROR
    except re.error as exc:
        print(f"ERROR: invalid regular expression: {exc}", file=sys.stderr)
        return EXIT_USAGE

    if args.count:
        print(len(matches))
    else:
        shown = matches[: args.max] if args.max else matches
        for file, number, text in shown:
            prefix = f"{file}:" if len(args.files) > 1 else ""
            print(f"{prefix}{number}: {text}")
        if args.max and len(matches) > args.max:
            print(f"... {len(matches) - args.max} more match(es) not shown")
    return EXIT_OK if matches else EXIT_CHECK_FAILED


def cmd_which(args) -> int:
    results = find_tools(args.tools)
    for name, location in results.items():
        status = "OK     " if location else "MISSING"
        print(f"[{status}] {name:<15} {location or ''}")
    return EXIT_OK if all(results.values()) else EXIT_CHECK_FAILED


# ---------------------------------------------------------------------------
# Argument parser with sub-commands
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="testkit",
        description="Reusable helper commands for desktop test automation.",
        epilog="Exit codes: 0=ok, 1=check failed/no match, 2=usage error, 3=file error",
    )
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    p = sub.add_parser("sysinfo", help="show system information")
    p.set_defaults(func=cmd_sysinfo)

    p = sub.add_parser("disk", help="show free disk space")
    p.add_argument("--path", default="C:\\", help="drive or folder (default: C:\\)")
    p.add_argument("--min-free-gb", type=float,
                   help="fail (exit 1) if free space is below this value")
    p.set_defaults(func=cmd_disk)

    p = sub.add_parser("search", help="search text in files")
    p.add_argument("pattern", help="text (or regex with --regex) to find")
    p.add_argument("files", nargs="+", help="one or more files")
    p.add_argument("--regex", action="store_true", help="treat pattern as a regex")
    p.add_argument("-i", "--ignore-case", action="store_true")
    p.add_argument("-c", "--count", action="store_true", help="print only the count")
    p.add_argument("--max", type=int, default=0, help="show at most N matches")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("which", help="check tools are on the PATH")
    p.add_argument("tools", nargs="+", help="tool names, e.g. python git")
    p.set_defaults(func=cmd_which)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)          # dispatch to the chosen sub-command


if __name__ == "__main__":
    sys.exit(main())
