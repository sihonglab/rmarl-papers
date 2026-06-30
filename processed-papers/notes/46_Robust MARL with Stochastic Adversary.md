# 46. Robust Multi-Agent Reinforcement Learning with Stochastic Adversary

## 元信息 (Metadata)
- **标题**: Robust Multi-Agent Reinforcement Learning with Stochastic Adversary
- **作者**: Ziyuan Zhou, Guanjun Liu, MengChu Zhou, Weiran Guo
- **机构**: Tongji University（同济大学）；Zhejiang Gongshang University；New Jersey Institute of Technology (NJIT)
- **发表**: ICML (PMLR) 2025
- **链接/arXiv**: 未明确

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动（ε-bounded ℓ∞ 观测对抗扰动）
- **方法范式**: 对抗训练；factorized maximum-entropy MARL（soft policy）；policy-adversarial director + generator；CTDE（VDN/QMIX 主干）
- **关键词**: adversarial training, stochastic adversary, maximum entropy, observation perturbation, CTDE, robust MARL

## TL;DR（一句话总结）
提出 ATSA：用一个由 Stochastic Director (SDor) 与 SDor-guided Generator (STor) 组成的随机对抗者在线对抗训练，SDor 在最小化团队回报同时最大化策略熵给出策略扰动建议，STor 按建议生成观测扰动，从而避免对最强对抗者的过拟合并保持干净环境性能。

## 问题与动机 (Problem & Motivation)
MARL 模型对观测扰动敏感，可信度低。已有对抗训练存在两大问题：(1) 过拟合到对抗扰动——用最强对抗者训练会丢失干净环境性能；(2) actor 与 director 不对齐——把 SARL 的 policy adversarial actor-director 框架搬到 MARL 时，STor 生成的观测扰动与 director 意图不一致，导致训练不稳定。此外直接套用分类任务对抗训练存在短期/长期目标错配、高维动作空间困难等挑战。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 观测对抗者，扰动限制在 clean 观测的 ε-bounded ℓ∞ 球 B^i_ε 内。形式化为 OD-POMDP（观测对抗）与 PD-POMDP（策略对抗，动作空间为策略扰动方向）。SDor 用随机软策略（最大熵）而非最强确定性对抗者。
- **设定**: cooperative；CTDE；online（对抗者与 protagonist 在线交替训练）；discrete action + deterministic protagonist policy

## 方法 (Method)
1. 将 PD-POMDP 视为概率图模型，引入最优性变量，定义 SDor 的最大熵目标（最小化团队回报 + 最大化策略熵）。
2. SDor 用 factorized soft policy iteration 学习，满足 individual-global-optimal 条件；通过软 Bellman backup 与 TD 误差训练个体 soft-Q、joint/individual soft value 与 weight 网络，策略梯度更新个体软策略。
3. STor 在给定 SDor 动作下，通过最小化 protagonist 在对抗观测与 clean 观测下策略的 KL 散度，用 FGSM 求解生成观测扰动。
4. 提出 SDor-STor loss（cross-entropy）量化 STor 实际扰动与 SDor 建议扰动之间的差距，并加入 SDor 个体策略目标（系数 κ）以对齐二者。

## 理论贡献 (Theoretical Contributions)
- Theorem 3.4：factorized soft policy iteration 收敛到全局最优 joint soft policy。
- Proposition 3.2/3.3：给出最大熵目标下最优 joint/individual soft 策略形式。
- Theorem 3.5：SDor 的最优 joint soft policy 与最优 STor 结合可诱导针对 protagonist 的最优随机观测对抗者。

## 实验 (Experiments)
- **环境/Benchmark**: SMAC（3m, 3s_3z, 8m）；Connected and Autonomous Vehicles (CAV) 自动驾驶场景（3 AV + 1–4 人驾车）
- **Baselines**: NoAdv, Random Noise, FGSM, ATLA, PAAD, PR, PR-REP, ERNIE, RAP, ROMANCE-p/s；主干 VDN 与 QMIX
- **评估指标**: SMAC 胜率（500 episodes）；CAV 累计奖励与碰撞率 CR；在六种对抗者下的平均（AVG）

## 主要结果 (Key Results)
1. SMAC 上 ATSA 训练的 protagonist 在六种对抗者下平均胜率最高（如 QMIX 在 3m/3s_3z/8m 的 AVG 达 0.99/0.98/0.99），显著优于基线（Wilcoxon p<0.05）。
2. ATSA 在干净（NoAdv）与随机噪声环境同样保持高性能，未因对抗训练而过拟合；ROMANCE、ATLA 等在多种对抗下崩到接近 0。
3. CAV 场景下 ATSA 在多数对抗者下取得较高奖励与较低碰撞率，整体鲁棒性领先。

## 局限与未来工作 (Limitations & Future Work)
方法面向 discrete action + deterministic protagonist policy 设定；引入额外超参数（温度 α、对齐系数 κ）与训练复杂度；连续动作/随机策略扩展、更大规模场景未在正文充分讨论。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"观测对抗 + 对抗训练"主线，核心在于用 maximum-entropy 随机对抗者缓解过拟合，并用 director-generator 对齐损失解决 actor-director 错配，与 ATLA/PAAD/ROMANCE 等可证明最优对抗者方法形成对比，是 CTDE 下观测鲁棒训练的代表性工作。
