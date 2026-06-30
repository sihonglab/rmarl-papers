"""Step 8f: download open-access PDFs for the gap papers not yet in
'download papers/'. Resolution order per paper:
  1. arXiv id (from bib eprint or the xlsx link)         -> arxiv.org/pdf
  2. Unpaywall (by DOI)                                   -> best OA pdf
  3. OpenAlex   (by DOI/title)                            -> OA pdf url
  4. arXiv title search (validated)                       -> arxiv.org/pdf
Paywalled papers with no OA copy are reported for manual download.
"""
import os
import re
import json
import time
import urllib.parse
import urllib.request
import urllib.error
from xml.etree import ElementTree as ET
import common as C

DLDIR = os.path.join(C.PROJECT_DIR, "download papers")
MAILTO = "sihonghe.ai@gmail.com"
UA = {"User-Agent": f"rmarl-survey/1.0 (mailto:{MAILTO})"}

# the 12 gap keys already downloaded by the user (mapped from the PDFs)
HAVE = {"gao2018adversarial", "yemini2025resilient", "ma2023decentralized",
        "zhang2023safe", "zhao2023less", "nisioti2021robust",
        "pham2022evaluating", "zhang2023robustness", "su2020byzantine",
        "mcmahan2024roping", "lauffer2026robust", "fang2024hardness"}


def get(url, timeout=30, tries=3, raw=False):
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                       timeout=timeout)
            return r.read() if raw else r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and i < tries - 1:
                time.sleep(3 * (i + 1)); continue
            raise


def norm(s):
    return C.normalize_title(re.sub(r"\bmarl\b",
                                    "multi agent reinforcement learning", s, flags=re.I))


def arxiv_ids_from_xlsx():
    ids = {}
    for r in C.load_json("xlsx_new_rows.json"):
        m = re.search(r"arxiv\.org/abs/([\w.]+)", r.get("link") or "")
        if m:
            ids[norm(r["title"])] = m.group(1).split("v")[0]
    return ids


def unpaywall_pdf(doi):
    try:
        j = json.loads(get(f"https://api.unpaywall.org/v2/{doi}?email={MAILTO}"))
    except Exception:
        return None
    loc = j.get("best_oa_location") or {}
    if loc.get("url_for_pdf"):
        return loc["url_for_pdf"]
    for loc in j.get("oa_locations") or []:
        if loc.get("url_for_pdf"):
            return loc["url_for_pdf"]
    return None


def openalex_pdf(doi, title):
    try:
        if doi:
            w = json.loads(get(f"https://api.openalex.org/works/doi:{doi}?mailto={MAILTO}"))
        else:
            q = urllib.parse.quote(re.sub(r"[^A-Za-z0-9 ]", " ", title))
            res = json.loads(get(f"https://api.openalex.org/works?search={q}"
                                 f"&per_page=1&mailto={MAILTO}")).get("results", [])
            w = res[0] if res else {}
    except Exception:
        return None
    for path in [("best_oa_location", "pdf_url"), ("primary_location", "pdf_url"),
                 ("open_access", "oa_url")]:
        v = (w.get(path[0]) or {}).get(path[1])
        if v:
            return v
    return None


def arxiv_search(title):
    q = urllib.parse.quote(f'ti:"{title[:80]}"')
    try:
        root = ET.fromstring(get(f"http://export.arxiv.org/api/query?search_query={q}&max_results=3"))
    except Exception:
        return None
    ns = {"a": "http://www.w3.org/2005/Atom"}
    from rapidfuzz import fuzz
    for e in root.findall("a:entry", ns):
        t = " ".join((e.findtext("a:title", "", ns)).split())
        if fuzz.token_sort_ratio(norm(title), norm(t)) >= 88:
            return e.findtext("a:id", "", ns).split("/abs/")[-1].split("v")[0]
    return None


def save_pdf(url, key):
    try:
        data = get(url, timeout=60, raw=True)
    except Exception as e:
        return f"download failed ({repr(e)[:40]})"
    if not data[:5].startswith(b"%PDF"):
        # some OA links are landing pages; give up rather than save HTML
        return "not a PDF (landing page)"
    path = os.path.join(DLDIR, key + ".pdf")
    with open(path, "wb") as f:
        f.write(data)
    return f"OK {len(data)//1024} KB"


def main():
    from rapidfuzz import fuzz, process
    gaps = json.load(open("/tmp/gaps.json"))
    xax = arxiv_ids_from_xlsx()
    xkeys = list(xax)
    todo = [g for g in gaps if g["key"] not in HAVE
            and not os.path.exists(os.path.join(DLDIR, g["key"] + ".pdf"))]
    print(f"{len(gaps)} gaps; have {len(HAVE)}; to download {len(todo)}\n")

    got, manual = [], []
    for g in todo:
        key, doi, title = g["key"], g["doi"], g["title"]
        aid = g["arxiv"]
        if not aid and xkeys:               # fuzzy-match title -> xlsx arXiv id
            b = process.extractOne(norm(title), xkeys, scorer=fuzz.token_sort_ratio)
            if b and b[1] >= 88:
                aid = xax[b[0]]
        url = src = None
        if aid:
            url, src = f"https://arxiv.org/pdf/{aid}.pdf", "arxiv"
        if not url and doi:
            url = unpaywall_pdf(doi); src = "unpaywall"
        if not url and (doi or title):
            url = openalex_pdf(doi, title); src = "openalex"
        if not url:
            a = arxiv_search(title)
            if a:
                url, src = f"https://arxiv.org/pdf/{a}.pdf", "arxiv-search"

        if not url:
            manual.append((key, title, doi))
            print(f"  [no OA ] {key:26} {title[:40]}  (doi:{doi or '-'})")
            continue
        res = save_pdf(url, key)
        if res.startswith("OK"):
            got.append(key)
            print(f"  [{src:11}] {key:26} {res}")
        else:
            manual.append((key, title, doi))
            print(f"  [FAIL {src}] {key:26} {res}  -> {title[:34]}")
        time.sleep(0.4)

    print(f"\ndownloaded {len(got)} ; still manual: {len(manual)}")
    print("\n=== need manual download (paywalled / no OA copy) ===")
    for key, title, doi in manual:
        link = f"https://doi.org/{doi}" if doi else "(no DOI)"
        print(f"  - {title[:60]}\n      {link}")
    json.dump([m[0] for m in manual], open("/tmp/manualkeys.json", "w"))


if __name__ == "__main__":
    main()
