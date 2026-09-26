"""
03_json_read_write.py
=====================
Day 3 - Reading and writing JSON files with the ``json`` module.

The 4 functions to remember
---------------------------
    json.dump(obj, file)     Python -> JSON file
    json.load(file)          JSON file -> Python
    json.dumps(obj)          Python -> JSON string
    json.loads(text)         JSON string -> Python
("s" = string)

What this example shows
-----------------------
1. Writing nested test data (dict/list) to JSON with indent for readability
2. Reading it back and navigating nested structures
3. Type mapping (JSON true/null -> Python True/None)
4. Updating a JSON file (read -> modify -> write)
5. Handling a broken JSON file (json.JSONDecodeError)

Run:  python 03_json_read_write.py
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox"
SANDBOX.mkdir(exist_ok=True)

JSON_FILE = SANDBOX / "test_suite.json"


def write_json():
    suite = {
        "suite_name": "Notepad Smoke Tests",
        "app_path": "notepad.exe",
        "retry_on_failure": True,
        "max_retries": 2,
        "owner": None,
        "tests": [
            {"id": "NP-01", "action": "type_text", "data": "Hello", "enabled": True},
            {"id": "NP-02", "action": "save_as", "data": "out.txt", "enabled": True},
            {"id": "NP-03", "action": "close", "data": None, "enabled": False},
        ],
    }
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        # indent=2 makes the file human-readable (and git-diff friendly)
        json.dump(suite, f, indent=2)
    print(f"[WRITE] {JSON_FILE.name} written")
    print(JSON_FILE.read_text(encoding="utf-8"))


def read_json():
    with open(JSON_FILE, encoding="utf-8") as f:
        suite = json.load(f)
    print("[READ] Navigating the structure:")
    print(f"  suite_name        : {suite['suite_name']}")
    print(f"  retry_on_failure  : {suite['retry_on_failure']!r}  (JSON true  -> {type(suite['retry_on_failure']).__name__})")
    print(f"  owner             : {suite['owner']!r}  (JSON null  -> None)")
    print(f"  max_retries type  : {type(suite['max_retries']).__name__}  (numbers keep their type, unlike CSV)")
    enabled = [t["id"] for t in suite["tests"] if t["enabled"]]
    print(f"  enabled tests     : {enabled}")
    # .get() with default avoids KeyError for optional keys
    print(f"  timeout (optional): {suite.get('timeout', 30)}")
    return suite


def update_json():
    """Read -> modify -> write back. JSON files are rewritten as a whole."""
    with open(JSON_FILE, encoding="utf-8") as f:
        suite = json.load(f)
    suite["tests"].append({"id": "NP-04", "action": "verify_title", "data": "Untitled", "enabled": True})
    suite["max_retries"] = 3
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(suite, f, indent=2)
    print(f"\n[UPDATE] Now {len(suite['tests'])} tests, max_retries={suite['max_retries']}")


def string_round_trip():
    # Useful when a CLI tool prints JSON to stdout (very common!)
    cli_output = '{"status": "ok", "version": "2.4.1", "errors": []}'
    data = json.loads(cli_output)
    print(f"\n[LOADS] Parsed CLI output -> status={data['status']}, errors={data['errors']}")
    print(f"[DUMPS] Back to string   -> {json.dumps(data, sort_keys=True)}")


def broken_json_demo():
    bad_file = SANDBOX / "broken.json"
    # Trailing comma + single quotes are NOT valid JSON (a very common mistake)
    bad_file.write_text("{'name': 'demo', 'tests': [1, 2, 3,],}", encoding="utf-8")
    try:
        with open(bad_file, encoding="utf-8") as f:
            json.load(f)
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] broken.json is invalid: {e.msg} (line {e.lineno}, col {e.colno})")
        print("        Tip: JSON needs double quotes and no trailing commas.")


if __name__ == "__main__":
    write_json()
    read_json()
    update_json()
    string_round_trip()
    broken_json_demo()
