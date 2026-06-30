# 写作流程计划 — Robust MARL Review（单人独写）

## Context

你已经把"前置资料"备齐：191 篇分好类的语料（`robust-marl-CLASSIFIED.md`）、160 篇逐篇标准化笔记（`processed-papers/notes/` 中文 + `notes-en/` 英文）、引文分析（`citation-analysis/reports/`）、可编译的 LaTeX 工程（`paper/`，13 个 section 文件 + `refs.bib` 164 条）、竞品综述 PDF（`review-papers/`）。写作规范（thesis、四段式模板、记号表、glossary）已**自包含在本文件**中。


**当前 LaTeX 填充状态**（实测）：
- `02-background.tex` 基本写完（163 行实质内容）。
- 其余 12 个 section 都是**带骨架的 TODO**：每个文件头已写好 outline、预填了 `\cite{key}`、列了本节 MASTER 编号、标了必答的两个收尾问题（Q1 为何 MARL-specific / Q2 open gap），并给了小结表 stub。
- `12-challenges.tex` 是 stub，但 `robust-marl-MASTER.md §13` 已有 C1–C10 完整草稿可直接移植。

**目标**：把这些骨架按统一模板填成正文，产出投 ACM CSUR 的完整 survey。本计划给出**单人、可重复的章节级 SOP**；模板/记号/glossary/竞品定位均自包含于下文，不依赖任何外部文档。

> 注：你未指定我（Claude）的角色。下面 SOP 对"你自己写"和"让我按节起草初稿、你审改"两种模式都适用；任一节都可单独喊我起草。

---

## 阶段 0 — 先钉死主轴（spine），一次性

每节都要回扣它，所以必须最先冻结。产物放进 `paper/`：

1. **Thesis 一句话** + **taxonomy 图**：在 `paper/fig/taxonomy.tex` 画出"Branch I 单智能体复现维度（model/state/action/reward）+ Branch II MARL 独有维度（队友不可信 / 通信被攻击 / curse of multiagency）"的树。`01-introduction.tex:29` 已 `\input{fig/taxonomy}`。
2. **统一记号表**：钉死核心记号（状态 $s$、观测 $o$、联合动作 $\mathbf{a}=(a_1,\dots,a_n)$、智能体数 $n$、不确定集 $\mathcal{U}$、转移核 $P$、奖励 $r$、策略 $\pi$、worst-case 价值 $\underline V$、Markov game $\mathcal G$），放 `02-background.tex` 或单列 preliminaries 小节。
   - **背景奠基工作的覆盖**：把各 en note 的「Cited references (resolved...)」与 `citation-analysis/reports/02_most_cited_references.md` 交叉，得到被反复引用的奠基文献（robust MDP、Markov game、MADDPG/QMIX、minimax RARL 等），确保 §2 背景与 §11 引全、不漏。
3. **Glossary**：robust / resilient / safe / secure 的区分 + uncertainty set / curse of multiagency / robust equilibrium / distributionally robust。开篇讲清。
4. **竞品定位**：读 `review-papers/` 里 CSUR'25 SoK 与单智能体 robust-RL 综述，把差异化段落落到 `02-background.tex` 的 related work（覆盖更广 + 统一"扰动来源"taxonomy）。
5. **定写作风格样板（style guide）**：从 `review-papers/` 选 1–2 篇成熟综述（如《Robust RL: A Review of Foundations and Recent Advances》、CSUR'25 SoK）作为**行文风格参照**——学它们的：每节开场如何过渡、代表作如何嵌进段落（叙述式而非清单式）、对比表的列设计、"we"的用法与时态、how-to-cite 的密度。把要点记成 1 页 style note，写每节时对齐。我（Claude）起草时也按此风格仿写。

---

## 阶段 1 — 章节级 SOP（对每个 section §3–§11 重复）

每节固定走这 6 步，保证"像一个人写的"：

