"""
Lab 1 - run the mini framework end to end (no GUI needed).

    python run_demo.py              # dev: DEBUG log file, flaky clicks -> watch the retries
    python run_demo.py --env qa     # qa : INFO log file, no flakiness, longer timeouts

Then open logs/run_<timestamp>.log and compare it with the console output.
"""
import argparse
import sys

from app_sim.simulated_desktop import SimulatedDesktop
from core.config_reader import get_config
from core.logger import get_logger, setup_logging
from pages.calculator_window import CalculatorWindow


def main():
    parser = argparse.ArgumentParser(description="Mini framework demo")
    parser.add_argument("--env", help="dev or qa (default: TEST_ENV or default_env)")
    args = parser.parse_args()

    config = get_config(args.env)
    log_file = setup_logging(config["log_level"], keep_last=config["keep_logs"])
    log = get_logger("run_demo")
    log.info("Environment: %s", config["env"])

    checks = [(7, "+", 8, 15), (12, "*", 11, 132), (5, "-", 9, -4), (84, "/", 4, 21)]
    failures = 0
    calc = CalculatorWindow(config, SimulatedDesktop()).open()
    try:
        for a, op, b, expected in checks:
            actual = calc.calculate(a, op, b)
            if actual == expected:
                log.info("PASS %s %s %s = %s", a, op, b, actual)
            else:
                failures += 1
                log.error("FAIL %s %s %s: expected %s, got %s", a, op, b, expected, actual)
                calc.screenshot(f"calc_{a}{op}{b}".replace("/", "div").replace("*", "mul"))
    except Exception:
        log.exception("Unexpected error - see traceback")
        calc.screenshot("unexpected_error")
        failures += 1
    finally:
        calc.close()

    log.info("Finished: %d check(s), %d failure(s). Log: %s", len(checks), failures, log_file)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
