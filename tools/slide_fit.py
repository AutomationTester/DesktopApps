"""
slide_fit.py
============
Make every Marp slide fit its 1280 x 720 canvas before exporting.

WHY
    Marp renders each "---" slide on a fixed canvas with overflow: hidden.
    A slide whose content is taller than the canvas is clipped silently -
    the bottom rows of a table, the last bullets or code lines simply vanish
    from the PPTX / PDF. Marp never splits or shrinks a slide (only code
    blocks auto-scale).

WHAT IT DOES (no Markdown content is removed or rewritten)
    1. Render the deck to HTML with Marp and measure every slide in headless
       Edge/Chrome: does the content reach into the bottom padding?
    2. Overflowing slide without a density class -> add the deck's own
       "compact" class (defined in each deck's front matter).
    3. Still overflowing -> split it into continuation slides "... (cont.)",
       between blocks, list items, table rows (header repeated) or code lines.
       Directives (_class ...) go to every part, trainer notes to the first.
    4. Repeat until every slide fits.

    validate() then checks the result: no slide overflows, and every word of
    every original slide is present in its parts.

USED BY  tools/export_materials.py, tools/build_trainer_kit.py
"""

import html
import json
import os
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from markdown_it import MarkdownIt

# --no-stdin: without it Marp waits for Markdown on stdin whenever it is not
# started from a terminal (e.g. from another script) and hangs forever.
MARP = ["@marp-team/marp-cli@4", "--no-stdin"]
BROWSERS = [
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
]
MAX_PASSES = 8
CONT = " (cont.)"
DENSER = "compact"                      # class defined in every deck's style block
DENSE_CLASSES = {"compact", "tight"}

DIRECTIVE = re.compile(
    r"^_?(theme|style|headingDivider|size|math|title|description|author|image|"
    r"keywords|url|marp|lang|paginate|header|footer|class|backgroundColor|"
    r"backgroundImage|backgroundPosition|backgroundRepeat|backgroundSize|color|"
    r"transition)\s*:")
COMMENT = re.compile(r"<!--(.*?)-->", re.S)

MEASURE_JS = r"""
<script>
window.addEventListener('load', async () => {
  await document.fonts.ready;
  const out = [];
  document.querySelectorAll('svg > foreignObject > section').forEach((s) => {
    const cs = getComputedStyle(s), r = s.getBoundingClientRect();
    const k = r.height / s.offsetHeight;                 // svg scale factor
    const limit = s.offsetHeight - parseFloat(cs.paddingBottom);
    let bottom = 0;
    for (const c of s.children) {
      if (getComputedStyle(c).position === 'absolute') continue;
      bottom = Math.max(bottom, (c.getBoundingClientRect().bottom - r.top) / k);
    }
    out.push({over: Math.round(bottom - limit), text: s.textContent});
  });
  const pre = document.createElement('pre');
  pre.id = 'slide-fit-result';
  pre.textContent = JSON.stringify(out);
  document.body.appendChild(pre);
});
</script>"""

_md = MarkdownIt("commonmark").enable("table")


# ---- deck <-> slides -------------------------------------------------------------
@dataclass
class Slide:
    text: str
    origin: int                     # 1-based slide number in the source deck
    changes: list[str] = field(default_factory=list)


def split_deck(text: str) -> tuple[str, list[Slide]]:
    """(front matter incl. its '---' fences, slides). Slides are separated by
    top-level horizontal rules, exactly as Marp does."""
    if not text.startswith("---\n"):
        raise ValueError("deck must start with a '---' front matter block")
    end = text.index("\n---\n", 4) + 5
    front, body = text[:end], text[end:]
    lines = body.split("\n")
    cuts = [t.map for t in _md.parse(body) if t.type == "hr" and t.level == 0]
    slides, start = [], 0
    for a, b in cuts:
        slides.append("\n".join(lines[start:a]))
        start = b
    slides.append("\n".join(lines[start:]))
    return front, [Slide(s.strip("\n"), n) for n, s in enumerate(slides, start=1)]


def join_deck(front: str, slides: list[Slide]) -> str:
    return front + "\n" + "\n\n---\n\n".join(s.text for s in slides) + "\n"


def comments(block: str) -> list[str]:
    return [c.strip() for c in COMMENT.findall(block)]


def is_directive(block: str) -> bool:
    found = comments(block)
    return bool(found) and all(
        all(DIRECTIVE.match(line.strip()) for line in c.splitlines() if line.strip())
        for c in found)


def notes(slide: Slide) -> str:
    """Presenter notes = non-directive HTML comments (Marp's rule)."""
    return "\n\n".join(c for c in comments(slide.text)
                       if c and not is_directive(f"<!--{c}-->"))


