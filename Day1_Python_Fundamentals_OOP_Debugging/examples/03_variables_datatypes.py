"""
Example 03 - Variables and Data Types
======================================
Day 1 | Topic: Variables and data types

How to run:
    python 03_variables_datatypes.py

A variable is a NAME that points to a VALUE.
Python works out the type automatically (dynamic typing).
Use type(value) to see the type of any value.
"""

# ---------------------------------------------------------------
# 1. Basic (scalar) data types
# ---------------------------------------------------------------
test_case_id = "TC_LOGIN_001"   # str   -> text
retry_count = 3                 # int   -> whole number
response_time = 1.75            # float -> decimal number (seconds)
is_passed = True                # bool  -> True / False
defect_id = None                # NoneType -> "no value yet"

print("--- Basic data types ---")
print(test_case_id, "->", type(test_case_id))
print(retry_count, "->", type(retry_count))
print(response_time, "->", type(response_time))
print(is_passed, "->", type(is_passed))
print(defect_id, "->", type(defect_id))

# ---------------------------------------------------------------
# 2. Strings - the most common type in automation
#    (window titles, button names, log messages...)
# ---------------------------------------------------------------
print("\n--- Working with strings ---")
window_title = "Untitled - Notepad"
print("Title          :", window_title)
print("Upper case     :", window_title.upper())
print("Length         :", len(window_title))
print("Contains Notepad?", "Notepad" in window_title)
print("Replace        :", window_title.replace("Untitled", "report.txt"))
print("First 8 chars  :", window_title[0:8])        # slicing [start:end]

# f-strings: put variables directly inside text using {}
tester = "Priya"
print(f"{tester} executed {test_case_id} in {response_time} seconds")

# ---------------------------------------------------------------
# 3. Type conversion (casting)
#    Values read from files/screens usually arrive as TEXT.
# ---------------------------------------------------------------
print("\n--- Type conversion ---")
text_from_screen = "42"                   # looks like a number, but it is text
as_number = int(text_from_screen)         # convert str -> int
print(as_number + 8)                      # 50 (maths works now)
print(str(retry_count) + " retries")      # convert int -> str to join text
print(float("99.5"), bool(0), bool(1))   # 99.5 False True

# ---------------------------------------------------------------
# 4. Collection types
# ---------------------------------------------------------------
print("\n--- list: ordered, changeable ---")
test_results = ["PASS", "FAIL", "PASS", "SKIP"]
test_results.append("PASS")             # add at end
print(test_results)
print("First result :", test_results[0])   # index starts at 0
print("Last result  :", test_results[-1])  # -1 = last item
print("Total results:", len(test_results))
print("PASS count   :", test_results.count("PASS"))

print("\n--- tuple: ordered, NOT changeable ---")
screen_resolution = (1920, 1080)        # fixed values -> tuple
print("Width:", screen_resolution[0], "Height:", screen_resolution[1])

print("\n--- dict: key -> value pairs ---")
login_data = {
    "username": "admin",
    "password": "Admin@123",
    "role": "manager",
}
print("Username:", login_data["username"])
login_data["role"] = "tester"                       # update a value
login_data["remember_me"] = True                    # add a new key
print("All keys:", list(login_data.keys()))
print("Safe get (missing key):", login_data.get("otp", "not provided"))

print("\n--- set: unique values only ---")
browsers_tested = {"Chrome", "Edge", "Chrome", "Firefox"}
print(browsers_tested, "-> duplicates removed, count =", len(browsers_tested))

# ---------------------------------------------------------------
# 5. Variable naming rules (PEP 8 style)
# ---------------------------------------------------------------
# good : snake_case, meaningful  -> expected_title, max_wait_seconds
# bad  : x, a1, ExpectedTitle (that style is for classes), 1st_value (invalid)
MAX_WAIT_SECONDS = 30   # UPPER_CASE = a constant by convention
print("\nConstant MAX_WAIT_SECONDS =", MAX_WAIT_SECONDS)
