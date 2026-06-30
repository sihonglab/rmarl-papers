# 15. Multi-agent Policy Evaluation via Primal-dual Online Time-averaging

## 元信息 (Metadata)
- **标题**: Multi-agent Policy Evaluation via Primal-dual Online Time-averaging
- **作者**: Gang Chen, Changli Pu, Yaoyao Zhou
- **机构**: School of Automation, Chongqing University, Chongqing, China
- **发表**: Preprint submitted to Journal of Parallel and Distributed Computing, 2023（未正式同行评审，SSRN preprint）
- **链接/arXiv**: https://ssrn.com/abstract=4564190

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 环境不确定性（时变、联合连通的通信拓扑）、外部噪声（external/Gaussian noise）对估计的影响
- **方法范式**: 分布式优化、primal-dual saddle point（Fenchel 对偶）、MSPBE 最小化、online time-averaging（Laplacian averaging）
- **关键词**: distributed policy evaluation, primal-dual, MSPBE, time-varying digraph, online time-averaging

## TL;DR（一句话总结）
本文针对协作 MARL 的分布式策略评估问题，将 MSPBE 最小化经 Fenchel 对偶转化为 primal-dual 鞍点问题，并提出带 online time-averaging 的分布式算法，在时变且联合连通的有向通信网络下证明了 sublinear 收敛，提升对噪声和通信不确定性的鲁棒性。

## 问题与动机 (Problem & Motivation)
协作 MARL 中的策略评估若使用中心控制器，存在维护成本高、易受攻击/失效、无法保护隐私等问题。现有分布式方案多假设无向、固定拓扑，难以应对实际中的隐私导致的单向通信与不确定环境导致的时变/间歇连通网络，且对外部噪声敏感。本文针对两种场景：(1) 一组 agent 并行计算评估给定联合策略的值函数；(2) 状态空间划分为子空间，各 agent 在各子空间分布式探索。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不确定性体现在通信网络（时变、联合连通有向图，weight-balanced，Assumption 1）以及估计过程中的 ubiquitous/外部噪声（实验中加 Gaussian noise）；非对抗智能体攻击模型
- **设定**: cooperative；fully distributed / decentralized（neighbor 通信，无中心控制器）；online

## 方法 (Method)
- 用线性函数逼近 Vθ(s)=φ(s)ᵀθ，将策略评估写为 MSPBE 最小化（含正则项），再写成加权最小二乘形式 ½‖Aθ−b‖²_{C⁻¹}+½ρ‖θ‖²。
- 利用 Fenchel duality 引入对偶变量 ω，将其转为 primal-dual 鞍点问题，并以一致性约束（θ₁=…=θ_N）写成分布式 consensus 形式。
- 提出 Algorithm 1：primal-dual 协议同时做 (i) 基于时变 Laplacian 的 consensus 更新、(ii) 梯度上升/下降、(iii) online time-averaging（对 θ、ω 做运行时间平均 θ^a、ω^a）以平滑噪声影响。
- 两类学习率：常数率 η=ε/T^△（0.5<△<1）与时变率 η_t=ε/√t。

## 理论贡献 (Theoretical Contributions)
- Theorem 1：在 Assumption 1 下，consensus 约束随 T→∞ 满足。
- Theorem 2：常数学习率下收敛率 O(1/T^{1−△})。
- Theorem 3：时变学习率 η_t=ε/√t 下收敛率 O(1/√t)。
- 给出 primal-dual 累积估计误差上下界（Lemma 3–5）。

## 实验 (Experiments)
- **环境/Benchmark**: Mountain Car（并行计算场景，6 个 agent，SARSA 采样）；9×6 网格划分为 6 个 3×3 子网格的分布式探索场景（6 个机器人）
- **Baselines**: inexact ADMM [18]（仅适用无向图，对比于无向 cycle graph）
- **评估指标**: MSPBE（估计误差 J）收敛曲线、θ^a 一致性收敛、不同图拓扑/学习率下的收敛速度、对 Gaussian 噪声的免疫性

## 主要结果 (Key Results)
- 在时变、联合连通拓扑下 primal-dual 估计误差仍收敛，时变学习率收敛速度快于常数学习率，增益 ε/k 越大收敛越快。
- 与 inexact ADMM 精度相当（均达 ~1% 误差），但本算法无需对 C 求逆，计算复杂度更低。
- online time-averaging 的 θ^a 在 Gaussian 噪声下平滑且更好收敛到最优解，验证抗噪声鲁棒性。

## 局限与未来工作 (Limitations & Future Work)
- 仅做策略评估（policy evaluation），未涉及策略优化/控制；网格场景做了 3×3 的简化；为 preprint，未经同行评审。鲁棒性偏向通信不确定与噪声平滑，非对抗式威胁。未来工作未明确。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"通信/网络不确定性 + 噪声鲁棒"线路，结合分布式优化（primal-dual、MSPBE、Fenchel 对偶）与协作 MARL 策略评估；可与 networked MARL、distributed TD/GTD、saddle-point 优化等主题对照，是面向通信鲁棒性的理论性工作。
