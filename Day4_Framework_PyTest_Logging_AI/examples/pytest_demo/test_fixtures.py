"""
test_fixtures.py - setup/teardown, yield fixtures, scopes, conftest fixtures.

See the execution order live:
    pytest test_fixtures.py -s        (-s = show print output)
    pytest test_fixtures.py --setup-show
"""
import pytest

from calculator import Calculator

EVENTS = []          # records the order in which setup/teardown happen


# ---------------------------------------------------------------------------
# xUnit-style module setup/teardown (what unittest users know) - still works
# ---------------------------------------------------------------------------
def setup_module(module):
    print("\n[setup_module]    once, before the first test in this file")


def teardown_module(module):
    print("\n[teardown_module] once, after the last test in this file")


# ---------------------------------------------------------------------------
# Fixtures with different scopes
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def shared_app():
    """MODULE scope: created once for all tests in this file (like launching the
    app once to save time)."""
    print("\n[module fixture]  launch app")
    EVENTS.append("module-setup")
    app = Calculator().open()
    yield app
    print("\n[module fixture]  close app")
    app.close()


@pytest.fixture
def fresh_state(shared_app):
    """FUNCTION scope (default): runs before EACH test - resets state so tests
    stay independent even though they share one app."""
    EVENTS.append("function-setup")
    shared_app.clear()
    yield shared_app
    EVENTS.append("function-teardown")


def test_first_calculation(fresh_state):
    fresh_state.calculate(2, "+", 2)
    assert len(fresh_state.history) == 1


def test_second_calculation_starts_clean(fresh_state):
    # history was cleared by the fixture - test does not depend on the previous one
    assert fresh_state.history == []
    fresh_state.calculate(5, "*", 2)
    assert fresh_state.history[-1][-1] == 10


def test_module_fixture_created_once(shared_app):
    # However many tests used shared_app before this one, it was set up only ONCE
    assert EVENTS.count("module-setup") == 1
    assert shared_app.is_open


# ---------------------------------------------------------------------------
# Fixtures from conftest.py: calculator, logger, config (no import needed)
# ---------------------------------------------------------------------------
def test_uses_conftest_calculator(calculator, logger):
    logger.info("Running with the conftest calculator fixture")
    assert calculator.is_open
    assert calculator.calculate(9, "-", 4) == 5


def test_config_depends_on_env(config):
    # pytest --env qa  -> timeout 15
    assert config["env"] in ("dev", "qa")
    assert config["timeout"] > 0


# ---------------------------------------------------------------------------
# Built-in fixtures: tmp_path, request.addfinalizer, caplog
# ---------------------------------------------------------------------------
def test_tmp_path_for_files(tmp_path):
    """tmp_path = unique empty folder per test, cleaned up automatically."""
    report = tmp_path / "export.txt"
    report.write_text("TOTAL=42\n")
    assert report.read_text().strip() == "TOTAL=42"


def test_addfinalizer(request):
    calc = Calculator().open()
    request.addfinalizer(calc.close)          # alternative to yield for teardown
    assert calc.is_open


def test_caplog_checks_log_messages(calculator, caplog):
    """caplog captures log records so you can ASSERT on logging."""
    caplog.set_level("DEBUG")
    calculator.calculate(6, "/", 3)
    assert "6.0 / 3.0 = 2.0" in caplog.text
    assert any(r.levelname == "DEBUG" for r in caplog.records)


# ---------------------------------------------------------------------------
# Autouse fixture: applies to every test in this file without being requested
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def announce(request):
    yield
    # request.node.name = current test name
    print(f"  -> finished {request.node.name}")
