"""
Lab 3 - Faulty Script 5 (BONUS): OOP MISTAKES
==============================================
How to run:
    python lab3_bug5_oop_error.py

Purpose of the script:
    A small "page object" for a login window (simulated, no real GUI).

Expected output after you fix it:
    Login: user=admin, open=True

This file has 3 classic OOP bugs:
    * one raises TypeError
    * one raises AttributeError
    * one gives no error at all, but a wrong value
"""


class BaseWindow:
    def __init__(self, title):
        self.title = title
        self.is_open = False

    def open(self):
        self.is_open = True


class LoginWindow(BaseWindow):
    def __init__(self, title):
        self.username = ""

    def enter_username(username):
        self.username = username

    def summary(self):
        return f"{self.title}: user={self.username}, open={self.is_open}"


window = LoginWindow("Login")
window.open
window.enter_username("admin")
print(window.summary())
