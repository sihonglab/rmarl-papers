"""Step 8c: append the prepared gap rows (data/xlsx_new_rows.json) to
robust-marl-MASTER.md as a clearly-marked supplement section, in the master's
own line style, grouped by the existing §-taxonomy and numbered continuing from
the last corpus entry. Rows already present elsewhere in the master (e.g. the
ACM CSUR survey in §10) are skipped. Idempotent: the block is delimited by HTML
markers and rebuilt on each run. A timestamped backup is written first.
"""
import os
import re
import shutil
import datetime
from rapidfuzz import fuzz, process
import common as C

MD = os.path.join(C.PROJECT_DIR, "robust-marl-MASTER.md")
BEGIN = "<!-- BEGIN cite-analysis-supplement -->"
END = "<!-- END cite-analysis-supplement -->"
ANCHOR = "## §10 竞品 / 邻近综述"

# category -> (sort order, section heading used in the supplement)
SECT = {
    "Model/Environment Uncertainty (DRMG/Theory)": (1, "§1 环境/模型不确定性（DRMG / 理论）"),
    "State/Observation Perturbation": (2, "§2 状态 / 观测扰动"),
    "Adversarial Attacks & Training": (3, "§3 对抗攻击与对抗训练"),
    "Communication Robustness": (4, "§4 通信鲁棒"),
    "Teammates/Byzantine/Fault Tolerance": (5, "§5 队友不可信 / Byzantine / Fault-Tolerant"),
    "Offline / Distribution Shift": (7, "§7 Offline / 分布偏移"),
    "Benchmarks & Evaluation": (8, "§8 Benchmark / 测评"),
    "Applications & Safe-Robust": (9, "§9 安全 + 鲁棒 & 应用"),
}


def norm_expand(s):
    """Normalise + expand 'MARL' so abbreviated and spelled-out titles align."""
    s = re.sub(r"\bmarl\b", "multi agent reinforcement learning", s, flags=re.I)
    return C.normalize_title(s)


def already_in_md(title, md_norm, md_titles):
    # the Standen ACM CSUR'25 survey is already in §10 (listed with the "ML"
    # abbreviation, so fuzzy on link-text misses it) — match its signature.
    if re.search(r"attacks and defen[cs]es", title, re.I) and \
            re.search(r"multi[- ]?agent", title, re.I):
        return ("§10 survey", 100, -1)
    # token_sort (order/length sensitive) avoids the subset inflation that
    # token_set produces against short generic titles.
    hit = process.extractOne(norm_expand(title), md_norm,
                             scorer=fuzz.token_sort_ratio)
    return hit if hit and hit[1] >= 90 else None


def main():
    rows = C.load_json("xlsx_new_rows.json")
    md = open(MD, encoding="utf-8").read()

    # idempotent: strip any previous block FIRST, so numbering and the
    # duplicate-check below are computed against the original master only.
    md = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\s*-+\s*",
                "", md, flags=re.S)

    # titles already present anywhere in the master (skip duplicates)
    md_titles = re.findall(r"\[([^\]]{12,})\]\(", md)
    md_norm = [norm_expand(t) for t in md_titles]

    kept, skipped = [], []
    for r in rows:
        h = already_in_md(r["title"], md_norm, md_titles)
        (skipped if h else kept).append((r, h))

    # order: by section, then citation count desc
    kept.sort(key=lambda rh: (SECT.get(rh[0]["category"], (99, ""))[0],
                              -rh[0]["count"]))

    # continue numbering from the last "N." corpus entry
    last_no = max(int(n) for n in re.findall(r"(?m)^(\d+)\.\s", md)) if \
        re.search(r"(?m)^\d+\.\s", md) else 146
    last_no = max(last_no, 146)

    lines = [BEGIN,
             "## 引文分析补充语料（编号 {0}–{1}，待并入 §1–§9）★"
             .format(last_no + 1, last_no + len(kept)), "",
             "对 §1–§9 已处理的 133 篇做参考文献引文分析（`citation-analysis/`）所得："
             "被本语料引用、但前 146 篇未收录的 robust-MARL 工作。52 条候选去重后 "
             "**{0} 篇**（另 1 篇 ACM CSUR'25 综述已在 §10，未重复）。".format(len(kept)),
             "来源标记 `[C]`；`(被引 N×)` = 被本语料中 N 篇引用；★ = 被引 ≥5。",
             "> ⚠️ 自动抽取草稿：少数 venue/作者可能有误；§5 中部分为控制论/分布式优化"
             "（fault-tolerant control、consensus、Byzantine optimization）背景文献，"
             "相关性偏弱，并入前建议人工筛选。", ""]

    n = last_no
    cur = None
    for r, _ in kept:
        sect = SECT.get(r["category"], (99, "其他"))[1]
        if sect != cur:
            cur = sect
            lines += ["", f"### 补充 {sect}", ""]
        n += 1
        title = r["title"]
        link = r["link"]
        head = f"[{title}]({link})" if link else f"{title}"
        bib = f" `{r['bibkey']}`"
        va = f" — {r['venue_authors']}" if r["venue_authors"] else ""
        star = " ★" if r["count"] >= 5 else ""
        tail = f" [C]（被引 {r['count']}×）{star}"
        nolink = "" if link else " ｜链接待补"
        lines.append(f"{n}. {head}{bib}{va}{tail}{nolink}")

    lines += ["", f"**补充小计：{len(kept)}**（来自引文分析，未计入原 146 篇语料）", "",
              END, "", "---", ""]
    block = "\n".join(lines)

    # insert before §10 (previous block already stripped above)
    idx = md.index(ANCHOR)
    new_md = md[:idx] + block + md[idx:]

    # update the legend line to document the [C] tag (once)
    if "`C`引文分析" not in new_md:
        new_md = new_md.replace(
            "来源标记：`M`原始md / `B`bib(附key) / `W`web检索。",
            "来源标记：`M`原始md / `B`bib(附key) / `W`web检索 / `C`引文分析补充。", 1)

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(MD, os.path.join(C.PROJECT_DIR,
                                  f"robust-marl-MASTER.backup-{ts}.md"))
    with open(MD, "w", encoding="utf-8") as f:
        f.write(new_md)

    print(f"backup : robust-marl-MASTER.backup-{ts}.md")
    print(f"added  : {len(kept)} entries (No {last_no+1}..{last_no+len(kept)})")
    print(f"skipped (already in master): "
          f"{[r['title'][:45] for r,_ in skipped]}")
    from collections import Counter
    print("by section:",
          {SECT[r['category']][1].split()[0]: c for (r, _) in kept
           for c in [sum(1 for x, _ in kept if x['category'] == r['category'])]})


if __name__ == "__main__":
    main()
