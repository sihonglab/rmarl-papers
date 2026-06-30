# 135. Robust Multi-Agent Reinforcement Learning Method Based on Adversarial Domain Randomization for Real-World Dual-UAV Cooperation

## 元信息 (Metadata)
- **标题**: Robust Multi-Agent Reinforcement Learning Method Based on Adversarial Domain Randomization for Real-World Dual-UAV Cooperation
- **作者**: Shutong Chen, Guanjun Liu, Ziyuan Zhou, Kaiwen Zhang, Jiacun Wang
- **机构**: Department of Computer Science, Tongji University, Shanghai（同济大学）；Monmouth University, NJ, USA
- **发表**: IEEE Transactions on Intelligent Vehicles (TIV), Vol. 9, No. 1, January 2024
- **链接/arXiv**: DOI 10.1109/TIV.2023.3307134

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 环境/模型不确定性、sim2real gap（仿真与现实差距）、传感器噪声/GPS 噪声、物理参数变化
- **方法范式**: 对抗训练（adversarial domain randomization，nature player）、minimax/robust Markov game、博弈论均衡（Nash equilibrium 存在性）、prioritized experience replay
- **关键词**: MARL, sim2real transfer, adversarial domain randomization, prioritized experience replay, dual-UAV cooperative transportation

## TL;DR（一句话总结）
提出 adversarial domain randomization (ADR) 方法，用一个"nature player"对抗式生成更合理/更具挑战的训练环境，将 MARL 建模为 adversarial stationary Markov game 并证明 Nash 均衡存在，从而训练出可稳定从仿真迁移到真实双 UAV 协同运输的鲁棒策略。

## 问题与动机 (Problem & Motivation)
多 UAV 紧密协同（如双机吊运货物）控制极复杂，MARL 依赖大量试错难以在真实世界采集数据，通常仿真训练后迁移真机。但 sim2real gap 难以保证迁移成功。传统 domain randomization 在预定义范围内均匀采样参数，导致策略不稳定（高方差）、收敛慢、难应对复杂情况。需要更高质量的随机化环境生成与更高效的采样方法。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不确定性由 domain randomization 参数集 U 建模（6 个物理/感知参数，如 GPS 位置噪声、主引擎强度等，bounded space）；nature player（μ）作为对抗者在 U 中选择最坏情况参数，agent 在最坏情况下最大化期望回报（max-min）。
- **设定**: cooperative（双 UAV 共享 team reward）；CTDE（部分可观，R-MADDPG + LSTM 推断 u 分布）；online 训练 + sim2real 迁移。

## 方法 (Method)
- **ADR / nature player**: 将带 domain randomization 的 MARL 建模为 nonstationary Markov game，进一步引入 nature player μ:S→U 最小化内层价值，得到 adversarial stationary Markov game，目标为 max_π min_μ；用 encoder-decoder 网络生成下一步随机化参数 u。
- **nature player 损失**: loss = α0·r + β0·KL − ω0·MSE，平衡对抗性（降低 agent reward）、KL（u 分布接近正态）、MSE（保证 u 随机性）；α0→1 偏对抗、α0→0 偏一般随机化。
- **基础算法**: 在 R-MADDPG 上加入 u 作为 critic 输入（式 11/12），用 LSTM cell state 处理部分可观与时序。
- **PERDRE**: 针对 domain randomization 经验的优先经验回放，按 critic loss 排名 + 子集回放次数逆排名计算重要性权重 Iw 与采样概率，加速收敛而不损性能。
- **分布式分层 sim2real 迁移**: 软件分为 Data Perception / Action Decision / Low-level Control 三层，同构分布部署到各 UAV 机载计算机，迁移时仅替换感知层模块。

## 理论贡献 (Theoretical Contributions)
- Property 1: 有限 S、U、A 的 nonstationary Markov game 中至少存在一个 nonstationary Markov perfect Nash equilibrium。
- Property 2: adversarial stationary Markov game 中至少存在一个 perfect Nash equilibrium（μ*, π*）（基于 robust Markov game 中 Nash 存在性结论 [45] 及 Markov game Nash 存在性）。
- 给出非平稳 Markov game 价值函数 Bellman 方程推导（附录 A）及算法时间复杂度分析。

## 实验 (Experiments)
- **环境/Benchmark**: (1) LunarLander-v2（单一随机化参数 MES，主引擎强度）；(2) Dual-UAV cooperative transportation（AirSim + Unreal Engine 仿真 + 真实双 UAV 系统，6 个随机化参数）。
- **Baselines**: DQN/R-MADDPG（固定环境无随机化）；UDRDQN/UDRMA（传统均匀 domain randomization）；ADRDQN/ADRMA（本文）；PERDRE vs RER（随机经验回放）。
- **评估指标**: mean reward、任务完成率（completion rate）、完成时间步、收敛速度、真机飞行试验成功率。

## 主要结果 (Key Results)
- LunarLander：MES 减小（任务变难）时 DQN 失效、UDRDQN 在中等 MES 后挣扎，ADRDQN 在挑战环境中稳定且能适应正常环境。
- Dual-UAV：随 GPS 噪声增大，R-MADDPG 失效、UDRMA 约 65% 完成率，ADRMA 各情况完成率 >75%；均匀随机化环境测试 ADRMA ~80%、UDRMA ~73%(波动大)、R-MADDPG ~45%。
- PERDRE 将收敛从约 10000 episode 提前到约 6000 episode 而不损性能（20000 episode 约 45 小时）。
- 真机迁移：R-MADDPG 难适应真实；Case III/IV 中 ADRMA 比 UDRMA 更稳定（但耗时更长）。

## 局限与未来工作 (Limitations & Future Work)
高维随机化参数下难以直观界定"更难"的环境；ADR 稳定但部分真机案例完成耗时更长；训练成本高（仿真串行交互慢）。未来：将 ADR + PERDRE 与不同 RL 算法结合用于更多实际任务；进一步改进 domain randomization 方法。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"环境/模型不确定性 + 对抗训练"主线与 sim2real 鲁棒迁移应用线；用对抗 nature player 实现 max-min robust Markov game 并提供 Nash 均衡存在性理论，是对抗训练 + 博弈论均衡 + 真实机器人部署相结合的代表性工作。
