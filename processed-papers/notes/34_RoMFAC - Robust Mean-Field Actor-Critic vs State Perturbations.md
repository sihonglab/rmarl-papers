# 34. RoMFAC: A Robust Mean-Field Actor-Critic Reinforcement Learning against Adversarial Perturbations on States

## 元信息 (Metadata)
- **标题**: RoMFAC: A robust mean-field actor-critic reinforcement learning against adversarial perturbations on states
- **作者**: Ziyuan Zhou, Guanjun Liu
- **机构**: Department of Computer Science, Tongji University, Shanghai, China
- **发表**: arXiv:2205.07229v2 (2023)；扩展版发表于 IEEE Transactions on Neural Networks and Learning Systems (DOI 10.1109/TNNLS.2023.3278715)
- **链接/arXiv**: arXiv:2205.07229

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗状态/观测扰动 (white-box state perturbations, PGD 攻击)
- **方法范式**: 对抗训练、mean-field actor-critic、action loss 正则化（repetitive regularization）、博弈论 (State-Adversarial Stochastic Game)
- **关键词**: mean-field MARL, state perturbation, adversarial training, action loss, SASG, scalability

## TL;DR（一句话总结）
针对可扩展但对状态扰动敏感的 Mean-Field Actor-Critic (MFAC)，提出 RoMFAC：在 actor 训练目标中加入"clean 与 adversarial 状态下动作差异"的 action loss 并施以重复正则化 (repetitive regularization)，并定义 State-Adversarial Stochastic Game (SASG) 证明动作损失收敛、对抗扰动可防御，从而在不损失干净性能的前提下提升大规模 MARL 对状态扰动的鲁棒性。

## 问题与动机 (Problem & Motivation)
MARL 决策依赖观测状态，观测的任何不确定性都会误导动作。MFAC 借助 mean-field 理论解决大量智能体的可扩展性问题，但本文发现其对状态扰动敏感，会显著降低团队回报。单智能体对抗攻防已有进展，但多智能体研究稀少且面临额外挑战：被扰动智能体数量未知、对部分智能体的扰动会影响其他智能体。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 对手对 M (≤N) 个智能体的状态施加确定性扰动 v_j: S→B_j（仅依赖当前状态、不随时间变化，仅扰动该智能体观测而不改变环境）；测试用 10-step PGD、ℓ∞ 预算 ε=0.075 的白盒攻击。
- **设定**: cooperative/competitive（battle、pursuit）；mean-field actor-critic；online，self-play 训练

## 方法 (Method)
1. **新 actor 目标函数**: 由两部分组成——基于采样 clean 状态期望累计折扣回报的 policy gradient 项，以及表示 clean 与 adversarial 状态下所采取动作差异的 action loss 项。
2. **Repetitive regularization**: 对 action loss 的权重 μ（及扰动界 ε）进行重复式变化（按公式分轮调度），使智能体既探索新的正向行为又持续增强对抗鲁棒性。
3. **SASG 建模**: 将目标函数推广到 stochastic game，定义 State-Adversarial Stochastic Game，研究其基本性质（动作损失收敛性、对抗扰动可防御性）。
4. 框架可迁移到 MFAC 之外的其他 MARL 方法。

## 理论贡献 (Theoretical Contributions)
- 证明所提 action loss function 收敛。
- 证明 SASG 在联合最优对抗扰动下不一定存在 Nash equilibrium，但对抗扰动仍可被防御（防御性的理论保证）。
- SA-MDP 被指出是 SASG 的特例。

## 实验 (Experiments)
- **环境/Benchmark**: MAgent 的两个场景：battle 与 pursuit（大规模多智能体）。
- **Baselines**: MFAC、SA-MFAC（固定权重 μ + 递增 ε）、SA-MFAC3（μ 恒定但 ε 重复变化）、RoMFAC1（μ 仅线性增加一次的消融变体）、RoMFAC。
- **评估指标**: 平均总回报、胜率、击杀对手数；在被攻击智能体数 0/8/16/32/48/64 下评估。

## 主要结果 (Key Results)
1. 未做鲁棒训练的 MFAC 在状态扰动下协作策略被严重破坏（攻击空格、行动散乱），被攻击智能体越多退化越严重。
2. RoMFAC 最有效：随被攻击智能体增加性能仅轻微下降，且在干净（0 攻击）环境下性能也优于其他方法（鲁棒性不牺牲干净性能）。
3. RoMFAC1 与 RoMFAC 对比体现 repetitive regularization 的重要性；将该正则化加到 SA-MFAC（即 SA-MFAC3）在 pursuit 场景提升明显。

## 局限与未来工作 (Limitations & Future Work)
当前聚焦 MFAC，未来拟将方法扩展到其他 MARL 方法；SASG 下 Nash 均衡不一定存在仍是理论限制；实验限于 MAgent 两个场景。

## 与综述的关联 (Relevance to Survey)
属于状态对抗鲁棒 MARL 中"对抗训练 + 正则化"路线，将单智能体 SA-MDP 思想扩展到 mean-field 大规模 MARL，并提供 SASG 博弈论分析。与 paper 28/29 的状态对抗博弈理论、QMIX 状态对抗鲁棒化等互补，强调可扩展性与干净性能保持。