# ---- slide anatomy ----------------------------------------------------------------
@dataclass
class Block:
    lines: list[str]
    kind: str                         # paragraph, list, table, code, other
    head: list[str] = field(default_factory=list)   # repeated on every part
    tail: list[str] = field(default_factory=list)
    units: list[list[str]] = field(default_factory=list)  # split points between
    ordered_start: int | None = None


def parse_slide(text: str):
    """-> directives, heading line (or None), body blocks, notes blocks."""
    lines = text.split("\n")
    tokens = _md.parse(text)
    directives, heading, body, note_blocks = [], None, [], []
    for i, t in enumerate(tokens):
        if t.level != 0 or not t.map or t.nesting == -1:
            continue
        a, b = t.map
        chunk = lines[a:b]
        if t.type == "html_block" and comments(t.content):
            (directives if is_directive(t.content) else note_blocks).append(chunk)
        elif t.type == "heading_open" and heading is None and not body:
            heading = chunk[0]
        elif t.type in ("bullet_list_open", "ordered_list_open"):
            items = [x.map for x in tokens[i + 1:] if x.type == "list_item_open"
                     and x.level == 1 and x.map and a <= x.map[0] < b]
            units = [lines[x0:x1] for x0, x1 in items]
            start = int(t.attrGet("start") or 1) if t.type == "ordered_list_open" else None
            body.append(Block(chunk, "list", units=units, ordered_start=start))
        elif t.type == "table_open":
            body.append(Block(chunk, "table", head=chunk[:2], units=[[r] for r in chunk[2:]]))
        elif t.type == "fence":
            body.append(Block(chunk, "code", head=chunk[:1], tail=chunk[-1:],
                              units=[[r] for r in chunk[1:-1]]))
        else:
            body.append(Block(chunk, "paragraph" if t.type == "paragraph_open" else "other"))
    return directives, heading, body, note_blocks


def renumber(item: list[str], number: int) -> list[str]:
    first = re.sub(r"^(\s*)\d+([.)])", rf"\g<1>{number}\g<2>", item[0], count=1)
    return [first, *item[1:]]


def split_slide(slide: Slide) -> list[Slide]:
    """Split into two balanced parts. Returns [slide] if it cannot be split."""
    directives, heading, body, note_blocks = parse_slide(slide.text)
    # flatten to positions: (block index, unit index); cut "before" a position
    positions, weights = [], []
    for bi, blk in enumerate(body):
        if blk.units and len(blk.units) > 1:
            for ui, unit in enumerate(blk.units):
                positions.append((bi, ui))
                weights.append(len(unit) + (1.5 if ui == 0 else 0))
        else:
            positions.append((bi, 0))
            weights.append(len(blk.lines) + 1.5)
    if len(positions) < 2:
        return [slide]
    total = sum(weights)
    best, best_score = None, None
    for k in range(1, len(positions)):
        left = sum(weights[:k])
        bi, ui = positions[k]
        score = abs(total / 2 - left) / total
        if ui > 0:
            score += 0.12                     # prefer cuts between blocks
        prev = body[positions[k - 1][0]]
        if ui == 0 and prev.kind == "paragraph" and prev.lines[-1].rstrip().endswith(":"):
            score += 0.5                      # keep "intro:" with what it introduces
        if best_score is None or score < best_score:
            best, best_score = k, score
    cut_bi, cut_ui = positions[best]

    def part(blocks_with_units, first: bool) -> Slide:
        out = ["\n".join(d) for d in directives]
        if heading:
            out.append(heading if first else heading + CONT)
        for blk, sel in blocks_with_units:
            if sel is None:
                out.append("\n".join(blk.lines))
                continue
            units = [blk.units[i] for i in sel]
            if blk.kind == "list" and blk.ordered_start is not None and sel[0] > 0:
                units[0] = renumber(units[0], blk.ordered_start + sel[0])
            out.append("\n".join(blk.head + [l for u in units for l in u] + blk.tail))
        if first:
            out += ["\n".join(n) for n in note_blocks]
        return Slide("\n\n".join(out), slide.origin)

    left, right = [], []
    for bi, blk in enumerate(body):
        n = len(blk.units) if blk.units and len(blk.units) > 1 else 0
        if bi < cut_bi:
            left.append((blk, None))
        elif bi > cut_bi:
            right.append((blk, None))
        elif cut_ui == 0:
            right.append((blk, None))
        else:
            left.append((blk, list(range(cut_ui))))
            right.append((blk, list(range(cut_ui, n))))
    return [part(left, True), part(right, False)]


def slide_classes(slide: Slide) -> set[str]:
    m = re.search(r"<!--\s*_?class:\s*([^-\n]+?)\s*-->", slide.text)
    return set(m.group(1).split()) if m else set()


