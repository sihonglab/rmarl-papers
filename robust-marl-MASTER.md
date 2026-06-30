# Robust MARL — 总表（Master List，完整枚举版）

合并去重自三份来源（归档于 `raw-data/`）：原始 `robust-marl.md`（81篇）、`robust-marl-2025H2-2026.md`（web检索9篇）、整库 `rmarl-paper-from-25-to-26.bib`（相关~80篇），并入两轮（2026-06）补充检索新增 7 篇。
**每篇一行、连续编号 1–146、可审计**。来源标记：`M`原始md / `B`bib(附key) / `W`web检索 / `C`引文分析补充。⚠️=待核实venue，★=高价值。
整理日期：2026-06-17。分类主轴：**鲁棒性针对什么扰动**。
**标题为可点击链接**（arXiv / 出版社 / DOI / SSRN）；少数无法可靠定位的标 `链接待补`。一篇可归 2+ 类的，在行尾以 `｜跨 §X` 标注（主类即所在节）。

---

## 数量核对

| 来源 | 条目 | 说明 |
|---|---|---|
| 原始 md | 81 | 其中 4 篇移入 §11 背景、4 篇移入 §12 排除 |
| bib 相关 | ~80 | 已扣 `he2023robust`×5、`shi2024breaking`×2、`zaman`×2 等内部重复 |
| web 检索（三轮） | 16 | 含两轮补充 sweep |
| 跨源重叠 | ~22 | 在多源同时出现，只计一次 |
| **核心语料（§1–§9）** | **146** | 逐条枚举，编号 1–146，与底部小计一致 |
| 另：§10 综述 9 · §11 背景/学位 若干 · §12 排除 4 | — | 不计入核心语料 |

---

## §1 环境/模型不确定性（DRMG / 理论主线）★

