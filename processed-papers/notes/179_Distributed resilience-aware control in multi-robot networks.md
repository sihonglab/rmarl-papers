# 179. Distributed Resilience-Aware Control in Multi-Robot Networks

## 元信息 (Metadata)
- **标题**: Distributed Resilience-Aware Control in Multi-Robot Networks
- **作者**: Haejoon Lee, Dimitra Panagou
- **机构**: University of Michigan, Ann Arbor（Department of Robotics；Department of Aerospace Engineering）
- **发表**: IEEE CDC 2025；arXiv:2504.03120
- **链接/arXiv**: arXiv:2504.03120；doi:10.1109/CDC57313.2025.11312021

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: misbehaving / faulty agents（共享错误状态信息）、Byzantine/容错（resilient consensus），兼顾安全约束（碰撞规避）
- **方法范式**: resilient consensus（W-MSR）、Control Barrier Function (CBF)、distributed control、time-varying graph 充分条件
- **关键词**: resilient consensus, W-MSR, control barrier function, multi-robot networks, distributed control, collision avoidance

## TL;DR（一句话总结）
针对多机器人网络中存在 misbehaving 智能体时的 resilient consensus 问题，提出一个仅用本地信息、不依赖固定拓扑与全局状态估计的分布式 CBF 控制律：先给出基于 normal 智能体度数 (degree) 的时变网络 resilient consensus 充分条件，再据此设计同时保证 resilience 与避碰的控制器。

## 问题与动机 (Problem & Motivation)
多智能体 consensus 在存在共享错误信息的 misbehaving 智能体时性能退化，resilient consensus（如 W-MSR）依赖 r-robustness、(r,s)-robustness 等全局组合性网络性质，难以在线计算；现有 resilience-aware 方法或假设固定拓扑、或需要全局状态知识，在物理受限、安全与 resilience 冲突的动态环境中不现实，且 misbehaving 智能体共享的不可靠信息会破坏全局状态估计。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 网络中存在 misbehaving / 异常智能体，可能广播错误状态；采用 W-MSR 式过滤，要求保持 normal 智能体的局部连接（度数）以维持 resilience
- **设定**: cooperative 多机器人 consensus；fully distributed / decentralized；离散时间 W-MSR 动力学；single-integrator 机器人动力学、time-varying 通信图

## 方法 (Method)
- 建立时变网络下 resilient consensus 的充分条件，仅依赖 normal 智能体的 degree（邻居数），将其推广到离散时间 W-MSR（区别于 [7] 基于全体智能体度数的连续时间结论）
- 基于该充分条件设计 CBF 控制器，使每个 normal 机器人的度数维持在阈值以上，从而保持 resilient 结构
- CBF 同时编码避碰约束，保证 inter-agent collision avoidance
- 控制器只用本地可得信息（自身与邻居状态），不需估计全局状态或所有机器人的控制动作

## 理论贡献 (Theoretical Contributions)
给出时变网络中基于 normal 智能体度数的 resilient consensus 充分条件；并证明所提分布式控制器在一定假设下同时保证 resilience 与 safety（避碰）。偏控制理论保证，非样本复杂度型。

## 实验 (Experiments)
- **环境/Benchmark**: 多机器人导航仿真
- **Baselines**: 与依赖固定拓扑 / 全局状态估计的既有 resilience-aware CBF 方法对比（定性）
- **评估指标**: resilient consensus 是否达成、normal 智能体度数维持、避碰、对全局信息的依赖性

## 主要结果 (Key Results)
- 仿真验证所提分布式控制律可在无固定拓扑、仅用本地信息条件下保证 resilient consensus 与避碰
- 相比既有方法，聚焦 normal 智能体的局部连接而非全局 resilience 性质，消除了对不可靠全局状态估计的依赖，并显式处理了被以往 CBF 方法忽视的 inter-agent collision

## 局限与未来工作 (Limitations & Future Work)
仅用 single-integrator 动力学与仿真验证；充分条件可能保守；未涉及更复杂动力学、真实硬件或更强对抗模型；度数阈值与任务灵活性之间存在权衡。

## 与综述的关联 (Relevance to Survey)
属控制理论侧的 resilient consensus / 容错背景工作，与 robust MARL 中 [[Byzantine / fault-tolerance]] 线相邻：W-MSR 与 r-robustness 是去中心化 MARL 抵御 misbehaving 智能体的理论基石，与 [[resilient consensus]]、[[distributed control / CBF safety]] 主题相关，可为 MARL 通信层鲁棒性提供网络拓扑层面的保证。
