"""
build_trainer_kit.py
====================
Re-brand the course exports with the client's Trainer Kit 2024 (Cognixia).

    Slide decks  -> built on "Cognixia - PPT Template.pptx":
                    native title slide, Marp content slides on the branded
                    content layout, template "Thank You" slide, trainer notes.
                    The matching PDF is saved by PowerPoint.
                    Slides are fitted first by slide_fit.py (no clipped content).
    PDF documents (reading material, quizzes, labs, solutions)
                 -> copied with the Cognixia watermark (page centre, behind
                    the text) and the colour logo in the top-right margin.

The original exports/ folder is only read, never changed. Output goes to
exports_TrainerKit2024/, mirroring the Day folder structure.

REQUIREMENTS
    Node.js (Marp CLI via npx), Microsoft Edge or Chrome
    Microsoft PowerPoint (deck -> PDF)
    pip install python-pptx pymupdf pillow numpy pywin32

HOW TO RUN (from the repository root)
    python tools/build_trainer_kit.py                        -> everything
    python tools/build_trainer_kit.py Day2                   -> only paths containing "Day2"
    python tools/build_trainer_kit.py --trainer "Jane Doe"   -> name on the title slide
    python tools/build_trainer_kit.py --out DIR              -> write to DIR
"""

import argparse
import copy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image
from pptx import Presentation
from pptx.opc.packuri import PackURI
from pptx.util import Pt

sys.path.insert(0, str(Path(__file__).resolve().parent))
import slide_fit  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "exports"
OUT = ROOT / "exports_TrainerKit2024"
KIT = ROOT / "Trainer Kit 2024"
TEMPLATE = KIT / "Cognixia - PPT Template.pptx"
WATERMARK = KIT / "Cognixia Watermark.png"
LOGO = KIT / "Logo_Color.png"

COURSE = "Python Desktop Application Automation Testing"
MARP = slide_fit.MARP

# Template slide indexes (0-based) and the branded content layout
TPL_TITLE, TPL_THANK_YOU = 0, 7
CONTENT_LAYOUT = "Slide 1 master"

# Cognixia look for the Marp-rendered content (brand blue #3A7AFB, Poppins)
BRAND_CSS = """  /* Cognixia brand (added by build_trainer_kit.py) */
  section { background: #ffffff; color: #1f2937; }
  section h1 { color: #3A7AFB; font-family: Poppins, "Segoe UI Semibold", "Segoe UI", sans-serif; font-weight: 700; }
  section h2, section h3 { color: #1E3A8A; }
  section table th { background: #3A7AFB; color: #ffffff; }
  section::after { color: #3A7AFB; }
"""


# ---- slide decks -------------------------------------------------------------
def render_slides(md: Path, tmp: Path) -> tuple[list[Path], list[str]]:
    """Marp -> one PNG per slide, rendered with the brand CSS, after
    slide_fit made every slide fit. Returns (images, notes per slide)."""
    text = md.read_text(encoding="utf-8")
    if "style: |\n" not in text:
        raise SystemExit(f"{md}: expected a 'style: |' block in the front matter")
    branded_text = text.replace("style: |\n", "style: |\n" + BRAND_CSS, 1)
    fitted = slide_fit.fit_markdown(branded_text, tmp / "fit")
    for change in fitted.changes:
        print(f"      fit: {change}")
    problems = slide_fit.validate(branded_text, fitted, tmp / "fit")
    if problems:
        raise SystemExit("fitted deck failed validation:\n  " + "\n  ".join(problems))
    branded = tmp / md.name
    branded.write_text(fitted.text, encoding="utf-8")
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if npx is None:
        raise SystemExit("npx not found - install Node.js LTS")
    img_dir = tmp / "img"
    cmd = [npx, "--yes", *MARP, str(branded), "--images", "png", "--image-scale", "1.5",
           "--allow-local-files", "-o", str(img_dir / "s.png")]
    result = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", env=slide_fit.marp_env(),
                            timeout=600)
    if result.returncode != 0:
        raise SystemExit("Marp failed: " + (result.stderr or result.stdout)[-800:])
    images = sorted(img_dir.glob("s.*.png"))
    if len(images) != len(fitted.slides):
        raise SystemExit(f"{len(images)} images for {len(fitted.slides)} fitted slides")
    return images, fitted.notes


