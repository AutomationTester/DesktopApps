"""
Lab 3 - Faulty Script 5 (BONUS): OOP MISTAKES (FIXED)
======================================================
How to run:
    python lab3_bug5_oop_error.py

Bugs fixed:
  1. TypeError: LoginWindow.enter_username() takes 1 positional argument but 2 were given
     Every instance method needs 'self' as its FIRST parameter. Python passes
     the object automatically, so window.enter_username("admin") sends 2 values.
  2. AttributeError: 'LoginWindow' object has no attribute 'title'
     The child __init__ did not call super().__init__(title), so the parent
     never created self.title and self.is_open.
  3. Logic bug: window.open (no brackets) only REFERS to the method, it does
     not CALL it. No error, but open=False. Fix: window.open()
"""


class BaseWindow:
    def __init__(self, title):
        self.title = title
        self.is_open = False

    def open(self):
        self.is_open = True


class LoginWindow(BaseWindow):
    def __init__(self, title):
        super().__init__(title)             # FIX 2: let the parent set title/is_open
        self.username = ""

    def enter_username(self, username):     # FIX 1: added self
        self.username = username

    def summary(self):
        return f"{self.title}: user={self.username}, open={self.is_open}"


window = LoginWindow("Login")
window.open()                               # FIX 3: call the method with ()
window.enter_username("admin")
print(window.summary())
