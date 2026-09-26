"""
07_subprocess_linux_commands.py
===============================
Day 3 - Executing Linux (and Windows) commands from Python with subprocess.

Key points
----------
* subprocess.run([...]) is the modern, recommended API (Popen is for
  long-running / interactive processes, as used for GUI apps on Day 2).
* Pass the command as a LIST:  ["ls", "-l", "/tmp"]   (safe, no shell parsing)
* shlex.split("ls -l '/my folder'") turns a string into that list correctly.
* capture_output=True + text=True  -> result.stdout / result.stderr are str.
* shell=True is only needed for shell built-ins (Windows "dir", "echo")
  or pipes/wildcards. Avoid it with user input (shell injection risk).
* Cross-platform: check platform.system() / sys.platform and shutil.which().

This script runs safely on Windows, Linux, macOS and Git Bash.
It only lists/reads; it creates one sample file inside examples/sandbox/.

Run:  python 07_subprocess_linux_commands.py
"""

import platform
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox"
SANDBOX.mkdir(exist_ok=True)

OS_NAME = platform.system()          # 'Windows', 'Linux' or 'Darwin' (macOS)
IS_WINDOWS = OS_NAME == "Windows"


def banner(title):
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)


def step1_detect_os():
    banner("1. Detect the operating system")
    print(f"platform.system()  = {OS_NAME}")
    print(f"sys.platform       = {sys.platform}")
    print(f"Python executable  = {sys.executable}")
    # shutil.which tells us if a command exists on PATH (like Linux 'which')
    for tool in ("ls", "grep", "git", "bash", "python"):
        print(f"which({tool!r:8}) -> {shutil.which(tool) or 'NOT FOUND'}")


def step2_list_directory():
    banner("2. List a directory: 'ls -l' on Linux, 'dir' on Windows")
    if IS_WINDOWS:
        # 'dir' is a cmd.exe BUILT-IN, not an .exe -> needs shell=True
        cmd = f'dir "{HERE}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        # On Linux/macOS use a list - no shell needed
        cmd = ["ls", "-l", str(HERE)]
        result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Command     : {cmd}")
    print(f"Return code : {result.returncode}   (0 = success)")
    lines = result.stdout.splitlines()
    print(f"stdout ({len(lines)} lines, first 8 shown):")
    for line in lines[:8]:
        print("   " + line)

    if IS_WINDOWS and shutil.which("ls"):
        # Git for Windows puts Linux tools (ls, grep, find...) on PATH
        r = subprocess.run(["ls", "-l", str(HERE)], capture_output=True, text=True)
        print(f"\nBonus: 'ls' found on PATH ({shutil.which('ls')})")
        print(f"ls -l returned {r.returncode}, first line: {r.stdout.splitlines()[0] if r.stdout else ''}")


def step3_shlex():
    banner("3. shlex.split - turn a command STRING into a safe LIST")
    command_line = "grep -i 'error code' \"app log.txt\""
    print(f"String          : {command_line}")
    print(f"str.split()     : {command_line.split()}     <- WRONG, breaks quoted parts")
    print(f"shlex.split()   : {shlex.split(command_line)}  <- correct")
    # shlex.quote does the reverse: safely quote a value for a shell string
    print(f"shlex.quote()   : {shlex.quote('my file; rm -rf /')}  <- dangerous text neutralised")


def step4_portable_command():
    banner("4. The most portable 'command': run Python itself")
    # sys.executable is the python currently running -> exists on every OS
    result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
    print(f"{sys.executable} --version -> {result.stdout.strip() or result.stderr.strip()}")


def step5_grep_like_search():
    banner("5. Search a log file: 'grep' if available, else Python/findstr")
    log = SANDBOX / "app.log"
    log.write_text(
        "2026-09-26 10:00:01 INFO  Application started\n"
        "2026-09-26 10:00:05 ERROR Could not connect to DB\n"
        "2026-09-26 10:00:09 INFO  Retrying\n"
        "2026-09-26 10:00:12 ERROR Timeout after 30s\n",
        encoding="utf-8",
    )
    if shutil.which("grep"):
        cmd = ["grep", "-n", "ERROR", str(log)]
    elif IS_WINDOWS:
        cmd = ["findstr", "/n", "ERROR", str(log)]     # Windows equivalent of grep
    else:
        cmd = None

    if cmd:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"Command: {' '.join(cmd[:3])} <log>")
        print(result.stdout.rstrip())
        # grep exit codes: 0 = match found, 1 = no match, 2 = error
        print(f"Return code: {result.returncode}")
    # Pure-Python fallback always works (and is often the better choice!)
    errors = [l for l in log.read_text(encoding="utf-8").splitlines() if "ERROR" in l]
    print(f"Python fallback found {len(errors)} ERROR lines")


def step6_env_and_cwd():
    banner("6. Run a command in a specific folder (cwd=) with extra env vars")
    import os
    env = {**os.environ, "TEST_ENV": "qa"}   # copy current env + add one var
    result = subprocess.run(
        [sys.executable, "-c", "import os; print(os.getcwd()); print('TEST_ENV =', os.environ['TEST_ENV'])"],
        capture_output=True, text=True, cwd=SANDBOX, env=env,
    )
    print(result.stdout.rstrip())


if __name__ == "__main__":
    step1_detect_os()
    step2_list_directory()
    step3_shlex()
    step4_portable_command()
    step5_grep_like_search()
    step6_env_and_cwd()
