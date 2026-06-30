"""Update processed-papers/INDEX.md: append rows for the new gap notes (147-193)
and refresh the total count. Reads each note's H1 title and TL;DR.
"""
import os
import re
import glob
import urllib.parse

PROC = "/Users/sihonghe/Desktop/papers/review-rmarl/processed-papers"
INDEX = os.path.join(PROC, "INDEX.md")
NOTES = os.path.join(PROC, "notes")


def note_info(path):
    txt = open(path, encoding="utf-8").read()
    h1 = re.search(r"^#\s*(\d+)\.\s*(.+)", txt, re.M)
    no = int(h1.group(1)); title = h1.group(2).strip()
    m = re.search(r"##\s*TL;DR[^\n]*\n+([^\n]+)", txt)
    tldr = m.group(1).strip() if m else ""
    return no, title, tldr


def main():
    # gather new notes (No >= 147)
    rows = {}
    for p in glob.glob(os.path.join(NOTES, "*.md")):
        base = os.path.basename(p)
        m = re.match(r"(\d+)_", base)
        if not m or int(m.group(1)) < 147:
            continue
        no, title, tldr = note_info(p)
        href = "notes/" + urllib.parse.quote(base)
        rows[no] = f"| {no} | [{no}. {title}]({href}) | {tldr} |"

    idx = open(INDEX, encoding="utf-8").read()
    # update count = existing distinct row numbers + new
    existing = set(int(n) for n in re.findall(r"(?m)^\|\s*(\d+)\s*\|", idx))
    total = len(existing | set(rows))
    idx = re.sub(r"共 \*\*\d+\*\* 篇", f"共 **{total}** 篇", idx, count=1)

    # append new rows after the last table row
    new_block = "\n".join(rows[n] for n in sorted(rows))
    lines = idx.rstrip().splitlines()
    last_tbl = max(i for i, l in enumerate(lines) if re.match(r"^\|\s*\d+\s*\|", l))
    lines = lines[:last_tbl + 1] + [new_block] + lines[last_tbl + 1:]
    open(INDEX, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"INDEX updated: total {total}; appended {len(rows)} rows "
          f"({min(rows)}-{max(rows)})")
    missing_tldr = [n for n in rows if "| " + str(n) + " |" in "" ]
    blanks = [n for n in sorted(rows) if rows[n].endswith("|  |")]
    if blanks:
        print("  WARNING rows with empty TL;DR:", blanks)


if __name__ == "__main__":
    main()
