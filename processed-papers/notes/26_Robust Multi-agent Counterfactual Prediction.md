# 26. Robust Multi-agent Counterfactual Prediction

## 元信息 (Metadata)
- **标题**: Robust Multi-agent Counterfactual Prediction
- **作者**: Alexander Peysakhovich, Christian Kroer, Adam Lerer（equal contribution）
- **机构**: Facebook AI Research / Facebook Core Data Science
- **发表**: NeurIPS 2019（33rd Conference on Neural Information Processing Systems, Vancouver）
- **链接/arXiv**: 未明确

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对建模假设违反的鲁棒性——agent 理性假设、均衡假设、点可识别性、reward/utility 函数模型设定误差（model misspecification、bounded rationality）
- **方法范式**: 博弈论（Bayesian games、BNE / ε-BNE）、partial identification（集值解概念）、fictitious play、revelation game 抽象、minimax/区间界（optimistic & pessimistic bounds）
- **关键词**: counterfactual prediction, mechanism design, ε-equilibrium, partial identification, fictitious play, Bayesian games, robustness

## TL;DR（一句话总结）
提出 RMAC（robust multi-agent counterfactual prediction），用 revelation game 的 ε-BNE 集合来刻画在放松理性、均衡、可识别、模型设定假设下的反事实预测区间（最乐观/最悲观界），并给出一阶算法 RFP（revelation game fictitious play）计算之，应用于拍卖、择校等机制设计场景。

## 问题与动机 (Problem & Motivation)
机制设计者常需用日志数据做反事实预测："若改变博弈规则 G→G'，结果会怎样？"难点：agent 是策略性的（规则变会改行为），且其私有信息/效用函数不可观测。现有方法（结构估计、逆强化学习）假设 agent 完全理性、系统处于（唯一）均衡、模型设定正确、类型点可识别——这些在实践中往往不成立（人类决策有偏差、可能多重均衡或多类型分布）。需要一种衡量结论对这些假设违反之敏感性的方法。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 用 ε-BNE 放松四条标准假设（Equilibrium、Identification、Uniqueness、Specification）。ε 度量 agent 偏离 best response 的最大 regret（可解释为次优化/误设定程度，如拍卖中以美元计），ε-BNE 是集值解概念。
- **设定**: 多智能体一次性 Bayesian game（competitive/strategic）；offline（用 logged data D 做反事实推断）；分析者视角，非训练 RL 策略

## 方法 (Method)
- **Revelation game 抽象**: 将反事实估计等价为一个 revelation game 的均衡求解——每个 data-player 报告类型 θ̂ 与反事实动作 â，损失为 G-Regret 与 G'-Regret 的最大值。Theorem 1 证明标准假设下其有唯一 BNE（如实揭示真类型与反事实动作）。
- **RMAC 界**: 考虑 revelation game 的 ε-BNE 集合中，关于评估函数 V（如收入、效率、公平、truthfulness）的最小（ε-pessimistic）与最大（ε-optimistic）元素，构成鲁棒反事实预测的下界与上界。
- **RFP 算法**: 改编 fictitious play——每步各 data-player 在对历史博弈的 ε-best-response 集合中选择使 V 最小（悲观，α=−1）或最大（乐观，α=+1）的 type-action 对，随机打破平局。

## 理论贡献 (Theoretical Contributions)
- **Theorem 1**: 标准假设 1-3 满足时，revelation game 有唯一 BNE，即如实揭示真类型与反事实动作。
- **Theorem 2（硬度）**: 精确计算 ε-RMAC 界是 NP-hard——即便每数据点仅单一可行类型且只有两个数据点；或无目标函数、有限类型且 G' 仅两玩家时亦 NP-hard。
- **Theorem 3**: 若悲观（乐观）RFP 收敛到 σ*，则 σ* 是 revelation game 的 locally V-optimal ε-BNE（无单边严格 ε-best-response 偏离能进一步减小/增大 V）。
- 附录给出带均衡约束的数学规划 (MPEC) 及两玩家情形的混合整数规划。

## 实验 (Experiments)
- **环境/Benchmark**: 机制设计经典域——拍卖（first-price 2-player → second-price with reserve / N-player first-price）、择校 (school choice: Boston vs RSD，3 学生 3 学校)、社会选择（附录）
- **Baselines**: 标准结构估计 / 点识别（ε=0）与标准误差界（statistical uncertainty）作对照
- **评估指标**: 反事实收入 (revenue)、社会福利 (social welfare)、truthfulness 等评估函数 V 的 RMAC 区间宽度

## 主要结果 (Key Results)
- 拍卖：即使很小的 ε（如 0.01，仅约 4% 误设定）也会产生远宽于标准误差界的收入界；理论上 worst-case ε-equilibrium 使收入下降约 √(2ε)。
- 改变拍卖 reserve 的反事实稳健性不对称：提高 reserve 的估计稳健，降低 reserve 的不稳健。
- 择校：Boston→RSD 由于多类型分布与观测动作一致（点不可识别），即便小 ε 的 RMAC 界也很宽（truthfulness 提升可能 26% 或 0%）；反向 RSD→Boston 因 RSD 真实揭示使类型良好设定，RMAC 界更紧。

## 局限与未来工作 (Limitations & Future Work)
- RFP 基于 fictitious play，一般博弈中可能不收敛（仅在两人零和/势博弈保证收敛）；算法修改可能显著影响表现。
- 精确计算 RMAC 界 NP-hard，难以扩展到大实例。
- 未来：将解概念扩展到 no-regret learning；用可处理函数逼近的深度多智能体学习算法 (deep CFR、neural fictitious self-play 等) 处理更复杂环境；结合 robust/automated mechanism design。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"博弈论 + 对建模假设鲁棒（bounded rationality / model misspecification）"线路的较独特工作，关注的是反事实推断而非策略训练的鲁棒性，用 ε-equilibrium 集值解刻画不确定性。与 partial identification、机制设计、no-regret learning、fictitious play / CFR 等主题相关；为综述提供"均衡假设放松带来的鲁棒区间"这一分析视角，补充以训练为中心的鲁棒 MARL 主流。
