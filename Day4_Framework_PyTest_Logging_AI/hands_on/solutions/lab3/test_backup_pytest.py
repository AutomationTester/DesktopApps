"""
Lab 3 - stretch goal solution: the improved check as pytest tests.

    pytest test_backup_pytest.py -v
    pytest test_backup_pytest.py --html=reports/lab3_report.html --self-contained-html
"""
import subprocess
import sys

import pytest

import improved_backup_test as bt


@pytest.fixture(autouse=True, scope="module")
def logging_on():
    bt.setup_logging()


@pytest.mark.parametrize("file_count", [1, 3])
def test_backup_copies_all_files(file_count):
    assert bt.run_backup_check(file_count=file_count, timeout=15)


def test_missing_source_folder_returns_exit_code_2(tmp_path):
    result = subprocess.run([sys.executable, str(bt.TOOL), str(tmp_path / "nope"), str(tmp_path / "out")],
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 2
    assert "source folder not found" in result.stderr
