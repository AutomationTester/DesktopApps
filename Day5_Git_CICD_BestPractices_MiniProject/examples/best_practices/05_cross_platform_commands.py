"""
05_cross_platform_commands.py  -  writing automation that runs on
                                  Windows AND the Linux CI runner
=================================================================
Topics:
  1. Detect the OS (platform / sys.platform / os.name)
  2. Prefer Python APIs over shell commands (shutil, pathlib, platform)
  3. When you must run a command: pass a LIST, no shell=True, use sys.executable
  4. Pick OS-specific commands explicitly (dir vs ls, ping -n vs ping -c)
  5. Line endings: \\r\\n (Windows) vs \\n (Linux) - how to compare text safely
  6. Environment variables and PATH differences

Run:
    python 05_cross_platform_commands.py
"""

import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

IS_WINDOWS = sys.platform.startswith("win")


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def show_os() -> None:
    section("1. Which OS am I on?")
    print("platform.system() :", platform.system())     # Windows / Linux / Darwin
    print("sys.platform      :", sys.platform)          # win32 / linux / darwin
    print("os.name           :", os.name)               # nt / posix
    print("os.sep / linesep  :", repr(os.sep), repr(os.linesep))


def python_instead_of_shell() -> None:
    section("2. Prefer Python APIs over shell commands")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "a.txt"
        src.write_text("hello", encoding="utf-8")
        shutil.copy(src, Path(tmp) / "b.txt")            # instead of copy / cp
        names = sorted(p.name for p in Path(tmp).iterdir())  # instead of dir / ls
        print("files:", names)
    print("disk usage of temp drive (GB free):",
          round(shutil.disk_usage(tempfile.gettempdir()).free / 1e9, 1))
    print("is 'git' on PATH?  ->", shutil.which("git") or "not found")


def run_command_safely() -> None:
    section("3. Running a command portably")
    # sys.executable = the exact python running this script (works in venvs, on CI)
    result = subprocess.run(
        [sys.executable, "-c", "import sys; print('child python', sys.version.split()[0])"],
        capture_output=True, text=True, timeout=30, check=False,
    )
    print("return code:", result.returncode)
    print("stdout     :", result.stdout.strip())


def os_specific_command() -> None:
    section("4. OS-specific commands - choose explicitly")
    if IS_WINDOWS:
        cmd = ["cmd", "/c", "echo", "hello", "from", "cmd.exe"]  # built-ins need cmd /c
        ping_hint = "ping -n 1 localhost"
    else:
        cmd = ["echo", "hello from /bin/echo"]
        ping_hint = "ping -c 1 localhost"
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    print("command :", cmd)
    print("output  :", out.stdout.strip())
    print("ping on this OS would be:", ping_hint)


def line_endings() -> None:
    section("5. Line endings")
    windows_text = "line1\r\nline2\r\n"
    linux_text = "line1\nline2\n"
    print("raw equal?        ", windows_text == linux_text)
    print("splitlines equal? ", windows_text.splitlines() == linux_text.splitlines())
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "le.txt"
        # newline="" writes exactly what we give; default text mode translates \n
        f.write_text(linux_text, encoding="utf-8", newline="")
        print("bytes on disk     :", f.read_bytes())
        print("read back as text :", repr(f.read_text(encoding="utf-8")))
    print("Tip: add a .gitattributes with  '* text=auto'  and  '*.sh text eol=lf'")


def env_vars() -> None:
    section("6. Environment variables")
    home = Path.home()
    print("home dir          :", home)
    print("USERNAME / USER   :", os.environ.get("USERNAME") or os.environ.get("USER"))
    print("CI running?       :", os.environ.get("CI", "false"))  # GitHub sets CI=true
    print("PATH separator    :", repr(os.pathsep))               # ';' Windows, ':' Linux


def main() -> None:
    show_os()
    python_instead_of_shell()
    run_command_safely()
    os_specific_command()
    line_endings()
    env_vars()


if __name__ == "__main__":
    main()
