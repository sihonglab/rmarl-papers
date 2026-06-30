# 8. Distributionally Robust Online Markov Game with Linear Function Approximation

## 元信息 (Metadata)
- **标题**: Distributionally Robust Online Markov Game with Linear Function Approximation
- **作者**: Zewu Zheng, Yuanyuan Lin
- **机构**: Department of Statistics and Data Science, The Chinese University of Hong Kong
- **发表**: arXiv preprint 2025（标注 Copyright © 2026，疑似 AAAI 2026 投稿）
- **链接/arXiv**: arXiv:2511.07831v1

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 环境/模型不确定性（transition dynamic shift，sim-to-real gap），distributionally robust
- **方法范式**: DRMG 理论、d-rectangular uncertainty set、least-square value iteration (LSVI)、robust CCE、regret 分析、线性函数逼近
- **关键词**: distributionally robust Markov game, linear function approximation, robust CCE, regret bound, d-rectangularity

## TL;DR（一句话总结）
首次为 online distributionally robust general-sum Markov game（带线性函数逼近）设计可证明样本高效的算法 DR-CCE-LSI，找到 ε-近似 robust CCE，并给出关于特征维度 d 极小极大最优的 regret 界。

## 问题与动机 (Problem & Motivation)
RL 的 sim-to-real gap（训练与部署环境差异导致性能下降）促使 distributionally robust RL 研究，但在 MARL 中均衡对环境扰动更敏感。大状态空间需线性函数逼近；然而 online robust general-sum 线性 Markov game 此前从未被研究。本文回答：能否为此设定设计可证明样本高效算法？

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 测试环境的 transition kernel 落在以 nominal kernel P⁰ 为中心、半径 σ_i（每个 player 各自不确定性水平/风险偏好）的 d-rectangular total-variation uncertainty set 内。每个 player 优化最坏情况价值。
- **设定**: competitive / general-sum；centralized learning（全局线性函数逼近）；online（交互式数据收集）；目标是 robust CCE

## 方法 (Method)
- 建模 d-rectangular robust linear Markov game，保证 robust action-value 仍为线性，避免一般函数逼近的 completeness 假设。
- 利用强对偶 + vanishing minimal value 假设将 robust Bellman 算子化为可计算形式 inf_μ Eμ[V]=σ_i·E_{P̃}[V]，避免 support shift。
- DR-CCE-LSI（Algorithm 1）：对每个 player、每个特征坐标 j 做 ridge regression 估计 ν，加入针对多智能体设计的 agent-specific 乐观 bonus 项 Γ（由 d 个 UCB 组成，区别于非鲁棒线性 MDP），构造乐观 Q 估计。
- Find-CCE 子程序（Algorithm 2）：用 ε-cover 上的近似 CCE 解决 general-sum 游戏中 CCE 关于 payoff 不 Lipschitz（不稳定）的覆盖数难题，保持计算可行。

## 理论贡献 (Theoretical Contributions)
- Theorem 4.1：构造两玩家 general-sum robust Markov game，证明无附加假设时 online regret 下界 Ω(σ·HK)——根本性 hardness 结果。
- 采用 vanishing minimal value 假设（Assumption 4.2）+ Proposition 4.3 给出直观等价刻画，规避 support shift。
- Theorem 5.1：DR-CCE-LSI 的 instance-dependent regret 上界。
- Theorem 5.2：bonus 累加项可能为 Ω(K)，揭示 online robust 线性逼近独有的 learnability 难题。
- Corollary 5.3：在 feature mapping ϕ 非退化等结构条件下，regret 为 O(dH·min{H, 1/min σ_i}·√K)，是首个在 online 线性逼近 robust 设定下关于 d 极小极大最优的结果，匹配单智能体最佳结果。

## 实验 (Experiments)
- **环境/Benchmark**: 自构造线性 Markov game（5 状态、2 玩家、H=3，含 self-absorbing fail state s_f，参数 ρ 控制进入 fail state 概率/不确定性水平）
- **Baselines**: NQOVI（非鲁棒 online 线性 Markov game 的 SOTA）
- **评估指标**: 不同不确定性水平下的平均奖励

## 主要结果 (Key Results)
- 随不确定性水平增大，DR-CCE-LSI 显著优于不考虑鲁棒性的 NQOVI，性能退化温和，验证应对 sim-to-real gap 的有效性。
- regret 关于特征维度 d 极小极大最优；理论上不同 player 的 σ_i 体现风险偏好，bound 依赖 max_i β_i，意味着同游戏中玩家应有共同风险偏好以获最佳样本效率。

## 局限与未来工作 (Limitations & Future Work)
- 上界关于 horizon H 与信息论下界 Ω(dH^{1/2}·...) 仍有 √H 差距；拟引入 variance-weighted ridge regression 改进，但多智能体下学习单调价值函数的要求不可得，非平凡。
- 仅 centralized 全局线性逼近；decentralized robust 设定仍开放。
- 依赖 vanishing minimal value 假设与 feature mapping 结构条件。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"环境/模型不确定性 (distributionally robust Markov game)"理论线，是将单智能体 DR 线性 MDP 的 online 样本复杂度结果首次推广到 general-sum 线性 Markov game 的工作。与 DRMG offline/generative model 框架（Blanchet et al.、Shi et al.、Jiao & Li）及 online 线性 Markov game（NQOVI、Xie et al.）形成对照，是理论/样本复杂度方向的重要补充。
