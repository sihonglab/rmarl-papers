# 76. Learning Robust Multi-Agent Policies via Selective Adversarial Fault Induction (MARTA)

## 元信息 (Metadata)
- **标题**: Learning Robust Multi-Agent Policies via Selective Adversarial Fault Induction
- **作者**: David Mguni, Yaqi Sun, Haojun Chen, Wanrong Yang, Amir Darabi, Larry Olanrewaju Orimoloye, Yaodong Yang
- **机构**: Queen Mary University London; Peking University; University of Liverpool; Snowflake Inc.
- **发表**: Preprint (arXiv) 2026
- **链接/arXiv**: arXiv:2508.08800v2

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 智能体失效/故障 (agent malfunction)、actuator-level 故障；含 worst-case 与随机故障两种 regime；带预算约束
- **方法范式**: 对抗训练、switching control、minimax Markov game、Q-learning 收敛理论、plug-and-play 鲁棒层
- **关键词**: fault-tolerant MARL, Switcher-Adversary, switching control, minimax value, budget constraint

## TL;DR（一句话总结）
提出 MARTA，一个即插即用的鲁棒性层，通过 Switcher-Adversary 机制在协调关键状态下选择性地注入智能体故障，训练协作 MARL 智能体对故障鲁棒，并给出收敛性理论保证。

## 问题与动机 (Problem & Motivation)
主流 cooperative MARL（尤其 CTDE 范式）默认智能体可靠执行学到的策略，但现实中 actuator/sensor 故障常见，单个智能体失效会破坏协调导致严重性能退化。已有单智能体 FT 方法常引入 always-on 对抗者，导致策略过度保守。该问题在 MARL 理论中被显著忽视。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 在 Dec-MDP 上引入 Switcher（决定何时、对哪个 agent 触发故障，动作集 {0}∪N）与 Adversary（控制故障行为，random 或 worst-case 策略）。故障使某 agent 动作被对抗策略覆盖。每次触发有成本 c，或受总预算 n 约束（MARTA-B 用增广状态 y_t 跟踪剩余预算）。
- **设定**: cooperative（团队奖励）；CTDE（QMIX/VDN 骨干）；online 训练

## 方法 (Method)
- 构造 (N+2)-player 非零和 fault-switching Markov game：N 个协作 agent、Switcher、Adversary；Adversary 与 Switcher 目标为 -v。
- Switcher 用 switching control，在 state 决定是否激活故障及激活哪个 agent，激活成本 c 鼓励仅在最有害状态干预，避免过度保守。
- 用 switching-augmented Bellman 算子的 Q-learning 变体学习，将 Switcher 动作并入 Q 函数。
- MARTA-B 变体改用预算约束，几乎必然满足预算同时最优使用。
- 实现：N agent 各有 action policy 与 adversarial policy（QMIX/VDN 骨干），Switcher 用 soft actor-critic，共享 replay buffer，即插即用无需改架构。

## 理论贡献 (Theoretical Contributions)
- 证明 game G 的 minimax value 存在且唯一（Bellman 算子收缩 + Banach 不动点）。
- 证明均衡策略为 Markov perfect equilibrium。
- 证明 Q-learning 变体以概率 1 收敛到 Q*（Theorem 3.3）。
- 扩展到 linear function approximation 下的收敛，给出投影 Bellman 算子收缩与误差界 ‖Φr*-Q*‖≤(1-γ²)^(-1/2)‖ΠQ*-Q*‖。
- 证明 MARTA-B（带预算）收敛到最优联合值函数。

## 实验 (Experiments)
- **环境/Benchmark**: Traffic Junction (TJ)、Level-Based Foraging (LBF)、MPE SimpleTag、SMACv2 (3m/8m/2s3z)
- **Baselines**: QMIX、VDN、MADDPG、M3DDPG、EIR（robust/adversarial MARL）
- **评估指标**: test return mean、win rate、collision/failure rate、capture rate、focused fire rate、fault-conditioned win rate

## 主要结果 (Key Results)
- 最终性能提升：SMAC 最高 116.7%（MARTA-VDN, 3m）、MPE SimpleTag 21.4%、LBF 44.6%、TJ 11.1%（QMIX）。
- 显著降低故障率（如 TJ collision rate、MPE failure rate 从 17.5% 降到 5.0%）。
- switching control 学习优于随机 Bernoulli 触发；c↓0 增加 FT 偏好。
- 在动态/train-test 分布漂移 (Case 2) 下优于 EIR；MARTA-MADDPG 优于 M3DDPG。

## 局限与未来工作 (Limitations & Future Work)
- 理论保证仅适用于 tabular 与 linear function approximation，不直接覆盖深度网络参数化。
- 仅针对 non-strategic actuator 故障，不建模策略性/协同欺骗对手（与 Byzantine-robust 不同 regime）。
- 成本 c 在部分应用中难以选取（故引入预算变体）。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"智能体失效/容错 (fault tolerance)"主题，与对抗训练线（M3DDPG、Pinto et al.）和 minimax Markov game 理论线相关；其 switching control + budget 设计区别于 always-on adversary，提供了选择性、状态相关的故障注入与收敛保证，是 cooperative CTDE 容错的代表性工作。
