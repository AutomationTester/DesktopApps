"""
STARTER - END-TO-END desktop workflow test (mini project part A)

    expressions (CSV chosen by --env) -> Calculator -> Notepad temp file -> save -> verify ON DISK

Needs a real, unlocked Windows 10/11 desktop:
    pytest -m desktop tests/test_e2e_calc_to_notepad.py --env dev -v

Fixtures available from tests/conftest.py:
    config      (session)  settings of the selected --env
    calculator  (module)   CalculatorPage, already open; closed after the module
    notepad     (function) NotepadPage on 'automation_note.txt' (we need our OWN name, so we
                           build our own fixture below using ReportNotepadPage)
"""
import pytest

from utils.data_reader import read_csv  # noqa: F401
from workflows.calc_to_notepad import build_report_lines, compute_all, write_report  # noqa: F401
from workflows.mini_project_settings import get_mini_project_settings

pytestmark = [pytest.mark.desktop, pytest.mark.regression]


@pytest.fixture
def settings(config):
    return get_mini_project_settings(config)


@pytest.fixture
def report_notepad(config, settings, tmp_path):
    """OUR OWN empty report file opened in Notepad; only our tab is closed afterwards."""
    from pages.report_notepad_page import ReportNotepadPage  # Windows-only import

    # TODO 1: build the file name from settings["report_prefix"] and config["env"]
    report_file = tmp_path / "TODO_report.txt"
    # TODO 2: the file MUST exist before open_file() - create it empty (utf-8)
    page = ReportNotepadPage(config).open_file(report_file)
    yield page
    # TODO 3: teardown - close ONLY our tab (which NotepadPage method?)


def test_expressions_report_end_to_end(calculator, report_notepad, settings):
    # TODO a: rows = read_csv(<file name from settings>) and assert it is not empty
    # TODO b: results = compute_all(calculator, rows)
    # TODO c: lines = build_report_lines(results); expected_text = write_report(report_notepad, lines)
    # TODO d: assert the file ON DISK equals expected_text (report_notepad.saved_text_normalised())
    # TODO e: assert every result passed - show the failing lines in the assertion message
    pytest.skip("TODO: implement the end-to-end test")


@pytest.mark.smoke
def test_single_expression_appended(calculator, report_notepad):
    # TODO: calculate 6 * 7, append "6 * 7 = 42" with append_line, save, verify from disk
    pytest.skip("TODO: implement the smoke test")
