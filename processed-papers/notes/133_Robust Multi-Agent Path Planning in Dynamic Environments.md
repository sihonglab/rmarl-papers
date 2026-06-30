# 133. Robust Path Planning through Multi-Agent Reinforcement Learning in Dynamic Environments

## 元信息 (Metadata)
- **标题**: Robust Path Planning through Multi-Agent Reinforcement Learning in Dynamic Environments
- **作者**: Jonas De Maeyer, Hossein Yarahmadi, Moharram Challenger
- **机构**: University of Antwerp (UA) & Flanders Make（比利时）；Ayatollah Boroujerdi University（伊朗）
- **发表**: Technical Report 2025（arXiv preprint，未正式 venue）
- **链接/arXiv**: arXiv:2511.15284v1 [cs.RO]

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 环境动态变化 / 不确定性（动态障碍物随时间出现，引入路径规划不确定性）
- **方法范式**: 分层环境分解（hierarchical decomposition）、tabular Q-learning、federated Q-learning（FedAsynQ）、基于成功率的再训练触发
- **关键词**: Path Planning, MARL, Dynamic Environment, Federated Q-learning, Hierarchical Planning

## TL;DR（一句话总结）
提出一种基于分层环境分解 + 联邦 Q-learning 的 region-aware MARL 框架，使移动机器人在含动态障碍物的环境中能高效、有针对性地局部再规划路径，鲁棒适应环境变化。

## 问题与动机 (Problem & Motivation)
传统路径规划算法（A*、Dijkstra）假设环境静态且完全已知，在动态、未知环境中失效。已有 MARL 方法多假设环境变化不可定位，导致大量不必要的全局重规划。Yarahmadi et al. 提出区域分解的局部重规划方法，但存在：依赖全局规划器（未知环境不可用）、每次变化即触发重训练、子环境间无连接关系（无可行回退路径）、评估场景过于简单（每步仅一个障碍变化）等局限。本文针对这些缺陷改进。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不确定性来自环境中动态障碍物的随时间变化（位置未知但变化可被局部检测/定位，confined to bounded region）；非对抗性扰动，而是自然动态性。
- **设定**: cooperative（federated 协作）；DTDE / 分布式（federated Q-learning，无全局规划器，契合 DAI）；online 学习与再训练。

## 方法 (Method)
- **分层分解框架**: 将环境递归二分为子环境，组织成树（root=整个环境，leaf=最小原子区域）；同父的兄弟节点对应相邻区域，建立子环境间关系。
- **多级再规划**: 智能体通常在 leaf 层操作；若局部不可行（无充电站/路径被阻），则向上升一级，在所有兄弟子环境上联合重规划，扩大搜索范围。
- **再训练条件**: 基于受影响子环境的成功率（success rate）判断是否需要再训练，仅当策略有效性低于阈值时才重训练，避免不必要计算。
- **四种实现**: (1) 仅 leaf 重规划（近似 Yarahmadi）；(2) 利用层级多级重规划；(3)(4) federated Q-learning（FedAsynQ_EqAvg / FedAsynQ_ImAvg），并行学习并通过联邦平均聚合 Q-table 加速。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证。含时间复杂度分析与 Q-learning 收敛性检测（Q-table 迭代差阈值），但无新理论保证。

## 实验 (Experiments)
- **环境/Benchmark**: 自建 maze grid 环境，三种难度（easy/medium/hard，依障碍/充电站/自由空间密度）、多种尺寸（50×50 至 300×300），每步多个障碍同时变化；含 edge case（左上象限无充电站）。
- **Baselines**: 两种 A*-based 基线（A* Oracle，理论上界，假设完全已知动态环境）；单智能体 tabular Q-learning 变体。
- **评估指标**: Accuracy（成功率）、Adaptation Time、Cumulative Adaptation Time、Average Path Length、Initial Training Time。

## 主要结果 (Key Results)
- 两种 federated 方法（FedAsynQ_EqAvg、FedAsynQ_ImAvg）表现最佳，跨所有尺寸与难度成功率接近 A* Oracle，且适应时间低、扩展性优。
- 路径长度略长于 A* Oracle，但在强调高效鲁棒适应而非最优性的前提下可接受。
- MARL（federated）一致优于单智能体版本，验证了 DAI / 分布式学习的有效性。

## 局限与未来工作 (Limitations & Future Work)
分层分解目前仅支持已知维度、矩形/方形环境；大型未知环境的初始训练耗时（tabular RL 探索性）。未来：引入 Deep RL 提升泛化与性能；扩展分解框架支持任意/未知形状环境。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"环境不确定性/动态变化"应用线，但鲁棒性偏向工程鲁棒适应（dynamic obstacle adaptation）而非形式化对抗或 DRMG 理论。与课程/分层方法、federated MARL、机器人路径规划应用主题相关，可作为应用驱动、tabular/联邦学习类的代表案例。
