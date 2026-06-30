# Robust MARL — Master List (从 bib 清洗筛选)

来源：`rmarl-paper-from-25-to-26.bib`（整库导出，约 300 条，已剔除无关条目与重复 key）。
本表只保留与 **robust MARL** 直接相关或可作背景引用的文献，按类别组织。`key` 为 bib 内的引用键，可直接 `\cite{}`。
整理日期：2026-06-17。⚠️ = 需核实 venue / 疑似预印本。

> 调研重心是 **2025+**；2020–2024 奠基作单列 **§0 Foundations**，供历史脉络引用。

---

## §0 Foundations（2020–2024 奠基，必引但非重点）

| key | 标题 | venue / 年 | 类别 |
|---|---|---|---|
| `bukharin2023robust` | Robust MARL via Adversarial Regularization | NeurIPS 2023 | 状态/动作 + 理论 |
| `han2022solution` | What is the Solution for State-Adversarial MARL? | arXiv'22 → TMLR'24 | 状态观测，解概念 |
| `herobust` / `he2023robust`(2307.16212) | Robust MARL with State Uncertainty | TMLR 2023 | 状态观测，理论 |
| `shi2024sample` | Sample-Efficient Robust MARL in Face of Environmental Uncertainty | ICML 2024 | 环境/模型，理论 |
| `shi2024breaking` | Breaking the Curse of Multiagency in Robust MARL | arXiv'24 → ICML'25 | 环境/模型，理论 |
| `li2024byzantine` | Byzantine Robust Cooperative MARL as a Bayesian Game | ICLR 2024 | 队友/Byzantine |
| `zaman2024robust` | Robust Cooperative MARL: Mean-Field Type Game Perspective | L4DC 2024 | 环境/模型，理论 |
| `li2023mir2` | MIR2: Provably Robust MARL by Mutual Information Regularization | arXiv 2023 | 状态观测，方法 |
| `yu2024robust` | Robust Communicative MARL with Active Defense (ADMAC) | AAAI 2024 | 通信 |
| `zhou2023robustness` | Robustness Testing for MARL: State Perturbations on Critical Agents | arXiv 2023 | 攻击/benchmark |
| `guo2024enhancing` | Enhancing the Robustness of QMIX against State-Adversarial Attacks | Neurocomputing 2024 | 状态观测，方法 |
| `zhou2024adversarial` | Adversarial Attacks on MADRL in Continuous Action Space | TSMC 2024 | 攻击 |
| `agrawal2023robustness` | Robustness to Multi-Modal Env Uncertainty in MARL via Curriculum | arXiv 2023 (Furong Huang) | 环境/模型，方法 |
| `mazumdar2024tractable` | Tractable Equilibrium Computation in Markov Games through Risk Aversion | arXiv 2024 | 理论 / risk-averse |
| `mazumdar2024behavioral` | A Behavioral Economics Approach to Principled MARL | NeurIPS'24 WS | 理论 / risk-averse |
| `zhang2025safety`(=zhang2023safe) | Safety-Guaranteed Robust MARL w/ Hierarchical Control for CAVs | ICRA 2025 | 安全+鲁棒，应用 |

---

## §1 环境 / 模型不确定性（DRMG，理论主线）★核心增量

| key | 标题 | venue / 年 | 备注 |
|---|---|---|---|
| `qu2026distributionally`(=`learningdistributionally`) | Distributionally Robust Cooperative MARL via Robust Value Factorization | **ICLR 2026** | Caltech (Qu/Yeh/Panaganti/Mazumdar/Wierman)；DRO 进值分解 |
| `farhat2026sample` | Sample-Efficient DR MARL via Online Interaction | **ICLR 2026** | Yue Wang 组；online DRMG，MORNAVI |
| `farhat2025online` | Online Robust MARL under Model Uncertainties | arXiv'25 (2508.02948) | 同上的预印早期版，写作时合并 |
| `zhang2026provably` | Provably Convergent Actor-Critic in Risk-averse MARL | arXiv 2026 | Zhang & Mazumdar；risk-averse 新支线 |
| `chen2025multi` | Multi-Agent Robust Policy Evaluation via Primal-Dual Online Time-Averaging | Sci China Inf Sci 2025 | 鲁棒策略评估 |
| `li2025sample` | Sample-Efficient Robust Offline Self-Play for Model-Based RL | 2025 ⚠️ | offline + 鲁棒 |
| `pei2025distributionally` | Distributionally Robust MARL for Intelligent Traffic Control | arXiv 2025 | DRMG 应用 |
| `kahe2026distributed` | Distributed Primal-Dual for Constrained MARL w/ General Parameterization | IEEE TAC 2026 | constrained，边缘相关 |

