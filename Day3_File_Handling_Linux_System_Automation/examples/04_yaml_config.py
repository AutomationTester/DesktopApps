"""
04_yaml_config.py
=================
Day 3 - Introduction to YAML for configuration (PyYAML).

YAML = "YAML Ain't Markup Language". It is a superset of JSON designed for
humans: no braces, no quotes needed, comments allowed. It is the de-facto
format for config files (GitHub Actions, Docker Compose, Kubernetes, Ansible).

Install once:  pip install pyyaml      (import name is  yaml)

What this example shows
-----------------------
1. Loading YAML text with yaml.safe_load   (NEVER plain yaml.load on untrusted files)
2. Scalars, lists, nested maps, comments, multi-line strings
3. Type gotchas (yes/no -> bool, 010 -> int, version 1.10 -> float 1.1)
4. Writing Python data to YAML with yaml.safe_dump
5. Handling a YAML syntax error (yaml.YAMLError)

Run:  python 04_yaml_config.py
"""

from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox"
SANDBOX.mkdir(exist_ok=True)

SAMPLE_YAML = """\
# Test run configuration  (comments are allowed in YAML, not in JSON!)
project: Calculator Automation
version: "1.10"          # quoted -> stays a string. Unquoted 1.10 becomes float 1.1
app:
  path: calc.exe
  window_title: Calculator
  launch_timeout: 10     # int
backend: uia
headless: false          # bool
browsers: [chrome, edge] # inline (flow) list - JSON style also works
test_groups:             # block list
  - smoke
  - regression
report:
  format: csv
  output_dir: reports/
description: |
  Multi-line text keeps
  its line breaks with the pipe symbol.
"""


def load_yaml_text():
    config = yaml.safe_load(SAMPLE_YAML)     # returns normal dict/list/str/int/bool
    print("[LOAD] Parsed YAML into a Python", type(config).__name__)
    for key, value in config.items():
        print(f"  {key:<14} = {value!r}  ({type(value).__name__})")
    print(f"\n  Nested access: config['app']['launch_timeout'] = {config['app']['launch_timeout']}")
    return config


def type_gotchas():
    tricky = yaml.safe_load("""
    answer: yes        # YAML 1.1 treats yes/no/on/off as booleans!
    country: NO        # Norway?  -> False
    zip_code: 01234    # leading zero -> may be parsed as octal int, NOT the string you wanted
    safe_zip: "01234"  # quote it to be safe
    version: 1.10      # float 1.1
    empty:             # nothing -> None
    """)
    print("\n[GOTCHAS] Surprising YAML types (quote values when in doubt):")
    for k, v in tricky.items():
        print(f"  {k:<9} -> {v!r} ({type(v).__name__})")


def write_yaml(config):
    out_file = SANDBOX / "generated_config.yaml"
    config["report"]["format"] = "json"
    with open(out_file, "w", encoding="utf-8") as f:
        # sort_keys=False keeps the original order; default_flow_style=False = block style
        yaml.safe_dump(config, f, sort_keys=False, default_flow_style=False)
    print(f"\n[DUMP] Wrote {out_file.name}:")
    print(out_file.read_text(encoding="utf-8"))

    # Read it back from the file - the normal way you will use YAML
    with open(out_file, encoding="utf-8") as f:
        again = yaml.safe_load(f)
    print(f"[RELOAD] report.format is now '{again['report']['format']}'")


def bad_yaml_demo():
    bad = "app:\n  path: calc.exe\n   timeout: 10\n"   # inconsistent indentation
    try:
        yaml.safe_load(bad)
    except yaml.YAMLError as e:
        first_line = str(e).splitlines()[0]
        print(f"\n[ERROR] Invalid YAML -> {first_line}")
        print("        Tip: YAML uses SPACES for indentation (never tabs), be consistent.")


if __name__ == "__main__":
    cfg = load_yaml_text()
    type_gotchas()
    write_yaml(cfg)
    bad_yaml_demo()