1. [Robust MARL with Model Uncertainty](https://proceedings.neurips.cc/paper/2020/hash/774412967f19ea61d448977ad9749078-Abstract.html) — NeurIPS 2020, Kaiqing Zhang [M]
2. [Sample-Efficient Robust MARL in Face of Environmental Uncertainty](https://arxiv.org/abs/2404.18909) `shi2024sample` — ICML 2024 [M][B] ★
3. [Breaking the Curse of Multiagency in Robust MARL](https://arxiv.org/abs/2409.20067) `shi2024breaking` — ICML 2025（含 [OpenReview 2023 "Can We Break the Curse"](https://openreview.net/forum?id=zpDiqoZ4au) 早期版）[M][B] ★
4. [Taming the Curses of Multiagency … Linear Function Approximation](https://arxiv.org/abs/2605.03125) — arXiv 2026, Gai & Shi [W]
5. [Distributionally Robust Cooperative MARL via Robust Value Factorization](https://arxiv.org/abs/2602.11437) `qu2026distributionally`(=`learningdistributionally`) — ICLR 2026, Caltech [B][W] ★
6. [Sample-Efficient DR MARL via Online Interaction](https://arxiv.org/abs/2508.02948) `farhat2026sample`(=`farhat2025online`; =原md "Online Robust MARL under Model Uncertainties") — ICLR 2026, Yue Wang组 [M][B][W] ★
7. [Strategically Robust MARL with Linear Function Approximation](https://arxiv.org/abs/2603.09208) — arXiv 2026, Mazumdar/Ratliff [W]
8. [Distributionally Robust Online Markov Game w/ Linear Func Approx](https://arxiv.org/abs/2511.07831) — arXiv 2025 ⚠️ [W]
9. [Distributionally Robust Markov Games with Average Reward](https://arxiv.org/abs/2508.03136) — arXiv 2025, Roch & Yue Wang [W]
10. [Robust Cooperative MARL: Mean-Field Type Game Perspective](https://proceedings.mlr.press/v242/zaman24a.html) `zaman2024robust` — L4DC 2024, Başar [M][B]
11. [Tractable Equilibrium Computation via Risk Aversion](https://arxiv.org/abs/2406.14156) `mazumdar2024tractable` — arXiv 2024 [B]
12. Behavioral Economics Approach to Principled MARL `mazumdar2024behavioral` — NeurIPS'24 WS [B] ｜链接待补
13. [Provably Convergent Actor-Critic in Risk-averse MARL](https://arxiv.org/abs/2602.12386) `zhang2026provably` — arXiv 2026, Zhang & Mazumdar [B]
14. [Robust Mean-Field Games with Risk Aversion and Bounded Rationality](https://arxiv.org/abs/2602.13353) — arXiv 2026, Tsiotras 组 [W]
15. Multi-Agent Robust Policy Evaluation via Primal-Dual Online Time-Averaging `chen2025multi` — Sci China IS 2025 [B] ｜链接待补
16. [Robustness to Multi-Modal Env Uncertainty via Curriculum](https://arxiv.org/abs/2310.08746) `agrawal2023robustness` — arXiv 2023, Furong Huang [B]
17. [Adaptive Robust Estimator for MARL](https://arxiv.org/abs/2603.21574) `li2026adaptive` — arXiv 2026 [B]
18. Distributed Primal-Dual for Constrained MARL `kahe2026distributed` — IEEE TAC 2026 [B] ｜链接待补
19. [Scalable Robust MARL for Model Uncertainty](https://ieeexplore.ieee.org/abstract/document/10383458) — CDC 2023, 韩国 [M]
20. [Data-Driven Robust MARL](https://ieeexplore.ieee.org/abstract/document/9943500) — MLSP 2022, Shaofeng Zou [M]
21. [Minimax-Optimal MARL in Markov Games w/ Generative Model](https://papers.nips.cc/paper_files/paper/2022/hash/62b4fea131cfd5b7504eae356b75bbd8-Abstract-Conference.html) — NeurIPS 2022, Gen Li [M]
22. [Towards Robust MARL](https://ojs.aaai.org/index.php/AAAI-SS/article/view/31222) — AAAI-SS 2024, Aritra Mitra [M]
23. [Robust MARL via Bayesian Distributional Value Estimation](https://www.sciencedirect.com/science/article/pii/S0031320323006155) — Pattern Recognition 2024 [M]
24. [Robust MARL Driven by Correlated Equilibrium](https://openreview.net/forum?id=JvPsKam58LX) — rej. ICLR 2021, Jun Wang [M]
25. [Restless and Uncertain: Robust Policies for Restless Bandits](https://proceedings.mlr.press/v180/killian22a.html) — UAI 2022, Harvard/Cambridge [M]
26. [Robust Multi-agent Counterfactual Prediction](https://proceedings.neurips.cc/paper/2019/hash/fc9b003bb003a298c2ad0d05e4342bdc-Abstract.html) — NeurIPS 2019 [M]
27. [GOV-REK: Governed Reward Engineering Kernels](https://arxiv.org/abs/2404.01131) — AAMAS 2024（奖励设计）[M]

**小计：27**

---

## §2 状态 / 观测扰动

28. [Robust MARL with State Uncertainty](https://arxiv.org/abs/2307.16212) `herobust`/`he2023robust` — TMLR 2023, Sihong He [M][B] ★
29. [What is the Solution for State-Adversarial MARL?](https://arxiv.org/abs/2212.02705) `han2022solution` — TMLR 2024, Fei Miao [M][B]
30. [Robust MARL via Adversarial Regularization](https://proceedings.neurips.cc/paper_files/paper/2023/hash/d6f8517fceeca1e2cd61721dff786c14-Abstract-Conference.html) `bukharin2023robust` — NeurIPS 2023, Tuo Zhao [M][B] ｜跨 §3（state+action 对抗训练）
31. [MIR2: Mutual Information Regularization](https://ieeexplore.ieee.org/abstract/document/11074764) `li2023mir2`/`li2025robust` — arXiv'23 → TNNLS 2025 [M][B]
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

**小计：15**

---

## §3 对抗攻击 与 对抗训练

43. [Robust MARL via Minimax Deep Deterministic Policy Gradient (M3DDPG)](https://ojs.aaai.org/index.php/AAAI/article/view/4327) — AAAI 2019, Fei Fang ★ [M] ｜跨 §1（minimax 环境）
44. [Wolfpack Adversarial Attack for Robust MARL](https://arxiv.org/abs/2502.02844) `lee2025wolfpack` — ICML 2025 [M][B]
45. [Interaction-Breaking Adversarial Learning Framework for Robust MARL](https://arxiv.org/abs/2605.18024) — ICML 2026, Han 组（Wolfpack 同团队）[W]
46. [Robust MARL with Stochastic Adversary](https://openreview.net/forum?id=bnhFueOeav) `zhou2025robust` — ICML 2025 [M][B]
47. Camouflage Adversarial Attacks on MARL `lu2025camouflage` — TSP 2025 [B] ｜链接待补
48. [Constrained Black-Box Attacks against MARL](https://arxiv.org/abs/2508.09275) `andam2025constrained` — arXiv 2025 [B]
49. Black-Box Adversarial Robustness Testing w/ Partial Observation `zhang2025black` — ICPADS 2025 [B] ｜跨 §8 ｜链接待补
50. [Finding the Weakest Link: Attack vs MA Communications](https://arxiv.org/abs/2605.13170) `standen2026finding` — arXiv 2026 [B] ｜跨 §4
51. Adversarial Attacks on MADRL in Continuous Action Space `zhou2024adversarial` — TSMC 2024 [B] ｜链接待补
52. [Adversarial DRL Attacks on MA Cooperative Driving](https://doi.org/10.1049/itr2.70066) `alzubaidi2025adversarial` — IET ITS 2025 [B] ｜跨 §9
53. [Action-Oriented Adversarial Attacks on Trajectory Prediction via MARL](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5348784) `zhao5348784action` — SSRN ⚠️ [B] ｜跨 §9
54. [Reward-Poisoning Attacks on Offline MARL](https://ojs.aaai.org/index.php/AAAI/article/view/26240) — AAAI 2023, Young Wu 等 [W] ｜跨 §7（reward 扰动，填补空白）
55. [Co-Evolving Complexity: Adversarial MARL Curricula](https://arxiv.org/abs/2509.03771) `hill2025co` — arXiv 2025 [B]
56. [Heterogeneous MA Adversarial RL in IsaacLab](https://arxiv.org/abs/2510.01264) `peterson2025framework` — arXiv 2025 [B]
57. [Robust MA Coordination via Evolutionary Auxiliary Adversarial Attackers](https://ojs.aaai.org/index.php/AAAI/article/view/26388) — AAAI 2023 [M]
58. [Adversarial DRL for Robust MA Autonomous Driving Policies](https://ieeexplore.ieee.org/abstract/document/10043282) — APSEC 2022 [M] ｜跨 §9
59. [On the Robustness of Cooperative MARL](https://ieeexplore.ieee.org/abstract/document/9283830) — SPW 2020, Sai Qian Zhang（security）[M] ｜跨 §8

**小计：17**

---

## §4 通信鲁棒（noise + 攻击 + certified）

60. [Robust Communicative MARL with Active Defense (ADMAC)](https://ojs.aaai.org/index.php/AAAI/article/view/29708) `yu2024robust` — AAAI 2024, Tsinghua [M][B]
61. [Certifiably Robust Policy Learning vs Adversarial Communication](https://openreview.net/forum?id=dCOL0inGl3e) — ICLR 2023, Furong Huang ★ [M]
62. [Certified Policy Smoothing for Cooperative MARL](https://ojs.aaai.org/index.php/AAAI/article/view/26756) — AAAI 2023 [M]
63. [Mis-spoke or Mis-lead: Robustness in Communicative MARL](https://arxiv.org/abs/2108.03803) — AAMAS 2022, Bo An [M] ｜跨 §3
64. [Robust MA Communication with Graph Information Bottleneck](https://ieeexplore.ieee.org/abstract/document/10334015) — TPAMI 2024, Bo An [M]
65. [Robust Cooperative MARL via Multi-View Message Certification](https://link.springer.com/article/10.1007/s11432-023-3853-y) — Sci China IS 2024, Nanjing [M]
66. [Succinct & Robust MA Communication w/ Temporal Message Control](https://proceedings.neurips.cc/paper_files/paper/2020/hash/c82b013313066e0702d58dc70db033ca-Abstract.html) — NeurIPS 2020, Sai Qian Zhang [M]
67. Robust and Efficient Communication in MARL `liu2026robust` — Chaos 2026 [B] ｜链接待补
68. [Robust MA Comm via Decentralization-Oriented Adversarial Training](https://arxiv.org/abs/2504.21278) `ma2025robust` — arXiv 2025 [B]
69. [Robust Multi-UAV: Noise-Resilient Comm + Attention](https://arxiv.org/abs/2503.02913) `zhao2025towards` — arXiv 2025 [B] ｜跨 §9
70. [DCT-MARL: Dynamic Communication Topology for Platoon](https://arxiv.org/abs/2508.12633) `xu2025dct` — arXiv 2025 [B] ｜跨 §9
71. [Effective Communications: Joint Learning over Noisy Channels](https://ieeexplore.ieee.org/abstract/document/9466501) — Journal 2021, UK [M]
72. [Robust MARL with Social Empowerment (Coordination & Communication)](https://arxiv.org/abs/2012.08255) — arXiv 2020 [M]

**小计：13**

---

## §5 队友不可信 / Byzantine / Fault-Tolerant / Trust（多智能体独有）★

73. [Byzantine Robust Cooperative MARL as a Bayesian Game](https://arxiv.org/abs/2305.12872) `li2024byzantine` — ICLR 2024 [M][B]
74. [Bayesian Robust Cooperative MARL Against Unknown Adversaries](https://openreview.net/forum?id=ydVFxjjtbA) `kazaribayesian` — ICLR 2026 ★ [B][W]
75. IBGP: Imperfect Byzantine Generals for Zero-Shot Robustness `mao2025ibgp` — AGI 2025 [B] ｜跨 §6 ｜链接待补
76. [Fault-Tolerant MA Learning w/ Adversarial Budget Constraints](https://arxiv.org/abs/2508.08800) `mguni2025fault` — arXiv 2025, Yaodong Yang [B]
77. Towards Fault Tolerance in MARL `shi2025towards` — TASE 2025 [B] ｜链接待补
78. [Fully Byzantine-Resilient Distributed MA Q-Learning](https://arxiv.org/abs/2604.02791) — CDC 2026, Panagou [W]
79. [Decentralized Byzantine-Resilient MARL w/ Reward Machines](https://openreview.net/forum?id=ydVFxjjtbA) — 2025 ⚠️venue [W]
80. Trust-Based Information Filtering for Decentralized MARL (UAV) `rudzitis2025trust` — WMNC 2025 [B] ｜链接待补
81. TrustOrch: Dynamic Trust-Aware Orchestration `hu2025trustorch` — 2025 [B] ｜跨 §6 ｜链接待补
82. [Trust-MARL: On-Ramp Merging](https://arxiv.org/abs/2506.12600) `pan2025trust` — arXiv 2025 [B] ｜跨 §9
83. Modeling Trust & Deception via Werewolf Game `patel2025modeling` — 2025 ⚠️ [B] ｜链接待补
84. Unsupervised Partner Design Enables Robust Ad-hoc Teamwork — ICML 2026 [W] ｜链接待补
85. [Resilient MARL with Adversarial Value Decomposition](https://ojs.aaai.org/index.php/AAAI/article/view/17348) — AAAI 2021, TU Munich [M] ｜跨 §3
86. [Robust Multi-Agent Bandits over Undirected Graphs](https://dl.acm.org/doi/abs/10.1145/3570614) — ACM ToMACS 2022（dishonest 队友）[M]

**小计：14**

---

## §6 LLM 多智能体安全 / 鲁棒（全新前沿）★差异化卖点

87. [Evo-MARL: Co-Evolutionary MARL for Internalized Safety](https://arxiv.org/abs/2508.03864) `pan2025evo` — arXiv 2025 [B] ｜跨 §3
88. [AdvEvo-MARL: Safety via Adversarial Co-Evolution](https://arxiv.org/abs/2510.01586) `pan2025advevo` — arXiv 2025 [B] ｜跨 §3
89. Safe MARL with Natural Language Constraints `wang2026safe` — AAAI 2026 [B] ｜链接待补
90. Collaborative Comm for Edge LLM in Adversarial Networks (MARL Stackelberg) `hong2025collaborative` — IoT 2025 [B] ｜跨 §4 ｜链接待补
91. [LLM-based MARL: Current and Future Directions](https://arxiv.org/abs/2405.11106) — arXiv 2024（短综述）[M]

**小计：5**

---

## §7 Offline / 分布偏移鲁棒（新增子领域）

92. Partial Action Replacement: Distribution Shift in Offline MARL `jin2026partial` — AAAI 2026 [B] ｜链接待补
93. Sample-Efficient Robust Offline Self-Play (model-based) `li2025sample` — 2025 ⚠️ [B] ｜跨 §1 ｜链接待补

**小计：2**

---

## §8 Benchmark / 测评

94. [Robust Gymnasium: Unified Modular Benchmark for Robust RL](https://arxiv.org/abs/2502.19652) — ICLR 2025, Gu & Shi ★ [M]
95. [StarCraft+: Benchmarking MA Algorithms in Adversary Paradigm](https://arxiv.org/abs/2512.16444) `li2025starcraft+` — arXiv 2025 [B] ｜跨 §3
96. [Measuring Robustness of MARL under Partial Agent Failure](https://doi.org/10.1145/3759355.3759373) `barta2025measuring` — FAIR 2025 [B] ｜跨 §5
97. [Empirical Study on Robustness and Resilience in Cooperative MARL](https://arxiv.org/abs/2510.11824) — NeurIPS 2025, Bo An/Yaodong Yang 组 [W] ｜跨 §5
98. [Robustness Testing for MARL: State Perturbations on Critical Agents](https://arxiv.org/abs/2306.06136) — arXiv 2023, Ziyuan Zhou [M] ｜跨 §2,§3
99. [Towards Comprehensive Testing on Robustness of Cooperative MARL](https://openaccess.thecvf.com/content/CVPR2022W/ArtOfRobust/html/Guo_Towards_Comprehensive_Testing_on_the_Robustness_of_Cooperative_Multi-Agent_Reinforcement_CVPRW_2022_paper.html) — CVPRW 2022 [M] ｜跨 §3
100. [SMACv2: Improved Benchmark for Cooperative MARL](https://proceedings.neurips.cc/paper_files/paper/2023/hash/764c18ad230f9e7bf6a77ffc2312c55e-Abstract-Datasets_and_Benchmarks.html) — NeurIPS 2023, Whiteson [M]
101. [MATE: Benchmarking MARL in Distributed Target Coverage Control](https://proceedings.neurips.cc/paper_files/paper/2022/hash/b2a1c152f14a4b842a9ddb3bd84c62a1-Abstract-Datasets_and_Benchmarks.html) — NeurIPS 2022, Yaodong Yang [M]
102. [Mava: Research Library for Distributed MARL in JAX](https://arxiv.org/abs/2107.01460) — arXiv 2021 [M]
103. [A Pilot Study of Observation Poisoning on Selective Reincarnation in MARL](https://link.springer.com/article/10.1007/s11063-024-11625-w) — Neural Proc. Letters 2024 [M] ｜跨 §3
104. [MARL for Traffic Signal Control: Algorithms and Robustness Analysis](https://ieeexplore.ieee.org/abstract/document/9294623) — ITSC 2020, Monash [M] ｜跨 §9
105. [Evaluating Robustness of DRL for Autonomous Policies in MA Urban Driving](https://ieeexplore.ieee.org/abstract/document/10062456) — QRS 2023 [M] ｜跨 §9

**小计：12**

---

## §9 安全+鲁棒 & 应用

本节多为应用导向，按场景分子表。`源`列：M=原始md / B=bib / W=web；备注含跨类与待办标记。

#### 9a. 安全+鲁棒（CAV 为主，多为 Fei Miao 组）

| # | 标题 | venue·年 | 源 | 备注 |
|---|---|---|---|---|
| 106 | [Safety-Guaranteed Robust MARL w/ Hierarchical Control for CAVs](https://arxiv.org/abs/2309.11057) `zhang2025safety` | ICRA 2025 | M·B | 跨 §2 |
| 107 | [Robust & Safe MARL Framework w/ Comm for AVs](https://arxiv.org/abs/2506.00982) `smith2025robust` | arXiv 2025 | M·B | 跨 §4 |
| 108 | 5G-Enabled Safe & Robust Deep MARL for CAV `miao20255g` | 2025 ⚠️ | B | 链接待补 |
| 109 | Robustness-Enhanced Cooperative ACC via Joint MARL `dong2025robustness` | Neurocomputing 2025 | B | 链接待补 |
| 110 | [Robust MARL vs Adversarial Attacks for Cooperative Self-Driving](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/rsn2.70033) `wang2025robust` | IET RSN 2025 | M·B | 跨 §3 |
| 111 | [Transferring MARL Policies for Autonomous Driving Sim-to-Real](https://ieeexplore.ieee.org/abstract/document/9981319) | IROS 2022 | M | |
| 112 | [Safe Robust MARL with Neural Control Barrier Functions & Safety Attention](https://www.sciencedirect.com/science/article/abs/pii/S0020025524014816) | Information Sciences 2024 | B | CBF |

#### 9b. 电网 / 能源

| # | 标题 | venue·年 | 源 | 备注 |
|---|---|---|---|---|
| 113 | Distributed Robust Dispatch for Networked Microgrids (Coalition Game + Safe MARL) `pu2025distributed` | TII 2025 | B | 链接待补 |
| 114 | Robust Voltage Control via Safe DRL vs State Perturbations `tian2025robust` | PCMP 2025 | B | 跨 §2 · 链接待补 |
| 115 | [GNN-Based MARL for Active Voltage Control: Topology Robustness](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5960743) `eze5960743graph` | SSRN ⚠️ | B | |
| 116 | [Uncertainty-Aware Knowledge Transformers for P2P Energy Trading](https://arxiv.org/abs/2507.16796) `shah2025uncertainty` | arXiv 2025 | B | |
| 117 | Combating Uncertainties in Smart Grid: MARL w/ Imperfect State Info `ghasemi2024combating` | IoT-J 2024 | B | 链接待补 |
| 118 | [Robust Regional Coordination of Inverter-Based Volt/Var Control](https://ieeexplore.ieee.org/abstract/document/9511622) | T-Smart Grid 2021 | M | |
| 119 | [Resilience Enhancement of MARL Demand Response vs Adversarial Attacks](https://www.sciencedirect.com/science/article/pii/S0306261922009850) | Applied Energy 2022 | M | 跨 §3 |
| 120 | [MA DRL for Robustness of EV Charging vs Cyber-Attacks](https://www.sciencedirect.com/science/article/pii/S0360544224024435) | Energy 2024 | M | 跨 §3 |
| 121 | [Model-Free MARL for Robust Power Management in Micro-Grid](https://ieeexplore.ieee.org/abstract/document/10406423) | IAS 2023 | M | |
| 122 | [Optimal Bi-Level Bidding/Dispatching via Distributed Robust MA DRL](https://ieeexplore.ieee.org/abstract/document/9745992) | Power System 2022 | M | |

#### 9c. 交通 / 路网 / 物流

| # | 标题 | venue·年 | 源 | 备注 |
|---|---|---|---|---|
| 123 | [Distributionally Robust MARL for Intelligent Traffic Control](https://arxiv.org/abs/2512.18558) `pei2025distributionally` | arXiv 2025 | B | 跨 §1 |
| 124 | [Decentralized MARL w/ VLC for Robust Urban Traffic Signal](https://doi.org/10.3390/su172210056) `vieira2025decentralized` | Sustainability 2025 | B | |
| 125 | Robust Real-Time Control for High-Frequency Bus Service `low2026robust` | JITS 2026 | B | 链接待补 |
| 126 | [Distributionally Robust MARL for Dynamic Chute Mapping](https://arxiv.org/abs/2503.09755) `liu2025distributionally` | arXiv 2025 (Amazon) | M·B | 跨 §1 |
| 127 | [Robust & Scalable Routing with MA Deep RL for MANETs](https://arxiv.org/abs/2101.03273) | arXiv 2021 (Boeing) | M | |
| 128 | [DeepCQ+: Robust & Scalable Routing with MA Deep RL](https://ieeexplore.ieee.org/abstract/document/9652948) | 2021 | M | |
| 129 | [Robust Multi-vehicle Routing for Last-Mile Logistics](https://link.springer.com/chapter/10.1007/978-981-97-7244-5_41) | WBD 2024 | M | |
| 130 | [Coordinated Robust Real-Time Control for Sewer Overflow & Urban Flooding](https://www.sciencedirect.com/science/article/pii/S0043135422014439) | Water Research 2023 | M | |

#### 9d. UAV / USV / 机器人 / 其他

| # | 标题 | venue·年 | 源 | 备注 |
|---|---|---|---|---|
| 131 | ROMUC: Robust Policy Learning for Multi-USV Cooperative Tasks `li2025romuc` | ACAIT 2025 | B | 链接待补 |
| 132 | [Robust UAV Wireless Comm via MARL to Optimize Coverage](https://doi.org/10.3390/drones9050321) `khan2025robust` | Drones 2025 | B | |
| 133 | Robust Multi-Agent Path Planning in Dynamic Environments `le2025robust` | 2025 ⚠️ | B | 链接待补 |
| 134 | Robust Control of Water Distribution Networks (MA Curriculum) `amarnath2026robust` | Water Res. Mgmt 2026 | B | 链接待补 |
| 135 | [Robust MARL via Adversarial Domain Randomization for Dual-UAV](https://ieeexplore.ieee.org/abstract/document/10225713) | TIV 2024 (Tongji) | M | 跨 §3 |
| 136 | [Robust MA Coverage Path Planning for UAVs in 3D](https://ieeexplore.ieee.org/abstract/document/10354596) | ROBIO 2023 | M | |
| 137 | [Mobility-as-a-Resilience-Service in IoRT via Robust MA DRL](https://ieeexplore.ieee.org/abstract/document/10855408) | J-IoT 2025 | M | |
| 138 | [Robust MA Federated RL for Task Offloading](https://link.springer.com/chapter/10.1007/978-981-96-2409-6_21) | Springer 2023 | M | |
| 139 | [Robust MARL for Noisy Environments](https://link.springer.com/article/10.1007/s12083-021-01133-2) | Journal 2022 (Hunan U) | M | |
| 140 | [Robust MA Patrolling Strategies Using RL](https://link.springer.com/chapter/10.1007/978-3-319-12970-9_17) | non-top venue | M | |
| 141 | [Air Combat Autonomous Maneuver via Robust MARL](https://ieeexplore.ieee.org/abstract/document/9264567) | ICCA 2020 | M | |

#### 9e. 网络安全 / CPS

| # | 标题 | venue·年 | 源 | 备注 |
|---|---|---|---|---|
| 142 | RMAAC: Robust MA Actor-Critic for Malware Defense in Social IoT `shen2025rmaac` | TDSC 2025 | B | 链接待补 |
| 143 | MARL for Cyber Defence: Transferability & Scalability `thomas2026multi` | Applied AI Letters 2026 | B | 链接待补 |
| 144 | Towards Robust Autonomous Cyber Defence Agents (Hybrid AI) `holz2025towards` | NetSoft 2025 | B | 链接待补 |
| 145 | [Hierarchical Adversarially-Resilient MARL for CPS Security](https://ojs.aaai.org/index.php/AAAI-SS/article/view/35403) `alqithami2025hierarchical` | AAAI Symp 2025 | B | 链接待核实 |

#### 9f. 金融

| # | 标题 | venue·年 | 源 | 备注 |
|---|---|---|---|---|
| 146 | Meta-Adaptive Risk-Aware MARL for Portfolio Management (MARS) `chen2026mars` | AAAI 2026 | B | 链接待补 |

**小计：41**（9a 7 · 9b 10 · 9c 8 · 9d 11 · 9e 4 · 9f 1）

---

<!-- BEGIN cite-analysis-supplement -->
## 引文分析补充语料（规范 ID 散布于 147–193，已对齐 `INDEX.md`/`xlsx`；待并入 §1–§9）★

对 §1–§9 已处理的 133 篇做参考文献引文分析（`citation-analysis/`）所得：被本语料引用、但前 146 篇未收录的 robust-MARL 工作。52 条候选去重后 **45 篇**（另：规范 ID 156 = ACM CSUR'25 SoK 综述 `standen2023adversarial` 已在 §10、不计入；ID 160 = #65 `yuan2024cooperative` 重复，不另列）。**本块编号已对齐 `processed-papers/INDEX.md` 与 `robust-marl-papers.xlsx`，可按 ID 直接取 `notes-en/` 笔记。**
来源标记 `[C]`；`(被引 N×)` = 被本语料中 N 篇引用；★ = 被引 ≥5。
> ⚠️ 自动抽取草稿：少数 venue/作者可能有误；§5 中部分为控制论/分布式优化（fault-tolerant control、consensus、Byzantine optimization）背景文献，相关性偏弱，并入前建议人工筛选。


### 补充 §1 环境/模型不确定性（DRMG / 理论）

150. Decentralized robust v-learning for solving markov games with model uncertainty `ma2023decentralized` — JMLR 2023 [C]（被引 8×） ★ ｜链接待补
159. Roping in uncertainty: Robustness and regularization in markov games `mcmahan2024roping` — ICML 2024, Mazumdar et al. [C]（被引 3×） ｜链接待补
182. Robust and diverse multi-agent learning via rational policy gradient `lauffer2026robust` — NeurIPS 2026, Lauffer et al. [C]（被引 1×） ｜链接待补
186. Adversarial policy gradient for alternating markov games `gao2018adversarial` — 2014 [C]（被引 1×） ｜链接待补
190. [Learning markov games with adversarial opponents: Efficient algorithms and fundamental limits](https://arxiv.org/abs/2203.06803) `liu2022markov` — arXiv 2022, Liu et al. [C]（被引 1×）

### 补充 §2 状态 / 观测扰动

153. [Safe and robust multi-agent reinforcement learning for connected autonomous vehicles under state perturbations](https://arxiv.org/abs/2309.11057) `zhang2023safe` — arXiv 2023, Zhang et al. [C]（被引 5×） ★
176. [Less is more: Robust robot learning via partially observable multi-agent reinforcement learning](https://arxiv.org/abs/2309.1479) `zhao2023less` — arXiv 2023, Zhao et al. [C]（被引 1×）

### 补充 §3 对抗攻击与对抗训练

147. [ROMAX: Certifiably robust deep multi-agent reinforcement learning via convex relaxation](https://arxiv.org/abs/2109.06795) `sun2022romax` — ICRA 2022, Sun et al. [C]（被引 10×） ★
152. [Attacking cooperative multi-agent reinforcement learning by adversarial minority influence](https://arxiv.org/abs/2302.03322) `li2023attacking` — arXiv 2023, Li et al. [C]（被引 6×） ★
157. [Efficient adversarial attacks on online multi-agent reinforcement learning](https://arxiv.org/abs/2307.07670) `liu2023efficient` — NeurIPS 2023 [C]（被引 3×）
158. One4all: Manipulate one agent to poison the cooperative multi-agent reinforcement learning `zheng2023one4all` — 2023, Zheng et al. [C]（被引 3×） ｜链接待补
162. Marnet: Backdoor attacks against cooperative multi-agent reinforcement learning `chen2022marnet` — 2022 [C]（被引 1×） ｜链接待补
164. Security analysis of poisoning attacks against multi-agent reinforcement learning `xie2021security` — 2021 [C]（被引 1×） ｜链接待补
172. Robust reward-free actor-critic for cooperative multi-agent reinforcement learning `lin2024reward` — IEEE TNNLS 2024, Lin et al. [C]（被引 1×） ｜链接待补
174. Robust multi-agent Q-learning in cooperative games with adversaries `nisioti2021robust` — AAAI 2021, Nisioti et al. [C]（被引 1×） ｜链接待补
181. [Distributed robust optimization for multi-agent systems with guaranteed finite-time convergence](https://arxiv.org/abs/2309.01201) `wu2023distributed` — arXiv 2023, Wu et al. [C]（被引 1×）
192. Data poisoning to fake a nash equilibria for markov games `wu2024data` — AAAI 2024, Wu et al. [C]（被引 1×） ｜链接待补

### 补充 §4 通信鲁棒

148. [Gaussian process based message filtering for robust multi-agent cooperation in the presence of adversarial communication](https://arxiv.org/abs/2012.00508) `mitchell2020gaussian` — ICLR 2020, Madry et al. [C]（被引 9×） ★
149. [Adversarial Attacks On Multi-Agent Communication](https://arxiv.org/abs/2101.06560) `tu2021adversarial` — ICCV 2021, Tsipras et al. [C]（被引 9×） ★
166. Safe multi-agent reinforcement learning for wireless applications against adversarial communications `lv2024safe` — IEEE Transactions 2024, Lv et al. [C]（被引 1×） ｜链接待补
168. The emergence of adversarial communication in multi-agent reinforcement learning `blumenkamp2021emergence` — CoRL 2020 [C]（被引 1×） ｜链接待补
169. Communication-robust multi-agent learning by adaptable auxiliary multi-agent adversary generation `yuan2024communication` — Frontiers of Computer Science 2024, Yuan et al. [C]（被引 1×） ｜链接待补
183. Adaptive frequency and delay compensation in multi-agent systems: Enhancing communication efficiency and robustness `wang2024adaptive` — 2024, Wang et al. [C]（被引 1×） ｜链接待补

### 补充 §5 队友不可信 / Byzantine / Fault-Tolerant

151. Learning and testing resilience in cooperative multi-agent systems `phan2020learning` — AAMAS 2020, Phan et al. [C]（被引 7×） ★ ｜链接待补
161. Adversarial attacks in consensus-based multi-agent reinforcement learning `figura2021adversarial` — ACC 2021 [C]（被引 2×） ｜链接待补
163. Communication-efficient and resilient distributed deep reinforcement learning for multi-agent systems `yao2024communication` — 2024, Yao et al. [C]（被引 1×） ｜链接待补
167. Towards resilience for multi-agent qd-learning `xie2021resilience` — CDC 2021, Xie et al. [C]（被引 1×） ｜链接待补
170. Resilient multi-agent reinforcement learning with function approximation `ye2024resilient` — IEEE TAC 2024, Ye et al. [C]（被引 1×） ｜链接待补
171. Toward resilient multi-agent actor-critic algorithms for distributed reinforcement learning `lin2020resilient` — ACC 2020, Lin et al. [C]（被引 1×） ｜链接待补
175. An overview on multi-agent consensus under adversarial attacks `ishii2019overview` — Annual Reviews in Control 2019 [C]（被引 1×） ｜链接待补
177. Adaptive fault-tolerant tracking control for discrete-time multi-agent systems via reinforcement learning algorithm `li2021adaptive` — 2021, Li et al. [C]（被引 1×） ｜链接待补
178. Byzantine-resilient multi-agent distributed optimization under redundancy `zhai2025byzantine` — IEEE TCNS 2025, Zhai et al. [C]（被引 1×） ｜链接待补
179. Distributed resilience-aware control in multi-robot networks `lee2025distributed` — CDC 2025 [C]（被引 1×） ｜链接待补
180. Towards a fault-tolerant multi-agent system architecture `kumar2000fault` — 2000, Kumar et al. [C]（被引 1×） ｜链接待补
184. A survey on fault tolerant multi agent system `arfat2016survey` — 2016, Arfat et al. [C]（被引 1×） ｜链接待补
185. On the hardness of decentralized multi-agent policy evaluation under byzantine attacks `fang2024hardness` — 2024, Hairi et al. [C]（被引 1×） ｜链接待补
187. Large-scale mean-field federated learning for detection and defense: A byzantine robustness approach in IoT `sun2024large` — 2024, Sun et al. [C]（被引 1×） ｜链接待补
188. Fault-tolerant consensus of leader-following multi-agent systems with jointly connected topologies `li2023fault` — 2023, Li et al. [C]（被引 1×） ｜链接待补
189. Byzantine-resilient multi-agent optimization `su2020byzantine` — IEEE TAC 2021, Su et al. [C]（被引 1×） ｜链接待补
191. Fault-tolerant cooperative control of multi-agent systems: A survey of trends and methodologies `yang2020fault` — IEEE Transactions 2020, Yang et al. [C]（被引 1×） ｜链接待补
193. Resilient distributed optimization for multi-agent cyberphysical systems `yemini2025resilient` — IEEE TAC 2025, Yemini et al. [C]（被引 1×） ｜链接待补

### 补充 §8 Benchmark / 测评

155. [Evaluating robustness of cooperative MARL: A model-based approach](https://arxiv.org/abs/2202.03558) `pham2022evaluating` — 2022, Pham et al. [C]（被引 5×） ★
165. Robustness evaluation of multi-agent reinforcement learning algorithms using gnas `zhang2023robustness` — 2023 [C]（被引 1×） ｜链接待补

### 补充 §9 安全 + 鲁棒 & 应用

154. [A robust and constrained multi-agent reinforcement learning electric vehicle rebalancing method in amod systems](https://arxiv.org/abs/2209.08230) `he2022constrained` — IROS 2022, He et al. [C]（被引 5×） ★
173. Robust lane change decision for autonomous vehicles in mixed traffic: A safety-aware multi-agent adversarial reinforcement learning approach `wang2022lane` — Transportation Research 2022 [C]（被引 1×） ｜链接待补

**补充小计：45**（来自引文分析，未计入原 146 篇语料）

<!-- END cite-analysis-supplement -->

---
## §10 竞品 / 邻近综述（positioning 必读，不计入语料）

- Robust RL: Methods, Benchmarks and Challenges `gu2026robust` — 2026（单智能体）｜链接待补
- Towards Robust Agents: Survey of Adversarial Attacks & Defenses in Deep RL `mohan2026towards` — IEEE Access 2026（单智能体）｜链接待补
- [Comprehensive Survey on MA Cooperative Decision-Making](https://arxiv.org/abs/2503.13415) `jin2025comprehensive` — arXiv 2025（泛 MARL）
- MARL: Methods, Trustworthiness, Applications in IV `zhou2024multiagent` — IEEE TIV 2024 ｜链接待补
- [MARL in Cybersecurity](https://arxiv.org/abs/2505.19837) `landolt2025multi` — arXiv 2025
- [Beyond Robustness: Taxonomy of Resilient Multi-Robot Systems](https://arxiv.org/abs/2109.12343) `prorok2021beyond` — arXiv 2021
- ⭐ [Adversarial ML Attacks and Defences in Multi-Agent Reinforcement Learning](https://dl.acm.org/doi/10.1145/3708320) `standen2023adversarial`（语料 ID 156；arXiv 2023 SoK [2301.04299](https://arxiv.org/abs/2301.04299)）— **ACM Computing Surveys 2025** —— **迄今最接近的竞品**：聚焦 MARL 的对抗攻防（≈本表 §3/§4/§5）。本 survey 需明确差异化：①覆盖更广（环境/模型不确定性 DRMG 理论、§6 LLM-MAS、§7 offline 均不在其范围）；②以"鲁棒性针对什么扰动"为统一 taxonomy 而非仅 attack/defence 二分。
- [Open Challenges in Multi-Agent Security: Towards Secure Systems of Interacting AI Agents](https://arxiv.org/abs/2505.02077) — arXiv 2025（偏 LLM-agent 安全，position paper）
- [A Survey of Safe RL and Constrained MDPs: Single-Agent and Multi-Agent Safety](https://arxiv.org/abs/2505.17342) — arXiv 2025（safe RL 综述，含多智能体安全一节，与 §6/§9 安全交叉）

> **空白结论**：单智能体 robust RL 综述不含多智能体维度；泛 MARL 综述不聚焦鲁棒；ACM CSUR'25 那篇只覆盖"对抗攻防"一支、缺理论/DRMG/LLM-MAS。**本 survey 仍有清晰空白**，但定位语必须正面区别于 CSUR'25 那篇。

---

## §11 背景引用（非 robust-MARL，铺垫用，不计入语料）

- **MARL 基石**：MADDPG (NeurIPS'17)、Networked Agents (ICML'18)、Stabilising Experience Replay/StarCraft (ICML'17)、FOP (ICML'21)
- **单智能体 Robust RL**：`shi2023curious`、`ding2023seeing`、`sun2024constrained`、`zhang2024distributionally`、`kitamura2025near`、`li2024towards`、`sun2024belief`、`sun2026diffusion`、`wang2025towards`、`erdem2025learning`
- **学位论文**：`zhang2025advancing`(Harvard'25)、`shi2023provable`(CMU'23)、`koruturk2026reinforcement`(VT'26)
- **He 团队 EV 应用线**（自引可选）：`he2023arobust`、`he2023data`、`he2020data`

---

## §12 已排除（原 md 标注"非 robust marl"，建议不收）

- Robust Experience Replay Sampling — 2022 Korea（原注：not about robust marl）
- RAMARL — 2022 Norway（原注：not very useful）
- Heterogeneous MARL for Unknown Environment Mapping — AAAI WS 2020（原注：no much robust marl）
- Coordination Between Individual Agents — AAAI 2021（原注：no much robust marl）

---

## §13 未来方向与挑战（Future Directions & Challenges）

> 基于本表 146 篇实际暴露的空白整理；每条标注对应章节/编号，可直接作为论文 `§12 Challenges`（`paper/sections/12-challenges.tex`）的底稿。

### C1. 统一处理 MARL 独有的三类维度
现有工作几乎都**孤立**处理单一扰动：要么模型不确定性（§1），要么通信攻击（§4），要么 Byzantine 队友（§5）。**没有一个框架同时**应对"环境不确定 + 队友不可信 + 通信被攻击"。真实多智能体系统三者并存，统一的威胁模型与算法是最大空白。

### C2. 打破 curse of multiagency，超越 tabular
DRMG 理论（§1）正从 tabular 走向函数逼近/在线/大状态空间（#4 #7 #8 #9），但保证仍是**部分的**：vanishing-minimal-value 等假设强、仅限特定不确定集（TV/KL）。**理论（tabular DRMG）与深度 MARL 实践之间的鸿沟**远未弥合。

### C3. 从"攻击"到"可证明的防御"
攻击文献（§3）数量与精巧度明显**领先**防御：多数防御是经验性/启发式的，面对自适应攻击者会被攻破。**可扩展的 certified robustness**（§4 的 certified smoothing/message certification 不随 agent 数扩展）和**有保证的对抗训练**是核心缺口。

### C4. 鲁棒解概念的碎片化
robust agent policy（#28）、robust Nash/equilibrium、Bayesian game（#73）、mean-field type（#10）、risk-averse QRE（#7 #14）——**解概念各说各话**，cooperative 与 competitive 的"鲁棒"定义不一致。需要一个统一、可比较的解概念框架。

### C5. 鲁棒性 vs 可扩展性的权衡
minimax / DRO（§1、§3）会**加剧** MARL 本就严峻的可扩展性问题（worst-case 优化 + 联合动作空间爆炸）。能随 agent 数扩展、又保持鲁棒保证的方法仍稀缺。

### C6. 异构 / 开放 / ad-hoc 团队的鲁棒
绝大多数工作假设**固定、同质**团队。对团队成员动态变化、临时队友（ad-hoc teamwork，#84）、开放多智能体系统的鲁棒性才刚起步——而这正是现实部署的常态。

### C7. LLM 多智能体安全的形式化
§6（LLM-MAS）目前以经验/协同进化（#87 #88）和 position paper 为主，**缺形式化保证**。如何把经典 robust-MARL 的解概念与理论（§1–§5）迁移到 LLM agent 团队（自然语言通信、涌现角色、prompt 注入）是全新且高价值的方向。

### C8. Offline、风险敏感与分布鲁棒的统一
offline robust MARL（§7）极小且无强保证；risk-averse 鲁棒（#11–#14）正在兴起；三者（offline 分布偏移、risk-sensitivity、DRMG 不确定集）在数学上相通却**尚未统一**。一个"robust + risk-aware + offline"的统一理论是开放问题。

### C9. 标准化评测与度量
§8 显示评测**碎片化**：缺统一的鲁棒性度量、缺面向"agent 失效"与"通信攻击"的标准 benchmark。Robust Gymnasium（#94）、StarCraft+（#95）、partial-failure 测评（#96）是起点，但远未形成社区公认标准。

### C10. Sim-to-real 与部署级保证
§9 应用绝大多数停留在**仿真**；真实世界的分布偏移、传感器/执行器故障、部署级的鲁棒性保证基本无人触及。sim-to-real 鲁棒迁移（#111）是稀有尝试。

> **贯穿主线**：C1/C6/C7 直接对应本综述 thesis——MARL 独有维度（队友/通信/multiagency）的鲁棒性，既最缺统一理论，也最具研究机会。论文 `§12` 建议以这 10 条为骨架，每条扩成 1 小段。

---

## 总计与去重记录

**语料合计（§1–§9）**：27+15+17+13+14+5+2+12+41 = **146 篇**（含两轮检索新增 7 篇，已并入对应章节）
（另 §10 综述 9、§11 背景/学位若干、§12 排除 4，均不计入核心语料）

**跨类索引**（一篇归 2+ 类，所在节为主类→列其次类，共 39 篇）：
- 跨 §1：#43(M3DDPG)、#93、#123、#126
- 跨 §2：#98、#106、#114
- 跨 §3：#30、#49、#59、#63、#85、#87、#88、#95、#98、#99、#103、#110、#119、#120、#135
- 跨 §4：#50、#90、#107
- 跨 §5：#35、#38、#96、#97
- 跨 §6：#75、#81
- 跨 §7：#54
- 跨 §9：#42、#52、#53、#58、#69、#70、#82、#104、#105

**跨源重叠已合并**（在多源出现，只计一次）：he state uncertainty、wolfpack、breaking curse、byzantine bayesian、qu2026、farhat、zaman、shi sample、yu active defense、li mir2、zhou stochastic adversary、kazari、liu chute mapping、zhang safety CAV、smith robust-safe AV、wang2025 self-driving 等约 22 篇。

**bib 内部物理重复**（编译前需在 .bib 删除）：`he2023robust`×5、`shi2024breaking`×2、`zaman2024robust`×2、`qu2026distributionally`=`learningdistributionally`、`farhat2026`/`farhat2025`、`vieira2025`=`augusto2025`、`ding2023get`×2。

**链接情况**：约 105 篇带可点击链接（arXiv/出版社/DOI/SSRN）；**约 24 篇标 `链接待补`**（仅期刊/会议名、无 arXiv，多为 TSMC/TII/TDSC/Neurocomputing/AAAI-ojs 等，需手动查 DOI）；#145 链接为推测，待核实。

**待办**：核实所有 ⚠️ venue 与 `链接待补`；为 `M`-only 无 key 条目补 BibTeX；据本 146 篇定章节配重（§1理论 + §3攻防 + §5 Byzantine + §9应用为主体，§6 LLM-MAS 为亮点）。
