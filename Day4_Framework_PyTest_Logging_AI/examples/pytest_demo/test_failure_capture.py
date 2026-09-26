"""
test_failure_capture.py - screenshot + log capture on failure.

The failing test is marked `demo_fail` and is DESELECTED by default
(pytest.ini: addopts = ... -m "not demo_fail").

Opt in to see the capture in action:
    pytest -m demo_fail
    pytest -m demo_fail --html=reports/failure_report.html --self-contained-html

What happens on failure (see conftest.py -> pytest_runtest_makereport):
    artifacts/<test>_<timestamp>.png  (or .txt if no screen is available)
    artifacts/<test>_<timestamp>_log.txt  (captured log + stdout + traceback)
    both attached to the pytest-html report as "extras"
"""
import pytest


@pytest.mark.demo_fail
def test_deliberate_failure_captures_evidence(calculator, logger, result_logger):
    logger.info("Step 1: add 2 + 2")
    result = calculator.calculate(2, "+", 2)
    logger.info("Step 2: verify the display shows 5 (wrong on purpose)")
    print("stdout is captured too")
    assert result == 5, "Display value mismatch - see screenshot and log in the report"


def test_passing_test_has_no_artifacts(calculator, result_logger):
    assert calculator.calculate(2, "+", 2) == 4
