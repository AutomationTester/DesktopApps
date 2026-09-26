"""
Lab 4 - STARTER - CLI-based configuration automation
====================================================
A command-line tool (argparse sub-commands) that manages environment
configs and runs config-driven checks.

  show      print the effective config for an env (secrets masked)   (DONE)
  get       read one value using a dotted key  e.g. app.launch_timeout (DONE)
  set       change one value (saved to a SANDBOX copy)               TODO
  validate  check required keys and types; exit code 1 if invalid    TODO
  run       execute checks from config/checks.yaml                   TODO

Examples:
  python lab4_config_cli.py show --env qa
  python lab4_config_cli.py get app.launch_timeout --env dev
  python lab4_config_cli.py set retries 5 --env qa
  python lab4_config_cli.py validate --env qa
  python lab4_config_cli.py run --env qa
Search for "# TODO". See hands_on/Lab_Guide.md, Lab 4.
"""

import argparse
import copy
import os
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TEMPLATE_DIR = HERE / "config"                 # read-only templates
WORK_DIR = HERE / "sandbox" / "lab4_config"    # editable copies
ENVS = ("dev", "qa")
REQUIRED = {"env": str, "app.name": str, "app.path": str, "app.launch_timeout": int,
            "report.format": str, "log_level": str, "retries": int}
ALLOWED_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}


def config_path(env):
    work = WORK_DIR / f"app_{env}.yaml"
    return work if work.exists() else TEMPLATE_DIR / f"app_{env}.yaml"


def load(env):
    with open(config_path(env), encoding="utf-8") as f:
        return yaml.safe_load(f)


def effective(env):
    """Config after environment-variable overrides + secret lookup."""
    cfg = copy.deepcopy(load(env))
    # TODO 1: if LAB_LOG_LEVEL is set, override cfg["log_level"]
    #         if LAB_RETRIES is set, override cfg["retries"] (convert to int!)
    token_var = cfg.get("secrets", {}).get("api_token_env", "LAB_API_TOKEN")
    cfg.setdefault("secrets", {})["api_token"] = os.environ.get(token_var)
    return cfg


def get_dotted(data, key):
    for part in key.split("."):
        if not isinstance(data, dict) or part not in data:
            raise KeyError(key)
        data = data[part]
    return data


def set_dotted(data, key, value):
    # TODO 2: walk/create nested dicts for all parts except the last,
    #         then assign the value.  set_dotted(cfg, "app.launch_timeout", 15)
    raise NotImplementedError("TODO 2: set_dotted")


def masked(cfg):
    out = copy.deepcopy(cfg)
    out["secrets"]["api_token"] = "****" if out["secrets"].get("api_token") else "<NOT SET>"
    return out


def cmd_show(args):
    print(f"# source: {config_path(args.env).relative_to(HERE)}")
    print(yaml.safe_dump(masked(effective(args.env)), sort_keys=False).rstrip())
    return 0


def cmd_get(args):
    try:
        print(get_dotted(effective(args.env), args.key))
        return 0
    except KeyError:
        print(f"ERROR: key '{args.key}' not found", file=sys.stderr)
        return 2


def cmd_set(args):
    # TODO 3: load(args.env), convert args.value with yaml.safe_load (so "5" -> 5),
    #         set_dotted(...), then yaml.safe_dump into WORK_DIR / f"app_{env}.yaml"
    #         (create WORK_DIR first). NEVER overwrite the template files.
    raise NotImplementedError("TODO 3: cmd_set")


def validate_config(cfg):
    errors = []
    # TODO 4: for each key/type in REQUIRED -> report missing keys and wrong types
    #         check log_level is in ALLOWED_LOG_LEVELS and retries is 0..5
    return errors


def cmd_validate(args):
    errors = validate_config(effective(args.env))
    print(f"{args.env}: {'INVALID' if errors else 'VALID'}")
    for e in errors:
        print(f"  - {e}")
    return 1 if errors else 0


def cmd_run(args):
    cfg = effective(args.env)
    with open(HERE / args.checks, encoding="utf-8") as f:
        checks = yaml.safe_load(f)["checks"]
    values = {"python": sys.executable, "env": cfg["env"], "retries": str(cfg["retries"])}
    # TODO 5: for each check:
    #   cmd = [part.format(**values) for part in check["command"]]
    #   run with subprocess.run(..., capture_output=True, text=True, timeout=...,
    #                           env={**os.environ, "TEST_ENV": cfg["env"]})
    #   PASS if returncode == check.get("expect_returncode", 0) and
    #           check.get("expect_in_stdout", "").format(**values) in stdout
    #   print PASS/FAIL per check and return 1 if any failed
    raise NotImplementedError("TODO 5: cmd_run")


def build_parser():
    parser = argparse.ArgumentParser(description="Lab 4 - configuration CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name, func, help_text):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("--env", choices=ENVS, default=os.environ.get("TEST_ENV", "dev"))
        p.set_defaults(func=func)
        return p

    add("show", cmd_show, "show effective config")
    add("get", cmd_get, "get one value").add_argument("key")
    p_set = add("set", cmd_set, "set one value")
    p_set.add_argument("key")
    p_set.add_argument("value")
    add("validate", cmd_validate, "validate config")
    add("run", cmd_run, "run config-driven checks").add_argument("--checks", default="config/checks.yaml")
    # STRETCH: add "export" (write effective config as JSON) and "reset" sub-commands
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except NotImplementedError as todo:
        print(f"Not finished yet -> {todo}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
