"""Step 8d: fetch authoritative BibTeX for the gap papers (data/xlsx_new_rows.json)
and append them to collected-papers/references.bib.

Source priority per paper:
  1. OpenAlex (published venue, full authors, pages, DOI) — primary
  2. arXiv API (preprint -> @misc with eprint)
  3. local metadata (@misc, marked TODO)

Cite keys are regenerated from the authoritative first author so they are clean
and collision-free; data/bib_keymap.json records {old_bibkey -> new_bibkey} so
step 12 can sync the keys into the master .md / .xlsx.

Idempotent: a marked block is removed and rebuilt on each run. Back up
references.bib before first use.
"""
import os
import re
import json
import time
import urllib.parse
import urllib.request
import urllib.error
from xml.etree import ElementTree as ET
from rapidfuzz import fuzz
import common as C

BIB = os.path.join(C.PROJECT_DIR, "collected-papers", "references.bib")
BEGIN = "% ===== BEGIN cite-analysis gap papers ====="
END = "% ===== END cite-analysis gap papers ====="
MAILTO = "sihonghe.ai@gmail.com"
UA = {"User-Agent": f"rmarl-survey-bibfetch/2.0 (mailto:{MAILTO})"}
SKIP = {"robust", "multi", "agent", "deep", "learning", "against", "multiagent",
        "reinforcement", "via", "with", "based", "using", "toward", "towards",
        "the", "for", "and", "a", "of", "in", "on", "an"}
CONF_RE = re.compile(r"conference|proceedings|symposium|workshop|\bicra\b|\bicml\b|"
                     r"neurips|\baaai\b|\biclr\b|\bijcai\b|\bcvpr\b|\biccv\b|"
                     r"\biros\b|\bcdc\b|automation|\bacc\b|aistats|\bcorl\b|aamas",
                     re.I)


def get(url, timeout=25, tries=4):
    for i in range(tries):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(url, headers=UA), timeout=timeout
            ).read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and i < tries - 1:
                time.sleep(5 * (i + 1))
                continue
            raise


def norm_expand(s):
    s = re.sub(r"\bmarl\b", "multi agent reinforcement learning", s, flags=re.I)
    return C.normalize_title(s)


def title_word(title):
    for w in re.sub(r"[^a-z0-9 ]", " ", title.lower()).split():
        if len(w) > 3 and w not in SKIP:
            return w
    return "x"


def make_key(surname, year, title, used):
    sur = re.sub(r"[^a-z]", "", (surname or "anon").lower()) or "anon"
    base = f"{sur}{year or ''}{title_word(title)}"
    k, i = base, 0
    while k in used:
        i += 1
        k = base + "abcdefghij"[i % 10]
    used.add(k)
    return k


def braces(s):
    # protect capitalised acronyms so BibTeX keeps their case
    return re.sub(r"\b([A-Z]{2,}|[A-Z][a-z]*[A-Z][A-Za-z]*)\b", r"{\1}", s)


# ---------------------------------------------------------------------------
def from_openalex(title):
    q = urllib.parse.quote(re.sub(r"[^A-Za-z0-9 ]", " ", title))
    url = (f"https://api.openalex.org/works?search={q}"
           f"&per_page=8&mailto={MAILTO}")
    res = json.loads(get(url, tries=2)).get("results", [])
    tnorm = norm_expand(title)
    best, score = None, 0
    for w in res:
        sc = fuzz.token_sort_ratio(tnorm, norm_expand(w.get("display_name") or ""))
        if sc > score:
            best, score = w, sc
    if not best or score < 72:
        return None, None, None
    return best, score, build_openalex_bib(best)