1. **取语料**：从 `robust-marl-CLASSIFIED.md` 抄出本节的**主类编号 + 跨类重复收录**两组清单（CLASSIFIED 每节末已分好）。
2. **代表作四段式**：对每篇代表作，打开 `processed-papers/notes-en/`（或中文 `notes/`）对应笔记 → 写【问题设定（针对哪类扰动/解概念）→ 方法一句话 → 理论/实验结论 → 局限 + 本综述归类 §X（含跨类）】。**行文按阶段 0 定的 style note 仿照 `review-papers/` 的叙述式风格**，把四段融进连贯段落，不要写成条目清单。每篇 en note 尾部两块要用足：
   - **「Related Work (verbatim excerpts)」**：作者自陈的谱系与对比对象 → 写本节的承接/对比叙述与"相对前作改进了什么"。**转述改写、勿照抄原文**。
   - **「Cited references (resolved...)」**：多篇代表作的共同奠基引用 → 在 §2 背景/§11 里正确引到、厘清方法谱系；缺 bibkey 的奠基工作记下来补 `refs.bib`/MASTER。
3. **次要论文一句话带过**，避免详略失衡。
4. **填小结表**：每个 `.tex` 已有表 stub（如 `tab:byzantine` 的列 Threat/Mechanism/Guarantee/Decentralized），把代表作填进去。
5. **写头尾**：开头 = 本节扰动维度 + 为什么 MARL 比单智能体难；结尾 = **回扣 thesis**，并正面回答文件头预设的 **Q1/Q2**。
6. **查漏 + 对 bib**：用 `citation-analysis/reports/03_missing_*` 与 `04_missing_vs_master_list.md` 确认没漏被引高的关键工作；确认每个 `\cite{key}` 在 `paper/refs.bib` 里存在（缺则补，遵守"先改 MASTER 再进 bib"）。

**推荐起草顺序**（你说无所谓，给一个降阻力的排法）：
- **先拿 §7 Byzantine（MASTER §5）做 pilot**：中等体量、是差异化卖点、最能体现 thesis——用它**校准模板/记号/四段式的颗粒度**，定稿后作为其余节的样板。
- 然后 **Branch II 差异化**：§8 LLM-MAS（`08-llm-mas.tex`，仅 5 篇，快）、§6 communication。
- 再 **Branch I 复现维度**：§3 model-uncertainty（理论最重，放状态好时写）、§4 state-observation、§5 adversarial。
- 最后 **支撑节**：§9 offline（2 篇，最快）、§10 benchmarks、§11 applications（41 篇但描述性、可批量套模板）。

---

## 阶段 2 — 框架节（等正文齐了再写）

- **§12 Challenges**：把 `robust-marl-MASTER.md §13` 的 C1–C10 移植进 `12-challenges.tex`，每条扩成一小段，引对应章节/编号。
- **§1 Introduction**：按 `01-introduction.tex` 文件头的 (a)–(f) outline 写流畅散文；contributions 列表回指实际成节内容。
- **§13 Conclusion**：收束 thesis + 重申三个 MARL 独有维度。
- intro/conclusion **必须放最后写**，才能准确反映正文。

## 阶段 3 — 跨章节图表

- taxonomy 图（阶段 0 已起）、**跨维度对比大表**（各节"扰动×方法×保证×是否去中心化"汇总）、**时间线图**（2017–2026 演进）。素材可取 `processed-papers/analysis_outputs/`（作者/团队协作图）做"研究版图"小图。

## 阶段 4 — 统稿、清洗、定稿

1. **一致性自审**（单人也要做一遍，模拟交叉评审）：记号统一？术语 robust/resilient/safe/secure 不混用？跨类论文有没有在两节各讲一遍正文（应一节详写、另一节一句话指回）？
2. **bib 清洗**：去物理重复（`he2023robust`×5、`shi2024breaking`×2、`zaman2024robust`×2、`qu2026`=`learningdistributionally`、`farhat2026`/`2025`、`vieira2025`=`augusto2025`、`ding2023get`×2），统一 key，补 `链接待补` 的 DOI。
3. **最终文献 sweep**：投稿前 1–2 周设 cutoff，补最新工作，避免被指过时。
4. **统语气润色**：逐节过一遍，保证一个声音。

---

## 关键文件

| 用途 | 路径 |
|---|---|
| 分类纲领（取每节清单） | `robust-marl-CLASSIFIED.md` |
| 唯一文献事实源 + §13 挑战草稿 | `robust-marl-MASTER.md` |
| 逐篇写作素材 | `processed-papers/notes-en/`、`notes/`、`INDEX.md` |
| 查漏/被引证据 | `citation-analysis/reports/02_*,03_*,04_*` |
| 待填正文（骨架已就位） | `paper/sections/03..13-*.tex` |
| 图/表 | `paper/fig/`、`paper/tab/` |
| 参考文献 | `paper/refs.bib`（164 条） |
| 模板/记号/glossary/竞品 | 本文件「阶段 0」、`review-papers/` |