def white_to_alpha(src: Path, dst: Path) -> None:
    """Turn the white slide background transparent (GIMP 'colour to alpha'),
    so the template's logo and corner graphics show through."""
    rgb = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    alpha = (255.0 - rgb).max(axis=2) / 255.0
    safe = np.where(alpha > 0, alpha, 1.0)[..., None]
    colour = 255.0 - (255.0 - rgb) / safe
    rgba = np.dstack([np.clip(colour, 0, 255), alpha * 255.0]).round().astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(dst, optimize=True)


def deck_titles(md: Path) -> tuple[str, str]:
    """(course title, "Day N: topic") from the deck's first '# ' and '## '.
    Day 1 opens with the course name; Days 2-5 open with '# Day N'."""
    title = subtitle = ""
    for line in md.read_text(encoding="utf-8").splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        elif line.startswith("## ") and title:
            subtitle = line[3:].strip()
            break
    if title.lower().startswith("day "):
        return COURSE, f"{title}: {subtitle}"
    return title, subtitle


def set_runs(shape, lines: list[tuple[str, int]]) -> None:
    """Replace the text of a template text box, keeping its first run's style."""
    tf = shape.text_frame
    first = tf.paragraphs[0]
    for extra in tf.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    for run in first.runs[1:]:
        run._r.getparent().remove(run._r)
    model = copy.deepcopy(first._p)
    for i, (text, size) in enumerate(lines):
        if i:
            tf._txBody.append(copy.deepcopy(model))
        run = tf.paragraphs[i].runs[0]
        run.text = text
        run.font.size = Pt(size)


def build_deck(md: Path, out_dir: Path, trainer: str, tmp: Path) -> list[Path]:
    images, notes = render_slides(md, tmp)

    prs = Presentation(str(TEMPLATE))
    sld_ids = prs.slides._sldIdLst
    keep = {TPL_TITLE, TPL_THANK_YOU}
    for i, sld_id in reversed(list(enumerate(sld_ids))):
        if i not in keep:
            prs.part.drop_rel(sld_id.rId)
            sld_ids.remove(sld_id)
    title_slide, thank_you = prs.slides[0], prs.slides[1]

    # 1) title slide: course + day title, trainer name
    title, subtitle = deck_titles(md)
    for shape in title_slide.shapes:
        if shape.has_text_frame and shape.text_frame.text == "Training Name":
            set_runs(shape, [(title, 32), (subtitle, 20)])
        elif shape.has_text_frame and shape.text_frame.text.startswith("By:"):
            set_runs(shape, [(f"By: {trainer}", 20)])
    if notes[0]:
        title_slide.notes_slide.notes_text_frame.text = notes[0]

    # 2) content slides (Marp slide 1 is the title -> replaced by the template)
    layout = next(l for l in prs.slide_layouts if l.name == CONTENT_LAYOUT)
    for n, img in enumerate(images[1:], start=1):
        clear = tmp / f"clear_{img.name}"
        white_to_alpha(img, clear)
        slide = prs.slides.add_slide(layout)
        for ph in list(slide.placeholders):          # date/footer/number boxes
            ph._element.getparent().remove(ph._element)
        slide.shapes.add_picture(str(clear), 0, 0, prs.slide_width, prs.slide_height)
        if notes[n]:
            slide.notes_slide.notes_text_frame.text = notes[n]

    # 3) "Thank You" last
    thank_you_id = next(s for s in sld_ids if prs.part.related_part(s.rId) is thank_you.part)
    sld_ids.remove(thank_you_id)
    sld_ids.append(thank_you_id)

    # python-pptx names new slides "slideN" by count -> clashes with the kept
    # template slides; renumber every slide (and its notes) uniquely.
    for n, slide in enumerate(prs.slides, start=1):
        slide.part.partname = PackURI(f"/ppt/slides/slide{n}.xml")
        if slide.has_notes_slide:
            slide.notes_slide.part.partname = PackURI(f"/ppt/notesSlides/notesSlide{n}.xml")

    pptx = out_dir / f"{md.stem}.pptx"
    prs.save(str(pptx))
    pdf = out_dir / f"{md.stem}.pdf"
    pptx_to_pdf(pptx, pdf)
    return [pptx, pdf]


