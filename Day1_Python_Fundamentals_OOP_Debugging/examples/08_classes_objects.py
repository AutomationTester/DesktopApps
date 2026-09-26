"""
Example 08 - Class and Object
==============================
Day 1 | Topic: Why OOP matters, Class and Object

How to run:
    python 08_classes_objects.py

CLASS  = a blueprint / template   (e.g. the design of a "Test Case" form)
OBJECT = a real thing made from it (e.g. TC_001, TC_002 ... filled forms)
"""

# ---------------------------------------------------------------
# 1. WITHOUT OOP - loose variables, easy to mix up
# ---------------------------------------------------------------
print("--- Without OOP ---")
tc1_id, tc1_title, tc1_status = "TC_001", "Login with valid user", "Not Run"
tc2_id, tc2_title, tc2_status = "TC_002", "Login with wrong password", "Not Run"
print(tc1_id, tc1_title, tc1_status)
print(tc2_id, tc2_title, tc2_status)
# Imagine 500 test cases like this... hard to manage!


# ---------------------------------------------------------------
# 2. WITH OOP - one class, many objects
# ---------------------------------------------------------------
class TestCase:
    """Blueprint for a test case."""

    def __init__(self, test_id, title):
        # Attributes: data that each object carries
        self.test_id = test_id
        self.title = title
        self.status = "Not Run"

    # Method: an action the object can perform
    def mark(self, status):
        self.status = status

    def show(self):
        print(f"{self.test_id} | {self.title:28} | {self.status}")


print("\n--- With OOP ---")
tc1 = TestCase("TC_001", "Login with valid user")        # object 1
tc2 = TestCase("TC_002", "Login with wrong password")    # object 2

tc1.mark("PASS")
tc2.mark("FAIL")

tc1.show()
tc2.show()

# ---------------------------------------------------------------
# 3. Each object is independent
# ---------------------------------------------------------------
print("\n--- Objects are independent ---")
print("tc1.status =", tc1.status)
print("tc2.status =", tc2.status)
print("Type of tc1:", type(tc1).__name__)
print("Is tc1 a TestCase?", isinstance(tc1, TestCase))

# ---------------------------------------------------------------
# 4. Many objects in a list - a mini test suite
# ---------------------------------------------------------------
print("\n--- A list of objects (test suite) ---")
suite = [
    TestCase("TC_003", "Search by customer name"),
    TestCase("TC_004", "Export report to PDF"),
    TestCase("TC_005", "Print invoice"),
]
for tc in suite:
    tc.mark("PASS")
    tc.show()

# ---------------------------------------------------------------
# 5. You already use objects every day in Python!
# ---------------------------------------------------------------
print("\n--- Everything in Python is an object ---")
title = "calculator"                 # a str object
print(title.upper())                 # calling a METHOD of the str object
results = ["PASS"]                   # a list object
results.append("FAIL")               # calling a METHOD of the list object
print(results)