def add_class(slide: Slide, cls: str) -> Slide:
    m = re.search(r"<!--\s*(_?)class:\s*([^-\n]+?)\s*-->", slide.text)
    if m:
        new = f"<!-- {m.group(1) or '_'}class: {m.group(2)} {cls} -->"
        text = slide.text[:m.start()] + new + slide.text[m.end():]
    else:
        text = f"<!-- _class: {cls} -->\n\n" + slide.text
    return Slide(text, slide.origin)


# ---- rendering + measuring ----------------------------------------------------------
def find_browser() -> Path:
    for path in BROWSERS:
        if path.exists():
            return path
    for name in ("msedge", "chrome", "google-chrome", "chromium"):
        if shutil.which(name):
            return Path(shutil.which(name))
    raise SystemExit("Edge or Chrome is required")


def marp_env() -> dict:
    """Marp must be told where the browser is, or it can hang looking for one."""
    return dict(os.environ, CHROME_PATH=str(find_browser()))


def measure(md_text: str, work: Path) -> list[dict]:
    """Render with Marp, return [{'over': px, 'text': str}] per slide.
    over > 0 -> content reaches into the bottom padding or past the slide."""
    work.mkdir(parents=True, exist_ok=True)
    src, page = work / "measure.md", work / "measure.html"
    src.write_text(md_text, encoding="utf-8")
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if npx is None:
        raise SystemExit("npx not found - install Node.js LTS")
    r = subprocess.run([npx, "--yes", *MARP, str(src), "--template", "bare",
                        "--allow-local-files", "-o", str(page)],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=marp_env(), timeout=300)
    if r.returncode != 0:
        raise SystemExit("Marp failed: " + (r.stderr or r.stdout)[-800:])
    page.write_text(page.read_text(encoding="utf-8").replace("</body>", MEASURE_JS + "</body>"),
                    encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="slide_fit_", ignore_cleanup_errors=True) as prof:
        dom = subprocess.run([str(find_browser()), "--headless=new", "--disable-gpu",
                              f"--user-data-dir={prof}", "--virtual-time-budget=15000",
                              "--dump-dom", page.resolve().as_uri()],
                             capture_output=True, text=True, encoding="utf-8",
                             errors="replace", timeout=300).stdout
    m = re.search(r'<pre id="slide-fit-result">(.*?)</pre>', dom, re.S)
    if not m:
        raise SystemExit("slide measurement failed (no result from the browser)")
    return json.loads(html.unescape(m.group(1)))


# ---- fit + validate --------------------------------------------------------------------
@dataclass
class FitResult:
    text: str                       # fitted Markdown
    slides: list[Slide]
    changes: list[str]              # human-readable log
    notes: list[str]                # presenter notes per fitted slide


def fit_markdown(text: str, work: Path) -> FitResult:
    front, slides = split_deck(text)
    changes = []
    for _ in range(MAX_PASSES):
        result = measure(join_deck(front, slides), work)
        if len(result) != len(slides):
            raise SystemExit(f"slide count mismatch: Marp {len(result)} vs parser {len(slides)}")
        bad = {i for i, r in enumerate(result) if r["over"] > 0}
        if not bad:
            break
        new = []
        for i, s in enumerate(slides):
            if i not in bad:
                new.append(s)
            elif not slide_classes(s) & DENSE_CLASSES:
                new.append(add_class(s, DENSER))
                changes.append(f"slide {s.origin}: +{result[i]['over']}px -> class '{DENSER}'")
            else:
                parts = split_slide(s)
                if len(parts) == 1:
                    raise SystemExit(f"slide {s.origin} overflows by {result[i]['over']}px "
                                     "and has nothing that can be split")
                new.extend(parts)
                changes.append(f"slide {s.origin}: +{result[i]['over']}px -> split in two")
        slides = new
    else:
        raise SystemExit(f"slides still overflow after {MAX_PASSES} passes")
    return FitResult(join_deck(front, slides), slides, changes, [notes(s) for s in slides])


def words(text: str) -> Counter:
    return Counter(re.findall(r"[A-Za-z0-9]+", text.lower()))


def validate(original: str, fitted: FitResult, work: Path) -> list[str]:
    """Problems found (empty list = OK): any overflowing slide, or any word of
    an original slide missing from the slides generated from it."""
    problems = []
    before = measure(original, work / "orig")
    after = measure(fitted.text, work / "fitted")
    for i, r in enumerate(after):
        if r["over"] > 0:
            problems.append(f"fitted slide {i + 1} still overflows by {r['over']}px")
    parts: dict[int, Counter] = {}
    for s, r in zip(fitted.slides, after):
        parts[s.origin] = parts.get(s.origin, Counter()) + words(r["text"])
    for n, r in enumerate(before, start=1):
        missing = words(r["text"]) - parts.get(n, Counter())
        if missing:
            problems.append(f"slide {n}: words missing {dict(missing)}")
    return problems
