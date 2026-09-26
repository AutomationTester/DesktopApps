"""
Example 10 - Inheritance (basic)
=================================
Day 1 | Topic: Inheritance

How to run:
    python 10_inheritance.py

Inheritance = a CHILD class gets everything from a PARENT class,
and can ADD new things or CHANGE (override) existing behaviour.

This is exactly how automation frameworks are built:
    BasePage  (common actions: open, close, take_screenshot)
      |-- LoginPage     (enter_username, enter_password, click_login)
      |-- DashboardPage (open_menu, logout)
"""


class BasePage:
    """Parent class - behaviour common to every screen of the app."""

    def __init__(self, window_title):
        self.window_title = window_title
        self.actions_log = []

    def log_action(self, action):
        self.actions_log.append(action)
        print(f"  [{self.window_title}] {action}")

    def open(self):
        self.log_action("Window opened")

    def take_screenshot(self, name):
        # simulated - on Day 2+ this will capture a real image
        self.log_action(f"Screenshot saved as {name}.png")

    def verify_title(self, expected):
        result = "PASS" if self.window_title == expected else "FAIL"
        self.log_action(f"Verify title '{expected}' -> {result}")
        return result == "PASS"


class LoginPage(BasePage):
    """Child class - inherits everything from BasePage and adds login actions."""

    def __init__(self):
        # super() calls the PARENT constructor so window_title/actions_log get created
        super().__init__("Login - Billing App")
        self.username = ""
        self.password = ""

    def enter_username(self, username):
        self.username = username
        self.log_action(f"Typed username '{username}'")

    def enter_password(self, password):
        self.password = password
        self.log_action("Typed password '********'")   # never print real passwords

    def click_login(self):
        self.log_action("Clicked Login button")
        return self.username == "admin" and self.password == "Admin@123"


class DashboardPage(BasePage):
    """Another child class."""

    def __init__(self):
        super().__init__("Dashboard - Billing App")

    # Method OVERRIDING: same name as parent, different behaviour
    def open(self):
        super().open()                                # still do the parent's work...
        self.log_action("Waiting for widgets to load")  # ...plus something extra

    def logout(self):
        self.log_action("Clicked Logout")


# ---------------------------------------------------------------
# Using the classes - a mini end-to-end flow
# ---------------------------------------------------------------
print("=== TC_010: Valid login lands on dashboard ===")

login = LoginPage()
login.open()                                   # inherited from BasePage
login.verify_title("Login - Billing App")      # inherited from BasePage
login.enter_username("admin")                  # defined in LoginPage
login.enter_password("Admin@123")
logged_in = login.click_login()

if logged_in:
    dashboard = DashboardPage()
    dashboard.open()                           # overridden version runs
    dashboard.verify_title("Dashboard - Billing App")
    dashboard.take_screenshot("TC_010_dashboard")
    dashboard.logout()
else:
    login.take_screenshot("TC_010_login_failed")

print("\n--- Checking the relationships ---")
print("LoginPage is a child of BasePage?", issubclass(LoginPage, BasePage))
print("login object is a BasePage?     ", isinstance(login, BasePage))
print("Actions recorded on login page  :", len(login.actions_log))