---

## 可直接使用的 Prompt（一节一个 subagent，互不干扰）

**隔离原则**：每个 subagent 只写**自己那一个** `paper/sections/*.tex`；**不直接改共享的 `refs.bib`**（避免并行写冲突）。`refs.bib` 是"必须讨论的论文"集合，但**不封顶**——本节确有价值的其他文献（尤其 en note『Cited references』里已解析的真实奠基工作、竞品/背景文献）都可引。新增引用走**侧车文件**：每个 agent 把自己新增的 bib 条目写进 `paper/sections/{{TEXFILE}}.addbib`（与正文同名的 sidecar），最后由你统一去重并入 `refs.bib`。这样多节可并行而零冲突。

### 通用模板（把 `{{...}}` 换成下表对应行即可直接粘贴）

```
你在为一篇《Robust MARL》综述（投 ACM CSUR）起草其中【一节】。只改你被指派的那一个 .tex 及其同名 sidecar .addbib；绝不触碰其他 section 文件，也绝不直接编辑 paper/refs.bib。

工作目录：/Users/sihonghe/Desktop/papers/review-rmarl
被指派章节：{{TOPIC}}
只可编辑此文件：paper/sections/{{TEXFILE}}
本节语料：在 robust-marl-CLASSIFIED.md 中标题为「{{CLASSIFIED_HEADER}}」的那一节，**主类条目 + 该节末「跨类重复收录」条目都要覆盖**。

THESIS（每段都要服务它）：单智能体 robust RL 的扰动维度（model/state/action/reward）在 MARL 中全部复现；MARL 额外引入三类单智能体没有的维度——队友不可信、通信被攻击、curse of multiagency。本节正文必须说清它和这条 thesis 的关系。

步骤：
1. 读 paper/sections/{{TEXFILE}}：它已有 outline、预填的 \cite{key}、必答的两个收尾问题（Q1 为何 MARL-specific / Q2 open gap）、以及小结表 stub。保留这套结构，把 TODO 填成正文。
2. 读 robust-marl-CLASSIFIED.md 对应节，拿到准确的论文清单与编号。【四段式】每篇代表作 = 问题设定（针对哪类扰动/解概念）→ 方法核心一句话 → 理论/实验结论 → 局限与本综述归类(§X,含跨类)。【每节结构】开头（本节扰动维度 + 为何 MARL 比单智能体难）→ 主体（按子簇组织，代表作四段式融进段落，次要论文一句话）→ 小结表 → 结尾（回扣 thesis + 答 Q1/Q2）。
3. 每篇代表作：**CLASSIFIED 的 ID 已与笔记编号对齐**，直接打开 `processed-papers/notes-en/{ID}_*.md` 即可（找不到可用 INDEX.md 按标题核对）。**若该 ID 没有笔记文件**（部分论文尚无笔记），则只依据 CLASSIFIED/INDEX 的 TL;DR 一句话带过，**严禁编造方法/结论**，并在报告里列出待补笔记。有笔记的，重点用足两块内容：
   - 正文区块（TL;DR / Problem & Motivation / Robustness Setting / Method / Theoretical Contributions / Key Results / Limitations / Relevance to Survey）→ 直接喂四段式。
   - 「Related Work (verbatim excerpts from the paper)」→ 作者自己怎么定位前作、与谁对比，用来写本节的**承接/谱系叙述**和"它相对前作改进了什么"，但**要改写转述、不得照抄原文**（避免抄袭/自我抄袭）。
   - 「Cited references (resolved from the paper's bibliography)」→ 用来：(a) 把多篇代表作共同引用的奠基工作识别出来、在背景里正确引到；(b) 厘清方法谱系（谁建立在谁之上）。若某奠基工作还没 bibkey，在报告里列出建议补 bib。
4. 风格：仿照 review-papers/「Robust Reinforcement Learning A Review of Foundations and Recent Advances.pdf」的成熟综述笔法——叙述式段落、不要条目清单；代表作的"问题设定→方法一句话→结论→局限与归类(§X,含跨类)"四段融进连贯散文；用 "we"；描述工作用一般现在时。
5. 成文：开头（本节对应哪类扰动 + 为什么 MARL 比单智能体难）→ 主体（按 CLASSIFIED 的子簇组织，代表作四段式融进段落，次要论文一句话带过）→ 填小结表 → 结尾（回扣 thesis 并正面回答文件头的 Q1、Q2）。
6. 引用规则：本节 CLASSIFIED 清单里的论文是**必须讨论**的；但**不限于 refs.bib**——确有价值的其他文献（尤其 en note『Cited references (resolved...)』里已解析的真实奠基/背景/竞品工作）也应引。优先用 refs.bib 已有 key；需要新引用时，**来源必须真实可核**（取自 note 的 resolved citations 或可核实出处），**严禁凭记忆杜撰 标题/作者/venue/年份**。每条新增引用：在正文 \cite{newkey}，并把对应 BibTeX 条目追加进 sidecar `paper/sections/{{TEXFILE}}.addbib`（不要动 refs.bib）。
7. 只编辑 paper/sections/{{TEXFILE}} 与其 sidecar .addbib 两个文件。最后【报告】：字数、覆盖论文数、(a) 用到但 refs.bib 里没有、已写进 .addbib 的新 key 清单；(b) 本节 CLASSIFIED 清单里还没有 bibkey 的论文；(c) 任何无法可靠核实出处、因而未敢引用的工作。
```

