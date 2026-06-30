"""Shared utilities for the robust-MARL citation analysis pipeline."""
import os
import re
import json
import unicodedata

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_DIR = os.path.dirname(HERE)
PROJECT_DIR = os.path.dirname(ANALYSIS_DIR)
PROCESSED_DIR = os.path.join(PROJECT_DIR, "processed-papers")
TEXT_DIR = os.path.join(PROCESSED_DIR, "text")
NOTES_DIR = os.path.join(PROCESSED_DIR, "notes")
DATA_DIR = os.path.join(ANALYSIS_DIR, "data")
REPORTS_DIR = os.path.join(ANALYSIS_DIR, "reports")


def load_json(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)


def dump_json(obj, name):
    path = os.path.join(DATA_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return path


# ---------------------------------------------------------------------------
# Text cleaning / normalisation
# ---------------------------------------------------------------------------
def fix_ligatures(s):
    return (s.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff")
             .replace("ﬃ", "ffi").replace("ﬄ", "ffl")
             .replace("–", "-").replace("—", "-")
             .replace("’", "'").replace("‘", "'")
             .replace("“", '"').replace("”", '"'))


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s)
                   if not unicodedata.combining(c))


# common stopwords to drop when building a title signature
_STOP = set("a an the of for in on to and or with via using by from is are be "
            "we our this that these those as at into over under via".split())


def normalize_title(s):
    """Aggressive normalisation used as the clustering / matching key."""
    s = fix_ligatures(s)
    s = strip_accents(s).lower()
    s = re.sub(r"\barxiv\b.*$", " ", s)           # drop arxiv tail
    s = re.sub(r"https?://\S+", " ", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def title_tokens(s):
    return [t for t in normalize_title(s).split() if t not in _STOP and len(t) > 1]


# ---------------------------------------------------------------------------
# Field extraction helpers (best-effort, regex based)
# ---------------------------------------------------------------------------
RE_ARXIV = re.compile(r"arxiv[:\s]*((?:\d{4}\.\d{4,5})|(?:[a-z\-]+/\d{7}))", re.I)
RE_YEAR = re.compile(r"\b(19[7-9]\d|20[0-4]\d)\b")
RE_DOI = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")


def extract_arxiv(s):
    m = RE_ARXIV.search(s)
    return m.group(1) if m else None


def extract_year(s):
    yrs = RE_YEAR.findall(s)
    return int(yrs[-1]) if yrs else None


_AUTHOR_CHUNK = re.compile(
    r"^(?:"
    r"(?:[A-ZÀ-Þ]\.[\s-]*)+[A-ZÀ-Þ][\w’'\-]+"        # F. Surname / J.-K. Kim
    r"|[A-ZÀ-Þ][\w’'\-]+,?\s+(?:[A-ZÀ-Þ]\.[\s-]*)+"  # Surname, F.
    r"|[A-ZÀ-Þ][\w’'\-]+"                              # bare Surname / initial
    r"|et al"
    r")[.,;]?$", re.U)


def _first_sentence(text):
    # split on a period that ends a real sentence (not an initial 'J.' nor 'al.')
    parts = re.split(r"(?<![A-Z])(?<!\bal)\.\s", text, maxsplit=1)
    return parts[0]


def _strip_leading_authors(e):
    parts = re.split(r",\s*", e)
    i = 0
    while i < len(parts) - 1:
        chunk = parts[i].strip()
        # an author chunk is short and matches a name pattern
        if len(chunk.split()) <= 3 and _AUTHOR_CHUNK.match(chunk):
            i += 1
            continue
        # handle '... and F. Surname' as the final author
        m = re.match(r"^(?:and|&)\s+(.*)$", chunk, re.I)
        if m and _AUTHOR_CHUNK.match(m.group(1).strip()):
            i += 1
            continue
        break
    rest = ", ".join(parts[i:])
    return re.sub(r"^(?:and|&|;|\.)\s+", "", rest, flags=re.I).strip()


def extract_title_guess(entry):
    """Best-effort title extraction from a single raw reference string."""
    e = fix_ligatures(entry).strip()
    e = re.sub(r"^\s*\[\d+\]\s*", "", e)      # numeric marker
    e = re.sub(r"^\s*\[[^\]]{2,40}\]\s*", "", e)  # [Author, year] marker
    e = re.sub(r"^\s*\d+\.\s*", "", e)

    # IEEE / ACM quoted-title style: "Title,"
    m = re.search(r'"([^"]{10,300}?)[,.]?"', e)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()

    # APA style: title follows the parenthesised year
    m = re.search(r"\((?:19|20)\d{2}[a-z]?\)\.?\s*", e)
    if m:
        rest = e[m.end():]
    else:
        rest = _strip_leading_authors(e)

    title = _first_sentence(rest)
    title = re.sub(r"\s+", " ", title).strip(" ,.;")
    return title[:300]


def classify(text):
    """Coarse topical bucket for a reference title/entry."""
    t = re.sub(r"-\s+", "", (text or "").lower())  # join 'multi- agent'
    t = " " + t + " "
    is_ma = bool(re.search(r"multi[ -]?agent|multiagent|\bmarl\b|markov game|"
                           r"mean[ -]field|multi[ -]robot|cooperative", t))
    is_rl = bool(re.search(r"reinforcement learning|\brl\b|q-learning|"
                           r"policy gradient|actor[- ]critic|markov decision", t))
    is_robust = bool(re.search(
        r"robust|resilien|adversar|byzantine|fault[- ]toleran|perturb|"
        r"uncertain|\battack|distributionally|poison|safe|certif", t))
    is_game = bool(re.search(r"\bnash\b|equilibri|\bgame\b|game theory|"
                             r"minimax|stackelberg|zero-sum", t))
    if is_robust and is_ma:
        return "robust_marl"
    if is_ma:
        return "marl"
    if is_robust and is_rl:
        return "robust_rl"
    if is_rl:
        return "rl"
    if is_game:
        return "game_theory"
    return "other"


def first_author_surname(entry):
    e = fix_ligatures(entry).strip()
    e = re.sub(r"^\s*\[\d+\]\s*", "", e)
    e = re.sub(r"^\s*\d+\.\s*", "", e)
    # patterns: "Surname, F." or "F. Surname" or "Firstname Surname"
    m = re.match(r"([A-Z][a-zA-Z'\-]+),\s*[A-Z]", e)
    if m:
        return m.group(1).lower()
    m = re.match(r"(?:[A-Z]\.\s*)+([A-Z][a-zA-Z'\-]+)", e)
    if m:
        return m.group(1).lower()
    m = re.match(r"[A-Z][a-zA-Z'\-]+\s+([A-Z][a-zA-Z'\-]+)", e)
    if m:
        return m.group(1).lower()
    return None