def pptx_to_pdf(pptx: Path, pdf: Path) -> None:
    import win32com.client
    app = win32com.client.Dispatch("PowerPoint.Application")
    pres = app.Presentations.Open(str(pptx), ReadOnly=True, Untitled=False, WithWindow=False)
    try:
        pres.SaveAs(str(pdf), 32)  # ppSaveAsPDF
    finally:
        pres.Close()


# ---- PDF documents ------------------------------------------------------------
def logo_png(tmp: Path) -> Path:
    """Colour logo cropped to its visible area (the PNG has wide padding)."""
    im = Image.open(LOGO)
    cropped = tmp / "logo_cropped.png"
    im.crop(im.getbbox()).save(cropped)
    return cropped


def brand_pdf(src: Path, dst: Path, logo: Path) -> None:
    doc = pymupdf.open(src)
    wm_w, wm_h = Image.open(WATERMARK).size
    lg_w, lg_h = Image.open(logo).size
    wm_xref = lg_xref = 0
    for page in doc:
        r = page.rect
        # watermark: 60 % of the page width, centred, behind the text
        w = r.width * 0.6
        h = w * wm_h / wm_w
        box = pymupdf.Rect((r.width - w) / 2, (r.height - h) / 2,
                           (r.width + w) / 2, (r.height + h) / 2)
        wm_xref = page.insert_image(box, filename=str(WATERMARK) if not wm_xref else None,
                                    xref=wm_xref, overlay=False)
        # logo: top-right page margin
        lw = 78
        lh = lw * lg_h / lg_w
        box = pymupdf.Rect(r.width - 48 - lw, 16, r.width - 48, 16 + lh)
        lg_xref = page.insert_image(box, filename=str(logo) if not lg_xref else None,
                                    xref=lg_xref)
    doc.save(dst, garbage=3, deflate=True)
    doc.close()


# ---- main ---------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("filters", nargs="*", help="only paths containing one of these")
    ap.add_argument("--trainer", default="Trainer", help='name shown as "By: ..."')
    ap.add_argument("--out", type=Path, default=OUT, help="output folder")
    args = ap.parse_args()
    out = args.out.resolve()

    def wanted(p: Path) -> bool:
        return not args.filters or any(f in str(p) for f in args.filters)

    decks = sorted(p for p in ROOT.glob("Day*/01_Presentation.md") if wanted(p))
    pdfs = sorted(p for p in SRC.rglob("*.pdf")
                  if wanted(p) and p.name != "01_Presentation.pdf")
    if not decks and not pdfs:
        print("Nothing matched.")
        return 1

    with tempfile.TemporaryDirectory(prefix="trainer_kit_",
                                     ignore_cleanup_errors=True) as tmp_name:
        tmp = Path(tmp_name)
        for md in decks:
            rel = md.relative_to(ROOT)
            out_dir = out / rel.parent
            out_dir.mkdir(parents=True, exist_ok=True)
            print(f"DECK  {rel}")
            work = tmp / rel.parent.name
            work.mkdir()
            for path in build_deck(md, out_dir, args.trainer, work):
                print(f"      -> {path.relative_to(out)} ({path.stat().st_size // 1024} KB)")

        logo = logo_png(tmp)
        for src in pdfs:
            dst = out / src.relative_to(SRC)
            dst.parent.mkdir(parents=True, exist_ok=True)
            brand_pdf(src, dst, logo)
            print(f"DOC   {dst.relative_to(out)}")

    print(f"\nDone: {len(decks)} decks, {len(pdfs)} documents. Output: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