### 各节参数表（每行替换模板里的三个占位符）

| TEXFILE | TOPIC | CLASSIFIED_HEADER |
|---|---|---|
| `03-model-uncertainty.tex` | 环境/模型不确定性（DRMG/理论主线） | `## §1 环境/模型不确定性（DRMG / 理论主线）★` |
| `04-state-observation.tex` | 状态/观测扰动 | `## §2 状态 / 观测扰动` |
| `05-adversarial.tex` | 对抗攻击与对抗训练 | `## §3 对抗攻击 与 对抗训练` |
| `06-communication.tex` | 通信鲁棒 | `## §4 通信鲁棒（noise + 攻击 + certified）` |
| `07-byzantine.tex` | 队友不可信/Byzantine/容错/Trust | `## §5 队友不可信 / Byzantine / Fault-Tolerant / Trust（多智能体独有）★` |
| `08-llm-mas.tex` | LLM 多智能体安全/鲁棒 | `## §6 LLM 多智能体安全 / 鲁棒（全新前沿）★ 差异化卖点` |
| `09-offline.tex` | Offline/分布偏移鲁棒 | `## §7 Offline / 分布偏移鲁棒（新增子领域）` |
| `10-benchmarks.tex` | Benchmark/测评 | `## §8 Benchmark / 测评` |
| `11-applications.tex` | 安全+鲁棒 & 应用 | `## §9 安全+鲁棒 & 应用` |

> intro(`01`)/background(`02`)/challenges(`12`)/conclusion(`13`) 不派 subagent——这些回扣全局、由你（lead）在阶段 2 亲自写（challenges 直接移植 MASTER §13 的 C1–C10）。

### 怎么跑（建议）
- **先单独跑 pilot**：用 `07-byzantine.tex` 那行跑一个 subagent，验收风格/颗粒度后，把它当样板。
- 其余 8 节可**逐个或并行**派 subagent（各写各文件，零冲突）。
- 全部回来后，你统一：把各节 `*.addbib` 去重合并进 `refs.bib`（核对真实性、统一 key 风格）、画 taxonomy/对比大表、写 intro/challenges/conclusion、统稿润色、跑编译。

---

## 验证（每节 + 收尾）

- 每写完一节：`cd paper && latexmk -pdf main.tex`，确认**无 undefined citation / reference**、PDF 正常生成（基线 `paper/main.pdf` 已可编译）。
- 收尾：通读 `main.pdf` 检查记号/术语/篇幅配重；篇幅目标 = §1理论 + §3攻防 + §5 Byzantine + §9应用为主体，§6 LLM-MAS 为亮点。
- 文末核对：CLASSIFIED 的 191 篇核心语料（规范 ID 1–193 除 156/160）是否都至少被某节引用一次（无遗漏语料）。
