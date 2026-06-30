# 79. Decentralized Byzantine-Resilient Multi-Agent Reinforcement Learning with Reward Machines in Temporally Extended Tasks

## 元信息 (Metadata)
- **标题**: Decentralized Byzantine-Resilient Multi-Agent Reinforcement Learning with Reward Machines in Temporally Extended Tasks
- **作者**: Anonymous（双盲审稿）
- **机构**: 未明确
- **发表**: Under review at ICLR 2026
- **链接/arXiv**: 未明确

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: Byzantine 智能体（发送伪造/对抗性信息）、容错；时序扩展任务（non-Markovian reward）
- **方法范式**: belief-based Byzantine detection、reward machines (RM)、tabular Q-learning + actor-critic、去中心化共识、收敛理论
- **关键词**: Byzantine resilience, reward machines, belief update, decentralized MARL, temporally extended tasks

## TL;DR（一句话总结）
提出全去中心化的 BQL-RM 与 BAC-RM，将 reward machines（编码时序任务结构）与基于信念的 Byzantine 检测机制结合，使 defender agent 在无中心协调者下隔离 Byzantine agent 影响并收敛到最优策略。

## 问题与动机 (Problem & Motivation)
协作 MARL 在真实分布式部署（自动驾驶网络、分布式传感器）中存在 Byzantine agent，会发送伪造信息破坏学习。已有 resilient RL 多依赖中心服务器或对 agent 行为有严格要求，且难以处理具有时序依赖/non-Markovian reward 的时序扩展任务。本文目标是在全去中心化、局部通信、时序扩展任务下实现 Byzantine 鲁棒且有收敛保证。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 每个 episode 开始随机选取一部分 agent 为 Byzantine（type θ_i=1），其从 ˆπ 采样动作替换 defender 动作并发送伪造信息。Assumption 1 要求 defender 数量 ≥ M·|Byzantine|+1。defender 不知他人 type，仅观测自身及邻居的动作与奖励（local communication），采用 state-adversarial MDP 视角，需对最坏情况对手鲁棒。
- **设定**: cooperative；fully decentralized（无中心协调者）；online；time-varying 通信网络

## 方法 (Method)
- 用 labeled MDP + reward machine (Mealy 机) 编码任务的时序依赖与 Markovian/non-Markovian 奖励，引导学习并支持迁移。
- belief-based Byzantine detection（Algorithm 1）：每个 agent 对每个邻居维护信念 ζ；若邻居动作偏离其最优动作则提升怀疑度，否则降低；再离散化为 defender(0)/suspicious(1)/Byzantine(2) 三类（阈值 βl,βu）。
- BQL-RM：tabular Q-learning，Q 函数定义在增广状态 (s, u, b, a)（MDP 状态、RM 状态、belief 状态），每 m 步更新 belief 隔离 Byzantine。
- BAC-RM：actor-critic 版本，使用两时间尺度随机逼近（critic 更新快于 actor），支持函数逼近。

## 理论贡献 (Theoretical Contributions)
- Theorem 1：belief update 机制收敛到 ground-truth belief。
- Theorem 2：BQL-RM 在 tabular 设定下几乎必然收敛到最优 Q 函数（基于增广状态空间 Bellman 算子收缩与 Markov 性保持）。
- Theorem 3：BAC-RM 几乎必然收敛到目标函数的 stationary point（两时间尺度分析，belief 检测保证无偏梯度）。
- 消除了对 Byzantine 比例的部分限制性假设，提供离散时间严格分析。

## 实验 (Experiments)
- **环境/Benchmark**: 6×4 grid-world foraging（level-based foraging 变体，3 个 agent 协作收集资源，1 个提供伪造信息）；附录含 Search and Rescue 任务
- **Baselines**: PPO-QMIX、COMA、M3DDPG（以及无 RM 的方法）
- **评估指标**: cumulative rewards、收敛速度

## 主要结果 (Key Results)
- BQL-RM 与 BAC-RM 均优于无 reward machine 的 baseline；PPO-QMIX 是最强 baseline，COMA/M3DDPG 因无法捕捉时序依赖而效果有限。
- BQL-RM 取得更高累积奖励、收敛更快；BAC-RM 表现良好但收敛较慢。
- belief update 能随时间有效识别 Byzantine agent，实现 defender 间鲁棒协作。

## 局限与未来工作 (Limitations & Future Work)
- tabular 方法难以扩展到大状态/动作空间（拟用函数逼近扩展）。
- belief 更新机制对噪声/模糊观测的鲁棒性有限，可用更丰富推断策略。
- agent 增多时通信约束更突出，需通信高效设计；经验性能对超参数与环境动态敏感。
- 未来：从数据学习 RM 结构、迁移到真实多机器人/网络系统。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"Byzantine/容错"与"对抗智能体"主题，特色在于全去中心化（无中心服务器）+ belief-based 检测 + reward machine 处理时序扩展任务，并提供 tabular 收敛保证。与 78（Byzantine edge attack 分布式 Q-learning）、Bayesian 类型对手 (BARDec-POMDP) 等方法线相关，是将形式化任务结构 (RM) 引入鲁棒 MARL 的代表。
