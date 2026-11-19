"""Reusable helpers: read test data files. Tests never open files themselves."""
import csv
import json

import yaml

from core.paths import TEST_DATA_DIR


def _path(name):
    return TEST_DATA_DIR / name


def read_csv(name):
    """test_data/<name>.csv -> list of dicts (values are strings)."""
    with open(_path(name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_json(name):
    with open(_path(name), encoding="utf-8") as f:
        return json.load(f)


def read_yaml(name):
    with open(_path(name), encoding="utf-8") as f:
        return yaml.safe_load(f)
