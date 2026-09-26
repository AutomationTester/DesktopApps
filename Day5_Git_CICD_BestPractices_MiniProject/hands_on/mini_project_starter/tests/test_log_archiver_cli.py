"""
STARTER - CLI tests for tools/log_archiver_cli.py (mini project part B)

Two tests are written as examples. Replace every pytest.skip("TODO ...") with a real test.
    pytest -m cli tests/test_log_archiver_cli.py -v --env dev
"""
import json      # noqa: F401
import sys
import zipfile   # noqa: F401

import pytest

from core.cli_runner import run_command
from core.paths import TOOLS_DIR
from workflows.mini_project_settings import get_mini_project_settings

TOOL = [sys.executable, str(TOOLS_DIR / "log_archiver_cli.py")]

pytestmark = pytest.mark.cli


@pytest.fixture
def run_tool(config):
    """Run the tool with the timeout from config.yaml -> returns a CommandResult."""
    def _run(*args):
        return run_command([*TOOL, *args], timeout=config["cli"]["command_timeout"])
    return _run


@pytest.fixture
def archive_settings(config):
    return get_mini_project_settings(config)["archive"]   # {"pattern": ..., "keep_last": ...}


@pytest.fixture
def log_folder(tmp_path):
    """Isolated test data: a private folder with 3 .log files and 1 .txt file (must be ignored)."""
    folder = tmp_path / "logs"
    folder.mkdir()
    for name in ("app.log", "db.log", "ui.log"):
        (folder / name).write_text(f"{name}: INFO started\n", encoding="utf-8")
    (folder / "notes.txt").write_text("not a log", encoding="utf-8")
    return folder


# ------------------------------------------------------------- examples (done)
@pytest.mark.smoke
def test_version(run_tool):
    result = run_tool("--version")
    assert result.ok
    assert "log_archiver_cli 1.0.0" in result.stdout


def test_unknown_command_is_usage_error(run_tool):
    result = run_tool("explode")
    assert result.returncode == 2
    assert "invalid choice" in result.stderr


# ------------------------------------------------------------- your turn
@pytest.mark.smoke
def test_collect_writes_valid_json(run_tool, tmp_path):
    # TODO: run "collect --output <tmp_path/info>", assert rc 0,
    #       exactly one sysinfo_*.json exists, it parses as JSON,
    #       python version matches sys.version_info, cpu_count >= 1
    pytest.skip("TODO: implement")


@pytest.mark.regression
def test_archive_contains_only_matching_files(run_tool, log_folder, tmp_path, archive_settings):
    # TODO: archive log_folder into tmp_path/"archives" using archive_settings["pattern"];
    #       assert "archived: 3 files" in stdout; open the zip and check the 3 names;
    #       zf.testzip() is None
    pytest.skip("TODO: implement")


@pytest.mark.regression
def test_keep_last_prunes_old_archives(run_tool, log_folder, tmp_path, archive_settings):
    # TODO: run archive keep_last + 2 times with --keep keep_last; assert only keep_last zips remain
    pytest.skip("TODO: implement")


@pytest.mark.regression
def test_missing_source_folder_exit_code(run_tool, tmp_path):
    # TODO: expected rc 2 and "source folder not found" on stderr
    pytest.skip("TODO: implement")


@pytest.mark.regression
def test_nothing_to_archive_exit_code(run_tool, tmp_path):
    # TODO: empty folder or pattern "*.nothing" -> rc 1 and "no files matching" on stderr
    pytest.skip("TODO: implement")