def build_openalex_bib(w):
    authors = [a["author"]["display_name"] for a in w.get("authorships", [])
               if a.get("author", {}).get("display_name")]
    src = (w.get("primary_location") or {}).get("source") or {}
    venue = src.get("display_name") or ""
    stype = src.get("type") or ""
    year = w.get("publication_year")
    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    bib = w.get("biblio") or {}
    fp, lp = bib.get("first_page"), bib.get("last_page")
    pages = f"{fp}--{lp}" if fp and lp else (fp or "")
    url = w.get("doi") or (w.get("primary_location") or {}).get("landing_page_url") or ""

    is_conf = stype == "conference" or CONF_RE.search(venue or "")
    fields = [("author", " and ".join(authors)),
              ("title", braces(w.get("display_name") or ""))]
    if is_conf:
        etype = "inproceedings"
        fields.append(("booktitle", venue))
    elif stype == "journal" or venue:
        etype = "article"
        fields.append(("journal", venue))
        if bib.get("volume"):
            fields.append(("volume", bib["volume"]))
        if bib.get("issue"):
            fields.append(("number", bib["issue"]))
    else:
        etype = "misc"
    if year:
        fields.append(("year", str(year)))
    if pages:
        fields.append(("pages", pages))
    if doi:
        fields.append(("doi", doi))
    if url:
        fields.append(("url", url))
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields if v)
    surname = authors[0].split()[-1] if authors else None
    return f"@{etype}{{KEY,\n{body}\n}}", surname


def from_crossref(title):
    q = urllib.parse.quote(title)
    url = (f"https://api.crossref.org/works?query.bibliographic={q}"
           f"&rows=8&mailto={MAILTO}")
    items = json.loads(get(url)).get("message", {}).get("items", [])
    tnorm = norm_expand(title)
    best, score = None, 0
    for it in items:
        t = (it.get("title") or [""])[0]
        sc = fuzz.token_sort_ratio(tnorm, norm_expand(t))
        if sc > score:
            best, score = it, sc
    if not best or score < 75:
        return None, None
    authors = [" ".join(x for x in [a.get("given"), a.get("family")] if x)
               for a in best.get("author", []) if a.get("family")]
    cont = (best.get("container-title") or [""])[0]
    typ = best.get("type", "")
    year = None
    dp = (best.get("issued") or {}).get("date-parts") or [[None]]
    if dp and dp[0]:
        year = dp[0][0]
    fields = [("author", " and ".join(authors)),
              ("title", braces((best.get("title") or [""])[0]))]
    if typ == "proceedings-article":
        etype = "inproceedings"
        fields.append(("booktitle", cont))
    elif typ == "journal-article" or cont:
        etype = "article"
        fields.append(("journal", cont))
        if best.get("volume"):
            fields.append(("volume", best["volume"]))
        if best.get("issue"):
            fields.append(("number", best["issue"]))
    else:
        etype = "misc"
    if year:
        fields.append(("year", str(year)))
    if best.get("page"):
        fields.append(("pages", best["page"].replace("-", "--")))
    if best.get("DOI"):
        fields.append(("doi", best["DOI"]))
        fields.append(("url", "https://doi.org/" + best["DOI"]))
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields if v)
    surname = authors[0].split()[-1] if authors else None
    return f"@{etype}{{KEY,\n{body}\n}}", surname


def from_arxiv(aid, title):
    url = f"http://export.arxiv.org/api/query?id_list={aid}&max_results=1"
    root = ET.fromstring(get(url))
    ns = {"a": "http://www.w3.org/2005/Atom"}
    e = root.find("a:entry", ns)
    if e is None:
        return None, None
    t = " ".join((e.findtext("a:title", "", ns) or "").split())
    authors = [a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)]
    year = (e.findtext("a:published", "", ns) or "")[:4]
    prim = e.find("arxiv:primary_category",
                  {"arxiv": "http://arxiv.org/schemas/atom"})
    cat = prim.get("term") if prim is not None else "cs.LG"
    bib = ("@misc{{KEY,\n  author = {{{au}}},\n  title = {{{t}}},\n"
           "  year = {{{y}}},\n  eprint = {{{aid}}},\n  archivePrefix = {{arXiv}},\n"
           "  primaryClass = {{{cat}}},\n  url = {{https://arxiv.org/abs/{aid}}}\n}}"
           ).format(au=" and ".join(authors), t=braces(t or title), y=year,
                    aid=aid, cat=cat)
    return bib, (authors[0].split()[-1] if authors else None)


def from_local(rec):
    au = re.sub(r"\s*et al\.?$", "", (rec["venue_authors"] or "").split(",")[-1]).strip()
    bib = ("@misc{{KEY,\n  title = {{{t}}},\n  howpublished = {{{v}}},\n"
           "  year = {{{y}}},\n  note = {{BibTeX not auto-located -- verify}}\n}}"
           ).format(t=braces(rec["title"]), v=rec["venue_authors"] or "",
                    y=rec["year"] or "")
    return bib, (au.split()[-1] if au else None)


