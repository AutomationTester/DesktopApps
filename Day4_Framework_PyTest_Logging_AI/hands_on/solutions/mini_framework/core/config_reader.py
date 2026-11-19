"""Configuration-driven execution: settings for the selected environment from config/config.yaml."""
import os

import yaml

from core.paths import CONFIG_DIR


def load_raw(path=CONFIG_DIR / "config.yaml"):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_config(env=None):
    """Return the settings dict for one environment.

    Priority: explicit `env` argument > TEST_ENV environment variable > default_env in the file.
    """
    data = load_raw()
    env = env or os.environ.get("TEST_ENV") or data["default_env"]
    if env not in data["environments"]:
        raise ValueError(f"Unknown environment '{env}'. Available: {list(data['environments'])}")
    settings = dict(data["environments"][env])
    settings["env"] = env
    return settings
