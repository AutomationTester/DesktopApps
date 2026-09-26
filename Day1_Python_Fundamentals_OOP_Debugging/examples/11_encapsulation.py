"""
Example 11 - Encapsulation (basic)
===================================
Day 1 | Topic: Encapsulation

How to run:
    python 11_encapsulation.py

Encapsulation = keep data and the code that protects it TOGETHER,
and stop outside code from changing data in a wrong way.

Python naming conventions:
    self.name      -> public    (use freely)
    self._name     -> protected (a hint: "internal, please don't touch")
    self.__name    -> private   (name-mangled, hard to reach from outside)

@property lets you READ a value like an attribute while still
controlling how it is SET.
"""


class TestConfig:
    """Holds settings for a test run and protects them from bad values."""

    def __init__(self, app_path, timeout_seconds=10, password="secret"):
        self.app_path = app_path                 # public
        self._timeout = 0                        # protected (internal)
        self.__password = password               # private
        self.timeout = timeout_seconds           # goes through the setter below

    # ---------- property: controlled access to _timeout ----------
    @property
    def timeout(self):
        """Getter - runs when you READ config.timeout"""
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        """Setter - runs when you WRITE config.timeout = value"""
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"timeout must be a positive number, got {value!r}")
        if value > 120:
            print(f"  Warning: timeout {value}s is very high, capping to 120s")
            value = 120
        self._timeout = value

    # ---------- controlled access to the private password ----------
    def masked_password(self):
        """Never expose the real password - show a masked version."""
        return "*" * len(self.__password)

    def check_password(self, attempt):
        return attempt == self.__password


# ---------------------------------------------------------------
# Using the class
# ---------------------------------------------------------------
config = TestConfig(r"C:\apps\qa\billing.exe", timeout_seconds=15, password="Qa@2026")

print("--- Public attribute ---")
print("App path:", config.app_path)

print("\n--- Property (looks like an attribute, but is validated) ---")
print("Timeout :", config.timeout)
config.timeout = 30
print("Timeout after change:", config.timeout)
config.timeout = 500                      # too high -> capped by the setter
print("Timeout after capping:", config.timeout)

print("\n--- Invalid value is rejected ---")
try:
    config.timeout = -5
except ValueError as error:
    print("Rejected:", error)
print("Timeout is still:", config.timeout)

print("\n--- Private data stays hidden ---")
print("Masked password :", config.masked_password())
print("Check 'abc'     :", config.check_password("abc"))
print("Check 'Qa@2026' :", config.check_password("Qa@2026"))

try:
    print(config.__password)             # cannot read it directly
except AttributeError as error:
    print("AttributeError:", error)

# Note: Python does not make it truly impossible - it renames it to
# _TestConfig__password ("name mangling"). Encapsulation in Python is
# about clear intent and safe interfaces, not about locking things.
print("(Name-mangled attribute exists:", hasattr(config, "_TestConfig__password"), ")")