---

## §2 状态 / 观测扰动

| key | 标题 | venue / 年 | 备注 |
|---|---|---|---|
| `li2025robust` | Robust MARL by Mutual Information Regularization (MIR2 期刊版) | **TNNLS 2025** | `li2023mir2` 的正式版 |
| `guo2025robust` | Robust Training in MADRL against Optimal Adversary | TSMC 2025 | Zhou/Liu 团队 |
| `shi2025fault` | Fault-Tolerant MARL for CAVs under Observation Perturbations | arXiv 2025 | on-ramp merging |
| `chen2026enhancing` | Enhancing Robustness in MARL via Temporal Consistency Regularization (self-distillation) | KBS 2026 | 新方法 |
| `fu2025rainbow` | Rainbow Delay Compensation: MARL for Delayed Observation | arXiv 2025 | 延迟观测鲁棒 |
| `hazra2025tackling` | Tackling Uncertainties in MARL via Agent Termination Dynamics | arXiv 2025 | agent 失效不确定性 |

---

## §3 对抗攻击 与 对抗训练（2025 爆发）

| key | 标题 | venue / 年 | 攻/防 |
|---|---|---|---|
| `lee2025wolfpack` | Wolfpack Adversarial Attack for Robust MARL | **ICML 2025** | 攻 |
| `zhou2025robust` | Robust MARL with Stochastic Adversary | **ICML 2025** | 防/训练 |
| `lu2025camouflage` | Camouflage Adversarial Attacks on MARL Systems | TSP 2025 | 攻 |
| `andam2025constrained` | Constrained Black-Box Attacks against MARL | arXiv 2025 | 攻 |
| `zhang2025black` | Black-Box Adversarial Robustness Testing w/ Partial Observation for MARL | ICPADS 2025 | 攻/测评 |
| `standen2026finding` | Finding the Weakest Link: Adversarial Attack against Multi-Agent Communications | arXiv 2026 | 攻（通信） |
| `alzubaidi2025adversarial` | Adversarial DRL Attacks on MA Autonomous Cooperative Driving | IET ITS 2025 | 攻（应用） |
| `zhao5348784action` | Action-Oriented Adversarial Attacks on Trajectory Prediction via MARL | SSRN ⚠️ | 攻（应用） |
| `hill2025co` | Co-Evolving Complexity: Adversarial Framework for Automatic MARL Curricula | arXiv 2025 | 防/课程 |
| `peterson2025framework` | Scalable Heterogeneous Multi-Agent Adversarial RL in IsaacLab | arXiv 2025 | 防/框架 |

---

## §4 通信鲁棒（noise + 攻击）

| key | 标题 | venue / 年 | 备注 |
|---|---|---|---|
| `liu2026robust` | Robust and Efficient Communication in MARL | Chaos 2026 | |
| `ma2025robust` | Robust Multi-Agent Communication Based on Decentralization-Oriented Adversarial Training | arXiv 2025 | |
| `zhao2025towards` | Robust Multi-UAV Collaboration: Noise-Resilient Communication + Attention | arXiv 2025 | |
| `xu2025dct` | DCT-MARL: Dynamic Communication Topology MARL for Platoon Control | arXiv 2025 | |

---

## §5 队友不可信 / Byzantine / Fault-Tolerant / Trust（多智能体独有，升温）★

| key | 标题 | venue / 年 | 备注 |
|---|---|---|---|
| `kazaribayesian` | Bayesian Robust Cooperative MARL Against Unknown Adversaries | **ICLR 2026** | 重点新作 |
| `mao2025ibgp` | IBGP: Imperfect Byzantine Generals Problem for Zero-Shot Robustness | AGI 2025 | LLM-MAS 交叉 |
| `mguni2025fault` | Fault-Tolerant Multi-Agent Learning with Adversarial Budget Constraints | arXiv 2025 | Yang Yaodong 组 |
| `shi2025towards` | Towards Fault Tolerance in Multi-Agent Reinforcement Learning | TASE 2025 | |
| `rudzitis2025trust` | Trust-Based Information Filtering for Robust Decentralized MARL in UAV Swarms | WMNC 2025 | |
| `hu2025trustorch` | TrustOrch: Dynamic Trust-Aware Orchestration for Robust MA Collaboration | 2025 | LLM-MAS 交叉 |
| `pan2025trust` | Trust-MARL: Trust-Based MARL for On-Ramp Merging | arXiv 2025 | 应用 |
| `patel2025modeling` | Modeling Trust and Deception in MARL Using the Werewolf Game | 2025 ⚠️ | |

