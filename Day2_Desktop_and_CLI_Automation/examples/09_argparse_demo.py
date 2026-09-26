"""
09_argparse_demo.py
===================
Day 2 - Professional command-line arguments with argparse

Imagine a test-runner script that a CI server (Jenkins, Azure DevOps,
GitHub Actions) calls with different settings. argparse gives us:
    * automatic --help / -h
    * type conversion (int, float, Path ...)
    * default values, choices, required options
    * clear error messages + exit code 2 on bad usage

TRY THESE
    python 09_argparse_demo.py --help
    python 09_argparse_demo.py Calculator
    python 09_argparse_demo.py Calculator --env qa --retries 3 -v
    python 09_argparse_demo.py Notepad --tags smoke regression --browserless
    python 09_argparse_demo.py Calculator --env prod          (invalid choice)
    python 09_argparse_demo.py Calculator --retries three     (invalid int)
    python 09_argparse_demo.py                                (missing positional)
"""

import argparse
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run_tests",
        description="Demo test runner for desktop applications.",
        epilog="Example: python 09_argparse_demo.py Calculator --env qa -v",
    )

    # 1. POSITIONAL argument - required, identified by its position
    parser.add_argument("app", help="application under test, e.g. Calculator")

    # 2. OPTIONAL argument with CHOICES and a DEFAULT
    parser.add_argument(
        "--env", choices=["dev", "qa", "uat"], default="dev",
        help="target environment (default: %(default)s)",
    )

    # 3. OPTIONAL argument with TYPE conversion
    parser.add_argument(
        "-r", "--retries", type=int, default=1, metavar="N",
        help="how many times to retry a failed test (default: %(default)s)",
    )

    # 4. FLAG - True if present, False otherwise
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print extra details")
    parser.add_argument("--browserless", action="store_true",
                        help="example of a second boolean flag")

    # 5. MULTIPLE values
    parser.add_argument("--tags", nargs="+", default=["smoke"],
                        help="one or more test tags (default: smoke)")

    # 6. PATH type
    parser.add_argument("--report", type=Path, default=Path("report.txt"),
                        help="where the report would be written")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    # parse_args() reads sys.argv[1:] by default; passing a list is handy
    # for unit tests:  main(["Calculator", "--env", "qa"])
    args = parser.parse_args(argv)

    # Our own validation that argparse cannot express
    if args.retries < 0:
        parser.error("--retries must be 0 or more")      # prints usage, exit 2

    print("Parsed arguments (argparse.Namespace):")
    print("  ", args)
    print()
    print(f"Application : {args.app}")
    print(f"Environment : {args.env}")
    print(f"Retries     : {args.retries} (type {type(args.retries).__name__})")
    print(f"Tags        : {', '.join(args.tags)}")
    print(f"Report file : {args.report} (type {type(args.report).__name__})")
    if args.verbose:
        print("Verbose mode ON -> would print every step of the test")
    return 0


if __name__ == "__main__":
    sys.exit(main())
