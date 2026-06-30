# Robust MARL — New Papers (after 2025.09)

收集范围：2025年9月之后的 robust MARL 新论文，重点覆盖顶会（NeurIPS 2025 / ICLR 2026 / ICML / AAMAS / CDC）和核心团队（Laixi Shi、Yue Wang、Fei Miao、Furong Huang、Eric Mazumdar/Caltech、Ziyuan Zhou）。
检索日期：2026-06-17。部分 venue 标注「待核实」，需在写作前确认最终发表处。

---

## 理论 / Distributionally Robust Markov Games

### [[2605.03125] Taming the Curses of Multiagency in Robust Markov Games with Large State Space through Linear Function Approximation](https://arxiv.org/abs/2605.03125)

2026-05 arXiv, Jingchu Gai, **Laixi Shi**. Pure theory. 是 "Breaking the Curse of Multiagency" 的后续：用线性函数逼近处理大状态空间下的 robust Markov game，样本复杂度避免随 agent 数指数增长。**Laixi Shi 团队最新理论主线。**

### [[2602.11437] Distributionally Robust Cooperative Multi-Agent Reinforcement Learning via Robust Value Factorization](https://arxiv.org/abs/2602.11437)

2026-02 arXiv, **ICLR 2026**. Chengrui Qu, Christopher Yeh, Kishan Panaganti, Eric Mazumdar, Adam Wierman (Caltech). 把 DRO 引入值分解（value factorization），保证个体 greedy 动作与团队最优联合动作在环境不确定下一致（robust IGM）。**新团队（Caltech Wierman/Mazumdar 组）进入这个方向，值得重点读。**

### [[2603.09208] Strategically Robust Multi-Agent Reinforcement Learning with Linear Function Approximation](https://arxiv.org/abs/2603.09208)

2026-03 arXiv. Jake Gonzales, Max Horwitz, Eric Mazumdar, Lillian J. Ratliff. Theory. 提出 RQRE-OVI 算法，计算 Risk-Sensitive Quantal Response Equilibrium，比 Nash 在 cross-play 下更鲁棒，有 finite-sample regret 分析。和上一篇同属 Mazumdar 生态，偏 game-theoretic robustness。

### [[2508.02948] Sample-Efficient Distributionally Robust Multi-Agent Reinforcement Learning via Online Interaction](https://arxiv.org/abs/2508.02948)

**注意：这篇已在旧 md 里（原标题 "Online Robust MARL under Model Uncertainties"）。** Yue Wang 组。2026-03 修订版改了标题。提出 MORNAVI（Multiplayer Optimistic Robust Nash Value Iteration），首次研究 DRMG 的 online learning（无需先验数据），对 TV / KL 不确定集有 low-regret 保证。**写作时用最新标题，更新 venue。**

### [[2511.07831] Distributionally Robust Online Markov Game with Linear Function Approximation](https://arxiv.org/abs/2511.07831)

2025-11 arXiv. Theory. Online DRMG + 线性函数逼近。和 2605.03125 主题接近，需对比二者贡献差异（待核实作者团队）。

---

## Byzantine / Resilience（队友不可信、agent 失效）

### [[2604.02791] Fully Byzantine-Resilient Distributed Multi-Agent Q-Learning](https://arxiv.org/abs/2604.02791)

2026-04 arXiv, **2026 IEEE CDC**. Haejoon Lee, Dimitra Panagou (Michigan). 分布式 Q-learning 在通信遭 Byzantine 攻击下仍能协同学到最优值函数。控制理论侧的 resilience 工作。

### [Decentralized Byzantine-Resilient Multi-Agent Reinforcement Learning with Reward Machines in Temporally Extended Tasks](https://openreview.net/forum?id=ydVFxjjtbA)

2025-09，venue 待核实（OpenReview）。完全去中心化方法 + reward machines，处理部分 agent 发送伪造/欺骗信息的情形；提出基于信念（belief-based）的 Byzantine 检测机制，defender 用观测到的动作和奖励迭代更新对同伴的概率怀疑。**新的 Byzantine-defense 方法，归入"队友鲁棒"章节。**

---

## Benchmark / 鲁棒性测评

### [Measuring the Robustness of Multi-Agent Reinforcement Learning Systems under Partial Agent Failure](https://dl.acm.org/doi/10.1145/3759355.3759373)

2025, Intelligent Robotics FAIR 2025 (ACM). 测量 MARL 系统在部分 agent 失效下的鲁棒性，benchmark/评测类。归入 benchmark 章节。

---

## Safety-critical / 应用（与 robustness 强相关）

### [NeurIPS 2025 Poster — HMARL-CBF: Hierarchical Multi-Agent Reinforcement Learning with Control Barrier Functions for Safety-Critical Autonomous Systems](https://neurips.cc/virtual/2025/poster/116828)

NeurIPS 2025. 分层 MARL + Control Barrier Function，做安全关键多智能体系统的安全策略学习。归入 safety/robust 交叉章节（视你对 scope 的取舍决定是否纳入）。

---

## 待进一步确认 / 边缘相关（搜索命中但相关性需人工判断）

- **NeurIPS 2025**：一篇关于 "state entropy regularization 提升对结构化/空间相关扰动的鲁棒性，并给出 reward/transition 不确定下的形式化保证" 的论文 —— 可能是单智能体，需核实是否 MARL（搜索摘要未给明确标题/作者）。
- **NeurIPS 2025 Poster — A Principle of Targeted Intervention for Multi-Agent Reinforcement Learning**（poster/117666）—— 相关性待判断。
- **ICLR 2026 — Cooperative Multi-agent RL with Communication Constraints**（OpenReview 9eWajl9SoK）—— 通信受限而非通信攻击，是否纳入"通信鲁棒"章节待定。
- **Furong Huang 组：已核实（2026-06-17 查其主页），2025.09 之后无新 robust MARL 论文。** 近期重心转向 LLM / diffusion LM / watermarking；唯一沾边的 2026 ICML "MAFE"（multi-agent 多阶段决策的公平性）与 robustness 无关。其 robust MARL 代表作仍是旧库里 ICLR 2023 certifiable communication 那篇，无需再查。
- Ziyuan Zhou 2025.09 后未检索到明确新作（旧 md 已收其 ICML 2025 "Stochastic Adversary"）。

---

## 写作待办（针对本批新文献）

1. 核实上述「待核实 / 待确认」条目的最终 venue 与作者。
2. 2508.02948 在旧 md 中更新标题与 venue（避免重复条目）。
3. 注意新出现的 **Caltech Wierman/Mazumdar 生态**（2602.11437 + 2603.09208）—— 这是 2026 年该方向的新势力，intro 里值得点名。
4. 理论主线趋势：DRMG + 线性函数逼近 + online learning + curse of multiagency —— 可作为"理论章节"的 2025-2026 小结叙事。
