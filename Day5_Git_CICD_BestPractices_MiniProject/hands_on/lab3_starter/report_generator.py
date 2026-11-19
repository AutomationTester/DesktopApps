"""
report_generator.py - the "application under test" for Lab 3 (do NOT modify)

A small command-line program that behaves like a real, slightly unreliable tool:
  * it takes a RANDOM time (0.5 - 3 s) to produce its report
  * sometimes it is "busy" and exits with code 75 without writing anything (transient error)
  * very rarely it HANGS (for 60 s - long enough to break any sane test, then it
    gives up with exit code 1 so it can never stay around forever)

Usage:
    python report_generator.py --out PATH [--mode random|ok|busy|hang] [--delay SECONDS]

Exit codes: 0 = report written, 75 = busy (try again later), 1 = hung then gave up,
            2 = usage error
"""
import argparse
import random
import sys
import time
from pathlib import Path

EXIT_OK, EXIT_BUSY = 0, 75


def main(argv=None):
    parser = argparse.ArgumentParser(prog="report_generator")
    parser.add_argument("--out", required=True, help="report file to create")
    parser.add_argument("--mode", choices=["random", "ok", "busy", "hang"], default="random")
    parser.add_argument("--delay", type=float, help="fixed delay instead of a random one")
    args = parser.parse_args(argv)

    mode = args.mode
    if mode == "random":
        roll = random.random()
        mode = "hang" if roll < 0.05 else "busy" if roll < 0.30 else "ok"

    delay = args.delay if args.delay is not None else random.uniform(0.5, 3.0)
    time.sleep(delay)

    if mode == "hang":
        time.sleep(60)                   # simulated deadlock (bounded for safety)
        print("ERROR: gave up after hanging", file=sys.stderr)
        return 1
    if mode == "busy":
        print("ERROR: resource busy, try again", file=sys.stderr)
        return EXIT_BUSY

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("REPORT OK\nrows=42\n", encoding="utf-8")
    print(f"report written: {out}")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
