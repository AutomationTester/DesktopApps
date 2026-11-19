"""
Mini project part B - CLI / system task automation: tools/log_archiver_cli.py

No GUI - runs on Windows, Linux and macOS:
    pytest -m cli tests/test_log_archiver_cli.py --env qa
"""
import json
import sys
import zipfile

import pytest

from core.cli_runner import run_command
from core.paths import TOOLS_DIR
from workflows.mini_project_settings import get_mini_project_settings

TOOL = [sys.executable, str(TOOLS_DIR / "log_archiver_cli.py")]

pytestmark = pytest.mark.cli


@pytest.fixture
def run_tool(config):
    def _run(*args):
        return run_command([*TOOL, *args], timeout=config["cli"]["command_timeout"])
    return _run


@pytest.fixture
def archive_settings(config):
    return get_mini_project_settings(config)["archive"]


@pytest.fixture
def log_folder(tmp_path):
    """Isolated test data: a private folder with 3 logs and 1 file that must be ignored."""
    folder = tmp_path / "logs"
    folder.mkdir()
    for name in ("app.log", "db.log", "ui.log"):
        (folder / name).write_text(f"{name}: INFO started\n", encoding="utf-8")
    (folder / "notes.txt").write_text("not a log", encoding="utf-8")
    return folder


@pytest.mark.smoke
def test_version(run_tool):
    result = run_tool("--version")
    assert result.ok
    assert "log_archiver_cli 1.0.0" in result.stdout


@pytest.mark.smoke
def test_collect_writes_valid_json(run_tool, tmp_path):
    result = run_tool("collect", "--output", tmp_path / "info")
    assert result.ok, result.stderr
    files = list((tmp_path / "info").glob("sysinfo_*.json"))
    assert len(files) == 1
    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data["python"] == ".".join(map(str, sys.version_info[:3]))
    assert data["cpu_count"] >= 1
    assert {"os", "hostname", "disk_free_gb"} <= data.keys()


@pytest.mark.regression
def test_archive_contains_only_matching_files(run_tool, log_folder, tmp_path, archive_settings):
    dest = tmp_path / "archives"
    result = run_tool("archive", "--source", log_folder, "--dest", dest,
                      "--pattern", archive_settings["pattern"])
    assert result.ok, result.stderr
    assert "archived: 3 files" in result.stdout
    [archive] = dest.glob("logs_*.zip")
    with zipfile.ZipFile(archive) as zf:
        assert sorted(zf.namelist()) == ["app.log", "db.log", "ui.log"]
        assert zf.testzip() is None          # archive is not corrupt


@pytest.mark.regression
def test_keep_last_prunes_old_archives(run_tool, log_folder, tmp_path, archive_settings):
    keep = archive_settings["keep_last"]
    dest = tmp_path / "archives"
    for _ in range(keep + 2):
        assert run_tool("archive", "--source", log_folder, "--dest", dest,
                        "--keep", str(keep)).ok
    assert len(list(dest.glob("logs_*.zip"))) == keep


@pytest.mark.regression
@pytest.mark.parametrize("args, expected_rc, stderr_text", [
    (["archive", "--source", "no_such_folder", "--dest", "out"], 2, "source folder not found"),
    (["archive", "--source", ".", "--dest", "out", "--pattern", "*.nothing"], 1, "no files matching"),
    (["explode"], 2, "invalid choice"),
], ids=["missing-source", "nothing-to-archive", "unknown-command"])
def test_error_exit_codes(run_tool, tmp_path, args, expected_rc, stderr_text):
    # make relative paths point into the private tmp folder
    args = [str(tmp_path / a) if a in ("no_such_folder", "out", ".") else a for a in args]
    result = run_tool(*args)
    assert result.returncode == expected_rc, result.stdout + result.stderr
    assert stderr_text in result.stderr
