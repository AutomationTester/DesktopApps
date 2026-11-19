"""
STARTER - these unit tests are COMPLETE (test-first). Do not change them;
implement workflows/calc_to_notepad.py until they all pass:
    pytest tests/test_workflow_helpers.py -v

Unit tests for the PURE parts of the mini project (no GUI).

They carry the `cli` marker so they run in the CLI job on ubuntu-latest AND windows-latest:
a bug in parsing/formatting is caught in seconds, without waiting for a desktop runner.
"""
import pytest

from utils.data_reader import read_csv
from workflows.calc_to_notepad import (ExpressionResult, build_report_lines, expected_value,
                                       format_number, parse_expression)
from workflows.mini_project_settings import DEFAULTS, get_mini_project_settings

pytestmark = pytest.mark.cli


@pytest.mark.parametrize("text, parts", [
    ("7 + 8", ("7", "+", "8")),
    ("100-45", ("100", "-", "45")),
    ("  -6 * 3 ", ("-6", "*", "3")),
    ("2.5 / 0.5", ("2.5", "/", "0.5")),
    ("7 - -3", ("7", "-", "-3")),
])
def test_parse_expression(text, parts):
    assert parse_expression(text) == parts


@pytest.mark.parametrize("bad", ["", "7 +", "seven + 8", "7 ^ 2", "1 + 2 + 3"])
def test_parse_expression_rejects_bad_input(bad):
    with pytest.raises(ValueError):
        parse_expression(bad)


@pytest.mark.parametrize("value, text", [(15.0, "15"), (2.5, "2.5"), (-18, "-18"), (1 / 3, "0.333333")])
def test_format_number(value, text):
    assert format_number(value) == text


def test_report_lines_contain_summary():
    results = [ExpressionResult("E1", "7 + 8", 15, 15.0), ExpressionResult("E2", "2 * 2", 5, 4.0)]
    lines = build_report_lines(results)
    assert lines[0] == "Calculator report"
    assert lines[1] == "E1 | 7 + 8 = 15 | expected 15 | PASS"
    assert lines[2].endswith("| FAIL")
    assert lines[-1] == "TOTAL 2 | PASSED 1 | FAILED 1"


@pytest.mark.smoke
def test_configured_expression_file_is_consistent(config):
    """The data file chosen for this --env exists and its 'expected' column is correct."""
    settings = get_mini_project_settings(config)
    rows = read_csv(settings["expressions_file"])
    assert rows
    for row in rows:
        a, op, b = parse_expression(row["expression"])
        assert expected_value(a, op, b) == pytest.approx(float(row["expected"])), row["id"]


def test_settings_fall_back_to_defaults():
    assert get_mini_project_settings({}) == DEFAULTS
    merged = get_mini_project_settings({"mini_project": {"archive": {"keep_last": 9}}})
    assert merged["archive"] == {"pattern": "*.log", "keep_last": 9}
    assert merged["expressions_file"] == DEFAULTS["expressions_file"]
