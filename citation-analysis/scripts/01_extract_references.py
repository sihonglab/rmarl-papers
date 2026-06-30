"""Step 1: extract reference sections and individual reference entries
from each of the 133 processed paper texts.

Outputs:
  data/papers.json      - id -> {file, short_title, canonical_title}
  data/references.json  - id -> [ {raw, title_guess, year, arxiv, author} ... ]
  data/extract_stats.json
"""
import os
import re
import glob
import common as C

SENT = "\x00"  # split sentinel
REF_HEADER = re.compile(r"^\s*(references|bibliography|references and notes)\s*$", re.I)
BRACKET = re.compile(r"\[(\d{1,3})\]")
ALPHA_BRACKET = re.compile(r"\[[A-Za-z][^\]]*?(?:19|20)\d{2}[a-z]?\]")


def paper_id_from_name(fname):
    m = re.match(r"(\d+)_", os.path.basename(fname))
    return int(m.group(1)) if m else None


def load_canonical_titles():
    """Map paper id -> full canonical title taken from the note files."""
    titles = {}
    for note in glob.glob(os.path.join(C.NOTES_DIR, "*.md")):
        pid = paper_id_from_name(note)
        if pid is None:
            continue
        with open(note, encoding="utf-8") as f:
            txt = f.read()
        m = re.search(r"\*\*标题\*\*\s*[:：]\s*(.+)", txt)
        title = m.group(1).strip() if m else None
        if not title:  # fall back to first H1
            m = re.search(r"^#\s*\d+\.\s*(.+)", txt, re.M)
            title = m.group(1).strip() if m else None
        titles[pid] = C.fix_ligatures(title) if title else None
    return titles


YEARTOK = re.compile(r"\b(?:19[7-9]\d|20[0-4]\d)\b")


def _ref_density(block):
    """Heuristic count of reference 'units' in a candidate block."""
    return max(len(BRACKET.findall(block)), len(YEARTOK.findall(block)))


def find_ref_section(text):
    """Return the references-section substring, or '' if not located.

    When several 'References' headers exist (e.g. a stray one in the appendix),
    pick the header whose following block looks most like a real bibliography.
    """
    lines = text.splitlines()
    headers = [i for i, ln in enumerate(lines) if REF_HEADER.match(ln)]
    if headers:
        best, best_score = None, -1
        for i in headers:
            block = "\n".join(lines[i + 1:i + 1 + 400])
            score = _ref_density(block)
            if score >= best_score:
                best, best_score = i, score
        return "\n".join(lines[best + 1:])

    # fallback: locate a late "[1]" that starts a bracketed list
    for m in BRACKET.finditer(text):
        if m.group(1) == "1" and m.start() > len(text) * 0.4:
            if BRACKET.search(text, m.end()):
                return text[m.start():]
    return ""


def cut_appendix(section):
    """Trim obvious appendix/supplementary material that follows references."""
    m = re.search(
        r"\n\s*(appendix\b|supplementary material\b|proof of\b|"
        r"[A-F]\s+(Preliminaries|Proofs?|Appendix|Additional|Notation|"
        r"Experiments?|Details)\b)",
        section, re.I)
    return section[:m.start()] if m else section


def split_bracketed(section):
    flat = re.sub(r"\s*\n\s*", " ", section)
    parts = re.split(r"\[(\d{1,3})\]\s*", flat)
    entries = []
    for i in range(1, len(parts), 2):
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if body:
            entries.append(body)
    return entries


def split_numbered(section):
    flat = "\n" + section
    parts = re.split(r"\n\s*(\d{1,3})\.\s+", flat)
    entries = []
    for i in range(1, len(parts), 2):
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        body = re.sub(r"\s*\n\s*", " ", body).strip()
        if body and len(body) > 20:
            entries.append(body)
    return entries


def split_authoryear(section):
    """Split a natbib-style (author-year, no numeric marker) reference list.

    Entries end with '<year>[a-z]?.' (optionally followed by a stray
    citation-count digit) and the next entry starts on a fresh author name
    (Capital letter + lowercase). Requiring Capital+lowercase after the year
    avoids splitting on 'ISBN'/'URL'/'DOI' that may follow a year mid-entry.
    """
    flat = re.sub(r"\s*\n\s*", " ", section)
    # next entry starts with a name (Cap+lower, e.g. 'Ming') OR initials
    # (e.g. 'K. E. Avrachenkov', 'J. Achiam').
    marked = re.sub(
        r"((?:19|20)\d{2}[a-z]?\.)\s+(?:\d[\d,\s]*\s+)?"
        r"(?=[A-ZÀ-Þ](?:[a-zà-ÿ]|\.\s*[A-ZÀ-Þ]))",
        r"\1" + SENT, flat)
    entries = [e.strip() for e in marked.split(SENT)]
    return [e for e in entries if len(e) > 25 and C.RE_YEAR.search(e)]


