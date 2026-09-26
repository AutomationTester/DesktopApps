"""
test_markers.py - built-in and custom markers.

    pytest -m smoke                       only smoke tests
    pytest -m "smoke or cli"              either marker
    pytest -m "regression and not slow"   combine with and / not
    pytest --markers                      list all registered markers
"""
import subprocess
import sys

import pytest

from calculator import Calculator


# ---------------------------------------------------------------------------
# Built-in: skip, skipif, xfail
# ---------------------------------------------------------------------------
@pytest.mark.skip(reason="Feature 'scientific mode' not implemented yet")
def test_scientific_mode():
    raise AssertionError("never runs")


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-only check")
def test_runs_only_on_windows():
    assert sys.platform == "win32"


@pytest.mark.skipif(sys.platform == "win32", reason="Linux-only check")
def test_runs_only_on_linux():
    assert sys.platform.startswith("linux")


@pytest.mark.xfail(reason="BUG-101: percentage uses integer division", strict=True)
def test_percentage_known_bug():
    # 12.5% of 10 should be 1.25; the buggy code returns 1.0
    assert Calculator().percentage(10, 12.5) == 1.25


def test_skip_at_runtime(config):
    if config["env"] != "qa":
        pytest.skip("only meaningful against the qa environment (use --env qa)")
    assert config["retries"] == 3


# ---------------------------------------------------------------------------
# Custom markers (registered in pytest.ini)
# ---------------------------------------------------------------------------
@pytest.mark.smoke
@pytest.mark.desktop
def test_smoke_open_and_add(calculator):
    assert calculator.calculate(1, "+", 1) == 2


@pytest.mark.regression
@pytest.mark.desktop
def test_regression_chain(calculator):
    total = calculator.calculate(10, "+", 5)
    total = calculator.calculate(total, "*", 2)
    assert total == 30


@pytest.mark.smoke
@pytest.mark.cli
def test_cli_python_version():
    """CLI-style test: run a command and validate return code + output."""
    result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True,
                            timeout=30)
    assert result.returncode == 0
    assert "Python 3" in result.stdout + result.stderr


@pytest.mark.regression
@pytest.mark.slow
def test_slow_many_operations(calculator):
    for i in range(1, 2001):
        calculator.calculate(i, "*", 2)
    assert len(calculator.history) == 2000


# ---------------------------------------------------------------------------
# Marker on a whole class
# ---------------------------------------------------------------------------
@pytest.mark.regression
class TestDivision:
    def test_divide(self, calculator):
        assert calculator.calculate(9, "/", 3) == 3

    def test_divide_negative(self, calculator):
        assert calculator.calculate(-9, "/", 3) == -3
