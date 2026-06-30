# 189. Byzantine-Resilient Multiagent Optimization

## 元信息 (Metadata)
- **标题**: Byzantine-Resilient Multiagent Optimization
- **作者**: Lili Su, Nitin H. Vaidya
- **机构**: MIT (CSAIL)；Georgetown University
- **发表**: IEEE Transactions on Automatic Control (TAC), Vol. 66, No. 5, 2021
- **链接/arXiv**: doi:10.1109/TAC.2020.3008139

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: Byzantine/容错（未知子集智能体任意对抗行为）、无中心协调节点的分布式攻击
- **方法范式**: distributed optimization、approximate Byzantine consensus + 本地梯度下降、(β,γ)-admissibility 刻画
- **关键词**: Byzantine-resilient, multiagent optimization, fault tolerance, distributed optimization, approximate consensus

## TL;DR（一句话总结）
研究无中心协调节点下的分布式多智能体优化中存在未知 Byzantine 故障智能体的问题，提出用 (β,γ)-admissibility 刻画 good agents 可达成的全局目标（局部代价函数的凸组合），给出不可能性下界与可证明 resilient 的算法（每步将 approximate Byzantine consensus 与本地梯度更新结合）。

## 问题与动机 (Problem & Motivation)
分布式多智能体优化常以"局部代价函数的平均"为全局目标，但该目标对 Byzantine 故障极其脆弱——哪怕单个对抗智能体即可完全操纵平均值。已有 Byzantine 容错工作多集中于 consensus，而无中心协调者的 Byzantine-resilient 优化研究稀缺。本文是最早研究该问题、并首次刻画可达全局目标凸系数结构的工作之一。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 未知子集（最多 b 个）智能体遭受 Byzantine 故障，可任意对抗；good agents 目标改为最小化 good agents 局部代价的"适当凸组合"而非全体平均
- **设定**: cooperative（good agents 协作）；decentralized（无中心协调，仅局部通信）；同步系统；聚焦标量局部代价函数

## 方法 (Method)
- 用 (β,γ)-admissibility 度量全局目标：γ 表示其凸组合至少非平凡涉及多少 good agents，β 表示权重下界
- 每个 good agent 每轮执行 approximate Byzantine consensus 更新（鲁棒地从邻居"收集"信息、过滤极端值）+ 本地 gradient descent 更新
- approximate consensus 用作在 Byzantine 存在下稳健聚合邻居信息的机制，而非 Blockchain 式的精确选择机制
- 给出依赖网络拓扑条件的可达 (β,γ) 刻画

## 理论贡献 (Theoretical Contributions)
- 不可能性（Theorem 1）：任何算法都无法保证 γ > n − φ − b（n 为智能体数，φ 为实际 Byzantine 数，b 为最大 Byzantine 数）
- 可达性（Theorem 3）：在特定拓扑条件下算法可保证一族 (β,γ)；完全图时达到 β = 1/(2(n−φ−b))、γ = n−φ−b，γ 匹配不可能性界，β 达最优值的 1/2 倍

## 实验 (Experiments)
- **环境/Benchmark**: 偏理论，无大规模实验；以完全图等拓扑做分析性刻画
- **Baselines**: 与"以平均为全局目标"的非鲁棒方案对比（说明其脆弱性）
- **评估指标**: (β,γ)-admissibility 可达性、与不可能性界的吻合度

## 主要结果 (Key Results)
- 首次刻画无中心协调下 Byzantine-resilient 优化可达全局目标的凸系数结构
- 完全图上算法的 γ 紧致匹配不可能性下界，β 达最优常数因子 1/2
- 揭示"平均目标"对单个 Byzantine 即崩溃，须改用 good agents 凸组合目标

## 局限与未来工作 (Limitations & Future Work)
结果限于标量局部代价函数，一般（多维/向量）局部函数留作重要未来方向；聚焦同步系统；β 与最优值仍差常数因子。

## 与综述的关联 (Relevance to Survey)
属控制论/分布式优化背景文献，是 robust MARL 中 [[Byzantine-resilient]] / 容错（fault-tolerance）方法线的邻接基础工作，为 MARL 中抵御恶意智能体、distributed optimization 下的鲁棒聚合提供理论范式（approximate consensus + 本地梯度、不可能性界），与 §通信攻击/智能体失效线相呼应。
