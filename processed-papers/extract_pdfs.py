#!/usr/bin/env python3
"""Extract text from all PDFs in collected-papers/ into processed-papers/text/.

Uses PyMuPDF (fitz). Each PDF -> a .txt with the same base name.
Skips files already extracted unless --force is passed.
"""
import sys
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "collected-papers"
OUT = ROOT / "processed-papers" / "text"
OUT.mkdir(parents=True, exist_ok=True)

force = "--force" in sys.argv


def extract(pdf_path: Path) -> str:
    parts = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            parts.append(page.get_text("text"))
    return "\n".join(parts)


def main():
    pdfs = sorted(SRC.glob("*.pdf"))
    print(f"Found {len(pdfs)} PDFs")
    ok, skipped, failed = 0, 0, []
    for pdf in pdfs:
        out_file = OUT / (pdf.stem + ".txt")
        if out_file.exists() and not force:
            skipped += 1
            continue
        try:
            text = extract(pdf)
            out_file.write_text(text, encoding="utf-8")
            ok += 1
            print(f"[OK] {pdf.name} -> {len(text)} chars")
        except Exception as e:  # noqa: BLE001
            failed.append((pdf.name, str(e)))
            print(f"[FAIL] {pdf.name}: {e}")
    print(f"\nDone. extracted={ok} skipped={skipped} failed={len(failed)}")
    for name, err in failed:
        print(f"  FAILED: {name}: {err}")


if __name__ == "__main__":
    main()
