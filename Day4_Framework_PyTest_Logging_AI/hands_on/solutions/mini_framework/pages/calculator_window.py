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
        for ch in text.lstrip("-"):
            self.click(auto_id=DIGIT_BUTTONS[ch])
        if text.startswith("-"):
            self.click(auto_id=NEGATE_BUTTON)

    def press_operator(self, operator):
        if operator not in OPERATOR_BUTTONS:
            raise ValueError(f"Unsupported operator '{operator}'. Use one of {list(OPERATOR_BUTTONS)}")
        self.click(auto_id=OPERATOR_BUTTONS[operator])

    def press_equals(self):
        self.click(auto_id=EQUALS_BUTTON)

    def display_text(self):
        return self.read_text(auto_id=RESULT_TEXT)

    @property
    def result(self):
        """Displayed value as float; raises ValueError for messages like 'Cannot divide by zero'."""
        return float(self.display_text().replace("Display is", "").replace(",", "").strip())

    def calculate(self, a, operator, b):
        """Business-level action: the test says WHAT, the window object knows HOW."""
        self.log.info("Calculate %s %s %s", a, operator, b)
        self.clear()
        self.wait_for_text("Display is 0", auto_id=RESULT_TEXT)
        self.enter_number(a)
        self.press_operator(operator)
        self.enter_number(b)
        self.press_equals()
        value = self.result
        self.log.info("Result = %s", value)
        return value

    def close(self):
        if self.is_open():
            self.log.info("Closing Calculator")
            self.window.close()
