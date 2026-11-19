"""
Mini project part A - END-TO-END desktop workflow

    expressions (config-selected CSV) -> Calculator -> Notepad temp file -> save -> verify on disk

Needs a real, unlocked Windows desktop session. Run:
    pytest -m desktop tests/test_e2e_calc_to_notepad.py --env dev --html=reports/e2e.html --self-contained-html
"""
import pytest

from utils.data_reader import read_csv
from workflows.calc_to_notepad import build_report_lines, compute_all, write_report
from workflows.mini_project_settings import get_mini_project_settings

pytestmark = [pytest.mark.desktop, pytest.mark.regression]


@pytest.fixture
def settings(config):
    return get_mini_project_settings(config)


@pytest.fixture
def report_notepad(config, settings, tmp_path):
    """OUR OWN empty report file opened in Notepad; only our tab is closed afterwards."""
    from pages.report_notepad_page import ReportNotepadPage  # Windows-only import

    report_file = tmp_path / f"{settings['report_prefix']}_{config['env']}.txt"
    report_file.write_text("", encoding="utf-8")
    page = ReportNotepadPage(config).open_file(report_file)
    yield page
    page.close_tab()          # teardown runs even when the test fails


def test_expressions_report_end_to_end(calculator, report_notepad, settings):
    # 1. Data - which file depends on --env (configuration-driven)
    rows = read_csv(settings["expressions_file"])
    assert rows, f"no rows in {settings['expressions_file']}"

    # 2. Calculator - one calculation per row (retried once if the display is not ready)
    results = compute_all(calculator, rows)

    # 3. Notepad - type the report into our temp file and save it
    lines = build_report_lines(results)
    expected_text = write_report(report_notepad, lines)

    # 4. Oracle - the file ON DISK, not just what the screen shows
    assert report_notepad.saved_text_normalised() == expected_text

    # 5. Business check - every calculation matched the expected value
    failed = [r.as_line() for r in results if not r.passed]
    assert not failed, "Calculator gave wrong answers:\n" + "\n".join(failed)


@pytest.mark.smoke
def test_single_expression_appended(calculator, report_notepad):
    """Smaller smoke version: one calculation, appended as a line."""
    value = calculator.calculate(6, "*", 7)
    report_notepad.append_line(f"6 * 7 = {value:g}")
    report_notepad.save()
    assert report_notepad.saved_text_normalised() == "6 * 7 = 42"
