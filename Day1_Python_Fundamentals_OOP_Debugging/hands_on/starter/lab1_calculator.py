"""
Lab 1 - Calculator using Functions (STARTER)
=============================================
How to run:
    python lab1_calculator.py

Right now most tests FAIL. Complete every "# TODO" until the self-test
prints "ALL TESTS PASSED". Read hands_on/Lab_Guide.md for full steps.
"""
import sys


# ------------------------------------------------------------------
# Task 1: basic operations
# ------------------------------------------------------------------
def add(a, b):
    """Return a + b."""
    return a + b          # done for you as an example


def subtract(a, b):
    """Return a - b."""
    # TODO: return the difference
    pass


def multiply(a, b):
    """Return a * b."""
    # TODO: return the product
    pass


def divide(a, b):
    """Return a / b. Raise ZeroDivisionError with a clear message if b is 0."""
    # TODO: if b is 0 -> raise ZeroDivisionError("Cannot divide by zero")
    # TODO: otherwise return a / b
    pass


# ------------------------------------------------------------------
# Task 2: extra operations
# ------------------------------------------------------------------
def power(a, b):
    """Return a raised to the power b."""
    # TODO: use the ** operator
    pass


def modulus(a, b):
    """Return the remainder of a / b."""
    # TODO: raise ZeroDivisionError if b is 0, else return a % b
    pass


def percentage(part, total):
    """Return what percent 'part' is of 'total' (e.g. pass percentage)."""
    # TODO: raise ZeroDivisionError if total is 0, else return part / total * 100
    return 0.0


# ------------------------------------------------------------------
# Task 3: one function that picks the right operation
# ------------------------------------------------------------------
OPERATIONS = {
    "+": add,
    # TODO: add "-", "*", "/", "**", "%" mapped to the matching functions
}


def calculate(a, operator, b):
    """Apply 'operator' to a and b. Raise ValueError for an unknown operator."""
    # TODO: if operator is not a key in OPERATIONS -> raise ValueError(f"Unsupported operator: {operator!r}")
    # TODO: look up the function in OPERATIONS and return function(a, b)
    return None


# ------------------------------------------------------------------
# Task 4: self-test (already written - read it and understand it)
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
        ("CALC_07", 0.1, "+", 0.2, 0.3),
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
            actual = type(error).__name__

        # TODO (Task 5): CALC_07 fails because 0.1 + 0.2 = 0.30000000000000004
        #   When both expected and actual are floats, compare with a tolerance:
        #   ok = abs(expected - actual) < 1e-9
        ok = expected == actual

        status = "PASS" if ok else "FAIL"
        passed += ok
        expression = f"{a} {op} {b}"
        print(f" {test_id}  {expression:<10} expected={expected!s:<18} actual={actual!s:<20} {status}")

    total = len(test_data)
    print("-" * 60)
    print(f" Passed {passed}/{total}  ({percentage(passed, total):.1f}%)")
    return passed == total


if __name__ == "__main__":
    # Stretch goal: if "--interactive" in sys.argv, ask the user for numbers
    # with input() in a while loop (see Lab_Guide.md)
    all_ok = run_self_test()
    print(" Overall:", "ALL TESTS PASSED" if all_ok else "SOME TESTS FAILED")
