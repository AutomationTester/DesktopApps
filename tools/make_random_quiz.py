"""Build a random MCQ quiz PDF from the Day1..Day5 03_Quiz.md files.

Usage:
    python tools/make_random_quiz.py [--count 15] [--seed N]

Parses every question + answer-key row from each day's quiz, picks a random
sample across all days, and prints an A4 PDF (questions first, answer key
with explanations at the end) via headless Edge/Chrome -- the same approach
as tools/export_materials.py.

Output: exports/Random_Quiz_<count>_Questions.pdf (and .md alongside it)
"""

import argparse
import random
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
QUIZ_FILES = sorted(ROOT.glob("Day*/03_Quiz.md"))

ANSWER_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*\*\*([A-D])\*\*\s*\|\s*(.+?)\s*\|\s*$")
QUESTION_START = re.compile(r"^\*\*(\d+)\.(.*)$")


def parse_quiz(path: Path):
    """Return a list of dicts: {day, number, body, answer, explanation}."""
    text = path.read_text(encoding="utf-8")
    day = path.parent.name.split("_")[0]  # e.g. "Day1"

    # Split the file into the question part and the answer-key part.
    m = re.search(r"^##\s*Answer [Kk]ey.*$", text, flags=re.MULTILINE)
    q_part, a_part = text[: m.start()], text[m.start():]

    answers = {}
    for line in a_part.splitlines():
        row = ANSWER_ROW.match(line.strip())
        if row:
            answers[int(row.group(1))] = (row.group(2), row.group(3))

    questions = []
    lines = q_part.splitlines()
    current = None
    for line in lines:
        start = QUESTION_START.match(line.strip())
        if start:
            if current:
                questions.append(current)
            current = {"number": int(start.group(1)), "body": [line]}
        elif current is not None:
            if line.strip() == "---":
                questions.append(current)
                current = None
            else:
                current["body"].append(line)
    if current:
        questions.append(current)

    result = []
    for q in questions:
        num = q["number"]
        if num not in answers:
            raise SystemExit(f"{path}: no answer-key row for question {num}")
        body = "\n".join(q["body"]).strip()
        # Drop the original question number; it is renumbered in the output.
        # Form "**1.** text" -> plain text; form "**1. text...**" keeps its
        # closing ** so the leading ** is re-added.
        body = re.sub(r"^\*\*\d+\.\s*\*\*\s*", "", body)
        body = re.sub(r"^\*\*\d+\.\s*", "**", body)
        result.append({
            "day": day,
            "source": path.parent.name,
            "number": num,
            "body": body,
            "answer": answers[num][0],
            "explanation": answers[num][1],
        })
    return result


def build_markdown(sample):
    out = [
        "# Random Quiz - 15 MCQ Questions",
        "",
        "15 randomly selected multiple-choice questions. Choose **one** "
        "answer per question.",
        "Answer key with explanations on the last page.",
        "",
        "---",
        "",
    ]
    for i, q in enumerate(sample, 1):
        body = q["body"]
        if body.startswith("**"):
            body = f"**{i}. " + body[2:]
        else:
            body = f"**{i}.** {body}"
        out += [body, ""]
    out += ["---", "", "## Answer Key", "",
            "| # | Answer | Explanation |",
            "|---|--------|-------------|"]
    for i, q in enumerate(sample, 1):
        out.append(f"| {i} | **{q['answer']}** | {q['explanation']} |")
    out.append("")
    return "\n".join(out)


CSS = """
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11pt;
       color: #1a1a2e; margin: 1.4cm 1.6cm; line-height: 1.45; }
h1 { color: #16325c; border-bottom: 3px solid #2e6fdb; padding-bottom: 6px; }
h2 { color: #16325c; page-break-before: always; }
code { background: #f0f2f7; padding: 1px 4px; border-radius: 3px;
       font-family: Consolas, monospace; font-size: 10pt; }
pre { background: #f6f8fa; border: 1px solid #d8dee8; border-radius: 6px;
      padding: 8px 12px; overflow-x: auto; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%; font-size: 9.5pt; }
th, td { border: 1px solid #c6cedd; padding: 5px 8px; text-align: left;
         vertical-align: top; }
th { background: #e8eef9; }
tr:nth-child(even) td { background: #f7f9fc; }
ul { margin: 4px 0 14px 0; }
li { margin: 2px 0; }
small { color: #7a8599; }
p { page-break-inside: avoid; }
"""


def to_pdf(md_text: str, target: Path):
    html_body = MarkdownIt("commonmark", {"html": True}).enable("table").render(md_text)
    page = (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<style>{CSS}</style></head><body>{html_body}</body></html>")
    browser = next((p for p in (
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        shutil.which("msedge"), shutil.which("chrome"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ) if p and Path(p).exists()), None)
    if not browser:
        raise SystemExit("Edge or Chrome is required to print the PDF")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "quiz.html"
        src.write_text(page, encoding="utf-8")
        subprocess.run([str(browser), "--headless=new", "--disable-gpu",
                        "--no-pdf-header-footer",
                        f"--print-to-pdf={target}", src.as_uri()],
                       check=True, timeout=120)
        for _ in range(20):
            if target.exists() and target.stat().st_size:
                break
            time.sleep(0.5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=15)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()

    pool = []
    for f in QUIZ_FILES:
        pool.extend(parse_quiz(f))
    print(f"Parsed {len(pool)} questions from {len(QUIZ_FILES)} quiz files")

    rng = random.Random(args.seed)
    sample = rng.sample(pool, args.count)
    sample.sort(key=lambda q: (q["day"], q["number"]))

    md_text = build_markdown(sample)
    out_dir = ROOT / "exports"
    out_dir.mkdir(exist_ok=True)
    md_path = out_dir / f"Random_Quiz_{args.count}_Questions.md"
    pdf_path = out_dir / f"Random_Quiz_{args.count}_Questions.pdf"
    md_path.write_text(md_text, encoding="utf-8")
    to_pdf(md_text, pdf_path)
    print(f"Wrote {md_path}")
    print(f"Wrote {pdf_path}")


if __name__ == "__main__":
    main()
