"""
export_python_code.py
=====================
Build ONE complete PDF per course day containing every Python file of that day
(examples, hands-on starters and solutions) with syntax highlighting, a cover
page, a clickable table of contents and PDF bookmarks.

Output (mirrors the exports/ layout used by export_materials.py):
    exports/Day1_.../04_Python_Code.pdf
    exports/Day2_.../04_Python_Code.pdf
    ...

REQUIREMENTS
    pip install reportlab pygments

HOW TO RUN (from the repository root)
    python tools/export_python_code.py              -> all days
    python tools/export_python_code.py Day2         -> only paths containing "Day2"
    python tools/export_python_code.py --out DIR    -> write to DIR instead of exports/
"""

import sys
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    XPreformatted,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "exports"
OUTPUT_NAME = "04_Python_Code.pdf"
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".venv", "venv", "sandbox", "sandbox_repo"}

MAX_COLS = 92          # characters per code line before wrapping
TAB_SIZE = 4
CODE_FONT_SIZE = 8

# Display order and titles of the top-level sections inside a Day folder.
SECTION_TITLES = {
    "examples": "Examples",
    "hands_on/starter": "Hands-on - Starter Files",
    "hands_on/solutions": "Hands-on - Solutions",
}

TOKEN_COLORS = [
    (Token.Comment, "#6a737d"),
    (Token.Keyword, "#d73a49"),
    (Token.Name.Builtin, "#005cc5"),
    (Token.Name.Function, "#6f42c1"),
    (Token.Name.Class, "#6f42c1"),
    (Token.Name.Decorator, "#6f42c1"),
    (Token.Literal.String.Doc, "#22863a"),
    (Token.Literal.String, "#032f62"),
    (Token.Literal.Number, "#005cc5"),
    (Token.Operator.Word, "#d73a49"),
]


def register_fonts():
    """Use Consolas when available (Windows); otherwise fall back to Courier."""
    fonts = Path("C:/Windows/Fonts")
    regular, bold = fonts / "consola.ttf", fonts / "consolab.ttf"
    if regular.exists():
        pdfmetrics.registerFont(TTFont("Code", str(regular)))
        pdfmetrics.registerFont(TTFont("Code-Bold", str(bold if bold.exists() else regular)))
        return "Code", "Code-Bold"
    return "Courier", "Courier-Bold"


CODE_FONT, CODE_FONT_BOLD = register_fonts()


def token_color(ttype):
    for base, color in TOKEN_COLORS:
        if ttype in base:
            return color
    return None


def highlight(source):
    """Return the source as reportlab XML markup with wrapped, numbered lines."""
    lines = [[]]  # each line is a list of (color, text)
    for ttype, value in lex(source.expandtabs(TAB_SIZE), PythonLexer()):
        color = token_color(ttype)
        parts = value.split("\n")
        for i, part in enumerate(parts):
            if i:
                lines.append([])
            if part:
                lines[-1].append((color, part))
    if lines and not lines[-1]:
        lines.pop()  # trailing newline produces an empty last line

    width = len(str(len(lines)))
    out = []
    for number, segments in enumerate(lines, 1):
        rows, row, used = [], [], 0
        for color, text in segments:
            while text:
                room = MAX_COLS - used
                chunk, text = text[:room], text[room:]
                row.append((color, chunk))
                used += len(chunk)
                if text:
                    rows.append(row)
                    row, used = [], 0
        rows.append(row)

        for index, row in enumerate(rows):
            gutter = str(number).rjust(width) if index == 0 else " " * width
            markup = f'<font color="#9aa0a6">{gutter}</font>  '
            if index:
                markup += "    "  # indent wrapped continuation lines
            for color, text in row:
                text = escape(text)
                markup += f'<font color="{color}">{text}</font>' if color else text
            out.append(markup)
    return "\n".join(out)


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", parent=base["Title"], fontSize=28, leading=34,
                                alignment=TA_CENTER, textColor=colors.HexColor("#1f2d3d")),
        "subtitle": ParagraphStyle("subtitle", parent=base["Normal"], fontSize=14, leading=20,
                                   alignment=TA_CENTER, textColor=colors.HexColor("#555555")),
        "section": ParagraphStyle("section", parent=base["Heading1"], fontSize=20, leading=24,
                                  textColor=colors.HexColor("#0b5394"), spaceBefore=0, spaceAfter=8),
        "file": ParagraphStyle("file", parent=base["Heading2"], fontSize=12.5, leading=16,
                               textColor=colors.HexColor("#1f2d3d"), spaceBefore=10, spaceAfter=1,
                               keepWithNext=1),
        "path": ParagraphStyle("path", parent=base["Normal"], fontName=CODE_FONT, fontSize=7.5,
                               leading=10, textColor=colors.HexColor("#6a737d"), spaceAfter=4,
                               keepWithNext=1),
        "code": ParagraphStyle("code", parent=base["Code"], fontName=CODE_FONT,
                               fontSize=CODE_FONT_SIZE, leading=CODE_FONT_SIZE + 2.4,
                               backColor=colors.HexColor("#f6f8fa"), borderColor=colors.HexColor("#d0d7de"),
                               borderWidth=0.5, borderPadding=5, leftIndent=0),
        "toc_title": ParagraphStyle("toc_title", parent=base["Heading1"], fontSize=20,
                                    textColor=colors.HexColor("#0b5394")),
        "body": ParagraphStyle("body", parent=base["Normal"], fontSize=10.5, leading=15),
    }


