# 118. Robust Regional Coordination of Inverter-Based Volt/Var Control via Multi-Agent Deep Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Robust Regional Coordination of Inverter-Based Volt/Var Control via Multi-Agent Deep Reinforcement Learning
- **作者**: Hangyue Liu, Cuo Zhang, Qingmian Chai, Ke Meng, Qinglai Guo, Zhao Yang Dong
- **机构**: University of New South Wales (UNSW), Sydney; Tsinghua University
- **发表**: IEEE Transactions on Smart Grid, Vol. 12, No. 6, 2021
- **链接/arXiv**: DOI: 10.1109/TSG.2021.3104139

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 环境/模型不确定性（PV 发电与负荷的时空不确定性，spatial & temporal uncertainties）；通信与逆变器响应延迟引起的扰动
- **方法范式**: MADDPG（CTDE）+ stochastic programming（scenario-based）；behavior cloning + expert target Q 初始化 + prioritized experience replay
- **关键词**: Volt/Var control, MADDPG, active distribution network, stochastic programming, uncertainty robustness

## TL;DR（一句话总结）
将主动配电网分区为多个子网（每个子网为一个 agent），用改进的 MADDPG 算法在 POMG 框架下学习逆变器无功设定值，并通过随机规划处理 PV/负荷的时空不确定性，实现实时、鲁棒的区域协调 Volt/Var 控制。

## 问题与动机 (Problem & Motivation)
配电网中高 PV 渗透带来电压偏差与网损问题。传统基于规则/数学/启发式的 VVC 方法在大规模系统及考虑不确定性时计算开销大甚至不可行；集中式方法存在通信、隐私与可扩展性问题；已有 DRL 方法多为集中式且未充分考虑可再生能源与负荷的时空波动，也未利用专家历史运行数据来改善训练。本文旨在用改进 DRL 实现毫秒级实时决策并在时空不确定性下鲁棒地调压降损。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不确定性作用于 PV 最大功率点出力与有功/无功负荷；spatial uncertainty 基于日前/小时前预测区间，temporal uncertainty 基于实时小幅波动（含通信与逆变器响应延迟）；通过 Monte Carlo 在预测区间内采样场景，并以场景发生概率加权目标，违约次数跨所有场景累加进惩罚项。
- **设定**: cooperative；CTDE（centralized training, decentralized execution）；online 决策（执行时仅用本地观测）

## 方法 (Method)
- 将多区域协调 VVC 建模为 partially observable Markov Game（POMG），每个子网控制中心为一个 agent，动作为逆变器连续无功设定值，奖励为电压偏差+网损+电压越限惩罚的负值。
- 采用改进 MADDPG：集中式 critic 使用全局状态-动作，策略网络仅用本地观测执行。
- 用 stochastic programming 将时空不确定性嵌入奖励：对每个决策时刻生成 U 个 temporal 场景，目标用场景概率 ξu 加权，电压违约跨场景求和。
- 训练增强：behavior cloning 预训练策略网络、用专家目标 Q 值估计预训练 Q 网络、proportional prioritized experience replay（含 flash replay 缓冲以减少优先级重算）。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（附录给出从状态-动作值函数到 Bellman 方程的标准推导，但无新收敛性或样本复杂度证明）。

## 实验 (Experiments)
- **环境/Benchmark**: IEEE 123-node feeder system，分为 4 个互联子网；PV 渗透率 100%；PV-peak 与 load-peak 两种工况；并测试网络重构（不同拓扑）场景。
- **Baselines**: 基于场景的数学随机优化（SOCP + GUROBI，记为 Math）；随机初始化 MADDPG（Rand. Init.）；自训练初始化 MADDPG（Self. Init.）。
- **评估指标**: 最大电压偏差 Vmax、平均绝对电压偏差 Vmean、网损 Ploss、违约场景数、训练时间、在线优化时间。

## 主要结果 (Key Results)
- 所提方法收敛更快、性能更优；在线决策时间约 0.014 秒，远快于数学随机优化，适合在线使用。
- 在 5000 个 Monte Carlo 实现场景下鲁棒性检验：所提方法与数学方法均能实现零运行违约，且所提方法网损更低、电压偏差可比。
- 在网络重构（拓扑改变）下仍保持高适用性与优于数学方法的性能，证明对拓扑变化鲁棒。

## 局限与未来工作 (Limitations & Future Work)
- 仅处理连续无功资源；未来将纳入 OLTC、可投切电容器、soft open point 等离散变量设备。
- 不确定性采用已知（均匀）分布；未来考虑分布模糊性（ambiguity set / distributionally robust）。
- 未来引入多任务机器学习处理多个冲突目标。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 在电力系统（智能电网）应用线，鲁棒性来源于对环境（可再生能源/负荷）不确定性的处理而非对抗攻击。代表"stochastic programming + CTDE MADDPG"实现 distributional/uncertainty robustness 的应用范式，可与基于 DRMG 理论或对抗训练的方法形成对照。
