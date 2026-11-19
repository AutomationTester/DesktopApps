"""
Mini project settings - read the `mini_project:` block of the selected environment in
config/config.yaml, falling back to safe defaults for any key that is missing.

Why defaults? The suite keeps working even before somebody merges the config snippet,
and each environment only has to list what is DIFFERENT (configuration-driven execution).
"""
import copy

DEFAULTS = {
    "expressions_file": "expressions.csv",   # inside test_data/
    "report_prefix": "calc_report",          # Notepad report file name prefix
    "archive": {
        "pattern": "*.log",                  # which files the archiver collects
        "keep_last": 3,                      # how many archives to keep
    },
}


def _merge(defaults, overrides):
    result = copy.deepcopy(defaults)
    for key, value in (overrides or {}).items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result


def get_mini_project_settings(config):
    """`config` is the dict returned by core.config_reader.get_config() (the `config` fixture)."""
    return _merge(DEFAULTS, config.get("mini_project"))
