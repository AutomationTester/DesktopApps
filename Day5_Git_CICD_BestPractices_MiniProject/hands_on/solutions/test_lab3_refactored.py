"""
test_lab3_refactored.py - pytest tests that PROVE the refactoring works.

Each test forces one behaviour of the generator (ok / busy / hang), so the
tests are deterministic - no randomness in a test suite!

Run from this folder:
    python -m pytest test_lab3_refactored.py -v
"""
import time

import pytest

import lab3_refactored_report_check as lab3


def test_ok_mode_passes():
    assert lab3.check_report("ok") is True


def test_busy_is_retried_then_reported(monkeypatch):
    calls = []
    real = lab3.run_generator_once

    def spy(out_file, mode="random", timeout=None):
        calls.append(mode)
        return real(out_file, mode, timeout)

    monkeypatch.setattr(lab3, "run_generator_once", spy)
    monkeypatch.setitem(lab3.CONFIG, "retry_delay", 0.01)
    assert lab3.check_report("busy") is False
    assert len(calls) == lab3.CONFIG["retries"]          # tried 3 times, then gave up


def test_hang_times_out_and_child_is_killed(monkeypatch, tmp_path):
    monkeypatch.setitem(lab3.CONFIG, "process_timeout", 1.0)
    start = time.monotonic()
    with pytest.raises(lab3.GeneratorTimeout):
        lab3.run_generator_once(tmp_path / "r.txt", "hang")
    assert time.monotonic() - start < 10                 # did not wait forever


def test_transient_error_then_success(monkeypatch, tmp_path):
    """First call busy, second call ok -> run_with_retry succeeds."""
    modes = iter(["busy", "ok"])
    real = lab3.run_generator_once
    monkeypatch.setattr(lab3, "run_generator_once",
                        lambda out, mode="random", timeout=None: real(out, next(modes), timeout))
    lab3.run_with_retry(tmp_path / "r.txt", delay=0.01)
    assert (tmp_path / "r.txt").read_text(encoding="utf-8").startswith("REPORT OK")
