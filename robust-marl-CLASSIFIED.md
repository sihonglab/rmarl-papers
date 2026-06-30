# Robust MARL — 统一分类表（Classified List）

> 由 `robust-marl-MASTER.md` 重新整理，并**对齐 `processed-papers/INDEX.md` 与 `robust-marl-papers.xlsx` 的规范编号（ID 1–193）**：1–146 不变；原"引文分析补充语料"已并入 §1–§9，并按 xlsx/INDEX 重新编号（散布于 147–193）。规范 ID **156** = §10 竞品 SoK 综述（不计入语料）、ID **160** = 与 #65 同一篇（xlsx 内重复），故核心语料仍为 **191 篇**，占用 1–193 中除 156/160 外的 191 个编号。**编号已与笔记 `notes-en/` 一致，可直接按 ID 取笔记。**
> 分类主轴沿用 **「鲁棒性针对什么扰动」**。**一篇文章可同时覆盖多个分类、允许重复收录**：在其主类正常列出，并在每个相关的次类下以「跨类重复收录」子表再列一次，标注 `（主类 §X）` 以示区分。行尾 `｜跨 §X` 标明该文还涉及哪些节。
> 因此**各节小计含重复**；不重复的核心语料总数仍为 **191 篇**（见文末口径说明）。
> 来源标记：`M`原始md / `B`bib(附key) / `W`web检索 / `C`引文分析补充。⚠️=待核实venue，★=高价值，`链接待补`=仅有venue无可靠链接。
> 整理日期：2026-06-29。本表将作为撰写 review 的章节骨架。

---

## 分类总览

> 「主类」= 唯一归属（不含重复），合计 191；「含跨类」= 加上重复收录的次类条目后该节的实际篇数。

| 节 | 主题 | 主类编号 | 主类 | 含跨类 |
|---|---|---|---|---|
| §1 | 环境/模型不确定性（DRMG / 理论主线）★ | 1–27, 150, 159, 182, 186, 190 | 32 | 36 |
| §2 | 状态 / 观测扰动 | 28–42, 153, 176 | 17 | 20 |
| §3 | 对抗攻击 与 对抗训练 | 43–59, 147, 152, 157, 158, 162, 164, 172, 174, 181, 192 | 27 | 41 |
| §4 | 通信鲁棒（noise + 攻击 + certified） | 60–72, 148, 149, 166, 168, 169, 183 | 19 | 22 |
| §5 | 队友不可信 / Byzantine / Fault-Tolerant / Trust ★ | 73–86, 151, 161, 163, 167, 170, 171, 175, 177–180, 184, 185, 187–189, 191, 193 | 32 | 36 |
| §6 | LLM 多智能体安全 / 鲁棒（前沿）★ | 87–91 | 5 | 7 |
| §7 | Offline / 分布偏移鲁棒 | 92–93 | 2 | 3 |
| §8 | Benchmark / 测评 | 94–105, 155, 165 | 14 | 16 |
| §9 | 安全+鲁棒 & 应用 | 106–146, 154, 173 | 43 | 53 |
| **合计** | **核心语料（去重）** | **1–193 除 156/160** | **191** | （234，含重复 43 次）|
| §10 | 竞品/邻近综述（positioning，不计入语料） | — | 9 | — |
| §11 | 背景引用（铺垫，不计入语料） | — | — | — |
| §12 | 已排除（非 robust-MARL） | — | 4 | — |

> 说明：§5、§3 的补充语料含部分**控制论/分布式优化背景**文献（fault-tolerant control、consensus、Byzantine optimization），相关性偏弱，行尾标 `⟂背景`，撰写时可作背景引用或进一步剔除。

---

## §1 环境/模型不确定性（DRMG / 理论主线）★

