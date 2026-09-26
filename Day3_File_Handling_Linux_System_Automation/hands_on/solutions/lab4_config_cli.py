"""
Lab 4 - SOLUTION - CLI-based configuration automation
=====================================================
A command-line tool (argparse sub-commands) that manages environment
configs and runs config-driven checks.

  show      print the effective config for an env (YAML + env var overrides, secrets masked)
  get       read one value using a dotted key         e.g.  app.launch_timeout
  set       change one value (saved to a SANDBOX copy - templates are never modified)
  validate  check required keys and types; exit code 1 if invalid
  run       execute checks from config/checks.yaml with values from the env config
  export    write the effective config as JSON (e.g. for another tool)

Examples:
  python lab4_config_cli.py show --env qa
  python lab4_config_cli.py get app.launch_timeout --env dev
  python lab4_config_cli.py set retries 5 --env qa
  python lab4_config_cli.py validate --env qa
  python lab4_config_cli.py run --env qa
  python lab4_config_cli.py export --env dev
  python lab4_config_cli.py reset
Environment variable overrides:  LAB_LOG_LEVEL, LAB_RETRIES
Secret:                          LAB_API_TOKEN (never stored in files)
"""

import argparse
import copy
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TEMPLATE_DIR = HERE / "config"                 # read-only templates (in git)
WORK_DIR = HERE / "sandbox" / "lab4_config"    # editable copies
ENVS = ("dev", "qa")
REQUIRED = {"env": str, "app.name": str, "app.path": str, "app.launch_timeout": int,
            "report.format": str, "log_level": str, "retries": int}
ALLOWED_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}


# ------------------------------------------------------------ helpers
def config_path(env):
    """Prefer the edited sandbox copy; fall back to the template."""
    work = WORK_DIR / f"app_{env}.yaml"
    return work if work.exists() else TEMPLATE_DIR / f"app_{env}.yaml"


def load(env):
    with open(config_path(env), encoding="utf-8") as f:
        return yaml.safe_load(f)


def effective(env):
    """Config after environment-variable overrides + secret lookup."""
    cfg = copy.deepcopy(load(env))
    if os.environ.get("LAB_LOG_LEVEL"):
        cfg["log_level"] = os.environ["LAB_LOG_LEVEL"]
    if os.environ.get("LAB_RETRIES"):
        cfg["retries"] = int(os.environ["LAB_RETRIES"])
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
    parts = key.split(".")
    for part in parts[:-1]:
        data = data.setdefault(part, {})
    data[parts[-1]] = value


def convert(text):
    """'5' -> 5, 'true' -> True, 'abc' -> 'abc'  (YAML rules do the work)."""
    return yaml.safe_load(text)


def masked(cfg):
    out = copy.deepcopy(cfg)
    token = out["secrets"].get("api_token")
    out["secrets"]["api_token"] = "****" if token else "<NOT SET>"
    return out


# ------------------------------------------------------------ commands
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
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    cfg = load(args.env)
    old = None
    try:
        old = get_dotted(cfg, args.key)
    except KeyError:
        pass
    set_dotted(cfg, args.key, convert(args.value))
    target = WORK_DIR / f"app_{args.env}.yaml"
    with open(target, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)
    print(f"{args.env}: {args.key}: {old!r} -> {convert(args.value)!r}  (saved to {target.relative_to(HERE)})")
    return 0


def validate_config(cfg):
    errors = []
    for key, typ in REQUIRED.items():
        try:
            value = get_dotted(cfg, key)
        except KeyError:
            errors.append(f"missing key: {key}")
            continue
        if not isinstance(value, typ) or isinstance(value, bool) and typ is int:
            errors.append(f"{key} should be {typ.__name__}, got {type(value).__name__} ({value!r})")
    if cfg.get("log_level") not in ALLOWED_LOG_LEVELS:
        errors.append(f"log_level must be one of {sorted(ALLOWED_LOG_LEVELS)}")
    if isinstance(cfg.get("retries"), int) and not 0 <= cfg["retries"] <= 5:
        errors.append("retries must be between 0 and 5")
    return errors


def cmd_validate(args):
    errors = validate_config(effective(args.env))
    if errors:
        print(f"{args.env}: INVALID")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"{args.env}: VALID")
    return 0


def cmd_run(args):
    cfg = effective(args.env)
    with open(HERE / args.checks, encoding="utf-8") as f:
        checks = yaml.safe_load(f)["checks"]
    values = {"python": sys.executable, "env": cfg["env"], "retries": str(cfg["retries"])}
    child_env = {**os.environ, "TEST_ENV": cfg["env"]}
    failed = 0
    for check in checks:
        cmd = [part.format(**values) for part in check["command"]]
        expect_rc = check.get("expect_returncode", 0)
        expect_out = check.get("expect_in_stdout", "").format(**values)
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=cfg["app"]["launch_timeout"],
                               env=child_env)
            ok = r.returncode == expect_rc and expect_out in r.stdout
            detail = f"rc={r.returncode} out={r.stdout.strip()[:40]!r}"
        except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
            ok, detail = False, type(exc).__name__
        failed += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] {check['name']:<38} {detail}")
    print(f"\n{len(checks) - failed}/{len(checks)} checks passed for env '{cfg['env']}'")
    return 1 if failed else 0


def cmd_export(args):
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    out = WORK_DIR / f"effective_{args.env}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(masked(effective(args.env)), f, indent=2)
    print(f"exported -> {out.relative_to(HERE)}")
    return 0


def cmd_reset(args):
    if WORK_DIR.exists():
        shutil.rmtree(WORK_DIR)
    print("sandbox config copies removed - templates are in effect again")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="Lab 4 - configuration CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name, func, help_text):
        p = sub.add_parser(name, help=help_text)
        if name != "reset":
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
    add("export", cmd_export, "export effective config as JSON")
    add("reset", cmd_reset, "discard edited copies")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
