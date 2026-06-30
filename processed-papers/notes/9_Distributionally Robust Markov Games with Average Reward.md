# 9. Distributionally Robust Markov Games with Average Reward

## 元信息 (Metadata)
- **标题**: Distributionally Robust Markov Games with Average Reward
- **作者**: Zachary Roch, Yue Wang
- **机构**: University of Central Florida (ECE / CS Department), Orlando, USA
- **发表**: ICML 2026 (PMLR 306)
- **链接/arXiv**: arXiv:2508.03136v4

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 模型不确定性 / 模型失配 (model mismatch, Sim-to-Real gap)、转移核 (transition kernel) 不确定性、对抗扰动
- **方法范式**: DRMG (distributionally robust Markov game) 理论、robust Bellman equation、博弈论均衡 (Nash Equilibrium)、minimax/pessimism、average-reward 准则
- **关键词**: distributionally robust Markov games, average reward, Nash equilibrium, robust Bellman equation, two-time-scale algorithm

## TL;DR（一句话总结）
首次系统研究平均奖励 (average-reward) 准则下的分布鲁棒马尔可夫博弈 (DR-MGs)，证明在 irreducible 与更一般的 weakly communicating 设定下平稳鲁棒 Nash 均衡的存在性，设计两个可证明收敛的算法 (Robust Nash-Iteration 与 robust TD Descent)，并证明平均奖励下的鲁棒 NE 可由折扣 DR-MG 在 γ→1 时逼近。

## 问题与动机 (Problem & Motivation)
Markov game 为竞争性多智能体序贯决策建模，但假设模型与真实环境失配（Sim-to-Real gap，源于非平稳、建模误差、外部扰动或对抗攻击）会使均衡策略性能严重退化。DR-MGs 通过在不确定性集上优化最坏情况性能提供鲁棒保证。已有工作集中于有限时域或折扣奖励设定；但许多长期运行系统（仓储机器人、通信网络、自动驾驶协调、金融市场、P2P 能源交易）更适合用长期平均奖励准则。平均奖励 DR-MG 研究尚在萌芽，且面临折扣/有限时域所没有的复杂性：(1) player-specific 环境（不同 agent 有不同最坏核）破坏 min-max 对偶，即便两玩家零和也须当作 general-sum；(2) 平均奖励依赖链分解结构、远不可处理；非鲁棒平均奖励 MG 甚至可能不存在平稳 NE。现有折扣/有限时域的存在性与算法（backward induction、依赖折扣鲁棒 Bellman 方程解唯一性）都无法直接推广。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 标准 (s,a)-rectangular 不确定性集 P=×Pa_s，对每个状态-动作对独立定义；agent 采用 pessimism 优化最坏情况鲁棒 average reward gπ_P,i = min_{P∈P} gπ_P,i。鲁棒 NE 按最坏情况性能定义。
- **设定**: competitive / general-sum 多玩家 Markov game（即便零和也退化为 general-sum）；平稳策略 (stationary policy)；infinite-horizon average reward；理论分析 + 算法

## 方法 (Method)
- 存在性 (irreducible 设定)：证明寻找 agent 的最佳响应等价于求解平均奖励鲁棒 Bellman 方程；其解集凸且半连续，从而最佳响应映射有不动点，平稳鲁棒 NE 存在。
- 存在性 (weakly communicating 设定，上述对应关系失效)：基于 constant-gain 最优鲁棒 Bellman 算子构造一个集值代理映射 (set-valued map)，证明其值是最佳响应策略的子集，并通过其凸性/连续性证明不动点存在 → NE 存在。
- 算法1 Robust Nash-Iteration：受标准 Nash value iteration 启发；在额外博弈结构假设与 normal-form NE 计算 oracle 下证明收敛到鲁棒 NE。
- 算法2 robust TD Descent：用 TD error 等价刻画 NE（其最小化者即鲁棒 NE），设计 two-time-scale 算法最小化 TD error，无需 NE oracle、可高效执行，并给出 stationary 收敛保证。
- 折扣逼近：证明平均奖励鲁棒 NE 可由折扣 DR-MG 在折扣因子足够大时逼近，从而可借助折扣设定成熟的数学性质与算法求解。

## 理论贡献 (Theoretical Contributions)
理论为主，核心贡献：(1) 最佳响应与平均奖励鲁棒 Bellman 方程解的对应关系（irreducible 设定）；(2) irreducible 与 weakly communicating 两种设定下平稳鲁棒 NE 的存在性证明；(3) Robust Nash-Iteration（在 oracle 与结构假设下收敛）与 robust TD Descent（two-time-scale，无 oracle，stationary 收敛保证）两个可证明收敛算法；(4) average-reward 鲁棒 NE 由 discounted 鲁棒 NE 在 γ→1 时逼近的连接结果。

## 实验 (Experiments)
- **环境/Benchmark**: 未明确（以理论与算法为主，正文前部未呈现实验章节）
- **Baselines**: 未明确
- **评估指标**: 未明确

## 主要结果 (Key Results)
- 给出平均奖励 DR-MG 第一个全面的理论与算法基础：在标准 irreducible 与更一般 weakly communicating 设定下均证明平稳鲁棒 NE 存在。
- 揭示平均奖励 DR-MG 的根本困难：player-specific 最坏核使 min-max 对偶失效，零和退化为 general-sum。
- 两个收敛算法分别在有/无 NE oracle 情形下求解鲁棒 NE。
- 建立 average-reward 与 discounted 鲁棒 NE 之间的逼近桥梁。

## 局限与未来工作 (Limitations & Future Work)
- 依赖 (s,a)-rectangular 不确定性集与 irreducible / weakly communicating 等结构假设。
- Robust Nash-Iteration 需要 normal-form NE 计算 oracle 与额外博弈结构假设。
- 偏理论，缺乏大规模实证验证（实验部分未在所读范围明确）。未来可放宽假设、探索函数逼近与样本复杂度等。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"模型/分布鲁棒性 (DRMG) 理论"这条核心线，是把单智能体 distributionally robust MDP 推广到多智能体并首次处理 average-reward 准则的基础性理论工作。与折扣/有限时域 DR-MG、robust Bellman、博弈论均衡存在性等主题直接相关，为综述的理论基础章节提供长期时域下鲁棒均衡的存在性与可计算性结论。
