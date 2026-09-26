"""Lab 2 - CLI tests: treat run_demo.py as a command-line application under test."""
import subprocess
import sys

import pytest

from core.paths import ROOT

pytestmark = pytest.mark.cli


def run_demo(*args, timeout=60):
    return subprocess.run([sys.executable, str(ROOT / "run_demo.py"), *args],
                          capture_output=True, text=True, timeout=timeout, cwd=ROOT)


@pytest.mark.smoke
@pytest.mark.parametrize("env", ["dev", "qa"])
def test_run_demo_passes_in_each_env(env):
    result = run_demo("--env", env)
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"Environment: {env}" in result.stdout
    assert "0 failure(s)" in result.stdout


@pytest.mark.regression
def test_unknown_env_fails_with_clear_message():
    result = run_demo("--env", "prod")
    assert result.returncode != 0
    assert "Unknown environment 'prod'" in result.stderr
