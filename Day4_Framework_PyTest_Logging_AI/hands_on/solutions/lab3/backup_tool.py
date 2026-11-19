"""
Lab 3 - the APPLICATION UNDER TEST (do not change this file).

A small command-line backup tool:
    python backup_tool.py <source_folder> <backup_folder>

Behaviour (like many real tools, it is slow and not atomic):
  1. waits 0.3 - 1.5 s before starting (random)
  2. writes status.json  {"status": "running", "files": 0}
  3. copies each file with a small delay
  4. writes status.json  {"status": "done", "files": <count>}   (files is an INTEGER)
Exit code 0 on success, 2 if the source folder does not exist.
"""
import json
import random
import shutil
import sys
import time
from pathlib import Path


def write_status(dst: Path, status: str, files: int):
    (dst / "status.json").write_text(json.dumps({"status": status, "files": files}),
                                     encoding="utf-8")


def main(argv):
    if len(argv) != 3:
        print("usage: backup_tool.py <source_folder> <backup_folder>", file=sys.stderr)
        return 2
    src, dst = Path(argv[1]), Path(argv[2])
    if not src.is_dir():
        print(f"ERROR: source folder not found: {src}", file=sys.stderr)
        return 2
    time.sleep(random.uniform(0.3, 1.5))
    dst.mkdir(parents=True, exist_ok=True)
    write_status(dst, "running", 0)
    files = sorted(p for p in src.iterdir() if p.is_file())
    for f in files:
        time.sleep(0.2)
        shutil.copy2(f, dst / f.name)
    write_status(dst, "done", len(files))
    print(f"Backup complete: {len(files)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
