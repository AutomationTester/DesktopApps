"""
validate_exports.py
===================
Check generated presentations against their own Day's 01_Presentation.md.

    Marp exports   (exports/ layout: 01_Presentation.pptx + .pdf, text in PDF)
      - PPTX slides == PDF pages
      - every word of the Markdown slides is in the PDF text (nothing lost)
      - the bottom band of every page is empty (nothing runs off the slide)
    Trainer Kit    (--kit: Cognixia template, slide images on the template)
      - PPTX slides == PDF pages
      - the bottom band of every slide image is transparent

HOW TO RUN (from the repository root)
    python tools/validate_exports.py exports
    python tools/validate_exports.py exports_TrainerKit2024 --kit
"""

import argparse
import io
import sys
import tempfile
from collections import Counter
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

sys.path.insert(0, str(Path(__file__).resolve().parent))
import slide_fit  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BAND = 28 / 720          # bottom band (fraction of slide height) that must stay empty
CORNER = 150 / 1280      # ...except the page number in the bottom-right corner


def band_is_empty(img: np.ndarray, transparent: bool) -> bool:
    h, w = img.shape[:2]
    band = img[int(h * (1 - BAND)):, : int(w * (1 - CORNER))]
    if transparent:
        return int(band[..., 3].max()) < 16
    return int(band[..., :3].min()) > 240


def check_marp(day: Path, out: Path, tmp: Path) -> list[str]:
    problems = []
    pptx, pdf = out / "01_Presentation.pptx", out / "01_Presentation.pdf"
    slides = len(Presentation(str(pptx)).slides)
    doc = pymupdf.open(pdf)
    if slides != doc.page_count:
        problems.append(f"PPTX {slides} slides vs PDF {doc.page_count} pages")
    source = (day / "01_Presentation.md").read_text(encoding="utf-8")
    expected = Counter()
    for r in slide_fit.measure(source, tmp / day.name):
        expected += slide_fit.words(r["text"])
    found = slide_fit.words(" ".join(page.get_text() for page in doc))
    missing = expected - found
    if missing:
        problems.append(f"words of {day.name}/01_Presentation.md missing from PDF: "
                        f"{dict(list(missing.items())[:15])}")
    for page in doc:
        pix = page.get_pixmap(dpi=72, annots=False)
        img = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, pix.n)
        if not band_is_empty(img, transparent=False):
            problems.append(f"page {page.number + 1}: content in the bottom band")
    return problems


def check_kit(out: Path) -> list[str]:
    problems = []
    pptx, pdf = out / "01_Presentation.pptx", out / "01_Presentation.pdf"
    prs = Presentation(str(pptx))
    pages = pymupdf.open(pdf).page_count
    if len(prs.slides) != pages:
        problems.append(f"PPTX {len(prs.slides)} slides vs PDF {pages} pages")
    for n, slide in enumerate(prs.slides, start=1):
        for shape in slide.shapes:
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE and shape.width == prs.slide_width:
                img = np.asarray(Image.open(io.BytesIO(shape.image.blob)).convert("RGBA"))
                if not band_is_empty(img, transparent=True):
                    problems.append(f"slide {n}: content in the bottom band")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path, help="export folder to check")
    ap.add_argument("--kit", action="store_true", help="Trainer Kit (Cognixia) layout")
    args = ap.parse_args()
    failed = 0
    with tempfile.TemporaryDirectory(prefix="validate_", ignore_cleanup_errors=True) as t:
        for day in sorted(ROOT.glob("Day*/01_Presentation.md")):
            day = day.parent
            out = args.folder.resolve() / day.name
            problems = check_kit(out) if args.kit else check_marp(day, out, Path(t))
            print(f"{'OK  ' if not problems else 'FAIL'} {day.name}")
            for p in problems:
                print(f"     - {p}")
            failed += bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
