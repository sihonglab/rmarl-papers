# 56. A Framework for Scalable Heterogeneous Multi-Agent Adversarial Reinforcement Learning in IsaacLab

## 元信息 (Metadata)
- **标题**: A Framework for Scalable Heterogeneous Multi-Agent Adversarial Reinforcement Learning in IsaacLab
- **作者**: Isaac Peterson*, Christopher Allred*, Jacob Morrey, Mario Harper（*共同一作）
- **机构**: Utah State University；US DEVCOM Army Research Laboratory（Allred）
- **发表**: 未明确（arXiv preprint，2025）
- **链接/arXiv**: arXiv:2510.01264v1 [cs.LG]；代码 https://directlab.github.io/IsaacLab-HARL/

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体 / 竞争性对手（adversarial competition，异构对手）
- **方法范式**: 对抗训练 / self-play；HAPPO（Heterogeneous-Agent PPO）+ team-specific critics；CTDE；课程学习（curriculum + zero-buffer）；高保真物理仿真平台/benchmark
- **关键词**: heterogeneous MARL, adversarial RL, IsaacLab, HAPPO, curriculum learning, robotics simulation

## TL;DR（一句话总结）
扩展 IsaacLab 仿真平台，提出 HARL-Adversarial (HARL-A) 框架，通过引入 team-specific critics 的 HAPPO 与课程学习，支持在高保真物理仿真中可扩展地训练形态/能力异构、目标非对称的多智能体对抗策略，并提供 Sumo/Soccer/3D Galaga 等 benchmark。

## 问题与动机 (Problem & Motivation)
MARL 在机器人协作中成功，GPU 并行仿真器（IsaacLab、MuJoCo）使大规模训练可行，但许多真实应用（pursuit-evasion、安全、竞争性操作）是竞争而非纯协作，且涉及形态/观测/动作异构、接触丰富的物理动力学。已有工作要么聚焦协作或简化对抗任务、缺乏异构形态，要么是孤立实现而非可扩展框架。缺少一个面向高保真仿真的可扩展、异构、对抗 MARL 统一框架。本文填补此空白。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 对手为另一队（可不同数量、不同形态/观测/动作）的竞争性智能体，近零和（r^(0) = -r^(1)）；鲁棒性来自对抗训练使策略能预判和反制对手策略。
- **设定**: competitive / adversarial（零和），异构 heterogeneous teaming；CTDE（centralized training, decentralized execution），每队独立 critic；online 训练（alternating "leapfrog" 冻结一方 vs 同时训练两方）

## 方法 (Method)
- 在 IsaacLab 中把已有的协作异构 HARL 管线扩展到对抗域；关键修正：单一共享 critic 在零和下会使 V(s)≈0、advantage 消失、PPO 梯度退化，因此引入 team-specific critics（HAPPO 形式），每队 critic 学对齐自身奖励的 V^(i)(s)，保证非平凡 advantage 信号。
- 课程学习：将复杂对抗任务分解为渐进阶段（Sumo: 走到点 → 推方块 → 直接对抗），用 zero-buffer 策略（占位零特征后续替换）保持观测空间一致、实现跨阶段策略无缝迁移。
- 设计 benchmark 环境：Sumo（Anymal C 四足 vs Leatherback rover，同构与异构队）、Soccer（1v1 异构）、3D Galaga（MiniTanks vs Crazy Fly 无人机的空地拦截）。
- 两种对抗训练范式：alternating（冻结一方更新另一方）与 simultaneous（同时更新），框架对两者均鲁棒。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（主要贡献是框架/benchmark与工程，理论上仅论证零和下共享 critic 导致 advantage 消失、需 team-specific critics）

## 实验 (Experiments)
- **环境/Benchmark**: 自建 IsaacLab 高保真物理环境——Sumo（同构/异构）、Soccer（1 Anymal vs 1 Leatherback）、3D Galaga；RTX 30/40 系 GPU 训练
- **Baselines**: 训练后策略 vs 其初始化版本（win rate）；与 heuristic/无对手感知微调策略对比；zero-buffer 有无对比
- **评估指标**: win rate（每 episode 1000 环境实例）、收敛曲线、涌现行为（定性）

## 主要结果 (Key Results)
- 引入 team-specific critics 后可在零和异构设定下稳定训练；trained 策略 win rate 随时间持续上升、untrained 对手 win rate 下降，证明有效对抗学习。
- 异构队涌现 role specialization：Leatherback rover 学会破坏 Anymal 腿部稳定（disruptor），Anymal 学会拖拽 rover 出界（grappler），无显式角色分配即出现分工。
- 课程学习 + zero-buffer 虽初期收敛变慢，但可在后续阶段无缝扩展状态空间、避免从头训练，加速整体课程；alternating 与 simultaneous 训练均产生有效策略（稳定性不同）。

## 局限与未来工作 (Limitations & Future Work)
- 3D Galaga 仅展示对抗交互而非真正对抗训练（策略不在线适应对手），属迁移/涌现能力证据。
- 对抗学习随机性强，涌现行为依赖随机初始化。
- 未来：集成 value-decomposition、graph attention network 等更多 MARL 算法；针对对抗域的 off-policy 方法提升鲁棒性；引入 exploitability、cross-play、对新对手鲁棒性等更丰富评估。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"对抗训练 / 竞争性 self-play 提升鲁棒性"线，并提供面向 embodied robotics 的高保真异构对抗 benchmark 平台。强调异构形态、接触动力学下的对抗竞争，可与 self-play 涌现复杂度（如 #55）、对抗扰动/正则化鲁棒训练对照，并为 robust MARL 评估（exploitability、对新对手鲁棒性）提供基础设施。
