# 167. Towards Resilience for Multi-Agent QD-Learning

## 元信息 (Metadata)
- **标题**: Towards Resilience for Multi-Agent QD-Learning
- **作者**: Yijing Xie, Shaoshuai Mou, Shreyas Sundaram
- **机构**: Purdue University, West Lafayette（College of Engineering / School of Aeronautics and Astronautics / School of Electrical and Computer Engineering）
- **发表**: IEEE CDC 2021；arXiv:2104.03153
- **链接/arXiv**: arXiv:2104.03153；doi:10.1109/CDC45484.2021.9683145

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: Byzantine 智能体（网络中任意/对抗行为的恶意节点）；分布式协同学习的容错
- **方法范式**: resilient consensus、QD-learning（distributed Q-learning）、邻域过滤型 resilient 聚合、几乎必然收敛分析
- **关键词**: Byzantine fault tolerance, resilient QD-learning, P2P networked MARL, (2F+1)-robust graph, almost sure convergence

## TL;DR（一句话总结）
针对 peer-to-peer 网络化 MARL 中 QD-learning 算法仅有单个 Byzantine 智能体即可被攻破的问题，提出一种 resilient QD-learning 算法，在网络拓扑满足 (2F+1)-robust 且每个 regular 智能体邻域内至多 F 个 Byzantine 节点时，证明所有 regular 智能体的值函数几乎必然收敛到全体 regular 智能体最优值函数的邻域。

## 问题与动机 (Problem & Motivation)
分布式 MARL 算法依赖邻居间的局部协调，虽对良性失效（benign failure）有一定鲁棒性，但一旦存在受网络攻击的恶意智能体，整个算法可能被破坏。已有 QD-learning（在无向网络上的 distributed Q-learning）即便只有一个对抗智能体也会失效。已有 resilient 分布式学习多依赖 client-server 架构（有可靠中心节点），或在 P2P 架构下仅做 policy evaluation。本文要在无中心协调的 P2P 网络、且存在任意行为 Byzantine 节点的情形下，仍保证 regular 智能体学到最优策略。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: Byzantine attack model——被攻陷智能体可发送任意（甚至协同对抗）的信息；每个 regular 智能体邻域内至多 F 个 Byzantine 节点；要求网络拓扑 (2F+1)-robust
- **设定**: fully cooperative；networked / decentralized（P2P，无中心节点）；online 分布式学习；时变有向网络

## 方法 (Method)
- 先将面向无向网络的 distributed Q-learning 扩展到时变有向网络（time-varying directed network）上的 QD-learning
- 在此基础上构造 resilient QD-learning：每个 regular 智能体在与邻居交换 Q 值/价值估计时，采用 resilient 聚合（剔除邻域中极端的若干个最大/最小值，类似 resilient consensus 中的过滤思想）以滤除 Byzantine 影响
- 在 (2F+1)-robust 拓扑与每邻域至多 F 个攻击者的条件下进行收敛性分析
- 给出当各状态下不同动作对应的最优 Q 值充分分离（sufficiently separated）时，regular 智能体可恢复全体 regular 智能体的最优策略

## 理论贡献 (Theoretical Contributions)
证明在 (2F+1)-robust 网络且每邻域至多 F 个 Byzantine 节点条件下，所有 regular 智能体值函数几乎必然（almost surely）收敛到全体 regular 智能体最优值函数的邻域；并给出"最优 Q 值充分分离 ⇒ 学到最优策略"的充分条件；同时刻画了原始 QD-learning 在对抗存在下的性能极限。属理论型（收敛性 + 图论条件）贡献。

## 实验 (Experiments)
- **环境/Benchmark**: 偏理论文章；以网络化 Markov 决策过程的数值/仿真验证为主（正文以理论分析为核心）
- **Baselines**: 原始（非 resilient）QD-learning
- **评估指标**: 值函数到最优值函数邻域的收敛性、对 Byzantine 节点的容忍能力

## 主要结果 (Key Results)
- 原始 QD-learning 在单个 Byzantine 智能体下即失效，凸显引入 resilience 的必要性
- 所提算法在图拓扑条件满足时保证 regular 智能体值函数几乎必然收敛到最优值的邻域
- 收敛邻域大小与网络结构、攻击者数量等相关；动作 Q 值充分分离时可恢复最优策略

## 局限与未来工作 (Limitations & Future Work)
依赖 (2F+1)-robust 图拓扑这一较强结构假设；收敛仅到最优值的邻域而非精确最优；采用表格型 Q 学习，未扩展到函数逼近/深度网络；以理论为主，大规模实证有限。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中 [[Byzantine/容错]] 与 [[resilient consensus]] 线的代表性工作，把控制/分布式优化中的 resilient consensus（graph robustness、邻域过滤）思想迁移到 networked MARL 的 QD-learning，强调拓扑条件下的几乎必然收敛保证；与 [[distributed/networked MARL]]、[[QD-learning]] 主题紧密相关。
