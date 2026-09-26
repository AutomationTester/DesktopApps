"""
BaseWindow - parent class of every window object ("Window Object Model",
the desktop version of the Page Object Model).

  * one class per application window (CalculatorWindow, LoginWindow ...)
  * tests talk ONLY to those classes, never to pywinauto directly
  * common behaviour (waiting, clicking with retry, logging, screenshots) lives here once

`desktop` is pywinauto.Desktop(backend="uia") in real life. In this lab we pass the
SimulatedDesktop, which offers the same methods, so no GUI is needed.
(Compare with ../../../../automation_framework/core/base_window.py - the real one.)
"""
from datetime import datetime

from core.logger import get_logger
from core.paths import SCREENSHOT_DIR
from core.waits import retry, wait_until


class BaseWindow:
    def __init__(self, config, desktop):
        self.config = config
        self.desktop = desktop
        self.app_timeout = config["timeouts"]["app_start"]
        self.element_timeout = config["timeouts"]["element"]
        self.retry_times = config["retry"]["times"]
        self.retry_delay = config["retry"]["delay"]
        self.log = get_logger(f"pages.{type(self).__name__}")
        self.window = None

    # ---------------- window level ----------------
    def connect(self, title):
        """Attach to a top-level window and WAIT until it is visible (no sleep)."""
        self.log.info("Waiting up to %ss for window '%s'", self.app_timeout, title)
        self.window = wait_until(lambda: self.desktop.window(title=title),
                                 timeout=self.app_timeout, message=f"window '{title}' to exist")
        self.window.wait("visible", timeout=self.app_timeout)
        self.log.info("Connected to '%s'", title)
        return self

    def is_open(self):
        return self.window is not None and self.window.exists(timeout=0)

    # ---------------- control level ----------------
    def find(self, **criteria):
        """Return a control, waiting until it exists. Prefer auto_id over title/index."""
        control = self.window.child_window(**criteria)
        control.wait("exists", timeout=self.element_timeout)
        return control

    def click(self, **criteria):
        """Click with retry + exponential backoff (values from config)."""
        @retry(times=self.retry_times, delay=self.retry_delay)
        def click_control():
            control = self.find(**criteria)
            self.log.debug("Click %s", criteria)
            try:
                control.invoke()             # UI Automation pattern - no mouse needed
            except AttributeError:
                control.click_input()        # fallback: real mouse click
        click_control()

    def read_text(self, **criteria):
        text = self.find(**criteria).window_text()
        self.log.debug("Read %s -> %r", criteria, text)
        return text

    def wait_for_text(self, expected, timeout=None, **criteria):
        return wait_until(lambda: expected in self.read_text(**criteria),
                          timeout=timeout or self.element_timeout,
                          message=f"text '{expected}' in {criteria}")

    def screenshot(self, name):
        """Real framework: PIL.ImageGrab / pyautogui screenshot -> .png.
        Simulated app: save a text 'snapshot' of the window state instead."""
        SCREENSHOT_DIR.mkdir(exist_ok=True)
        path = SCREENSHOT_DIR / f"{name}_{datetime.now():%Y%m%d_%H%M%S}.txt"
        state = self.window.engine.display() if self.window is not None else "no window"
        path.write_text(f"Window snapshot for {name}\nDisplay: {state}\n", encoding="utf-8")
        self.log.info("Screenshot saved: %s", path.name)
        return path