---

## §6 LLM 多智能体安全 / 鲁棒（全新前沿）★差异化卖点

| key | 标题 | venue / 年 | 备注 |
|---|---|---|---|
| `pan2025evo` | Evo-MARL: Co-Evolutionary MARL for Internalized Safety | arXiv 2025 | |
| `pan2025advevo` | AdvEvo-MARL: Internalized Safety through Adversarial Co-Evolution | arXiv 2025 | |
| `wang2026safe` | Safe MARL with Natural Language Constraints | **AAAI 2026** | |
| `hong2025collaborative` | Collaborative Comm for Edge LLM in Adversarial Networks (MARL Stackelberg) | IoT 2025 | |

---

## §7 Offline / 分布偏移鲁棒（新增子领域）

| key | 标题 | venue / 年 | 备注 |
|---|---|---|---|
| `jin2026partial` | Partial Action Replacement: Tackling Distribution Shift in Offline MARL | **AAAI 2026** | |
| `li2025sample` | (见 §1) Robust Offline Self-Play | 2025 | |

---

## §8 Benchmark / 测评

| key | 标题 | venue / 年 | 备注 |
|---|---|---|---|
| `li2025starcraft+` | StarCraft+: Benchmarking Multi-Agent Algorithms in Adversary Paradigm | arXiv 2025 | |
| `barta2025measuring` | Measuring the Robustness of MARL Systems under Partial Agent Failure | FAIR 2025 | |
| `zhang2025black` | (见 §3) Black-Box Robustness Testing | ICPADS 2025 | |

---

## §9 安全+鲁棒 / 应用（数量最多，选代表）

**安全+鲁棒（CAV，Miao 组等）**
| key | 标题 | venue / 年 |
|---|---|---|
| `smith2025robust` | Robust and Safe MARL Framework with Communication for AVs | arXiv 2025 (2506) |
| `miao20255g` | 5G-Enabled Safe and Robust Deep MARL for CAV Coordination | 2025 ⚠️ |
| `dong2025robustness` | Robustness-Enhanced Cooperative ACC via Generalised Joint MARL | Neurocomputing 2025 |

**电网 / 能源**
| key | 标题 | venue / 年 |
|---|---|---|
| `pu2025distributed` | Distributed Robust Dispatch for Networked Microgrids (Coalition Game + Safe MARL) | TII 2025 |
| `tian2025robust` | Robust Voltage Control via Safe DRL against State Perturbations | PCMP 2025 |
| `eze5960743graph` | GNN-Based MARL for Active Voltage Control: Topology Robustness | SSRN ⚠️ |
| `shah2025uncertainty` | Uncertainty-Aware Knowledge Transformers for P2P Energy Trading (MARL) | arXiv 2025 |

**交通 / 自动驾驶 / 机器人**
| key | 标题 | venue / 年 |
|---|---|---|
| `vieira2025decentralized`(=`augusto2025decentralized`) | Decentralized MARL w/ VLC for Robust Urban Traffic Signal Control | Sustainability 2025 |
| `low2026robust` | Robust Real-Time Control for High-Frequency Bus Service (MARL) | JITS 2026 |
| `li2025romuc` | ROMUC: Robust Policy Learning for Multi-USV Cooperative Tasks | ACAIT 2025 |
| `khan2025robust` | Robust UAV Wireless Comm via MARL to Optimize Coverage | Drones 2025 |
| `le2025robust` | Robust Multi-Agent Path Planning in Dynamic Environments | 2025 ⚠️ |
| `amarnath2026robust` | Robust Control of Water Distribution Networks (MA Curriculum) | Water Res. Mgmt 2026 |

**网络安全 / CPS**
| key | 标题 | venue / 年 |
|---|---|---|
| `shen2025rmaac` | RMAAC: Robust MA Actor-Critic for Malware Defense in Social IoT | TDSC 2025 |
| `thomas2026multi` | MARL for Cyber Defence: Transferability and Scalability | Applied AI Letters 2026 |
| `holz2025towards` | Towards Robust Autonomous Cyber Defence Agents (Hybrid AI) | NetSoft 2025 |
| `alqithami2025hierarchical` | Hierarchical Adversarially-Resilient MARL for CPS Security | AAAI Symp 2025 |

