# 47. Camouflage Adversarial Attacks on Multiple Agent Systems

## 元信息 (Metadata)
- **标题**: Camouflage Adversarial Attacks on Multiple Agent Systems
- **作者**: Ziqing Lu, Guanlin Liu, Lifeng Lai, Weiyu Xu
- **机构**: University of Iowa；University of California, Davis
- **发表**: 未明确（arXiv preprint）2024
- **链接/arXiv**: arXiv:2401.17405v1

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动（新型 camouflage 攻击，间接改变受害者观测）；与 state perception attack 对比
- **方法范式**: 攻击设计（offline/规划）；dynamic programming + within-step constrained optimization；博弈/MDP 理论分析
- **关键词**: camouflage attack, state perception attack, MARL, dynamic programming, cost-constrained attack, Markov game

## TL;DR（一句话总结）
提出一种新型对抗攻击"camouflage attack"：攻击者只改变其可控物体（或自身）的外观而不改变其真实状态，使所有受害 agent 观察到相同（相关）的被伪装外观从而被误导，并用 between-step 动态规划求最优伪装攻击，证明其效果可逼近更难实现的 state perception 攻击。

## 问题与动机 (Problem & Motivation)
MARL 用于安全攸关应用，需研究对抗攻击以评估最坏情况、构建鲁棒系统。已有攻击（action/reward/state poisoning、state perception）多直接改变受害者的属性或可任意操纵不同受害者的观测，但这种"自由"操纵在现实中难以实现。作者提出更实际的攻击：仅改变可控物体外观，多个受害者因看到同一伪装物体而产生相关/相同的错觉。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: m 个攻击者 vs n 个受害 agent；双方都已知受害者最优策略，受害者不知攻击存在。每个时间步分两阶段：先攻击使 agent 进入 delusional 状态 s_d，再按最优策略行动。Camouflage：外观 Y=g(X)，agent 观测 s_d=h_i(g(X))；不同受害者的错觉必须相关/相同（区别于可自由操纵的 state perception）。还考虑 instant cost-constrained（每步预算 B，攻击成功概率随预算与伪装距离变化）。
- **设定**: competitive（攻击者 vs 受害者群体）；attackers 视角的规划/offline 优化；受害者为 selfish、共享状态/动作空间与最优策略

## 方法 (Method)
1. 用 between-step dynamic programming + within-step static constrained optimization 计算最优伪装攻击：从 t=T 反向求每个 DPS 的值函数。
2. Within-step：在预算约束下优化攻击者预算分配向量 b，最小化转移到下一步各 DPS 的期望值 Σ P(b,·)·V*。
3. Between-step：用状态转移与期望奖励反向递推值函数 V*。
4. 建模攻击成功概率为预算/伪装难度的函数（伪装目标越近、预算越多越易成功）。

## 理论贡献 (Theoretical Contributions)
- Lemma IV.1：对带等式约束 vs 无约束的可分优化，给出最优值差距上界 o2 ≤ o1 ≤ o2 + min_j{C_j}。
- Theorem IV.2：当观测函数相同（受害者错觉一致）时，最优 camouflage 攻击下总奖励 TR^ca 介于最优 state-perception 攻击 TR^spa 与 TR^spa + min_j Σ C_ij 之间，即 camouflage 攻击效果可逼近更强的 state perception 攻击。

## 实验 (Experiments)
- **环境/Benchmark**: 小型合成 MDP/Markov game（T=5）：环形拓扑（3 状态，2 受害者 + 2 攻击者）；q×q 棋盘（q=3、q=2）
- **Baselines**: 无攻击；（自由）state perception 攻击
- **评估指标**: 受害者群体的期望总奖励（随时间累计）；预算对攻击效果的影响

## 主要结果 (Key Results)
1. 环形场景下 camouflage 攻击使奖励降至无攻击的 34.4%，而 state perception 攻击为 33.1%，二者接近——更易实现的 camouflage 攻击效果可与更强攻击相当。
2. 棋盘场景同样显著降低受害者奖励，框架适用于一般 m 攻击者-n 受害者。
3. cost-constrained 情形下，攻击预算越大，受害者获得奖励越小。

## 局限与未来工作 (Limitations & Future Work)
仅在小规模合成环境（有限 T、小状态空间）验证，偏理论；假设双方已知最优策略、受害者独立同策略；未涉及防御方法与大规模/深度 MARL 扩展。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 的攻击侧研究，提出新的、更现实的观测层攻击范式（间接、跨受害者相关的伪装），并理论刻画其与 state perception 攻击的关系，可作为评估 MARL 观测鲁棒性最坏情况的攻击模型补充。
