"""Window object for the Calculator. ALL locators for this window live here and nowhere else."""
from core.base_window import BaseWindow

DIGIT_BUTTONS = {str(d): f"num{d}Button" for d in range(10)}
OPERATOR_BUTTONS = {"+": "plusButton", "-": "minusButton", "*": "multiplyButton", "/": "divideButton"}
NEGATE_BUTTON = "negateButton"
EQUALS_BUTTON = "equalButton"
CLEAR_BUTTON = "clearButton"
RESULT_TEXT = "CalculatorResults"


class CalculatorWindow(BaseWindow):
    def open(self):
        settings = self.config["calculator"]
        self.log.info("Launching Calculator")
        # Real app: subprocess.Popen("calc.exe")
        self.desktop.launch(settings["window_title"],
                            startup_delay=settings["startup_delay"],
                            flaky_click_rate=settings["flaky_click_rate"])
        self.connect(title=settings["window_title"])
        self.clear()
        return self

    def clear(self):
        self.click(auto_id=CLEAR_BUTTON)

    def enter_number(self, number):
        text = str(int(float(number)))
        # TODO (Lab 1, step 6): click DIGIT_BUTTONS[ch] for every digit in text (ignore the '-')
        #                        then, if text starts with '-', click NEGATE_BUTTON
        raise NotImplementedError

    def press_operator(self, operator):
        # TODO (Lab 1, step 6): raise ValueError("Unsupported operator ...") if operator is unknown,
        #                        otherwise click OPERATOR_BUTTONS[operator]
        raise NotImplementedError

    def press_equals(self):
        self.click(auto_id=EQUALS_BUTTON)

    def display_text(self):
        return self.read_text(auto_id=RESULT_TEXT)

    @property
    def result(self):
        """'Display is 15' -> 15.0 ; raises ValueError for 'Cannot divide by zero'."""
        return float(self.display_text().replace("Display is", "").replace(",", "").strip())

    def calculate(self, a, operator, b):
        """Business-level action: the test says WHAT, the window object knows HOW."""
        self.log.info("Calculate %s %s %s", a, operator, b)
        # TODO (Lab 1, step 6):
        #   clear -> wait_for_text("Display is 0", auto_id=RESULT_TEXT) -> enter a -> operator
        #   -> enter b -> equals -> value = self.result -> log INFO "Result = ..." -> return value
        raise NotImplementedError

    def close(self):
        if self.is_open():
            self.log.info("Closing Calculator")
            self.window.close()