**金融 / 其他应用**
| key | 标题 | venue / 年 |
|---|---|---|
| `chen2026mars` | MARS: Meta-Adaptive Risk-Aware MARL for Portfolio Management | AAAI 2026 |

---

## §10 竞品 / 邻近综述（positioning 必读）

| key | 标题 | venue / 年 | 与本 survey 关系 |
|---|---|---|---|
| `gu2026robust` | Robust Reinforcement Learning: Methods, Benchmarks and Challenges | 2026 | 单智能体 robust RL，非 MARL |
| `mohan2026towards` | Towards Robust Agents: Survey of Adversarial Attacks and Defenses in Deep RL | IEEE Access 2026 | 单智能体 adversarial RL |
| `jin2025comprehensive` | Comprehensive Survey on Multi-Agent Cooperative Decision-Making | arXiv 2025 | 泛 MARL，不聚焦鲁棒 |
| `zhou2024multiagent` | MARL: Methods, Trustworthiness, Applications in IV, and Challenges | IEEE TIV 2024 | 偏 trustworthy + 应用 |
| `landolt2025multi` | MARL in Cybersecurity: From Fundamentals to Applications | arXiv 2025 | 领域综述 |
| `zhong2025survey` | Survey of Cooperative Decision-Making in AV Platooning Based on MARL | DSA 2025 | 领域综述 |
| `prorok2021beyond` | Beyond Robustness: A Taxonomy of Approaches towards Resilient Multi-Robot Systems | arXiv 2021 | multi-robot，无 RL 理论；taxonomy 可借鉴 |
| `cao2024survey` | Survey on LLM-Enhanced RL | TNNLS 2024 | 边缘，LLM+RL |

---

## §11 学位论文（可作 motivation / 背景引用）

| key | 标题 | 学校 / 年 |
|---|---|---|
| `zhang2025advancing` | Advancing Multi-Agent Systems with Scalable and Robust Learning and Control | Harvard 2025 |
| `shi2023provable` | Provable Algorithms for RL: Efficiency, Scalability, and Robustness | CMU 2023 |
| `koruturk2026reinforcement` | RL Benchmarking for Sustainable Energy: Perturbation Robustness, Safety, Multi-Agent | Virginia Tech 2026 |

---

## §12 单智能体 Robust RL（背景，章节铺垫用，非 MARL）

这些是 bib 里的单智能体 robust RL，用于 intro/related work 对比"MARL 多出哪些维度"：
`shi2023curious`（curious price of distributional robustness, NeurIPS'23）、`ding2023seeing`（spurious correlation, NeurIPS'23）、`sun2024constrained`（constrained RL under model mismatch）、`zhang2024distributionally`（DR constrained RL strong duality）、`kitamura2025near`（robust constrained MDP epigraph, ICLR'25）、`ghosh2024sample`（DR constrained MDP）、`li2024towards`（robust Q-learning Bellman infinity-error）、`sun2024belief`（belief-enriched pessimistic Q-learning）、`dongrobust`（structured adversarial ensemble）、`sun2026diffusion`（diffusion-guided adversarial state perturbation, NeurIPS）、`wang2025towards`（robust DRL vs env state perturbation）、`erdem2025learning`（balance mixed adversarial attacks）。

---

## 写作待办

1. **去重**：bib 里 `he2023robust` 出现 5 次、`shi2024breaking`/`zaman2024robust` 各 2 次、`qu2026distributionally`=`learningdistributionally`、`vieira2025`=`augusto2025`、`farhat2026`/`farhat2025` 同一工作不同版本 —— 编译前合并。
2. **补 venue**：标 ⚠️ 的条目（SSRN / 无 journal / 疑似 workshop）需确认正式发表处。
3. **配重判断**：§3 对抗攻防 与 §5 队友/Byzantine 在 2025+ 数量最多，应作为重点章节；§6 LLM-MAS 是差异化亮点；§1 理论是深度所在。
4. 与旧两个 md 合并去重（如 `lee2025wolfpack`、`zhou2025robust`、`kazaribayesian`、Robust Gymnasium 等已在 md 中）。
