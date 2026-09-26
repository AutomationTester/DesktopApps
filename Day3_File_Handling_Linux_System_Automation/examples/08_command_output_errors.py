"""
08_command_output_errors.py
===========================
Day 3 - Handling command outputs and errors.

Four things can go wrong when you run a command, and each is detected
differently:

    What happened                        How you detect it
    -----------------------------------  ----------------------------------------
    Command ran but reported failure     result.returncode != 0  (and stderr text)
                                         or check=True -> CalledProcessError
    Command hangs                        timeout=N -> subprocess.TimeoutExpired
    Command does not exist               FileNotFoundError (when not using shell)
    No permission to execute             PermissionError

To keep the demo 100% portable we use `python -c "..."` as our "CLI tool"
(it exists on every machine). The same handling applies to ls, grep, git...

Run:  python 08_command_output_errors.py
"""

import subprocess
import sys

PY = sys.executable


def banner(title):
    print("\n" + "-" * 70 + f"\n{title}\n" + "-" * 70)


def demo_success_and_output_parsing():
    banner("1. Success: parse stdout")
    # A fake CLI tool that prints a status table
    tool = "print('service  status'); print('db       RUNNING'); print('cache    STOPPED')"
    result = subprocess.run([PY, "-c", tool], capture_output=True, text=True)
    print(f"returncode = {result.returncode}")
    status = {}
    for line in result.stdout.splitlines()[1:]:         # skip header line
        name, state = line.split()
        status[name] = state
    print(f"Parsed dict: {status}")
    assert status["db"] == "RUNNING", "db should be running"
    print("ASSERT db == RUNNING -> PASS")


def demo_nonzero_returncode():
    banner("2. Failure reported by the tool: check returncode + stderr")
    tool = "import sys; print('processing...'); sys.stderr.write('ERROR: config file missing\\n'); sys.exit(3)"
    result = subprocess.run([PY, "-c", tool], capture_output=True, text=True)
    print(f"returncode = {result.returncode}")
    print(f"stdout     = {result.stdout.strip()!r}")
    print(f"stderr     = {result.stderr.strip()!r}")
    if result.returncode != 0:
        print("-> Test would be marked FAIL; stderr goes into the report")


def demo_check_true():
    banner("3. check=True raises CalledProcessError automatically")
    try:
        subprocess.run([PY, "-c", "import sys; sys.exit(2)"],
                       capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"CalledProcessError caught: cmd exit code {e.returncode}")
        print(f"  e.cmd    = {e.cmd[1:]}  (python path trimmed)")
        print(f"  e.stderr = {e.stderr!r}")


def demo_timeout():
    banner("4. Hanging command: timeout -> TimeoutExpired")
    try:
        subprocess.run([PY, "-c", "import time; time.sleep(10)"],
                       capture_output=True, text=True, timeout=1)
    except subprocess.TimeoutExpired as e:
        print(f"TimeoutExpired caught after {e.timeout}s - process was killed")


def demo_not_found():
    banner("5. Command does not exist -> FileNotFoundError")
    try:
        subprocess.run(["this_tool_does_not_exist", "--version"], capture_output=True, text=True)
    except FileNotFoundError as e:
        print(f"FileNotFoundError caught: {e.strerror}")
        print("Tip: check with shutil.which('tool') before running, or fix PATH")


def run_command(cmd, timeout=30):
    """
    Reusable helper you can copy into your own framework.
    NEVER raises - always returns a dict describing what happened.
    """
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"ok": r.returncode == 0, "returncode": r.returncode,
                "stdout": r.stdout.strip(), "stderr": r.stderr.strip(), "error": ""}
    except subprocess.TimeoutExpired:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": "", "error": f"timeout after {timeout}s"}
    except FileNotFoundError:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": "", "error": "command not found"}
    except PermissionError:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": "", "error": "permission denied"}


def demo_helper():
    banner("6. A robust run_command() helper used on several commands")
    commands = [
        [PY, "-c", "print('hello')"],
        [PY, "-c", "import sys; sys.exit(1)"],
        ["no_such_cmd_xyz"],
        [PY, "-c", "import time; time.sleep(5)"],
    ]
    for cmd in commands:
        res = run_command(cmd, timeout=1)
        label = "PASS" if res["ok"] else "FAIL"
        shown = " ".join(["python" if c == PY else c for c in cmd])[:45]
        print(f"{label}  {shown:<46} rc={res['returncode']}  {res['error'] or res['stdout']}")


def demo_bytes_vs_text():
    banner("7. Without text=True you get BYTES")
    r = subprocess.run([PY, "-c", "print('abc')"], capture_output=True)
    print(f"stdout type = {type(r.stdout).__name__}, value = {r.stdout!r}")
    print(f"decoded     = {r.stdout.decode().strip()!r}")


if __name__ == "__main__":
    demo_success_and_output_parsing()
    demo_nonzero_returncode()
    demo_check_true()
    demo_timeout()
    demo_not_found()
    demo_helper()
    demo_bytes_vs_text()
