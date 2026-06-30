# 181. Distributed Robust Optimization for Multi-Agent Systems with Guaranteed Finite-Time Convergence

## 元信息 (Metadata)
- **标题**: Distributed Robust Optimization for Multi-Agent Systems with Guaranteed Finite-Time Convergence
- **作者**: Xunhao Wu, Jun Fu
- **机构**: State Key Laboratory of Synthetical Automation for Process Industries, Northeastern University, Shenyang, China
- **发表**: arXiv 2023（投稿 Automatica）；arXiv:2309.01201
- **链接/arXiv**: arXiv:2309.01201

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 数据/参数 bounded uncertainty（测量、估计、实现误差导致的不确定性），即 distributed robust convex optimization (DRCO)
- **方法范式**: distributed optimization、robust counterpart / right-hand restriction、cutting-plane 式上下界逼近、finite-time consensus
- **关键词**: distributed robust convex optimization, bounded uncertainty, uniformly strongly connected network, finite-time convergence, multi-agent systems

## TL;DR（一句话总结）
针对 uniformly strongly connected 网络下带 bounded uncertainty 的分布式鲁棒凸优化问题 (DRCO)，提出一个分布式算法，通过 distributed lower/upper bounding 两个过程逼近全局最优，并用两种分布式终止方法保证所有智能体在有限步内同时停止、收敛到满足一定精度全局最优的可行 consensus 解。

## 问题与动机 (Problem & Motivation)
现有约束型分布式优化算法大多只适用于无向、weight-balanced 网络，且假设所有智能体的本地数据完全精确；但真实问题数据常因测量/实现误差而不确定。已有 DRCO 算法（robust counterpart、random projection、scenario-based、cutting-plane 类）或局限于特殊约束结构、或不能保证本地可行性、或只渐近收敛、或仅满足零阶最优而无明确全局最优精度保证。本文动机是在最弱网络假设（uniformly strong connectivity）下，给出有限步内定位满足一定精度全局最优可行 consensus 解的算法。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: compact bounded uncertainty set，作用于约束/数据；目标函数严格凸；通过在有限多个不确定性点上 enforce 约束并对右端项做 restriction 来鲁棒化
- **设定**: cooperative 分布式优化；fully distributed；time-varying、unbalanced directed graph，仅需 uniformly strong connectivity；迭代式（非 RL）

## 方法 (Method)
- 基于 right-hand restriction 思想构造 DRCO 的两个近似问题
- distributed lower bounding：将 compact 不确定集离散为有限点、外逼近 DRCO，给出全局最优值下界
- distributed upper bounding：逐步收紧右端约束 restriction 参数并加密不确定集离散，给出上界
- 两过程的本地目标之和分别构成全局最优值的上下界；改造 [48] 的 finite-time consensus 算法，使所有智能体在上下界 gap 达到目标精度时同时终止（提出两种终止方法并比较）

## 理论贡献 (Theoretical Contributions)
证明该分布式鲁棒凸优化算法在有限步内终止；所有智能体 finite-time 收敛到满足一定精度全局最优的可行 consensus 解，并保证本地可行性——区别于仅渐近收敛或仅零阶最优的既有工作。偏优化理论保证。

## 实验 (Experiments)
- **环境/Benchmark**: 数值案例研究（numerical case study）
- **Baselines**: 与既有 DRCO / 分布式优化算法对比（含两种终止方法间的性能比较）
- **评估指标**: 上下界 gap 收敛、有限步终止、解的可行性与全局最优精度

## 主要结果 (Key Results)
- 数值实验验证算法有效，可在有限迭代内使全部智能体同时终止并达到指定精度
- 两种分布式终止方法的性能被对比；算法在最弱的 uniformly strong connectivity 假设下兼顾 finite-time 收敛、本地可行性与全局最优精度

## 局限与未来工作 (Limitations & Future Work)
依赖严格凸目标与 compact bounded uncertainty 假设；离散化点数与 restriction 参数影响精度-计算权衡；仅小规模数值验证；未涉及非凸目标或学习型 / RL 设定。

## 与综述的关联 (Relevance to Survey)
属 distributed robust optimization 背景/相邻工作，与 robust MARL 的联系在于 DRCO 是去中心化多智能体在数据不确定下达成 robust consensus 的优化基础，可视为 [[distributed optimization]]、[[robust consensus]] 线的理论支撑，与 MARL critic / 价值评估的分布式共识、不确定性集建模思想相通。