def rekey(bib, key):
    return re.sub(r"^(@\w+\{)KEY,", r"\1" + key + ",", bib, count=1)


def main():
    rows = C.load_json("xlsx_new_rows.json")
    text = open(BIB, encoding="utf-8").read()
    # idempotent: drop any previously appended block
    text = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\s*",
                  "", text, flags=re.S).rstrip()
    used = set(re.findall(r"@\w+\{([^,]+),", text))

    cache_path = os.path.join(C.DATA_DIR, "bib_cache.json")
    cache = C.load_json("bib_cache.json") if os.path.exists(cache_path) else {}

    out, keymap, srcs = [], {}, {}
    for r in rows:
        title, src = r["title"], "local"
        aid = None
        m = re.search(r"arxiv\.org/abs/([\w.\-/]+)", r.get("link") or "")
        if m:
            aid = m.group(1)
        tnorm = norm_expand(title)

        # reuse a previously fetched authoritative entry (avoids re-hammering APIs)
        cached = cache.get(r["bibkey"])
        if cached and cached["src"] != "local":
            bib, surname, src = cached["bib"], cached["surname"], cached["src"]
            newkey = make_key(surname or r["bibkey"].rstrip("0123456789"),
                              r["year"], title, used)
            bib = rekey(bib, newkey)
            if newkey != r["bibkey"]:
                keymap[r["bibkey"]] = newkey
            out.append(f"% [{r['count']}x | {r['category']} | src:{src}] "
                       f"cited by {','.join('#'+str(p) for p in r['citing'])}\n" + bib)
            srcs[src] = srcs.get(src, 0) + 1
            print(f"  [{src:8}*] {newkey:28} {title[:42]}")
            continue

        def accept(b):
            """Only trust a fetched entry if its title matches the intended one."""
            m = re.search(r"title\s*=\s*\{(.+?)\}\s*,", b or "", re.S)
            bt = re.sub(r"[{}]", "", m.group(1)) if m else ""
            return fuzz.token_sort_ratio(tnorm, norm_expand(bt)) >= 82

        bib = surname = None

        def oa():
            w, sc, res = from_openalex(title)
            if not res:
                return None, None
            stype = ((w.get("primary_location") or {}).get("source") or {}
                     ).get("type")
            if stype == "repository" and aid:        # preprint -> arXiv @misc
                return from_arxiv(aid, title)
            return res

        # Crossref first (lenient, no throttling); OpenAlex fail-fast secondary;
        # arXiv-by-id last (can't mismatch). Validation gate rejects bad matches.
        attempts = [("crossref", lambda: from_crossref(title)),
                    ("openalex", oa)]
        if aid:
            attempts.append(("arxiv", lambda: from_arxiv(aid, title)))
        for name, fn in attempts:
            try:
                cand, csur = fn()
            except Exception as e:                   # noqa: BLE001
                print(f"  {name} error:", title[:36], repr(e)[:50])
                continue
            if cand and accept(cand):
                bib, surname, src = cand, csur, name
                break
        if not bib:
            bib, surname = from_local(r)
            src = "local"
        else:
            cache[r["bibkey"]] = {"bib": bib, "surname": surname, "src": src}

        newkey = make_key(surname or r["bibkey"].rstrip("0123456789"),
                          r["year"], title, used)
        bib = rekey(bib, newkey)
        if newkey != r["bibkey"]:
            keymap[r["bibkey"]] = newkey
        out.append(f"% [{r['count']}x | {r['category']} | src:{src}] "
                   f"cited by {','.join('#'+str(p) for p in r['citing'])}\n" + bib)
        srcs[src] = srcs.get(src, 0) + 1
        print(f"  [{src:8}] {newkey:28} {title[:44]}")
        time.sleep(0.2)

    block = "\n\n".join([BEGIN] + out + [END]) + "\n"
    with open(BIB, "w", encoding="utf-8") as f:
        f.write(text + "\n\n" + block)
    C.dump_json(keymap, "bib_keymap.json")
    C.dump_json(cache, "bib_cache.json")
    print(f"\nappended {len(out)} entries -> {BIB}")
    print("sources:", srcs)
    print(f"key remaps: {len(keymap)} -> data/bib_keymap.json")


if __name__ == "__main__":
    main()
