"""
10_subprocess_demo.py
=====================
Day 2 - Automating system commands with subprocess and os

Testers use this to:
    * check the environment before a test run (python version, tools on PATH)
    * start/stop the application under test
    * run other command-line tools and verify their output / exit code
    * collect evidence (ipconfig, systeminfo, logs) when a test fails

HOW TO RUN
    python 10_subprocess_demo.py

GOLDEN RULES
    1. Prefer subprocess.run([...list of args...]) - no shell needed, no
       quoting problems, no command-injection risk.
    2. capture_output=True + text=True -> output as str in result.stdout
    3. ALWAYS look at result.returncode (0 = success by convention).
    4. Use timeout= so a hanging tool cannot hang your whole test run.
    5. check=True turns a non-zero exit code into an exception.
    6. Built-in cmd.exe commands (dir, echo, type) need shell=True or
       ["cmd", "/c", "dir"] because they are not .exe files.
"""

import os
import platform
import subprocess
import sys


def section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def demo_basic_run() -> None:
    section("1. Run a program and capture its output")
    result = subprocess.run(
        [sys.executable, "--version"],     # sys.executable = the running python.exe
        capture_output=True, text=True,
    )
    print("args       :", result.args)
    print("returncode :", result.returncode)
    print("stdout     :", result.stdout.strip())


def demo_where_python() -> None:
    section("2. Is a tool on the PATH?  (where python)")
    result = subprocess.run(["where", "python"], capture_output=True, text=True)
    if result.returncode == 0:
        for line in result.stdout.splitlines():
            print("  found:", line)
    else:
        print("  python not found on PATH")


def demo_ipconfig() -> None:
    section("3. Parse output of a system command (ipconfig)")
    result = subprocess.run(["ipconfig"], capture_output=True, text=True,
                            timeout=30, errors="replace")
    ipv4 = [line.split(":", 1)[1].strip()
            for line in result.stdout.splitlines()
            if "IPv4 Address" in line]
    print("IPv4 addresses found:", ipv4 if ipv4 else "(none)")


def demo_return_codes() -> None:
    section("4. Return codes - PASS/FAIL signal of every command-line tool")
    ok = subprocess.run([sys.executable, "-c", "import sys; sys.exit(0)"])
    bad = subprocess.run([sys.executable, "-c", "import sys; sys.exit(3)"])
    print("exit(0) ->", ok.returncode, "| exit(3) ->", bad.returncode)


def demo_check_true() -> None:
    section("5. check=True raises CalledProcessError on failure")
    try:
        subprocess.run(
            [sys.executable, "-c", "import sys; print('boom', file=sys.stderr); sys.exit(1)"],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as err:
        print("Caught CalledProcessError")
        print("  returncode:", err.returncode)
        print("  stderr    :", err.stderr.strip())


def demo_timeout() -> None:
    section("6. timeout= protects against hanging tools")
    try:
        subprocess.run([sys.executable, "-c", "import time; time.sleep(10)"],
                       timeout=2)
    except subprocess.TimeoutExpired as err:
        print(f"Caught TimeoutExpired after {err.timeout} s - process was killed")


def demo_missing_program() -> None:
    section("7. Program that does not exist")
    try:
        subprocess.run(["this_tool_does_not_exist.exe"])
    except FileNotFoundError:
        print("Caught FileNotFoundError - check spelling / PATH")


def demo_shell_builtin() -> None:
    section("8. cmd.exe built-in commands (echo, dir)")
    result = subprocess.run(["cmd", "/c", "echo Hello from cmd"],
                            capture_output=True, text=True)
    print("echo ->", result.stdout.strip())
    # Equivalent but uses the shell - avoid with untrusted input:
    # subprocess.run("echo Hello", shell=True)


def demo_popen() -> None:
    section("9. Popen - start a process WITHOUT waiting (like launching an app)")
    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(1); print('child done')"],
                            stdout=subprocess.PIPE, text=True)
    print("started PID", proc.pid, "| still running?", proc.poll() is None)
    out, _ = proc.communicate(timeout=10)   # now wait for it to finish
    print("child said:", out.strip(), "| returncode:", proc.returncode)
    # For GUI apps: subprocess.Popen("calc.exe") then connect with pywinauto


def demo_os_module() -> None:
    section("10. The os module - environment and file system")
    print("current dir       :", os.getcwd())
    print("user name         :", os.environ.get("USERNAME", "?"))
    print("computer name     :", os.environ.get("COMPUTERNAME", "?"))
    print("PATH entries      :", len(os.environ.get("PATH", "").split(os.pathsep)))
    print("OS / release      :", platform.system(), platform.release())
    print("files in this dir :", len(os.listdir(os.path.dirname(os.path.abspath(__file__)))))
    # os.system("cls") also runs a command, but returns only the exit code
    # and cannot capture output -> prefer subprocess.run in test code.
    code = os.system("ver > nul")
    print("os.system('ver') exit code:", code)


def main() -> None:
    demo_basic_run()
    demo_where_python()
    demo_ipconfig()
    demo_return_codes()
    demo_check_true()
    demo_timeout()
    demo_missing_program()
    demo_shell_builtin()
    demo_popen()
    demo_os_module()
    print("\nAll demos finished.")


if __name__ == "__main__":
    main()
