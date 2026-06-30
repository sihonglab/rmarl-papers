# 13. Provably Convergent Actor-Critic for MARL through Risk-aversion

## 元信息 (Metadata)
- **标题**: Provably Convergent Actor-Critic for MARL through Risk-aversion
- **作者**: Yizhou Zhang, Eric Mazumdar
- **机构**: Department of Computing and Mathematical Sciences, California Institute of Technology (Caltech)
- **发表**: Preprint（arXiv:2602.12386v2, cs.MA, 2026；标注 Preprint, June 1, 2026）；正式 venue 未明确
- **链接/arXiv**: arXiv:2602.12386v2

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 策略风险/不确定性（risk-aversion，behavioral game theory），通过风险规避与有限理性正则化博弈以获得稳定可学习均衡（非外部对抗攻击，而是 risk-sensitive 鲁棒）
- **方法范式**: 风险敏感 (risk-averse)、博弈论均衡 (Risk-averse Quantal Response Equilibrium, RQE)、单时间尺度 Actor-Critic、contractive risk-adjusted Bellman operator、monotone games
- **关键词**: Risk-aversion、RQE、General-sum Markov Games、Actor-Critic、Finite-sample Convergence、Stationary Equilibrium

## TL;DR（一句话总结）
针对无穷视野 general-sum Markov game 中学习平稳均衡的难题，本文研究 Risk-averse Quantal Response Equilibrium (RQE)，证明在对智能体风险规避/有限理性的较弱假设下 RQE 唯一且平滑、风险调整 Bellman 算子为收缩，并设计一个"快 actor、慢 critic"的单时间尺度 Actor-Critic 算法，给出全局收敛的有限样本保证。

## 问题与动机 (Problem & Motivation)
在无穷视野 general-sum MG 中学习平稳策略是 MARL 基础性开放问题：经典博弈均衡 (Nash) 计算 PPAD-complete，平稳形式的相关/粗相关均衡也不可解，难以设计高效学习算法；近期转向非平稳均衡虽可解，但需历史依赖策略 (复杂度随时间视野增长) 且不反映实践中常用的平稳策略。本文从行为博弈论视角出发，通过对智能体行为 (而非博弈结构) 施加假设来获得可解性。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不施加外部对抗扰动；通过给智能体引入 risk-aversion 与 bounded rationality (quantal response)，使博弈正则化为 monotone game，从而获得唯一、平滑、可收缩学习的均衡 (risk-sensitive 鲁棒)。关键：假设作用在 agent 属性而非博弈结构，故适用于任意 general-sum 博弈。
- **设定**: general-sum (mixed/竞争-合作通用) Markov games；理论聚焦两玩家 (可扩展到 n 玩家)；学习平稳策略；含可扩展深度实现

## 方法 (Method)
1. **广义 RQE 可解性条件**: 弱化对玩家风险规避/有限理性的要求，证明比既有工作更广的博弈类拥有唯一且随收益矩阵平滑变化的 RQE。
2. **收缩性**: 据此证明 risk-adjusted Bellman operator 是收缩映射，支撑收敛的 value-based 学习。
3. **单时间尺度 Actor-Critic**: 与标准 (critic 快于 actor) 相反，policy (actor) 用较大步长、Q-function (critic) 用较小步长；用针对单时间尺度步长的耦合 Lyapunov drift 不等式的新型收缩分析证明有限样本收敛。
4. **可扩展实现**: 采用 policy/Q 网络与 replay buffer 适配现代深度 RL 基础设施。

## 理论贡献 (Theoretical Contributions)
- 广义条件下 RQE 的存在唯一性与对收益矩阵的平滑性。
- risk-adjusted Bellman operator 的收缩性证明。
- 单时间尺度 Actor-Critic 的全局收敛 + 有限样本保证（基于耦合 Lyapunov drift 收缩分析）。
- 声称为首个在 general-sum 折扣 MG 中、不对博弈结构附加假设、保证全局收敛到平稳均衡的 MARL 算法。

## 实验 (Experiments)
- **环境/Benchmark**: (1) normal-form inspection game；(2) Markov gridworld cooperation game；(3) MPE Simple Tag（固定 good agents）
- **Baselines**: risk-neutral baselines（风险中性方法）
- **评估指标**: 收敛稳定性/收敛模式、是否表现出风险规避行为

## 主要结果 (Key Results)
1. RQE 相比风险中性基线带来更稳定的收敛模式。
2. 学到的智能体表现出内在的风险规避行为。
3. 实验验证了理论的收敛性主张（跨三个环境）。

## 局限与未来工作 (Limitations & Future Work)
理论主要针对两玩家 (虽称可扩展 n 玩家)；可解性依赖恰当设计智能体的风险规避/有限理性 (需可控的 agent 设计)；实验环境规模较小。（论文未明确给出详尽 limitations，偏理论贡献）

## 与综述的关联 (Relevance to Survey)
robust MARL 中"风险敏感 (risk-averse) + 博弈论均衡"理论主线的核心工作，将鲁棒性内化为 agent 行为正则化以保证均衡可学习与收敛，与 risk-averse/风险敏感 MARL、quantal response 均衡线相关；其收缩 Bellman + 有限样本收敛分析可与其他提供收敛/样本复杂度保证的 robust MARL 理论 (如 2, 3, 126) 对照。
