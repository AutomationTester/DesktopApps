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


# TODO (Lab 2, step 2): write a MODULE-scoped fixture named `calculator` that
#   - creates CalculatorWindow(config, SimulatedDesktop()).open()
#   - yields it to the tests
#   - closes it afterwards (teardown)


# TODO (Lab 2, step 5): screenshot on failure
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#     - only continue if report.when == "call" and report.failed
#     - page = item.funcargs.get("calculator"); stop if None
#     - path = page.screenshot(item.name)
#     - html = item.config.pluginmanager.getplugin("html")
#     - if html: report.extras = getattr(report, "extras", []) +
#                 [html.extras.text(path.read_text(encoding="utf-8"), name="Window snapshot")]