**核心理论线（DRMG / minimax / sample-efficiency）**
1. [Robust MARL with Model Uncertainty](https://proceedings.neurips.cc/paper/2020/hash/774412967f19ea61d448977ad9749078-Abstract.html) — NeurIPS 2020, Kaiqing Zhang [M]
2. [Sample-Efficient Robust MARL in Face of Environmental Uncertainty](https://arxiv.org/abs/2404.18909) `shi2024sample` — ICML 2024 [M][B] ★
3. [Breaking the Curse of Multiagency in Robust MARL](https://arxiv.org/abs/2409.20067) `shi2024breaking` — ICML 2025 [M][B] ★
4. [Taming the Curses of Multiagency … Linear Function Approximation](https://arxiv.org/abs/2605.03125) — arXiv 2026, Gai & Shi [W]
5. [Distributionally Robust Cooperative MARL via Robust Value Factorization](https://arxiv.org/abs/2602.11437) `qu2026distributionally` — ICLR 2026, Caltech [B][W] ★
6. [Sample-Efficient DR MARL via Online Interaction](https://arxiv.org/abs/2508.02948) `farhat2026sample` — ICLR 2026, Yue Wang组 [M][B][W] ★
7. [Strategically Robust MARL with Linear Function Approximation](https://arxiv.org/abs/2603.09208) — arXiv 2026, Mazumdar/Ratliff [W]
8. [Distributionally Robust Online Markov Game w/ Linear Func Approx](https://arxiv.org/abs/2511.07831) — arXiv 2025 ⚠️ [W]
9. [Distributionally Robust Markov Games with Average Reward](https://arxiv.org/abs/2508.03136) — arXiv 2025, Roch & Yue Wang [W]
21. [Minimax-Optimal MARL in Markov Games w/ Generative Model](https://papers.nips.cc/paper_files/paper/2022/hash/62b4fea131cfd5b7504eae356b75bbd8-Abstract-Conference.html) — NeurIPS 2022, Gen Li [M]
150. Decentralized robust v-learning for solving Markov games with model uncertainty `ma2023decentralized` — JMLR 2023 [C]（被引 8×）★ ｜链接待补
159. Roping in uncertainty: Robustness and regularization in Markov games `mcmahan2024roping` — ICML 2024, Mazumdar et al. [C]（被引 3×）｜链接待补
190. [Learning Markov games with adversarial opponents: efficient algorithms and fundamental limits](https://arxiv.org/abs/2203.06803) `liu2022markov` — arXiv 2022 [C]（被引 1×）

**Mean-field / risk-averse / bounded-rationality 鲁棒均衡**
10. [Robust Cooperative MARL: Mean-Field Type Game Perspective](https://proceedings.mlr.press/v242/zaman24a.html) `zaman2024robust` — L4DC 2024, Başar [M][B]
11. [Tractable Equilibrium Computation via Risk Aversion](https://arxiv.org/abs/2406.14156) `mazumdar2024tractable` — arXiv 2024 [B]
12. Behavioral Economics Approach to Principled MARL `mazumdar2024behavioral` — NeurIPS'24 WS [B] ｜链接待补
13. [Provably Convergent Actor-Critic in Risk-averse MARL](https://arxiv.org/abs/2602.12386) `zhang2026provably` — arXiv 2026 [B]
14. [Robust Mean-Field Games with Risk Aversion and Bounded Rationality](https://arxiv.org/abs/2602.13353) — arXiv 2026, Tsiotras 组 [W]
182. Robust and diverse multi-agent learning via rational policy gradient `lauffer2026robust` — NeurIPS 2026 [C]（被引 1×）｜链接待补
186. Adversarial policy gradient for alternating Markov games `gao2018adversarial` — 2014 [C]（被引 1×）｜链接待补

**其他模型不确定性 / 估计 / 评估方法**
15. Multi-Agent Robust Policy Evaluation via Primal-Dual Online Time-Averaging `chen2025multi` — Sci China IS 2025 [B] ｜链接待补
16. [Robustness to Multi-Modal Env Uncertainty via Curriculum](https://arxiv.org/abs/2310.08746) `agrawal2023robustness` — arXiv 2023, Furong Huang [B]
17. [Adaptive Robust Estimator for MARL](https://arxiv.org/abs/2603.21574) `li2026adaptive` — arXiv 2026 [B]
18. Distributed Primal-Dual for Constrained MARL `kahe2026distributed` — IEEE TAC 2026 [B] ｜链接待补
19. [Scalable Robust MARL for Model Uncertainty](https://ieeexplore.ieee.org/abstract/document/10383458) — CDC 2023 [M]
20. [Data-Driven Robust MARL](https://ieeexplore.ieee.org/abstract/document/9943500) — MLSP 2022, Shaofeng Zou [M]
22. [Towards Robust MARL](https://ojs.aaai.org/index.php/AAAI-SS/article/view/31222) — AAAI-SS 2024, Aritra Mitra [M]
23. [Robust MARL via Bayesian Distributional Value Estimation](https://www.sciencedirect.com/science/article/pii/S0031320323006155) — Pattern Recognition 2024 [M]
24. [Robust MARL Driven by Correlated Equilibrium](https://openreview.net/forum?id=JvPsKam58LX) — rej. ICLR 2021, Jun Wang [M]
25. [Restless and Uncertain: Robust Policies for Restless Bandits](https://proceedings.mlr.press/v180/killian22a.html) — UAI 2022 [M]
26. [Robust Multi-agent Counterfactual Prediction](https://proceedings.neurips.cc/paper/2019/hash/fc9b003bb003a298c2ad0d05e4342bdc-Abstract.html) — NeurIPS 2019 [M]
27. [GOV-REK: Governed Reward Engineering Kernels](https://arxiv.org/abs/2404.01131) — AAMAS 2024（奖励设计）[M]

**跨类重复收录（主类在他节，此处再列）**
43. [Robust MARL via Minimax DDPG (M3DDPG)](https://ojs.aaai.org/index.php/AAAI/article/view/4327) — AAAI 2019, Fei Fang ★ [M]（主类 §3；此处归 §1 minimax 环境）
93. Sample-Efficient Robust Offline Self-Play (model-based) `li2025sample` — 2025 ⚠️ [B]（主类 §7；DRMG 不确定集）｜链接待补
123. [Distributionally Robust MARL for Intelligent Traffic Control](https://arxiv.org/abs/2512.18558) `pei2025distributionally` — arXiv 2025 [B]（主类 §9c）
126. [Distributionally Robust MARL for Dynamic Chute Mapping](https://arxiv.org/abs/2503.09755) `liu2025distributionally` — arXiv 2025 (Amazon) [M][B]（主类 §9c）

**小计：本节主类 32（1–27 + 150/159/182/186/190）｜跨类重复收录 4｜合 36**

---

## §2 状态 / 观测扰动

28. [Robust MARL with State Uncertainty](https://arxiv.org/abs/2307.16212) `herobust`/`he2023robust` — TMLR 2023, Sihong He [M][B] ★
29. [What is the Solution for State-Adversarial MARL?](https://arxiv.org/abs/2212.02705) `han2022solution` — TMLR 2024, Fei Miao [M][B]
30. [Robust MARL via Adversarial Regularization](https://proceedings.neurips.cc/paper_files/paper/2023/hash/d6f8517fceeca1e2cd61721dff786c14-Abstract-Conference.html) `bukharin2023robust` — NeurIPS 2023 [M][B] ｜跨 §3
31. [MIR2: Mutual Information Regularization](https://ieeexplore.ieee.org/abstract/document/11074764) `li2023mir2`/`li2025robust` — TNNLS 2025 [M][B]
32. [Enhancing Robustness of QMIX vs State-Adversarial Attacks](https://www.sciencedirect.com/science/article/abs/pii/S0925231223013140) `guo2024enhancing` — Neurocomputing 2024 [B]
33. Robust Training in MADRL against Optimal Adversary `guo2025robust` — TSMC 2025 [B] ｜链接待补
34. [RoMFAC: Robust Mean-Field Actor-Critic vs State Perturbations](https://arxiv.org/abs/2205.07229) — arXiv 2023, Ziyuan Zhou [M]
35. [Fault-Tolerant MARL for CAVs under Observation Perturbations](https://arxiv.org/abs/2511.23193) `shi2025fault` — arXiv 2025 [B] ｜跨 §5
36. Robustness via Temporal Consistency Regularization (self-distillation) `chen2026enhancing` — KBS 2026 [B] ｜链接待补
37. [Rainbow Delay Compensation: MARL for Delayed Observation](https://arxiv.org/abs/2505.03586) `fu2025rainbow` — arXiv 2025 [B]
38. [Tackling Uncertainties via Agent Termination Dynamics](https://arxiv.org/abs/2501.12061) `hazra2025tackling` — arXiv 2025 [B] ｜跨 §5
39. [Local Advantage Actor-Critic for Robust MA Deep RL](https://ieeexplore.ieee.org/abstract/document/9620607) — MRS 2021, Amato [M]
40. [Exploiting Local Observations for Robust Robot Learning](https://arxiv.org/abs/2309.14792) — arXiv 2023/25, Finland [M]
41. [Robust MARL against Adversaries on Observation](https://openreview.net/forum?id=eExA3Mk0Dxp) — rej. ICLR 2023, Nanjing [M]
42. [Attention-Enhanced MARL vs Observation Perturbations (Volt-VAR)](https://ieeexplore.ieee.org/abstract/document/10587051) — T-Smart Grid 2024 [M] ｜跨 §9
153. [Safe and robust MARL for connected autonomous vehicles under state perturbations](https://arxiv.org/abs/2309.11057) `zhang2023safe` — arXiv 2023 [C]（被引 5×）★ ｜跨 §9（=#106 早期版/同线）
176. [Less is more: robust robot learning via partially observable MARL](https://arxiv.org/abs/2309.1479) `zhao2023less` — arXiv 2023 [C]（被引 1×）

**跨类重复收录（主类在他节，此处再列）**
98. [Robustness Testing for MARL: State Perturbations on Critical Agents](https://arxiv.org/abs/2306.06136) — arXiv 2023, Ziyuan Zhou [M]（主类 §8；亦跨 §3）
106. [Safety-Guaranteed Robust MARL w/ Hierarchical Control for CAVs](https://arxiv.org/abs/2309.11057) `zhang2025safety` — ICRA 2025 [M][B]（主类 §9a）
114. Robust Voltage Control via Safe DRL vs State Perturbations `tian2025robust` — PCMP 2025 [B]（主类 §9b）｜链接待补

**小计：本节主类 17（28–42 + 153/176）｜跨类重复收录 3｜合 20**

---

## §3 对抗攻击 与 对抗训练

**对抗训练 / minimax 防御**
43. [Robust MARL via Minimax Deep Deterministic Policy Gradient (M3DDPG)](https://ojs.aaai.org/index.php/AAAI/article/view/4327) — AAAI 2019, Fei Fang ★ [M] ｜跨 §1
55. [Co-Evolving Complexity: Adversarial MARL Curricula](https://arxiv.org/abs/2509.03771) `hill2025co` — arXiv 2025 [B]
56. [Heterogeneous MA Adversarial RL in IsaacLab](https://arxiv.org/abs/2510.01264) `peterson2025framework` — arXiv 2025 [B]
57. [Robust MA Coordination via Evolutionary Auxiliary Adversarial Attackers](https://ojs.aaai.org/index.php/AAAI/article/view/26388) — AAAI 2023 [M]
58. [Adversarial DRL for Robust MA Autonomous Driving Policies](https://ieeexplore.ieee.org/abstract/document/10043282) — APSEC 2022 [M] ｜跨 §9
147. [ROMAX: Certifiably robust deep MARL via convex relaxation](https://arxiv.org/abs/2109.06795) `sun2022romax` — ICRA 2022 [C]（被引 10×）★
172. Robust reward-free actor-critic for cooperative MARL `lin2024reward` — IEEE TNNLS 2024 [C]（被引 1×）｜链接待补
174. Robust multi-agent Q-learning in cooperative games with adversaries `nisioti2021robust` — AAAI 2021 [C]（被引 1×）｜链接待补

**对抗攻击（policy / action / minority-influence / black-box）**
44. [Wolfpack Adversarial Attack for Robust MARL](https://arxiv.org/abs/2502.02844) `lee2025wolfpack` — ICML 2025 [M][B]
45. [Interaction-Breaking Adversarial Learning Framework for Robust MARL](https://arxiv.org/abs/2605.18024) — ICML 2026, Han 组 [W]
46. [Robust MARL with Stochastic Adversary](https://openreview.net/forum?id=bnhFueOeav) `zhou2025robust` — ICML 2025 [M][B]
47. Camouflage Adversarial Attacks on MARL `lu2025camouflage` — TSP 2025 [B] ｜链接待补
48. [Constrained Black-Box Attacks against MARL](https://arxiv.org/abs/2508.09275) `andam2025constrained` — arXiv 2025 [B]
49. Black-Box Adversarial Robustness Testing w/ Partial Observation `zhang2025black` — ICPADS 2025 [B] ｜跨 §8 ｜链接待补
50. [Finding the Weakest Link: Attack vs MA Communications](https://arxiv.org/abs/2605.13170) `standen2026finding` — arXiv 2026 [B] ｜跨 §4
51. Adversarial Attacks on MADRL in Continuous Action Space `zhou2024adversarial` — TSMC 2024 [B] ｜链接待补
152. [Attacking cooperative MARL by adversarial minority influence](https://arxiv.org/abs/2302.03322) `li2023attacking` — arXiv 2023 [C]（被引 6×）★
157. [Efficient adversarial attacks on online MARL](https://arxiv.org/abs/2307.07670) `liu2023efficient` — NeurIPS 2023 [C]（被引 3×）

**投毒 / 后门 / 安全分析（reward & data poisoning, backdoor）**
54. [Reward-Poisoning Attacks on Offline MARL](https://ojs.aaai.org/index.php/AAAI/article/view/26240) — AAAI 2023, Young Wu 等 [W] ｜跨 §7
158. One4all: manipulate one agent to poison cooperative MARL `zheng2023one4all` — 2023 [C]（被引 3×）｜链接待补
162. MARNet: backdoor attacks against cooperative MARL `chen2022marnet` — 2022 [C]（被引 1×）｜链接待补
164. Security analysis of poisoning attacks against MARL `xie2021security` — 2021 [C]（被引 1×）｜链接待补
192. Data poisoning to fake a Nash equilibria for Markov games `wu2024data` — AAAI 2024 [C]（被引 1×）｜链接待补
181. [Distributed robust optimization for MAS with guaranteed finite-time convergence](https://arxiv.org/abs/2309.01201) `wu2023distributed` — arXiv 2023 [C]（被引 1×）⟂背景

**应用导向的对抗攻击**（亦可见 §9）
52. [Adversarial DRL Attacks on MA Cooperative Driving](https://doi.org/10.1049/itr2.70066) `alzubaidi2025adversarial` — IET ITS 2025 [B] ｜跨 §9
53. [Action-Oriented Adversarial Attacks on Trajectory Prediction via MARL](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5348784) `zhao5348784action` — SSRN ⚠️ [B] ｜跨 §9
59. [On the Robustness of Cooperative MARL](https://ieeexplore.ieee.org/abstract/document/9283830) — SPW 2020 [M] ｜跨 §8

**跨类重复收录（主类在他节，此处再列）**
30. [Robust MARL via Adversarial Regularization](https://proceedings.neurips.cc/paper_files/paper/2023/hash/d6f8517fceeca1e2cd61721dff786c14-Abstract-Conference.html) `bukharin2023robust` — NeurIPS 2023 [M][B]（主类 §2；state+action 对抗训练）
63. [Mis-spoke or Mis-lead: Robustness in Communicative MARL](https://arxiv.org/abs/2108.03803) — AAMAS 2022, Bo An [M]（主类 §4）
85. [Resilient MARL with Adversarial Value Decomposition](https://ojs.aaai.org/index.php/AAAI/article/view/17348) — AAAI 2021, TU Munich [M]（主类 §5）
87. [Evo-MARL: Co-Evolutionary MARL for Internalized Safety](https://arxiv.org/abs/2508.03864) `pan2025evo` — arXiv 2025 [B]（主类 §6）
88. [AdvEvo-MARL: Safety via Adversarial Co-Evolution](https://arxiv.org/abs/2510.01586) `pan2025advevo` — arXiv 2025 [B]（主类 §6）
95. [StarCraft+: Benchmarking MA Algorithms in Adversary Paradigm](https://arxiv.org/abs/2512.16444) `li2025starcraft+` — arXiv 2025 [B]（主类 §8）
98. [Robustness Testing for MARL: State Perturbations on Critical Agents](https://arxiv.org/abs/2306.06136) — arXiv 2023, Ziyuan Zhou [M]（主类 §8）
99. [Towards Comprehensive Testing on Robustness of Cooperative MARL](https://openaccess.thecvf.com/content/CVPR2022W/ArtOfRobust/html/Guo_Towards_Comprehensive_Testing_on_the_Robustness_of_Cooperative_Multi-Agent_Reinforcement_CVPRW_2022_paper.html) — CVPRW 2022 [M]（主类 §8）
103. [Pilot Study of Observation Poisoning on Selective Reincarnation in MARL](https://link.springer.com/article/10.1007/s11063-024-11625-w) — Neural Proc. Letters 2024 [M]（主类 §8）
110. [Robust MARL vs Adversarial Attacks for Cooperative Self-Driving](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/rsn2.70033) `wang2025robust` — IET RSN 2025 [M][B]（主类 §9a）
119. [Resilience Enhancement of MARL Demand Response vs Adversarial Attacks](https://www.sciencedirect.com/science/article/pii/S0306261922009850) — Applied Energy 2022 [M]（主类 §9b）
120. [MA DRL for Robustness of EV Charging vs Cyber-Attacks](https://www.sciencedirect.com/science/article/pii/S0360544224024435) — Energy 2024 [M]（主类 §9b）
135. [Robust MARL via Adversarial Domain Randomization for Dual-UAV](https://ieeexplore.ieee.org/abstract/document/10225713) — TIV 2024 (Tongji) [M]（主类 §9d）
173. Robust lane change decision for AVs in mixed traffic: safety-aware MA adversarial RL `wang2022lane` — Transportation Research 2022 [C]（主类 §9a）｜链接待补

**小计：本节主类 27（43–59 + 147/152/157/158/162/164/172/174/181/192）｜跨类重复收录 14｜合 41**

---

## §4 通信鲁棒（noise + 攻击 + certified）

**Certified / message-certification 防御**
61. [Certifiably Robust Policy Learning vs Adversarial Communication](https://openreview.net/forum?id=dCOL0inGl3e) — ICLR 2023, Furong Huang ★ [M]
62. [Certified Policy Smoothing for Cooperative MARL](https://ojs.aaai.org/index.php/AAAI/article/view/26756) — AAAI 2023 [M]
65. [Robust Cooperative MARL via Multi-View Message Certification](https://link.springer.com/article/10.1007/s11432-023-3853-y) `yuan2024cooperative` — Sci China IS 2024 [M]（= xlsx 重复 ID 160）

**主动防御 / message filtering / 信息瓶颈**
60. [Robust Communicative MARL with Active Defense (ADMAC)](https://ojs.aaai.org/index.php/AAAI/article/view/29708) `yu2024robust` — AAAI 2024 [M][B]
64. [Robust MA Communication with Graph Information Bottleneck](https://ieeexplore.ieee.org/abstract/document/10334015) — TPAMI 2024, Bo An [M]
66. [Succinct & Robust MA Communication w/ Temporal Message Control](https://proceedings.neurips.cc/paper_files/paper/2020/hash/c82b013313066e0702d58dc70db033ca-Abstract.html) — NeurIPS 2020 [M]
68. [Robust MA Comm via Decentralization-Oriented Adversarial Training](https://arxiv.org/abs/2504.21278) `ma2025robust` — arXiv 2025 [B]
148. [Gaussian-process based message filtering for robust MA cooperation under adversarial communication](https://arxiv.org/abs/2012.00508) `mitchell2020gaussian` — ICLR 2020 [C]（被引 9×）★
169. Communication-robust MA learning by adaptable auxiliary adversary generation `yuan2024communication` — Frontiers Comp Sci 2024 [C]（被引 1×）｜链接待补

**通信攻击 / 涌现对抗通信**
63. [Mis-spoke or Mis-lead: Robustness in Communicative MARL](https://arxiv.org/abs/2108.03803) — AAMAS 2022, Bo An [M] ｜跨 §3
149. [Adversarial Attacks on Multi-Agent Communication](https://arxiv.org/abs/2101.06560) `tu2021adversarial` — ICCV 2021 [C]（被引 9×）★
168. The emergence of adversarial communication in MARL `blumenkamp2021emergence` — CoRL 2020 [C]（被引 1×）｜链接待补

**噪声信道 / 延迟补偿 / 协调-通信**
67. Robust and Efficient Communication in MARL `liu2026robust` — Chaos 2026 [B] ｜链接待补
69. [Robust Multi-UAV: Noise-Resilient Comm + Attention](https://arxiv.org/abs/2503.02913) `zhao2025towards` — arXiv 2025 [B] ｜跨 §9
70. [DCT-MARL: Dynamic Communication Topology for Platoon](https://arxiv.org/abs/2508.12633) `xu2025dct` — arXiv 2025 [B] ｜跨 §9
71. [Effective Communications: Joint Learning over Noisy Channels](https://ieeexplore.ieee.org/abstract/document/9466501) — Journal 2021, UK [M]
72. [Robust MARL with Social Empowerment](https://arxiv.org/abs/2012.08255) — arXiv 2020 [M]
166. Safe MARL for wireless applications against adversarial communications `lv2024safe` — IEEE Transactions 2024 [C]（被引 1×）｜链接待补
183. Adaptive frequency and delay compensation in MAS `wang2024adaptive` — 2024 [C]（被引 1×）｜链接待补

**跨类重复收录（主类在他节，此处再列）**
50. [Finding the Weakest Link: Attack vs MA Communications](https://arxiv.org/abs/2605.13170) `standen2026finding` — arXiv 2026 [B]（主类 §3）
90. Collaborative Comm for Edge LLM in Adversarial Networks (MARL Stackelberg) `hong2025collaborative` — IoT 2025 [B]（主类 §6）｜链接待补
107. [Robust & Safe MARL Framework w/ Comm for AVs](https://arxiv.org/abs/2506.00982) `smith2025robust` — arXiv 2025 [M][B]（主类 §9a）

**小计：本节主类 19（60–72 + 148/149/166/168/169/183）｜跨类重复收录 3｜合 22**

---

## §5 队友不可信 / Byzantine / Fault-Tolerant / Trust（多智能体独有）★

**Byzantine-robust cooperative MARL（Bayesian game / unknown adversary）**
73. [Byzantine Robust Cooperative MARL as a Bayesian Game](https://arxiv.org/abs/2305.12872) `li2024byzantine` — ICLR 2024 [M][B]
74. [Bayesian Robust Cooperative MARL Against Unknown Adversaries](https://openreview.net/forum?id=ydVFxjjtbA) `kazaribayesian` — ICLR 2026 ★ [B][W]
75. IBGP: Imperfect Byzantine Generals for Zero-Shot Robustness `mao2025ibgp` — AGI 2025 [B] ｜跨 §6 ｜链接待补
78. [Fully Byzantine-Resilient Distributed MA Q-Learning](https://arxiv.org/abs/2604.02791) — CDC 2026, Panagou [W]
79. [Decentralized Byzantine-Resilient MARL w/ Reward Machines](https://openreview.net/forum?id=ydVFxjjtbA) — 2025 ⚠️venue [W]

**Fault-tolerant / resilient MARL（RL 主线）**
76. [Fault-Tolerant MA Learning w/ Adversarial Budget Constraints](https://arxiv.org/abs/2508.08800) `mguni2025fault` — arXiv 2025, Yaodong Yang [B]
77. Towards Fault Tolerance in MARL `shi2025towards` — TASE 2025 [B] ｜链接待补
84. Unsupervised Partner Design Enables Robust Ad-hoc Teamwork — ICML 2026 [W] ｜链接待补
85. [Resilient MARL with Adversarial Value Decomposition](https://ojs.aaai.org/index.php/AAAI/article/view/17348) — AAAI 2021, TU Munich [M] ｜跨 §3
151. Learning and testing resilience in cooperative multi-agent systems `phan2020learning` — AAMAS 2020 [C]（被引 7×）★ ｜链接待补
170. Resilient MARL with function approximation `ye2024resilient` — IEEE TAC 2024 [C]（被引 1×）｜链接待补

**Trust / 信任过滤 / 欺骗建模**
80. Trust-Based Information Filtering for Decentralized MARL (UAV) `rudzitis2025trust` — WMNC 2025 [B] ｜链接待补
81. TrustOrch: Dynamic Trust-Aware Orchestration `hu2025trustorch` — 2025 [B] ｜跨 §6 ｜链接待补
82. [Trust-MARL: On-Ramp Merging](https://arxiv.org/abs/2506.12600) `pan2025trust` — arXiv 2025 [B] ｜跨 §9
83. Modeling Trust & Deception via Werewolf Game `patel2025modeling` — 2025 ⚠️ [B] ｜链接待补
86. [Robust Multi-Agent Bandits over Undirected Graphs](https://dl.acm.org/doi/abs/10.1145/3570614) — ACM ToMACS 2022（dishonest 队友）[M]

**共识 / 分布式优化的对抗与韧性（控制论背景，相关性偏弱）**
161. Adversarial attacks in consensus-based MARL `figura2021adversarial` — ACC 2021 [C]（被引 2×）⟂背景 ｜链接待补
163. Communication-efficient and resilient distributed deep RL for MAS `yao2024communication` — 2024 [C]（被引 1×）⟂背景 ｜链接待补
167. Towards resilience for multi-agent QD-learning `xie2021resilience` — CDC 2021 [C]（被引 1×）⟂背景 ｜链接待补
171. Toward resilient MA actor-critic for distributed RL `lin2020resilient` — ACC 2020 [C]（被引 1×）⟂背景 ｜链接待补
175. An overview on multi-agent consensus under adversarial attacks `ishii2019overview` — Annual Reviews in Control 2019 [C]（被引 1×）⟂背景 ｜链接待补
177. Adaptive fault-tolerant tracking control for discrete-time MAS via RL `li2021adaptive` — 2021 [C]（被引 1×）⟂背景 ｜链接待补
178. Byzantine-resilient MA distributed optimization under redundancy `zhai2025byzantine` — IEEE TCNS 2025 [C]（被引 1×）⟂背景 ｜链接待补
179. Distributed resilience-aware control in multi-robot networks `lee2025distributed` — CDC 2025 [C]（被引 1×）⟂背景 ｜链接待补
180. Towards a fault-tolerant multi-agent system architecture `kumar2000fault` — 2000 [C]（被引 1×）⟂背景 ｜链接待补
184. A survey on fault tolerant multi agent system `arfat2016survey` — 2016 [C]（被引 1×）⟂背景 ｜链接待补
185. On the hardness of decentralized MA policy evaluation under Byzantine attacks `fang2024hardness` — 2024 [C]（被引 1×）｜链接待补
187. Large-scale mean-field federated learning for Byzantine-robust detection/defense in IoT `sun2024large` — 2024 [C]（被引 1×）⟂背景 ｜链接待补
188. Fault-tolerant consensus of leader-following MAS with jointly connected topologies `li2023fault` — 2023 [C]（被引 1×）⟂背景 ｜链接待补
189. Byzantine-resilient multi-agent optimization `su2020byzantine` — IEEE TAC 2021 [C]（被引 1×）⟂背景 ｜链接待补
191. Fault-tolerant cooperative control of MAS: a survey `yang2020fault` — IEEE Transactions 2020 [C]（被引 1×）⟂背景 ｜链接待补
193. Resilient distributed optimization for MA cyberphysical systems `yemini2025resilient` — IEEE TAC 2025 [C]（被引 1×）⟂背景 ｜链接待补

**跨类重复收录（主类在他节，此处再列）**
35. [Fault-Tolerant MARL for CAVs under Observation Perturbations](https://arxiv.org/abs/2511.23193) `shi2025fault` — arXiv 2025 [B]（主类 §2）
38. [Tackling Uncertainties via Agent Termination Dynamics](https://arxiv.org/abs/2501.12061) `hazra2025tackling` — arXiv 2025 [B]（主类 §2）
96. [Measuring Robustness of MARL under Partial Agent Failure](https://doi.org/10.1145/3759355.3759373) `barta2025measuring` — FAIR 2025 [B]（主类 §8）
97. [Empirical Study on Robustness and Resilience in Cooperative MARL](https://arxiv.org/abs/2510.11824) — NeurIPS 2025, Bo An/Yaodong Yang 组 [W]（主类 §8）

**小计：本节主类 32（73–86 + 151/161/163/167/170/171/175/177–180/184/185/187–189/191/193）｜跨类重复收录 4｜合 36**

---

## §6 LLM 多智能体安全 / 鲁棒（全新前沿）★ 差异化卖点

87. [Evo-MARL: Co-Evolutionary MARL for Internalized Safety](https://arxiv.org/abs/2508.03864) `pan2025evo` — arXiv 2025 [B] ｜跨 §3
88. [AdvEvo-MARL: Safety via Adversarial Co-Evolution](https://arxiv.org/abs/2510.01586) `pan2025advevo` — arXiv 2025 [B] ｜跨 §3
89. Safe MARL with Natural Language Constraints `wang2026safe` — AAAI 2026 [B] ｜链接待补
90. Collaborative Comm for Edge LLM in Adversarial Networks (MARL Stackelberg) `hong2025collaborative` — IoT 2025 [B] ｜跨 §4 ｜链接待补
91. [LLM-based MARL: Current and Future Directions](https://arxiv.org/abs/2405.11106) — arXiv 2024（短综述）[M]

**跨类重复收录（主类在他节，此处再列）**
75. IBGP: Imperfect Byzantine Generals for Zero-Shot Robustness `mao2025ibgp` — AGI 2025 [B]（主类 §5）｜链接待补
81. TrustOrch: Dynamic Trust-Aware Orchestration `hu2025trustorch` — 2025 [B]（主类 §5）｜链接待补

**小计：本节主类 5（87–91）｜跨类重复收录 2｜合 7**

---

## §7 Offline / 分布偏移鲁棒（新增子领域）

92. Partial Action Replacement: Distribution Shift in Offline MARL `jin2026partial` — AAAI 2026 [B] ｜链接待补
93. Sample-Efficient Robust Offline Self-Play (model-based) `li2025sample` — 2025 ⚠️ [B] ｜跨 §1 ｜链接待补

**跨类重复收录（主类在他节，此处再列）**
54. [Reward-Poisoning Attacks on Offline MARL](https://ojs.aaai.org/index.php/AAAI/article/view/26240) — AAAI 2023, Young Wu 等 [W]（主类 §3；offline reward 扰动）

**小计：本节主类 2（92–93）｜跨类重复收录 1｜合 3**

---

## §8 Benchmark / 测评

**统一 benchmark / library**
94. [Robust Gymnasium: Unified Modular Benchmark for Robust RL](https://arxiv.org/abs/2502.19652) — ICLR 2025, Gu & Shi ★ [M]
95. [StarCraft+: Benchmarking MA Algorithms in Adversary Paradigm](https://arxiv.org/abs/2512.16444) `li2025starcraft+` — arXiv 2025 [B] ｜跨 §3
100. [SMACv2: Improved Benchmark for Cooperative MARL](https://proceedings.neurips.cc/paper_files/paper/2023/hash/764c18ad230f9e7bf6a77ffc2312c55e-Abstract-Datasets_and_Benchmarks.html) — NeurIPS 2023, Whiteson [M]
101. [MATE: Benchmarking MARL in Distributed Target Coverage Control](https://proceedings.neurips.cc/paper_files/paper/2022/hash/b2a1c152f14a4b842a9ddb3bd84c62a1-Abstract-Datasets_and_Benchmarks.html) — NeurIPS 2022, Yaodong Yang [M]
102. [Mava: Research Library for Distributed MARL in JAX](https://arxiv.org/abs/2107.01460) — arXiv 2021 [M]

**鲁棒性测评 / 失效与扰动测试**
96. [Measuring Robustness of MARL under Partial Agent Failure](https://doi.org/10.1145/3759355.3759373) `barta2025measuring` — FAIR 2025 [B] ｜跨 §5
97. [Empirical Study on Robustness and Resilience in Cooperative MARL](https://arxiv.org/abs/2510.11824) — NeurIPS 2025, Bo An/Yaodong Yang 组 [W] ｜跨 §5
98. [Robustness Testing for MARL: State Perturbations on Critical Agents](https://arxiv.org/abs/2306.06136) — arXiv 2023, Ziyuan Zhou [M] ｜跨 §2,§3
99. [Towards Comprehensive Testing on Robustness of Cooperative MARL](https://openaccess.thecvf.com/content/CVPR2022W/ArtOfRobust/html/Guo_Towards_Comprehensive_Testing_on_the_Robustness_of_Cooperative_Multi-Agent_Reinforcement_CVPRW_2022_paper.html) — CVPRW 2022 [M] ｜跨 §3
103. [Pilot Study of Observation Poisoning on Selective Reincarnation in MARL](https://link.springer.com/article/10.1007/s11063-024-11625-w) — Neural Proc. Letters 2024 [M] ｜跨 §3
155. [Evaluating robustness of cooperative MARL: a model-based approach](https://arxiv.org/abs/2202.03558) `pham2022evaluating` — 2022 [C]（被引 5×）★
165. Robustness evaluation of MARL algorithms using GNAS `zhang2023robustness` — 2023 [C]（被引 1×）｜链接待补

**应用域的鲁棒性分析**（亦可见 §9）
104. [MARL for Traffic Signal Control: Algorithms and Robustness Analysis](https://ieeexplore.ieee.org/abstract/document/9294623) — ITSC 2020, Monash [M] ｜跨 §9
105. [Evaluating Robustness of DRL for Autonomous Policies in MA Urban Driving](https://ieeexplore.ieee.org/abstract/document/10062456) — QRS 2023 [M] ｜跨 §9

**跨类重复收录（主类在他节，此处再列）**
49. Black-Box Adversarial Robustness Testing w/ Partial Observation `zhang2025black` — ICPADS 2025 [B]（主类 §3）｜链接待补
59. [On the Robustness of Cooperative MARL](https://ieeexplore.ieee.org/abstract/document/9283830) — SPW 2020, Sai Qian Zhang [M]（主类 §3）

**小计：本节主类 14（94–105 + 155/165）｜跨类重复收录 2｜合 16**

---

## §9 安全+鲁棒 & 应用

> 应用导向，按场景分子表。

### 9a. CAV / 自动驾驶（多为 Fei Miao 组）
106. [Safety-Guaranteed Robust MARL w/ Hierarchical Control for CAVs](https://arxiv.org/abs/2309.11057) `zhang2025safety` — ICRA 2025 [M][B] ｜跨 §2
107. [Robust & Safe MARL Framework w/ Comm for AVs](https://arxiv.org/abs/2506.00982) `smith2025robust` — arXiv 2025 [M][B] ｜跨 §4
108. 5G-Enabled Safe & Robust Deep MARL for CAV `miao20255g` — 2025 ⚠️ [B] ｜链接待补
109. Robustness-Enhanced Cooperative ACC via Joint MARL `dong2025robustness` — Neurocomputing 2025 [B] ｜链接待补
110. [Robust MARL vs Adversarial Attacks for Cooperative Self-Driving](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/rsn2.70033) `wang2025robust` — IET RSN 2025 [M][B] ｜跨 §3
111. [Transferring MARL Policies for Autonomous Driving Sim-to-Real](https://ieeexplore.ieee.org/abstract/document/9981319) — IROS 2022 [M]
112. [Safe Robust MARL with Neural CBF & Safety Attention](https://www.sciencedirect.com/science/article/abs/pii/S0020025524014816) — Information Sciences 2024 [B]（CBF）
154. [A robust and constrained MARL EV rebalancing method in AMoD systems](https://arxiv.org/abs/2209.08230) `he2022constrained` — IROS 2022 [C]（被引 5×）★
173. Robust lane change decision for AVs in mixed traffic: safety-aware MA adversarial RL `wang2022lane` — Transportation Research 2022 [C]（被引 1×）｜链接待补 ｜跨 §3

### 9b. 电网 / 能源
113. Distributed Robust Dispatch for Networked Microgrids (Coalition Game + Safe MARL) `pu2025distributed` — TII 2025 [B] ｜链接待补
114. Robust Voltage Control via Safe DRL vs State Perturbations `tian2025robust` — PCMP 2025 [B] ｜跨 §2 ｜链接待补
115. [GNN-Based MARL for Active Voltage Control: Topology Robustness](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5960743) `eze5960743graph` — SSRN ⚠️ [B]
116. [Uncertainty-Aware Knowledge Transformers for P2P Energy Trading](https://arxiv.org/abs/2507.16796) `shah2025uncertainty` — arXiv 2025 [B]
117. Combating Uncertainties in Smart Grid: MARL w/ Imperfect State Info `ghasemi2024combating` — IoT-J 2024 [B] ｜链接待补
118. [Robust Regional Coordination of Inverter-Based Volt/Var Control](https://ieeexplore.ieee.org/abstract/document/9511622) — T-Smart Grid 2021 [M]
119. [Resilience Enhancement of MARL Demand Response vs Adversarial Attacks](https://www.sciencedirect.com/science/article/pii/S0306261922009850) — Applied Energy 2022 [M] ｜跨 §3
120. [MA DRL for Robustness of EV Charging vs Cyber-Attacks](https://www.sciencedirect.com/science/article/pii/S0360544224024435) — Energy 2024 [M] ｜跨 §3
121. [Model-Free MARL for Robust Power Management in Micro-Grid](https://ieeexplore.ieee.org/abstract/document/10406423) — IAS 2023 [M]
122. [Optimal Bi-Level Bidding/Dispatching via Distributed Robust MA DRL](https://ieeexplore.ieee.org/abstract/document/9745992) — Power System 2022 [M]

### 9c. 交通 / 路网 / 物流
123. [Distributionally Robust MARL for Intelligent Traffic Control](https://arxiv.org/abs/2512.18558) `pei2025distributionally` — arXiv 2025 [B] ｜跨 §1
124. [Decentralized MARL w/ VLC for Robust Urban Traffic Signal](https://doi.org/10.3390/su172210056) `vieira2025decentralized` — Sustainability 2025 [B]
125. Robust Real-Time Control for High-Frequency Bus Service `low2026robust` — JITS 2026 [B] ｜链接待补
126. [Distributionally Robust MARL for Dynamic Chute Mapping](https://arxiv.org/abs/2503.09755) `liu2025distributionally` — arXiv 2025 (Amazon) [M][B] ｜跨 §1
127. [Robust & Scalable Routing with MA Deep RL for MANETs](https://arxiv.org/abs/2101.03273) — arXiv 2021 (Boeing) [M]
128. [DeepCQ+: Robust & Scalable Routing with MA Deep RL](https://ieeexplore.ieee.org/abstract/document/9652948) — 2021 [M]
129. [Robust Multi-vehicle Routing for Last-Mile Logistics](https://link.springer.com/chapter/10.1007/978-981-97-7244-5_41) — WBD 2024 [M]
130. [Coordinated Robust Real-Time Control for Sewer Overflow & Urban Flooding](https://www.sciencedirect.com/science/article/pii/S0043135422014439) — Water Research 2023 [M]

### 9d. UAV / USV / 机器人 / 其他
131. ROMUC: Robust Policy Learning for Multi-USV Cooperative Tasks `li2025romuc` — ACAIT 2025 [B] ｜链接待补
132. [Robust UAV Wireless Comm via MARL to Optimize Coverage](https://doi.org/10.3390/drones9050321) `khan2025robust` — Drones 2025 [B]
133. Robust Multi-Agent Path Planning in Dynamic Environments `le2025robust` — 2025 ⚠️ [B] ｜链接待补
134. Robust Control of Water Distribution Networks (MA Curriculum) `amarnath2026robust` — Water Res. Mgmt 2026 [B] ｜链接待补
135. [Robust MARL via Adversarial Domain Randomization for Dual-UAV](https://ieeexplore.ieee.org/abstract/document/10225713) — TIV 2024 (Tongji) [M] ｜跨 §3
136. [Robust MA Coverage Path Planning for UAVs in 3D](https://ieeexplore.ieee.org/abstract/document/10354596) — ROBIO 2023 [M]
137. [Mobility-as-a-Resilience-Service in IoRT via Robust MA DRL](https://ieeexplore.ieee.org/abstract/document/10855408) — J-IoT 2025 [M]
138. [Robust MA Federated RL for Task Offloading](https://link.springer.com/chapter/10.1007/978-981-96-2409-6_21) — Springer 2023 [M]
139. [Robust MARL for Noisy Environments](https://link.springer.com/article/10.1007/s12083-021-01133-2) — Journal 2022 (Hunan U) [M]
140. [Robust MA Patrolling Strategies Using RL](https://link.springer.com/chapter/10.1007/978-3-319-12970-9_17) — non-top venue [M]
141. [Air Combat Autonomous Maneuver via Robust MARL](https://ieeexplore.ieee.org/abstract/document/9264567) — ICCA 2020 [M]

### 9e. 网络安全 / CPS
142. RMAAC: Robust MA Actor-Critic for Malware Defense in Social IoT `shen2025rmaac` — TDSC 2025 [B] ｜链接待补
143. MARL for Cyber Defence: Transferability & Scalability `thomas2026multi` — Applied AI Letters 2026 [B] ｜链接待补
144. Towards Robust Autonomous Cyber Defence Agents (Hybrid AI) `holz2025towards` — NetSoft 2025 [B] ｜链接待补
145. [Hierarchical Adversarially-Resilient MARL for CPS Security](https://ojs.aaai.org/index.php/AAAI-SS/article/view/35403) `alqithami2025hierarchical` — AAAI Symp 2025 [B] ｜链接待核实

### 9f. 金融
146. Meta-Adaptive Risk-Aware MARL for Portfolio Management (MARS) `chen2026mars` — AAAI 2026 [B] ｜链接待补

### 9g. 跨类重复收录（主类在他节，此处再列）
42. [Attention-Enhanced MARL vs Observation Perturbations (Volt-VAR)](https://ieeexplore.ieee.org/abstract/document/10587051) — T-Smart Grid 2024 [M]（主类 §2；电网应用）
52. [Adversarial DRL Attacks on MA Cooperative Driving](https://doi.org/10.1049/itr2.70066) `alzubaidi2025adversarial` — IET ITS 2025 [B]（主类 §3；CAV）
53. [Action-Oriented Adversarial Attacks on Trajectory Prediction via MARL](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5348784) `zhao5348784action` — SSRN ⚠️ [B]（主类 §3；CAV）
58. [Adversarial DRL for Robust MA Autonomous Driving Policies](https://ieeexplore.ieee.org/abstract/document/10043282) — APSEC 2022 [M]（主类 §3；CAV）
69. [Robust Multi-UAV: Noise-Resilient Comm + Attention](https://arxiv.org/abs/2503.02913) `zhao2025towards` — arXiv 2025 [B]（主类 §4；UAV）
70. [DCT-MARL: Dynamic Communication Topology for Platoon](https://arxiv.org/abs/2508.12633) `xu2025dct` — arXiv 2025 [B]（主类 §4；车队）
82. [Trust-MARL: On-Ramp Merging](https://arxiv.org/abs/2506.12600) `pan2025trust` — arXiv 2025 [B]（主类 §5；CAV）
104. [MARL for Traffic Signal Control: Algorithms and Robustness Analysis](https://ieeexplore.ieee.org/abstract/document/9294623) — ITSC 2020, Monash [M]（主类 §8；交通）
105. [Evaluating Robustness of DRL for Autonomous Policies in MA Urban Driving](https://ieeexplore.ieee.org/abstract/document/10062456) — QRS 2023 [M]（主类 §8；CAV）
153. [Safe and robust MARL for connected autonomous vehicles under state perturbations](https://arxiv.org/abs/2309.11057) `zhang2023safe` — arXiv 2023 [C]（主类 §2；CAV）★

**小计：本节主类 43（106–146 + 154/173 ｜ 9a 9 · 9b 10 · 9c 8 · 9d 11 · 9e 4 · 9f 1）｜跨类重复收录 10（9g）｜合 53**

---

## §10 竞品 / 邻近综述（positioning 必读，不计入语料）

- Robust RL: Methods, Benchmarks and Challenges `gu2026robust` — 2026（单智能体）｜链接待补
- Towards Robust Agents: Survey of Adversarial Attacks & Defenses in Deep RL `mohan2026towards` — IEEE Access 2026（单智能体）｜链接待补
- [Comprehensive Survey on MA Cooperative Decision-Making](https://arxiv.org/abs/2503.13415) `jin2025comprehensive` — arXiv 2025（泛 MARL）
- MARL: Methods, Trustworthiness, Applications in IV `zhou2024multiagent` — IEEE TIV 2024 ｜链接待补
- [MARL in Cybersecurity](https://arxiv.org/abs/2505.19837) `landolt2025multi` — arXiv 2025
- [Beyond Robustness: Taxonomy of Resilient Multi-Robot Systems](https://arxiv.org/abs/2109.12343) `prorok2021beyond` — arXiv 2021
- ⭐ [Adversarial ML Attacks and Defences in MARL](https://dl.acm.org/doi/10.1145/3708320) `standen2023adversarial`（语料 ID 156；arXiv 2023 SoK 版 [2301.04299](https://arxiv.org/abs/2301.04299)）— **ACM Computing Surveys 2025** — 迄今最接近的竞品（≈本表 §3/§4/§5）。本 survey 差异化：①覆盖更广（DRMG 理论、§6 LLM-MAS、§7 offline 均不在其范围）；②以"鲁棒性针对什么扰动"为统一 taxonomy。
- [Open Challenges in Multi-Agent Security](https://arxiv.org/abs/2505.02077) — arXiv 2025（LLM-agent 安全 position）
- [A Survey of Safe RL and Constrained MDPs: Single/Multi-Agent Safety](https://arxiv.org/abs/2505.17342) — arXiv 2025

---

## §11 背景引用（非 robust-MARL，铺垫用，不计入语料）

- **MARL 基石**：MADDPG (NeurIPS'17)、Networked Agents (ICML'18)、Stabilising Experience Replay/StarCraft (ICML'17)、FOP (ICML'21)
- **单智能体 Robust RL**：`shi2023curious`、`ding2023seeing`、`sun2024constrained`、`zhang2024distributionally`、`kitamura2025near`、`li2024towards`、`sun2024belief`、`sun2026diffusion`、`wang2025towards`、`erdem2025learning`
- **学位论文**：`zhang2025advancing`(Harvard'25)、`shi2023provable`(CMU'23)、`koruturk2026reinforcement`(VT'26)
- **He 团队 EV 应用线**（自引可选）：`he2023arobust`、`he2023data`、`he2020data`

---

## §12 已排除（原 md 标注"非 robust marl"，建议不收）

- Robust Experience Replay Sampling — 2022 Korea
- RAMARL — 2022 Norway
- Heterogeneous MARL for Unknown Environment Mapping — AAAI WS 2020
- Coordination Between Individual Agents — AAAI 2021

---

## 重新分类要点（相对 MASTER 的变化）

1. **补充语料已全部并入 §1–§9，并按 `INDEX.md`/`xlsx` 规范编号（ID 散布于 147–193）**：原 `cite-analysis-supplement` 独立段落取消，按"补充 §X"归入对应主分类。1–146 编号不变。
2. **允许一文多类、重复收录**：覆盖多个分类的文章，在主类正常列出，并在每个相关次类下设「跨类重复收录」子表（§9 为 `9g`）再列一次，标 `（主类 §X）`。共 43 条次类重复（去重前 234 条 = 去重 191 + 重复 43）。
3. **§5 内部细分**：18 篇补充文献区分「RL 主线（韧性/Byzantine MARL）」与「控制论/分布式优化背景」（标 `⟂背景`），便于撰写时分层引用或剔除。
4. **§1/§3/§4 内部按方法主题再分簇**（理论线 / mean-field-risk / 攻击 / 防御 / certified），不改编号，仅排版聚类。
5. **去重核心语料总数 = 191**（原 146 + 补充 45），占用规范 ID 1–193 中除 156（§10 SoK 综述）与 160（=#65 重复）外的 191 个；§10–§12 不计入。

| 节 | §1 | §2 | §3 | §4 | §5 | §6 | §7 | §8 | §9 | 去重合计 |
|---|---|---|---|---|---|---|---|---|---|---|
| 主类篇数 | 32 | 17 | 27 | 19 | 32 | 5 | 2 | 14 | 43 | **191** |
| 含跨类 | 36 | 20 | 41 | 22 | 36 | 7 | 3 | 16 | 53 | 234 |
