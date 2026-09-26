"""
test_parametrize.py - one test function, many data sets.

    pytest test_parametrize.py -v
    pytest test_parametrize.py -k csv          (only the CSV-driven cases)
"""
import csv
from pathlib import Path

import pytest

from calculator import is_valid_username

DATA_FILE = Path(__file__).parent / "data" / "calc_cases.csv"


# ---------------------------------------------------------------------------
# 1. Basic parametrize: argument names + list of tuples
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-5, 5, 0),
    (2.5, 2.5, 5),
])
def test_add(calculator, a, b, expected):
    assert calculator.calculate(a, "+", b) == expected


# ---------------------------------------------------------------------------
# 2. Readable test IDs
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("name, valid", [
    ("abcd", False),
    ("abcde", True),
    ("abcdefghijkl", True),
    ("abcdefghijklm", False),
    ("user_01", False),
], ids=["min-1", "min", "max", "max+1", "underscore"])
def test_username_boundaries(name, valid):
    assert is_valid_username(name) is valid


# ---------------------------------------------------------------------------
# 3. pytest.param: attach a marker or id to ONE data row
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("a, op, b, expected", [
    (8, "/", 2, 4),
    pytest.param(1, "/", 3, 0.333, marks=pytest.mark.xfail(reason="exact compare of 1/3"),
                 id="one-third-exact"),
    pytest.param(100, "*", 100, 10000, marks=pytest.mark.slow, id="big-multiply"),
])
def test_with_param_objects(calculator, a, op, b, expected):
    assert calculator.calculate(a, op, b) == expected


# ---------------------------------------------------------------------------
# 4. Stacked parametrize = every combination (2 x 3 = 6 tests)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("a", [10, -10])
@pytest.mark.parametrize("op", ["+", "-", "*"])
def test_combinations_do_not_crash(calculator, a, op):
    assert isinstance(calculator.calculate(a, op, 2), float)


# ---------------------------------------------------------------------------
# 5. Data-driven from a CSV file
# ---------------------------------------------------------------------------
def load_csv_cases(path):
    """Read rows into pytest.param objects, using case_id as the test id."""
    with open(path, newline="", encoding="utf-8") as f:
        return [
            pytest.param(row["a"], row["op"], row["b"], float(row["expected"]), id=row["case_id"])
            for row in csv.DictReader(f)
        ]


@pytest.mark.parametrize("a, op, b, expected", load_csv_cases(DATA_FILE))
def test_calculator_from_csv(calculator, a, op, b, expected):
    assert calculator.calculate(a, op, b) == pytest.approx(expected)
