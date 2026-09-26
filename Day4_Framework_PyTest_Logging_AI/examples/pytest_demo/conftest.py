"""
conftest.py - shared fixtures and hooks for the pytest demo.

pytest loads this file AUTOMATICALLY (never import it). Everything defined here
is available to every test file in this folder and its sub-folders.

Contents:
  1. --env command line option + config fixture   (environment handling)
  2. logger fixture                                (session scope)
  3. calculator fixture with yield                 (setup / teardown)
  4. pytest_runtest_makereport hook                (capture artefacts on failure
                                                    and attach them to pytest-html)
  5. pytest-html customisation hooks               (optional)
"""
import base64
import logging
from datetime import datetime
from pathlib import Path

import pytest

from calculator import Calculator

HERE = Path(__file__).parent
ARTIFACT_DIR = HERE / "artifacts"

# Environment settings - in the real framework these come from config/config.yaml
ENVIRONMENTS = {
    "dev": {"timeout": 5, "retries": 1, "log_level": "DEBUG"},
    "qa": {"timeout": 15, "retries": 3, "log_level": "INFO"},
}


# ---------------------------------------------------------------------------
# 1. Custom command line option + config fixture
# ---------------------------------------------------------------------------
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", choices=sorted(ENVIRONMENTS),
                     help="target environment: dev or qa (default dev)")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def config(env):
    cfg = dict(ENVIRONMENTS[env], env=env)
    logging.getLogger("conftest").info("Loaded config for env=%s: %s", env, cfg)
    return cfg


# ---------------------------------------------------------------------------
# 2. Logger fixture
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def logger():
    """One named logger for the whole run. pytest's logging plugin captures it
    (shown on failure, written to log_file from pytest.ini)."""
    return logging.getLogger("demo")


# ---------------------------------------------------------------------------
# 3. Calculator fixture - setup before yield, teardown after yield
# ---------------------------------------------------------------------------
@pytest.fixture
def calculator(logger):
    logger.info("SETUP: opening calculator")
    calc = Calculator().open()
    yield calc                           # <- the test runs here
    logger.info("TEARDOWN: closing calculator")
    calc.close()                         # runs even if the test failed


# ---------------------------------------------------------------------------
# 4. Capture artefacts on failure
# ---------------------------------------------------------------------------
def _take_screenshot(path_no_ext: Path):
    """Real screenshot if Pillow's ImageGrab works (Windows desktop session),
    otherwise a text placeholder so the demo also works headless / on Linux CI.
    Returns (path, is_image)."""
    try:
        from PIL import ImageGrab
        image = ImageGrab.grab()
        path = path_no_ext.with_suffix(".png")
        image.save(path)
        return path, True
    except Exception as exc:                       # ImportError, OSError (no display) ...
        path = path_no_ext.with_suffix(".txt")
        path.write_text(f"Screenshot not available on this machine: {exc!r}\n", encoding="utf-8")
        return path, False


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Called 3 times per test (setup, call, teardown). We let pytest build the
    report first (yield), then inspect it."""
    outcome = yield
    report = outcome.get_result()

    # Make the report available to fixtures: item.rep_setup / rep_call / rep_teardown
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        ARTIFACT_DIR.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = ARTIFACT_DIR / f"{item.name}_{stamp}"

        shot_path, is_image = _take_screenshot(base)

        log_path = base.with_name(base.name + "_log.txt")
        log_path.write_text(
            f"TEST : {item.nodeid}\n"
            f"TIME : {stamp}\n\n"
            f"--- captured log ---\n{report.caplog}\n\n"
            f"--- captured stdout ---\n{report.capstdout}\n\n"
            f"--- failure ---\n{report.longreprtext}\n",
            encoding="utf-8",
        )
        logging.getLogger("conftest").error("Test failed - artefacts: %s, %s",
                                            shot_path.name, log_path.name)

        # Attach to pytest-html if it is installed and active
        pytest_html = item.config.pluginmanager.getplugin("html")
        if pytest_html is not None:
            extras = getattr(report, "extras", [])
            if is_image:
                b64 = base64.b64encode(shot_path.read_bytes()).decode("ascii")
                extras.append(pytest_html.extras.png(b64, name="Screenshot on failure"))
            else:
                extras.append(pytest_html.extras.text(shot_path.read_text(), name="Screenshot"))
            extras.append(pytest_html.extras.text(log_path.read_text(encoding="utf-8"),
                                                  name="Failure log"))
            report.extras = extras


@pytest.fixture
def result_logger(request, logger):
    """Uses the report stored by the hook above to log PASS/FAIL at teardown."""
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep is not None:
        logger.info("RESULT %s -> %s", request.node.name, rep.outcome.upper())


# ---------------------------------------------------------------------------
# 5. pytest-html customisation (optionalhook: no error if pytest-html is missing)
# ---------------------------------------------------------------------------
@pytest.hookimpl(optionalhook=True)
def pytest_html_report_title(report):
    report.title = "Day 4 - PyTest Demo Report"


def pytest_configure(config):
    # Metadata shown in the "Environment" table of the HTML report (pytest-metadata)
    if hasattr(config, "stash"):
        try:
            from pytest_metadata.plugin import metadata_key
            config.stash[metadata_key]["Project"] = "Day4 pytest_demo"
            config.stash[metadata_key]["Environment"] = config.getoption("--env")
        except Exception:
            pass
