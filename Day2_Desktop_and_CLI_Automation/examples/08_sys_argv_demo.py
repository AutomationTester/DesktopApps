"""
08_sys_argv_demo.py
===================
Day 2 - Command-line arguments the simple way: sys.argv

sys.argv is a plain Python LIST of strings:
    sys.argv[0]  -> the script name
    sys.argv[1:] -> everything the user typed after the script name

TRY THESE
    python 08_sys_argv_demo.py
    python 08_sys_argv_demo.py hello world
    python 08_sys_argv_demo.py "hello world"            (quotes = ONE argument)
    python 08_sys_argv_demo.py add 12 30
    python 08_sys_argv_demo.py add 12 abc               (error handling)
    python 08_sys_argv_demo.py smoke --env qa           (a tester-style call)

LIMITATIONS (why we move to argparse next)
    * Everything is a string - YOU convert types ("12" -> 12)
    * YOU write the --help text and the error messages
    * Optional flags like --env are painful to parse by hand
"""

import sys


def show_raw_arguments() -> None:
    print("sys.argv          =", sys.argv)
    print("script name       =", sys.argv[0])
    print("number of args    =", len(sys.argv) - 1)
    for index, value in enumerate(sys.argv[1:], start=1):
        print(f"  argv[{index}] = {value!r}  (type: {type(value).__name__})")


def add_command(args: list) -> int:
    """Handle:  add <number> <number>  -> returns an exit code."""
    if len(args) != 2:
        print("Usage: python 08_sys_argv_demo.py add <a> <b>")
        return 2                        # 2 = conventional 'bad usage' code
    try:
        a, b = float(args[0]), float(args[1])   # strings -> numbers
    except ValueError:
        print(f"Error: both values must be numbers, got {args[0]!r} and {args[1]!r}")
        return 2
    print(f"{a:g} + {b:g} = {a + b:g}")
    return 0


def smoke_command(args: list) -> int:
    """Handle:  smoke [--env NAME]  -> manual flag parsing (painful!)."""
    env = "dev"                              # default value
    if "--env" in args:
        position = args.index("--env")
        if position + 1 >= len(args):
            print("Error: --env needs a value, e.g. --env qa")
            return 2
        env = args[position + 1]
    print(f"Running smoke tests against environment: {env}")
    return 0


def main() -> int:
    show_raw_arguments()
    print()
    if len(sys.argv) < 2:
        print("No command given. Try: add 12 30   or   smoke --env qa")
        return 0

    command, rest = sys.argv[1], sys.argv[2:]
    if command == "add":
        return add_command(rest)
    if command == "smoke":
        return smoke_command(rest)
    print(f"(no special handling for {command!r})")
    return 0


if __name__ == "__main__":
    # sys.exit(code) -> the exit code is visible to the shell / CI server:
    #   PowerShell:  $LASTEXITCODE      cmd.exe:  %ERRORLEVEL%
    sys.exit(main())
