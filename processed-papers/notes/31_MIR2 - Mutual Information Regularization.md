# 31. Robust Multi-Agent Reinforcement Learning by Mutual Information Regularization (MIR3)

## 元信息 (Metadata)
- **标题**: Robust Multi-Agent Reinforcement Learning by Mutual Information Regularization
- **作者**: Simin Li, Ruixiao Xu, Jingqiao Xiu, Yuwei Zheng, Pu Feng, Yuqing Ma, Bo An, Yaodong Yang, Xianglong Liu
- **机构**: Beihang University（State Key Lab of CCSE/SDE）；Nanyang Technological University；National University of Singapore；Peking University；Zhongguancun Laboratory
- **发表**: IEEE TNNLS, Vol.36 No.10, October 2025（在线 2025-07-10）
- **链接/arXiv**: https://github.com/DIG-Beihang/MIR3 ；DOI 10.1109/TNNLS.2025.3577259

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 合作智能体的动作不确定性 / 最坏情况对抗动作（部分智能体被劫持或失控）；附带验证观测噪声、动作失效、环境不确定性
- **方法范式**: control-as-inference、mutual information regularization、information bottleneck、robust action prior、off-policy evaluation（隐式 max-min）
- **关键词**: mutual information regularization, robust MARL, control-as-inference, information bottleneck, action uncertainty

## TL;DR（一句话总结）
受人类"保持总体警惕而非穷举威胁"启发，将 robust MARL 框为 control-as-inference，证明最小化 history-action 之间的互信息 I(h;a) 是最坏情况鲁棒性的一个下界，从而无需对抗训练即可获得对最坏对抗动作的鲁棒性。

## 问题与动机 (Problem & Motivation)
合作 MARL 部署时，部分智能体可能因软硬件故障或被攻击而执行不可预测/最坏情况动作。每个智能体可被扰动或不被扰动，使威胁场景随智能体数指数增长。现有 max-min 方法要么把所有智能体当对手（过度悲观、不合作，如 M3DDPG/ROMAX/ERNIE），要么枚举威胁场景（探索不足、test 时仍脆弱，如 ROM-Q/EIR），且计算代价高。需要一种无需穷举威胁、计算高效的鲁棒方法。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: Action Adversarial Dec-POMDP (A²Dec-POMDP)，用划分 φ∈{0,1}^N 表示哪些智能体为对手；被扰动智能体的策略被零和最坏情况对抗策略 π_α 替换；攻击发生在测试期、defender 参数固定，攻击者拥有与 defender 相同的局部观测和动作空间。
- **设定**: cooperative；CTDE（互信息用 I(s;a) 近似 I(h;a) 以可扩展）；训练时仅用 φ=0^N（无对抗输入），但目标求解 max-min

## 方法 (Method)
- 将 robust MARL 写成 J(π)=J0(π)+E_φ[min_{π_α} J_φ(π)]，用 importance sampling 把对抗轨迹的 off-policy 评估转换到正常轨迹上。
- 核心：在奖励中加入 −λ·I(h_t; a_t) 作为鲁棒正则（MIR3），仅是 reward shaping，因此可叠加在任意合作 MARL 算法（MADDPG/QMIX/MAPPO）上。
- 互信息精确值不可解，用 CLUB（上界估计器）估计 I 作为 −I 的下界；CTDE 下用 I(s;a) 单次估计整个 team。
- 两种解释：information bottleneck（用最小充分历史信息解决任务，抑制 agent 间虚假关联、避免过度反应）与 robust action prior（−I(h;a)=E[−KL(π(a|h)‖p(a))]，将 max-entropy 的均匀先验替换为学得的鲁棒动作先验 p(a)）。

## 理论贡献 (Theoretical Contributions)
- Proposition 1：J(π) ≥ Σ_t E[r_t − λ·I(h_t; a_t)]，即最小化 history-action 互信息最大化鲁棒性的一个下界（三步证明：零和博弈下最优鲁棒策略与最优对手 log 概率仅差常数 → uniform coverage 假设下推导所有攻击轨迹下界 → 下界即互信息定义）。
- Proposition 2：因 MIR3 只是 shaped reward、不改变策略/转移/观测空间，Bellman 算子为压缩映射，tabular 情形下收敛到最优值函数。
- 计算复杂度分析：训练仅额外做一次 MI 估计，测试期零额外开销。

## 实验 (Experiments)
- **环境/Benchmark**: SMAC（六个任务，含异构 2s4z vs 2s3z、大规模 9 vs 8m）、Quads 四旋翼集群（连续控制，MAPPO）、10 智能体 rendezvous 机器人集群（含真实世界 e-puck2 部署）。
- **Baselines**: M3DDPG、ROMAX、ERNIE（全员当对手）、ROM-Q（一个或多个对手）、EIR（MAPPO 下，识别不可靠智能体）；backbone 为 MADDPG/QMIX/MAPPO。
- **评估指标**: 最坏情况对抗攻击下的合作/鲁棒回报（95% 置信区间）、每 epoch 训练时间、超参 λ 与 MI 估计器消融、对非对抗扰动（观测噪声、动作重复、对手难度提升）的鲁棒性。

## 主要结果 (Key Results)
- 尽管训练时不接触对手，MIR3 在六个 SMAC 任务、两种 backbone 上的最坏情况鲁棒性一致超过所有显式建模对手的 baseline，并保持（甚至略增）合作性能。
- 对多个对手（5 vs 3m 两对手）及连续控制（Quads/MAPPO）同样领先；对非对抗扰动（观测/动作/环境）比 max-min 方法泛化更好。
- 训练开销远低于显式威胁建模方法（如 MADDPG 4v3m 仅 +10.71% vs baseline 的 +29%；rendezvous +3.28% vs +149.21%）；测试期零开销。
- 真实世界机器人集群部署中比最佳 baseline 平均回报高 14.29%，行为不被对手带偏（保持聚集/focused fire），并出现 emergent pursuit-evade 行为。λ=5×10⁻⁴ 为最优折中；对不同 MI 估计器（VUB/L1Out/CLUB-Sample）均稳健，CLUB 最佳。

## 局限与未来工作 (Limitations & Future Work)
理论依赖 uniform coverage 假设（offline RL 常用，实际可能不成立，但作者认为在鲁棒语境下反而有利）；收敛保证仅在 tabular 情形，实际用非凸神经网络；λ 需调参，过大会导致合作与鲁棒性同时崩溃。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"动作鲁棒性 / 无对抗的正则化方法"主线，与 M3DDPG、ROMAX、ERNIE（minimax/对抗正则化）形成对照，提供基于 control-as-inference + 信息论（互信息/information bottleneck/action prior）的新范式，并以真实世界部署验证 sim2real 鲁棒性。
