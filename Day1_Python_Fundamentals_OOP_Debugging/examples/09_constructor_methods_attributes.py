"""
Example 09 - Constructor (__init__), Methods and Attributes
============================================================
Day 1 | Topic: Constructor, methods and attributes

How to run:
    python 09_constructor_methods_attributes.py

* __init__  -> runs AUTOMATICALLY when an object is created
* self      -> "this object" - Python passes it for you
* instance attribute -> belongs to one object   (self.title)
* class attribute    -> shared by all objects    (AppWindow.window_count)
* instance method    -> action using self data   (def maximize(self))
"""


class AppWindow:
    """Represents a desktop application window (simulated - no real GUI)."""

    # Class attribute: shared by ALL AppWindow objects
    window_count = 0

    def __init__(self, title, width=800, height=600):
        """Constructor: set up the starting state of the object."""
        # Instance attributes: each window has its own values
        self.title = title
        self.width = width
        self.height = height
        self.is_open = False
        self.controls = []                 # list of control names on the window
        AppWindow.window_count += 1        # update the shared counter
        print(f"[init] AppWindow created: '{self.title}'")

    # ---------------- Instance methods ----------------
    def open(self):
        self.is_open = True
        print(f"'{self.title}' opened ({self.width}x{self.height})")

    def close(self):
        self.is_open = False
        print(f"'{self.title}' closed")

    def maximize(self, screen_width=1920, screen_height=1080):
        self.width, self.height = screen_width, screen_height
        print(f"'{self.title}' maximized to {self.width}x{self.height}")

    def add_control(self, control_name):
        self.controls.append(control_name)

    def has_control(self, control_name):
        """Return True if the control exists on this window."""
        return control_name in self.controls

    def describe(self):
        """Return a one-line summary (methods can RETURN values)."""
        state = "OPEN" if self.is_open else "CLOSED"
        return f"{self.title} [{state}] controls={self.controls}"

    # ---------------- Special method ----------------
    def __str__(self):
        """Controls what print(object) shows."""
        return f"AppWindow(title='{self.title}')"


# ---------------------------------------------------------------
# Creating objects -> __init__ runs each time
# ---------------------------------------------------------------
calc = AppWindow("Calculator", 400, 600)
notepad = AppWindow("Notepad")              # uses default width/height

print("\n--- Calling methods ---")
calc.open()
calc.add_control("Button_1")
calc.add_control("Button_Plus")
calc.add_control("Button_Equals")
notepad.open()
notepad.maximize()

print("\n--- Reading attributes ---")
print("calc.title   :", calc.title)
print("calc.width   :", calc.width)
print("notepad size :", notepad.width, "x", notepad.height)

print("\n--- Methods that return values ---")
print(calc.describe())
print("Calculator has Button_Plus?", calc.has_control("Button_Plus"))
print("Calculator has Button_Sqrt?", calc.has_control("Button_Sqrt"))

print("\n--- Class attribute shared by all ---")
print("AppWindow.window_count =", AppWindow.window_count)

print("\n--- __str__ in action ---")
print(calc)
print(notepad)

print("\n--- Changing an attribute directly ---")
notepad.title = "report.txt - Notepad"
print(notepad.describe())
notepad.close()
calc.close()
