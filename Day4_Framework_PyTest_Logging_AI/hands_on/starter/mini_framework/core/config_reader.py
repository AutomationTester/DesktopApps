"""Configuration-driven execution: settings for the selected environment from config/config.yaml."""
import os

import yaml

from core.paths import CONFIG_DIR


def load_raw(path=CONFIG_DIR / "config.yaml"):
    """Return the whole YAML file as a dict."""
    # TODO (Lab 1, step 3): open the file with encoding="utf-8" and return yaml.safe_load(f)
    raise NotImplementedError


def get_config(env=None):
    """Return the settings dict for one environment.

    Priority: explicit `env` argument > TEST_ENV environment variable > default_env in the file.
    """
    data = load_raw()
    # TODO (Lab 1, step 3):
    #   1. choose env: env or os.environ.get("TEST_ENV") or data["default_env"]
    #   2. if env is not in data["environments"] -> raise ValueError with the valid names
    #   3. copy the environment dict, add settings["env"] = env, return it
    raise NotImplementedError
