#!/usr/bin/env python3
"""Merge a PO PDF + PI PDF into one renamed PDF (PO first, then PI). In-brain replacement
for the PPO Validator web app's merge step — uses PyMuPDF (fitz), which is already installed.

    py -3 _merge.py "<PO.pdf>" "<PI.pdf>" "<output.pdf>"
"""
import sys
import fitz  # PyMuPDF

def main():
    if len(sys.argv) < 4:
        print("usage: _merge.py <PO.pdf> <PI.pdf> <output.pdf>"); return 2
    po, pi, out = sys.argv[1], sys.argv[2], sys.argv[3]
    doc = fitz.open()
    for f in (po, pi):                      # PO first, then PI
        with fitz.open(f) as src:
            doc.insert_pdf(src)
    doc.save(out, garbage=4, deflate=True)  # compact
    n = doc.page_count
    doc.close()
    print(f"merged {n} pages -> {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
