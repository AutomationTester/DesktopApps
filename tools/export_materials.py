"""
export_materials.py
===================
Export the course Markdown files (Day1 .. Day5) to PPTX / PDF.

    Slide decks  (front matter "marp: true")  -> .pptx + .pdf    via Marp CLI
    Documents    (handbooks, quizzes, labs)   -> .pdf (A4)       via Edge/Chrome

Slide decks are first passed through slide_fit.py: slides too tall for the
1280 x 720 canvas (Marp would clip them) get the deck's "compact" class or
are split into "(cont.)" slides, and the result is validated (nothing
overflows, no word of the source is lost) before Marp exports it.

Output goes to exports/, mirroring the Day folder structure:
    exports/Day1_.../01_Presentation.pptx
    exports/Day1_.../01_Presentation.pdf
    exports/Day1_.../02_Reading_Material.pdf
    exports/Day1_.../hands_on/Lab_Guide.pdf

REQUIREMENTS
    Node.js (Marp CLI is fetched with npx on first use)
    Microsoft Edge or Google Chrome
    pip install markdown-it-py mdit-py-plugins    (in requirements.txt)

HOW TO RUN (from the repository root)
    python tools/export_materials.py              -> export everything
    python tools/export_materials.py Day2         -> only paths containing "Day2"
    python tools/export_materials.py --out DIR    -> write to DIR instead of exports/
"""

import html
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.anchors import anchors_plugin
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

sys.path.insert(0, str(Path(__file__).resolve().parent))
import slide_fit  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "exports"
MARP = slide_fit.MARP

BROWSERS = [
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
]

CSS = """
@page { size: A4; margin: 16mm 15mm; }
body { font-family: "Segoe UI", Arial, sans-serif; font-size: 10.5pt;
       line-height: 1.45; color: #1f2328; }
h1 { font-size: 20pt; border-bottom: 2px solid #d0d7de; padding-bottom: 4px; }
h2 { font-size: 15pt; border-bottom: 1px solid #d0d7de; padding-bottom: 3px;
     margin-top: 22px; }
h3 { font-size: 12.5pt; margin-top: 18px; }
h1, h2, h3, h4 { break-after: avoid; }
code { font-family: Consolas, "Courier New", monospace; font-size: 9pt;
       background: #f3f4f6; padding: 1px 4px; border-radius: 3px; }
pre { background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 5px;
      padding: 8px 10px; white-space: pre-wrap; word-wrap: break-word;
      break-inside: avoid; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; margin: 8px 0; font-size: 9.5pt; }
th, td { border: 1px solid #d0d7de; padding: 4px 8px; vertical-align: top; }
th { background: #f3f4f6; }
tr { break-inside: avoid; }
blockquote { border-left: 4px solid #d0d7de; margin-left: 0; padding-left: 12px;
             color: #57606a; }
hr { border: none; border-top: 1px solid #d0d7de; margin: 18px 0; }
a { color: #0969da; text-decoration: none; }
img { max-width: 100%; }
"""


def find_browser() -> Path:
    for path in BROWSERS:
        if path.exists():
            return path
    for name in ("msedge", "chrome", "google-chrome", "chromium"):
        found = shutil.which(name)
        if found:
            return Path(found)
    raise SystemExit("Edge or Chrome is required to print PDFs")


def is_deck(md: Path) -> bool:
    head = md.read_text(encoding="utf-8").lstrip()[:300]
    return head.startswith("---") and "marp: true" in head


def run(cmd: list[str], env: dict | None = None) -> bool:
    result = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", env=env)
    if result.returncode != 0:
        print("    ERROR:", (result.stderr or result.stdout).strip()[-800:])
    return result.returncode == 0


