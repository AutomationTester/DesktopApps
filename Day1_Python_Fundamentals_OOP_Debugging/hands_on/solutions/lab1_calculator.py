"""
Lab 1 - Calculator using Functions (SOLUTION)
==============================================
How to run:
    python lab1_calculator.py                 -> runs the automatic self-test
    python lab1_calculator.py --interactive   -> (stretch goal) asks YOU for input

The self-test section works like a tiny automated test suite:
every row of test data has inputs and an EXPECTED result, and the script
prints PASS/FAIL by comparing expected with actual.
"""
import sys


# ------------------------------------------------------------------
# Task 1: basic operations - one small function per job
# ------------------------------------------------------------------
def add(a, b):
    """Return a + b."""
    return a + b


def subtract(a, b):
    """Return a - b."""
    return a - b


def multiply(a, b):
    """Return a * b."""
    return a * b


def divide(a, b):
    """Return a / b. Raise ZeroDivisionError with a clear message if b is 0."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


# ------------------------------------------------------------------
# Task 2: extra operations
# ------------------------------------------------------------------
def power(a, b):
    """Return a raised to the power b."""
    return a ** b


def modulus(a, b):
    """Return the remainder of a / b."""
    if b == 0:
        raise ZeroDivisionError("Cannot take modulus by zero")
    return a % b


def percentage(part, total):
    """Return what percent 'part' is of 'total' (e.g. pass percentage)."""
    if total == 0:
        raise ZeroDivisionError("Total cannot be zero")
    return part / total * 100


# ------------------------------------------------------------------
# Task 3: one function that picks the right operation (reusability!)
# ------------------------------------------------------------------
OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "**": power,
    "%": modulus,
}


def calculate(a, operator, b):
    """Apply 'operator' to a and b. Raise ValueError for an unknown operator."""
    if operator not in OPERATIONS:
        raise ValueError(f"Unsupported operator: {operator!r}")
    function = OPERATIONS[operator]      # look up the function...
    return function(a, b)                # ...and call it


# ------------------------------------------------------------------
# Task 4: self-test (data-driven) - DO NOT need user input
# ------------------------------------------------------------------
def run_self_test():
    test_data = [
        # (test id, a, operator, b, expected)
        ("CALC_01", 10, "+", 5, 15),
        ("CALC_02", 10, "-", 15, -5),
        ("CALC_03", 6, "*", 7, 42),
        ("CALC_04", 9, "/", 2, 4.5),
        ("CALC_05", 2, "**", 10, 1024),
        ("CALC_06", 17, "%", 5, 2),
        ("CALC_07", 0.1, "+", 0.2, 0.3),           # float trap - see compare below
        ("CALC_08", 5, "/", 0, "ZeroDivisionError"),
        ("CALC_09", 5, "^", 2, "ValueError"),
    ]

    passed = 0
    print("=" * 60)
    print(" CALCULATOR SELF-TEST")
    print("=" * 60)
    for test_id, a, op, b, expected in test_data:
        try:
            actual = calculate(a, op, b)
        except (ZeroDivisionError, ValueError) as error:
            actual = type(error).__name__          # store the error NAME as result

        # floats: compare with a small tolerance (0.1 + 0.2 = 0.30000000000000004)
        if isinstance(expected, float) and isinstance(actual, float):
            ok = abs(expected - actual) < 1e-9
        else:
            ok = expected == actual

        status = "PASS" if ok else "FAIL"
        passed += ok                               # True counts as 1
        expression = f"{a} {op} {b}"
        print(f" {test_id}  {expression:<10} expected={expected!s:<18} actual={actual!s:<20} {status}")

    total = len(test_data)
    print("-" * 60)
    print(f" Passed {passed}/{total}  ({percentage(passed, total):.1f}%)")
    return passed == total


# ------------------------------------------------------------------
# Stretch goal: interactive mode (only with --interactive)
# ------------------------------------------------------------------
def run_interactive():
    print("Interactive calculator. Type 'q' to quit.")
    while True:
        first = input("First number (or q): ").strip()
        if first.lower() == "q":
            break
        op = input(f"Operator {list(OPERATIONS)}: ").strip()
        second = input("Second number: ").strip()
        try:
            result = calculate(float(first), op, float(second))
            print("Result:", result)
        except ValueError as error:
            print("Input error:", error)
        except ZeroDivisionError as error:
            print("Math error:", error)


if __name__ == "__main__":
    if "--interactive" in sys.argv:
        run_interactive()
    else:
        all_ok = run_self_test()
        print(" Overall:", "ALL TESTS PASSED" if all_ok else "SOME TESTS FAILED")
