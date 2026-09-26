"""Lab 2 - fixtures and hooks for the mini framework (loaded automatically by pytest)."""
import pytest

from app_sim.simulated_desktop import SimulatedDesktop
from core.config_reader import get_config
from core.logger import get_logger, setup_logging
from pages.calculator_window import CalculatorWindow

log = get_logger("tests")


def pytest_addoption(parser):
    parser.addoption("--env", default=None, help="environment from config/config.yaml: dev or qa")


def pytest_configure(config):
    # console=False: pytest already shows/captures log output; we only add our per-run file
    settings = get_config(config.getoption("--env"))
    setup_logging(settings["log_level"], keep_last=settings["keep_logs"], console=False)


@pytest.fixture(scope="session")
def config(request):
    settings = get_config(request.config.getoption("--env"))
    log.info("Environment: %s", settings["env"])
    return settings


@pytest.fixture(scope="module")
def calculator(config):
    """One Calculator window per test module (starting an app is slow)."""
    page = CalculatorWindow(config, SimulatedDesktop()).open()
    yield page
    page.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On failure of a test that uses the calculator: save a screenshot and attach it to pytest-html."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    page = item.funcargs.get("calculator")
    if page is None:
        return
    path = page.screenshot(item.name)
    log.error("Test %s failed - screenshot %s", item.name, path.name)
    html = item.config.pluginmanager.getplugin("html")
    if html is not None:
        report.extras = getattr(report, "extras", []) + [
            html.extras.text(path.read_text(encoding="utf-8"), name="Window snapshot")
        ]
