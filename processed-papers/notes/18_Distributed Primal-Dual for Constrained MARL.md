# 18. A Distributed Primal-Dual Method for Constrained Multi-agent Reinforcement Learning with General Parameterization

## 元信息 (Metadata)
- **标题**: A Distributed Primal-Dual Method for Constrained Multi-agent Reinforcement Learning with General Parameterization
- **作者**: Ali Kahe, Hamed Kebriaei (通讯)
- **机构**: School of ECE, University of Tehran; Institute for Research in Fundamental Sciences (IPM), Tehran, Iran
- **发表**: 未明确（arXiv:2410.15335v2, eess.SY, 2026；IEEE 期刊投稿格式）
- **链接/arXiv**: arXiv:2410.15335v2

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 安全约束（safety/fairness/efficiency constraints，全局共享约束）；非对抗式——属约束满足/安全 MARL 而非对抗鲁棒
- **方法范式**: Constrained Markov Game (CMG)、distributed primal-dual、actor-critic、Lagrangian relaxation、共识 (consensus) 优化、多时间尺度随机逼近
- **关键词**: Constrained MARL, primal-dual, actor-critic, Lagrange multiplier consensus, decentralized, duality gap

## TL;DR（一句话总结）
本文提出一个全分布式 primal-dual actor-critic 算法求解协作约束 MARL（CMARL），每个 agent 仅用局部信息维护各自的原变量与对偶变量（Lagrange 乘子），证明乘子达成共识、算法收敛到均衡点，并分析其相对未参数化精确解的次优性与对偶间隙界。

## 问题与动机 (Problem & Motivation)
许多 MARL 实际应用（微电网、电动车再平衡等）需满足安全/公平/效率约束，导致 CMARL。现有方法多依赖集中训练或部分协调，无法完全去中心化；且协作 CMARL 的对偶间隙可能非零，使满足全局约束变得困难。本文针对局部代价通过全局约束耦合的一般 CMARL，提出无需中心协调的在线分布式解法。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 非对抗。约束以全局约束函数 G_k(πθ)≤b_k 表达，是局部约束代价的平均；代价/约束含外生随机性。强调安全（约束满足）而非对抗扰动。
- **设定**: cooperative；fully decentralized / distributed online（networked agents，邻居通过通信图共享局部 critic 参数与乘子，无 CTDE 中心）；online

## 方法 (Method)
- 在 CMG 框架下将协作 CMARL 写为 minimax: inf_θ sup_λ L(πθ,λ)，全局 Lagrangian 可分解为局部 Lagrangian 之和。
- 因全局约束信息不可得，引入局部估计的 Lagrange 乘子 λ̂_n，每个 agent 估计全局乘子。
- 分布式 primal-dual actor-critic（Algorithm 1）三时间尺度：critic（TD 学习 + 邻居共识加权）、actor（投影策略梯度，advantage 基于局部 Q 近似）、对偶（局部约束估计 Ĝ_n 与乘子 λ̂_n 的共识 + 上升更新）。
- 学习率满足三时间尺度条件（γ≪β≪α），乘子最慢，可视为 actor 视角下准静态。

## 理论贡献 (Theoretical Contributions)
- Theorem 1：局部估计 Lagrange 乘子的 disagreement 分量几乎必然收敛到 0（达成共识）。
- Proposition 1 / Theorem 2：分布式 actor-critic 几乎必然收敛到投影动力系统的渐近稳定均衡，乘子共识值收敛到稳定均衡集 F。
- Proposition 2：若 λ̄ 在 Λ 内部，则所有约束满足（可行性）。
- Proposition 3：给出参数化对偶间隙上界 Δ̄_param，依赖个体/乘积参数化误差 ϵ_n、稳定分布 L1 距离与原始非零对偶间隙 Δ̄（Lemma 3–7 支撑）。

## 实验 (Experiments)
- **环境/Benchmark**: 自定义的合作型随机 Cournot 博弈（带约束、随机动态、时变需求）；离散化为 10 状态 × 每 agent 10 动作，状态转移服从二项分布
- **Baselines**: 未明确（主要验证理论收敛性，无对比基线）
- **评估指标**: 局部估计 Lagrange 乘子的共识与收敛；全局目标代价 J；全局约束违反 Ĝ−b

## 主要结果 (Key Results)
- 局部估计的 Lagrange 乘子达成共识并收敛（验证 Theorem 1、2）。
- 训练中算法有效降低全局目标代价 J，同时将约束违反维持在接近 0（验证可行性）。
- 全分布式（无中心协调）实现了一般耦合约束 CMARL 的求解。

## 局限与未来工作 (Limitations & Future Work)
- 实验仅在单一自定义 Cournot 博弈上验证、无对比基线、状态/动作空间较小且为线性函数逼近；对偶间隙非零导致次优；要求 Slater 条件、双随机通信图等假设。未来：更复杂环境与动态约束。

## 与综述的关联 (Relevance to Survey)
属于 robust/safe MARL 中"安全约束 + 分布式优化"线路，强调约束满足与去中心化收敛，而非对抗鲁棒；与 constrained Markov game、Lagrangian primal-dual、networked actor-critic、duality gap 分析等主题相关。可作为综述中"安全约束 MARL"子线的理论代表（注：本文鲁棒性意涵主要在约束/安全层面，引用了 He et al. 的 robust constrained EV rebalancing 工作）。