# ---- slide decks -------------------------------------------------------------
def export_deck(md: Path, out_dir: Path, tmp: Path) -> list[Path]:
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if npx is None:
        raise SystemExit("npx not found - install Node.js LTS")
    # make every slide fit (Marp clips overflowing slides silently)
    work = tmp / f"fit_{md.parent.name}"
    source = md.read_text(encoding="utf-8")
    fitted = slide_fit.fit_markdown(source, work)
    for change in fitted.changes:
        print(f"      fit: {change}")
    problems = slide_fit.validate(source, fitted, work)
    if problems:
        print("    ERROR: fitted deck failed validation:", *problems, sep="\n      ")
        return []
    deck = work / md.name             # decks use no relative images/links
    deck.write_text(fitted.text, encoding="utf-8")
    made = []
    for fmt, extra in (("pptx", []), ("pdf", ["--pdf-notes", "--pdf-outlines"])):
        target = out_dir / f"{md.stem}.{fmt}"
        cmd = [npx, "--yes", *MARP, str(deck), f"--{fmt}", *extra,
               "--allow-local-files", "-o", str(target)]
        if run(cmd, env=slide_fit.marp_env()):
            made.append(target)
    return made


# ---- documents -----------------------------------------------------------------
def highlight_code(code: str, lang: str, _attrs) -> str:
    try:
        lexer = get_lexer_by_name(lang or "text")
    except ClassNotFound:
        lexer = get_lexer_by_name("text")
    return highlight(code, lexer, HtmlFormatter(nowrap=True, noclasses=True,
                                                style="default"))


def markdown_to_html(md: Path) -> str:
    parser = (MarkdownIt("commonmark", {"html": True, "highlight": highlight_code})
              .enable(["table", "strikethrough"])
              .use(anchors_plugin, min_level=1, max_level=4))  # TOC links work
    body = parser.render(md.read_text(encoding="utf-8"))
    base = md.parent.as_uri() + "/"            # relative images/links resolve
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8">'
            f'<base href="{base}"><title>{html.escape(md.stem)}</title>'
            f"<style>{CSS}</style></head><body>{body}</body></html>")


def export_document(md: Path, out_dir: Path, browser: Path, tmp: Path) -> list[Path]:
    page = tmp / f"{md.stem}.html"
    page.write_text(markdown_to_html(md), encoding="utf-8")
    target = out_dir / f"{md.stem}.pdf"
    target.unlink(missing_ok=True)
    cmd = [str(browser), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
           f"--user-data-dir={tmp / ('profile_' + md.stem)}",  # not your open browser
           f"--print-to-pdf={target}", page.as_uri()]
    run(cmd)
    # msedge.exe returns at once and prints in the background -> wait for the file
    return [target] if wait_for_file(target) else []


def wait_for_file(path: Path, timeout: float = 90) -> bool:
    """True once the file exists and its size stopped changing."""
    end, last_size = time.time() + timeout, -1
    while time.time() < end:
        if path.exists():
            size = path.stat().st_size
            if size > 0 and size == last_size:
                return True
            last_size = size
        time.sleep(0.5)
    print(f"    ERROR: {path.name} was not created within {timeout:.0f} s")
    return False


def main() -> int:
    global OUT
    filters = sys.argv[1:]
    if "--out" in filters:
        i = filters.index("--out")
        OUT = Path(filters[i + 1]).resolve()
        del filters[i:i + 2]
    files = sorted(p for p in ROOT.glob("Day*/**/*.md")
                   if not filters or any(f in str(p) for f in filters))
    if not files:
        print("No Markdown files matched.")
        return 1
    browser = find_browser()
    failures = 0
    # the browser may still hold its profile files open -> ignore cleanup errors
    with tempfile.TemporaryDirectory(prefix="export_md_",
                                     ignore_cleanup_errors=True) as tmp_name:
        tmp = Path(tmp_name)
        for md in files:
            rel = md.relative_to(ROOT)
            out_dir = OUT / rel.parent
            out_dir.mkdir(parents=True, exist_ok=True)
            deck = is_deck(md)
            print(f"{'DECK' if deck else 'DOC '}  {rel}")
            expected = 2 if deck else 1
            made = (export_deck(md, out_dir, tmp) if deck
                    else export_document(md, out_dir, browser, tmp))
            for path in made:
                print(f"      -> {path.relative_to(OUT)} ({path.stat().st_size // 1024} KB)")
            failures += expected - len(made)
    print(f"\nDone: {len(files)} Markdown files, {failures} failed exports. Output: {OUT}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
