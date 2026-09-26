"""
Example 07 - Functions and Reusability
=======================================
Day 1 | Topic: Functions and reusability

How to run:
    python 07_functions.py

A function is a named, reusable block of code.
Write once -> call many times. Change once -> fixed everywhere.
"""
from datetime import datetime


# ---------------------------------------------------------------
# 1. Function with no parameters
# ---------------------------------------------------------------
def print_banner():
    """Print a separator line."""
    print("=" * 45)


# ---------------------------------------------------------------
# 2. Function with parameters and a return value
# ---------------------------------------------------------------
def verify_equal(expected, actual):
    """Return 'PASS' if both values are equal, else 'FAIL'."""
    if expected == actual:
        return "PASS"
    return "FAIL"


# ---------------------------------------------------------------
# 3. Default parameter values
# ---------------------------------------------------------------
def log(message, level="INFO"):
    """Print a log line with time stamp. level is optional."""
    time_now = datetime.now().strftime("%H:%M:%S")
    print(f"[{time_now}] [{level}] {message}")


# ---------------------------------------------------------------
# 4. Returning more than one value (Python returns a tuple)
# ---------------------------------------------------------------
def summarize(results):
    """Return (passed, failed, pass_percent) for a list of results."""
    passed = results.count("PASS")
    failed = results.count("FAIL")
    percent = passed / len(results) * 100 if results else 0.0
    return passed, failed, percent


# ---------------------------------------------------------------
# 5. Type hints (optional) - make the function easier to read
# ---------------------------------------------------------------
def is_within_sla(response_time: float, sla: float = 3.0) -> bool:
    """True when response time is within the allowed SLA seconds."""
    return response_time <= sla


# ---------------------------------------------------------------
# 6. A reusable "test step" function used many times
# ---------------------------------------------------------------
def run_check(check_name, expected, actual):
    """Run one verification and log it. Returns True if passed."""
    result = verify_equal(expected, actual)
    level = "INFO" if result == "PASS" else "ERROR"
    log(f"{check_name}: expected={expected!r} actual={actual!r} -> {result}", level)
    return result == "PASS"


# ---------------------------------------------------------------
# Using the functions
# ---------------------------------------------------------------
print_banner()
print(" Functions demo - Login screen checks")
print_banner()

log("Test started")                         # uses default level INFO
log("Disk space low", level="WARNING")      # keyword argument

# Reuse the same function for different checks
checks = [
    run_check("Window title", "Login", "Login"),
    run_check("Button text", "Sign In", "Sign In"),
    run_check("Error label", "", "Invalid password"),
]
print("All checks passed?", all(checks))

# Multiple return values -> unpack into three variables
passed, failed, percent = summarize(["PASS", "PASS", "FAIL", "PASS"])
print(f"\nSummary -> passed={passed}, failed={failed}, pass%={percent:.1f}")

# Type-hinted function with default parameter
print("2.5s within SLA?", is_within_sla(2.5))
print("4.2s within SLA?", is_within_sla(4.2))
print("4.2s within 5s SLA?", is_within_sla(4.2, sla=5))

# ---------------------------------------------------------------
# 7. Scope - variables inside a function are LOCAL
# ---------------------------------------------------------------
def demo_scope():
    local_value = "only visible inside demo_scope"
    return local_value

print("\nScope demo:", demo_scope())
# print(local_value)   # <- would raise NameError: it only lives inside the function

# ---------------------------------------------------------------
# 8. Built-in functions you will use daily
# ---------------------------------------------------------------
times = [1.2, 0.8, 2.9, 1.7]
print("\nBuilt-ins -> len:", len(times), "| min:", min(times),
      "| max:", max(times), "| sum:", round(sum(times), 2),
      "| sorted:", sorted(times))