class CodeDoc(BaseDocTemplate):
    def __init__(self, filename, day_label, **kwargs):
        super().__init__(filename, pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm,
                         topMargin=18 * mm, bottomMargin=18 * mm, title=f"{day_label} - Python Code",
                         author="Automation Training", **kwargs)
        self.day_label = day_label
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body")
        self.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=self._decorate)])
        self._anchor = 0

    def _decorate(self, canvas, doc):
        if doc.page == 1:
            return
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#6a737d"))
        canvas.drawString(self.leftMargin, A4[1] - 11 * mm, self.day_label)
        canvas.drawRightString(A4[0] - self.rightMargin, A4[1] - 11 * mm, "Python Code Reference")
        canvas.drawCentredString(A4[0] / 2, 9 * mm, f"Page {doc.page}")
        canvas.restoreState()

    def beforeDocument(self):
        self._anchor = 0

    def afterFlowable(self, flowable):
        level = getattr(flowable, "toc_level", None)
        if level is None:
            return
        text = flowable.getPlainText()
        key = f"toc-{self._anchor}"
        self._anchor += 1
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(text, key, level=level, closed=level == 0)
        self.notify("TOCEntry", (level, text, self.page, key))


def heading(text, style, level):
    para = Paragraph(escape(text), style)
    para.toc_level = level
    return para


def section_key(rel_dir):
    """Map a path relative to the day folder to (sort order, section title, sub-folder)."""
    posix = rel_dir.as_posix()
    for order, (prefix, title) in enumerate(SECTION_TITLES.items()):
        if posix == prefix or posix.startswith(prefix + "/"):
            sub = posix[len(prefix):].strip("/")
            return order, title, sub
    return len(SECTION_TITLES), "Other Files", posix if posix != "." else ""


def collect_files(day_dir):
    sections = {}
    for path in sorted(day_dir.rglob("*.py")):
        rel = path.relative_to(day_dir)
        if SKIP_DIRS & set(rel.parts):
            continue
        order, title, sub = section_key(rel.parent)
        sections.setdefault((order, title), []).append((sub, path, rel))
    return [(title, sorted(items, key=lambda i: (i[0], i[1].name)))
            for (_, title), items in sorted(sections.items())]


def pretty_day_name(day_dir):
    number, _, rest = day_dir.name.partition("_")
    return f"{number.replace('Day', 'Day ')} - {rest.replace('_', ' ')}"


def build_pdf(day_dir, out_path):
    styles = build_styles()
    sections = collect_files(day_dir)
    total_files = sum(len(items) for _, items in sections)
    total_lines = 0
    day_label = pretty_day_name(day_dir)

    story = [Spacer(1, 70 * mm),
             Paragraph(escape(day_label), styles["title"]),
             Spacer(1, 6 * mm),
             Paragraph("Complete Python Code Reference", styles["subtitle"]),
             Spacer(1, 4 * mm),
             Paragraph(f"{total_files} Python files &nbsp;|&nbsp; generated {date.today():%d %b %Y}",
                       styles["subtitle"]),
             PageBreak()]

    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("toc0", fontName="Helvetica-Bold", fontSize=11, leading=16, spaceBefore=6),
        ParagraphStyle("toc1", fontName="Helvetica", fontSize=9, leading=12.5, leftIndent=14),
    ]
    story += [Paragraph("Contents", styles["toc_title"]), toc, PageBreak()]

    for section_index, (title, items) in enumerate(sections):
        if section_index:
            story.append(PageBreak())
        story.append(heading(title, styles["section"], 0))
        for sub, path, rel in items:
            source = path.read_text(encoding="utf-8", errors="replace")
            total_lines += source.count("\n") + 1
            label = f"{sub}/{path.name}" if sub else path.name
            story.append(heading(label, styles["file"], 1))
            story.append(Paragraph(escape(rel.as_posix()), styles["path"]))
            story.append(XPreformatted(highlight(source), styles["code"]))
            story.append(Spacer(1, 6 * mm))

    doc = CodeDoc(str(out_path), day_label)
    doc.multiBuild(story)
    return total_files, total_lines


def main(argv):
    out_root = DEFAULT_OUT
    filters = []
    args = iter(argv)
    for arg in args:
        if arg == "--out":
            out_root = Path(next(args)).resolve()
        else:
            filters.append(arg)

    days = sorted(p for p in ROOT.glob("Day*") if p.is_dir()
                  and (not filters or any(f in p.name for f in filters)))
    if not days:
        print("No matching Day folders found.")
        return 1

    for day_dir in days:
        target = out_root / day_dir.name
        target.mkdir(parents=True, exist_ok=True)
        out_path = target / OUTPUT_NAME
        files, lines = build_pdf(day_dir, out_path)
        print(f"{day_dir.name}: {files} files, {lines} lines -> {out_path.relative_to(ROOT) if out_path.is_relative_to(ROOT) else out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
