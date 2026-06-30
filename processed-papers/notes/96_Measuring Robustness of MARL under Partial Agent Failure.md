# 96. Measuring the Robustness of Multi-Agent Reinforcement Learning Systems under Partial Agent Failure

## 元信息 (Metadata)
- **标题**: Measuring the Robustness of Multi-Agent Reinforcement Learning Systems under Partial Agent Failure
- **作者**: Zoltán Barta, Balázs Nagy, László Gulyás
- **机构**: Department of Artificial Intelligence, ELTE Eötvös Loránd University, Budapest, Hungary
- **发表**: Intelligent Robotics FAIR 2025 (IntRob '25) 2025
- **链接/arXiv**: https://doi.org/10.1145/3759355.3759373

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 智能体部分失效（partial agent failure）、观测/状态扰动（observation noise，传感器退化）
- **方法范式**: 实证评估 / fault injection 框架（非新算法），CTDE + MAPPO benchmark
- **关键词**: MARL, Robustness, MAPPO, Continuous Control, Partial Agent Failure, Reward Shaping

## TL;DR（一句话总结）
通过在评估阶段向部分智能体注入高斯观测噪声的故障注入框架，系统性测量 MAPPO 在两类合作导航任务下的鲁棒性，发现鲁棒性失效轴（受 agent 比例支配还是受噪声幅度支配）由 reward shaping 决定，且少数拓扑中心“hub”智能体主导整体失效。

## 问题与动机 (Problem & Motivation)
现实多机器人系统中传感器退化、执行器故障、通信丢失等部分失效不可避免，但多数 MARL 研究假设理想运行条件。现有鲁棒性工作主要聚焦于针对性、梯度攻击的最坏情况，对自然发生的传感器噪声与部分失效如何与任务级 reward 设计交互研究不足。本文以实证方式填补该空白。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 在评估（非训练）阶段对选定比例（10%/30%/50% 等）的智能体观测加零均值高斯噪声 õ_i = o_i + N(0, σ²)；同时变化噪声强度 σ（0–4.0）与受影响智能体比例（0–100%）。非对抗性、随机性扰动。
- **设定**: cooperative；CTDE（训练集中、执行去中心化）；训练时干净（noise-free），仅评估时注入扰动（online 训练 / 评估期扰动）

## 方法 (Method)
- 训练阶段：在无噪声环境用标准 MAPPO（actor-critic, CTDE, 参数共享, TorchRL 实现）训练，多随机种子（5 次独立 run）。
- 评估阶段故障注入：选取一定比例智能体，对其观测加高斯噪声，构建噪声评估环境网格（σ × 受影响比例）。
- 性能度量：以全局共享奖励（global reward）比较干净 vs 噪声场景，量化部分失效影响。
- 评估协议遵循 Gorsane et al. 的标准化合作 MARL 评估方案，聚合最后 50% checkpoint。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证。

## 实验 (Experiments)
- **环境/Benchmark**: VMAS（Vectorized Multi-Agent Simulator）中两个合作任务——Navigation（带碰撞惩罚 -1）与 Sampling（高斯密度场采样，无碰撞惩罚），均 10 智能体、连续动作/观测、全可观测。
- **Baselines**: 环境提供的启发式（heuristic）解法（带 lidar 反馈的避碰导航 / 朝高采样值区域引导）。
- **评估指标**: episodic return / 平均全局奖励；相对未扰动性能的退化百分比；return 标准差（不稳定性）。

## 主要结果 (Key Results)
- Navigation（有碰撞惩罚）：失效受“受影响智能体比例”支配。≤30% 失效时即使 σ=4.0 仍保留 ≥70% 干净奖励；≥50% 失效后奖励近线性下降，全部失效时相对变化 −144%。
- Sampling（无碰撞惩罚）：失效受“噪声幅度”支配。σ≲0.6 时即使 100% 智能体被污染仍近最优；一旦噪声半径超过 hotspot 半径，奖励对所有比例几乎同步崩塌。
- 方差分析揭示：位于智能体簇核心的中心“hub”智能体起不成比例的关键作用，其失效通过协调崩溃级联放大损失；相同噪声/比例下因涉及哪些具体智能体不同，return 可差异 >40%。
- 神经网络泛化提供“免费”的有限鲁棒性，但超过任务特定 breakpoint 后无法自行补偿。

## 局限与未来工作 (Limitations & Future Work)
仅评估单一算法（MAPPO）与两个 VMAS 任务，噪声仅为高斯观测噪声（非对抗）。未来：训练环境应反映真实约束（显式惩罚不安全碰撞）；识别并保护“critical/hub”智能体（冗余传感器、备份控制器）；研究 fault-isolation 机制防止误差传播；深入分析部分感知污染对全局性能的影响。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中“鲁棒性测量/实证评估”与“智能体失效（partial agent failure）/观测扰动”主题线。强调 reward shaping 对鲁棒性失效模式的决定作用，以及 critical agent 的概念，与 critical-agent 攻击测试（如 He et al. 2023、Zhou & Liu 2023、Guo et al. 2022）形成呼应，但本文是非对抗的自然故障视角。
