"""
BaseWindow - parent class of every window object ("Window Object Model",
the desktop version of the Page Object Model).

`desktop` is pywinauto.Desktop(backend="uia") in real life. In this lab we pass the
SimulatedDesktop (app_sim/simulated_desktop.py), which offers the same methods:
    desktop.window(title=...)  window.wait("visible", timeout=...)  window.child_window(**criteria)
    control.wait("exists", timeout=...)  control.invoke()  control.window_text()
"""
from datetime import datetime

from core.logger import get_logger
from core.paths import SCREENSHOT_DIR
from core.waits import retry, wait_until


class BaseWindow:
    def __init__(self, config, desktop):
        self.config = config
        self.desktop = desktop
        # TODO (Lab 1, step 5): read these from config instead of hard-coding
        #   config["timeouts"]["app_start"], config["timeouts"]["element"],
        #   config["retry"]["times"], config["retry"]["delay"]
        self.app_timeout = 5
        self.element_timeout = 3
        self.retry_times = 3
        self.retry_delay = 0.1
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
        """Return a control, waiting until it exists."""
        # TODO (Lab 1, step 5):
        #   control = self.window.child_window(**criteria)
        #   control.wait("exists", timeout=self.element_timeout)
        #   return control
        raise NotImplementedError

    def click(self, **criteria):
        """Click with retry + exponential backoff (values from config)."""
        @retry(times=self.retry_times, delay=self.retry_delay)
        def click_control():
            # TODO (Lab 1, step 5): find the control, log it at DEBUG level, call control.invoke()
            raise NotImplementedError
        click_control()

    def read_text(self, **criteria):
        # TODO (Lab 1, step 5): return self.find(**criteria).window_text()  (log it at DEBUG)
        raise NotImplementedError

    def wait_for_text(self, expected, timeout=None, **criteria):
        return wait_until(lambda: expected in self.read_text(**criteria),
                          timeout=timeout or self.element_timeout,
                          message=f"text '{expected}' in {criteria}")

    def screenshot(self, name):
        """Simulated app: save a text 'snapshot' of the window state (real app: PIL ImageGrab)."""
        SCREENSHOT_DIR.mkdir(exist_ok=True)
        path = SCREENSHOT_DIR / f"{name}_{datetime.now():%Y%m%d_%H%M%S}.txt"
        state = self.window.engine.display() if self.window is not None else "no window"
        path.write_text(f"Window snapshot for {name}\nDisplay: {state}\n", encoding="utf-8")
        self.log.info("Screenshot saved: %s", path.name)
        return path
