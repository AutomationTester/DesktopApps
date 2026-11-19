"""
Lab 2 solution - Task 6: BREAK the build on purpose, watch CI turn red, then fix it.

Copy to:  automation_framework/tests/test_break_ci.py   on a branch, e.g.
    git switch -c experiment/break-ci
    cp .../lab2_test_break_ci.py automation_framework/tests/test_break_ci.py
    git add . && git commit -m "test: deliberately failing test (lab 2)" && git push -u origin experiment/break-ci
Open a Pull Request -> the "CLI tests" checks fail -> the PR shows a red X.
Download the report artifact and find the failure message.

Fix: change EXPECTED_VERSION to "1.0.0" (or delete the file), commit, push -> checks go green.
"""
import sys

import pytest

from core.cli_runner import run_command
from core.paths import TOOLS_DIR

EXPECTED_VERSION = "9.9.9"   # WRONG on purpose - the tool reports 1.0.0

pytestmark = pytest.mark.cli


def test_version_matches_release_notes():
    result = run_command([sys.executable, str(TOOLS_DIR / "sysinfo_cli.py"), "--version"])
    assert result.ok
    assert EXPECTED_VERSION in result.stdout, f"tool says: {result.stdout.strip()}"
