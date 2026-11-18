"""
05_env_configs.py
=================
Day 3 - Managing environment configs (dev / qa / prod), environment
variables and secrets.

The golden rules
----------------
1. ONE code base, MANY config files: config/dev.yaml, config/qa.yaml, config/prod.yaml
2. Choose the environment at run time: --env qa   or   TEST_ENV=qa
3. Allow individual overrides with environment variables (e.g. APP_BASE_URL)
4. SECRETS (passwords, tokens) are NEVER stored in code or in git.
   The YAML only stores the *name* of the env var that holds the secret.

Priority (highest wins):  command line  >  environment variable  >  YAML file  >  default

How to set environment variables
--------------------------------
  Linux / macOS / Git Bash :  export TEST_ENV=qa
                              export APP_DB_PASSWORD='s3cret'
  Windows PowerShell       :  $env:TEST_ENV = "qa"
                              $env:APP_DB_PASSWORD = "s3cret"
  Windows cmd.exe          :  set TEST_ENV=qa
  One-off (Linux/Git Bash) :  TEST_ENV=qa python 05_env_configs.py

Run:
  python 05_env_configs.py                 (defaults to dev)
  python 05_env_configs.py --env qa
  python 05_env_configs.py --env prod --demo-overrides
"""

import argparse
import os
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
CONFIG_DIR = HERE / "config"
VALID_ENVS = ("dev", "qa", "prod")


def load_config(env_name):
    """Load config/<env>.yaml and apply environment-variable overrides."""
    if env_name not in VALID_ENVS:
        raise ValueError(f"Unknown environment '{env_name}'. Choose from {VALID_ENVS}")
    config_file = CONFIG_DIR / f"{env_name}.yaml"
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with open(config_file, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # --- Environment variable overrides (useful in CI pipelines) ------------
    if "APP_BASE_URL" in os.environ:
        config["base_url"] = os.environ["APP_BASE_URL"]
    if "APP_LOG_LEVEL" in os.environ:
        config["log_level"] = os.environ["APP_LOG_LEVEL"]
    if "APP_RETRIES" in os.environ:
        # env vars are ALWAYS strings -> convert
        config["retries"] = int(os.environ["APP_RETRIES"])

    # --- Secrets: read from the environment, never from the file -------------
    secret_var = config["db"]["password_env_var"]
    config["db"]["password"] = os.environ.get(secret_var)   # None if not set
    return config


def mask(secret):
    """Never print secrets in logs/reports. Show only that it exists."""
    if not secret:
        return "<NOT SET>"
    return secret[0] + "*" * (len(secret) - 1)


def show(config):
    print(f"  env_name   : {config['env_name']}")
    print(f"  base_url   : {config['base_url']}")
    print(f"  db         : {config['db']['user']}@{config['db']['host']}:{config['db']['port']}/{config['db']['name']}")
    print(f"  db password: {mask(config['db']['password'])}  (from env var {config['db']['password_env_var']})")
    print(f"  log_level  : {config['log_level']}")
    print(f"  retries    : {config['retries']}")
    print(f"  read_only  : {config.get('read_only', False)}")


def main():
    parser = argparse.ArgumentParser(description="Environment-aware config loader")
    # Default comes from the TEST_ENV env var, falling back to "dev"
    parser.add_argument("--env", default=os.environ.get("TEST_ENV", "prod"), choices=VALID_ENVS)
    parser.add_argument("--demo-overrides", action="store_true",
                        help="Temporarily set some env vars inside this process to show overrides")
    args = parser.parse_args()

    print(f"=== Loading configuration for '{args.env}' ===")
    show(load_config(args.env))

    if args.demo_overrides:
        # Setting os.environ here only affects THIS python process and its
        # children - it does not change your terminal's environment.
        os.environ["APP_BASE_URL"] = "http://override.local:9000"
        os.environ["APP_RETRIES"] = "5"
        os.environ["APP_DB_PASSWORD"] = "DemoOnly123"
        print(f"\n=== Same env '{args.env}' after setting APP_BASE_URL, APP_RETRIES, APP_DB_PASSWORD ===")
        show(load_config(args.env))
        for var in ("APP_BASE_URL", "APP_RETRIES", "APP_DB_PASSWORD"):
            os.environ.pop(var, None)

    print("\nTip: keep a .env.example (names only) in git, and add real .env files to .gitignore.")


if __name__ == "__main__":
    main()