PAREN_YEAR = re.compile(r"\((?:19|20)\d{2}[a-z]?\)")
APA_BOUNDARY = re.compile(
    r"(?<=\.)\s+(?=[A-ZÀ-Þ][A-Za-zà-ÿ'’\-]+,\s+[A-ZÀ-Þ]\.)")


def split_apa(section):
    """Split an APA-style list 'Surname, F. (2024). Title. Venue.' where the
    year sits in parentheses after the authors. Boundaries occur after a
    period when the next token is a 'Surname, I.' author group."""
    flat = re.sub(r"\s*\n\s*", " ", section)
    parts = APA_BOUNDARY.split(flat)
    entries = [re.sub(r"\s+", " ", p).strip() for p in parts]
    return [e for e in entries if len(e) > 25 and PAREN_YEAR.search(e)]


def split_alpha_bracket(section):
    """Split an '[Author et al., 2021]' style reference list."""
    flat = re.sub(r"\s*\n\s*", " ", section)
    parts = ALPHA_BRACKET.split(flat)
    entries = [re.sub(r"\s+", " ", p).strip() for p in parts[1:]]
    return [e for e in entries if len(e) > 25]


def split_fallback(section):
    """Last-resort: treat blank-line separated blocks as entries."""
    blocks = re.split(r"\n\s*\n", section)
    entries = []
    for b in blocks:
        b = re.sub(r"\s*\n\s*", " ", b).strip()
        if len(b) > 30 and C.RE_YEAR.search(b):
            entries.append(b)
    return entries


def parse_entries(section):
    section = cut_appendix(section)
    # Numeric [n] brackets are unambiguous; use them when they yield a real list.
    bracket_entries = split_bracketed(section) if BRACKET.search(section) else []
    if len(bracket_entries) >= 5:
        entries, method = bracket_entries, "bracket"
    else:
        # marker-less / mixed list: try each splitter, keep the most productive
        candidates = {
            "bracket": bracket_entries,
            "alpha-bracket": split_alpha_bracket(section),
            "apa": split_apa(section),
            "numbered": split_numbered(section)
            if re.search(r"\n\s*\d{1,3}\.\s+[A-ZÀ-Þ]", section) else [],
            "authoryear": split_authoryear(section),
            "fallback": split_fallback(section),
        }
        method = max(candidates, key=lambda k: len(candidates[k]))
        entries = candidates[method]
        if len(entries) < 4:  # nothing worked well
            entries, method = candidates["fallback"], "fallback"

    clean = []
    for e in entries:
        e = re.sub(r"\s+", " ", e).strip()
        if len(e) < 20:
            continue
        if len(e) > 1500:
            e = e[:1500]
        clean.append(e)
    return method, clean


def main():
    titles = load_canonical_titles()
    files = sorted(glob.glob(os.path.join(C.TEXT_DIR, "*.txt")),
                   key=lambda p: paper_id_from_name(p) or 0)

    papers, refs, stats = {}, {}, []
    for fp in files:
        pid = paper_id_from_name(fp)
        short = re.sub(r"^\d+_", "", os.path.basename(fp))[:-4]
        with open(fp, encoding="utf-8", errors="ignore") as f:
            text = C.fix_ligatures(f.read())
        papers[pid] = {
            "id": pid,
            "file": os.path.basename(fp),
            "short_title": short,
            "canonical_title": titles.get(pid) or short,
        }
        section = find_ref_section(text)
        if not section.strip():
            refs[pid] = []
            stats.append({"id": pid, "method": "NONE", "n": 0, "short": short})
            continue
        method, entries = parse_entries(section)
        parsed = [{
            "raw": e,
            "title_guess": C.extract_title_guess(e),
            "year": C.extract_year(e),
            "arxiv": C.extract_arxiv(e),
            "author": C.first_author_surname(e),
        } for e in entries]
        refs[pid] = parsed
        stats.append({"id": pid, "method": method, "n": len(parsed), "short": short})

    C.dump_json(papers, "papers.json")
    C.dump_json(refs, "references.json")
    C.dump_json(stats, "extract_stats.json")

    total = sum(s["n"] for s in stats)
    none = [s for s in stats if s["method"] == "NONE"]
    low = [s for s in stats if 0 < s["n"] < 8]
    from collections import Counter
    print(f"papers: {len(papers)}   total reference entries: {total}")
    print(f"avg refs/paper (with refs): "
          f"{total / max(1, len([s for s in stats if s['n']>0])):.1f}")
    print("methods:", dict(Counter(s["method"] for s in stats)))
    print(f"papers with NO refs ({len(none)}):", [s["id"] for s in none])
    print(f"papers with <8 refs ({len(low)}):",
          [(s["id"], s["n"], s["method"]) for s in low])


if __name__ == "__main__":
    main()
