# 1. Robust Multi-Agent Reinforcement Learning with Model Uncertainty

## 元信息 (Metadata)
- **标题**: Robust Multi-Agent Reinforcement Learning with Model Uncertainty
- **作者**: Kaiqing Zhang, Tao Sun, Yunzhe Tao, Sahika Genc, Sunil Mallya, Tamer Başar
- **机构**: University of Illinois at Urbana-Champaign (ECE & CSL); Amazon Web Services
- **发表**: NeurIPS 2020
- **链接/arXiv**: 未明确（NeurIPS 2020 论文）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 模型不确定性（reward function 与 transition probability 的 distribution-free 不确定性，sim-to-real gap）
- **方法范式**: Robust Markov Game (robust stochastic game)、minimax / worst-case、nature player、Q-learning、actor-critic 与 function approximation、博弈论均衡
- **关键词**: Robust Markov Game, Robust Nash Equilibrium, model uncertainty, MADDPG, nature player

## TL;DR（一句话总结）
首次将 MARL 的模型不确定性形式化为 robust Markov game，引入"nature"对抗玩家建模最坏情况，提出 robust Markov perfect Nash equilibrium 解概念，并给出有收敛保证的 Q-learning 以及可扩展的 Robust-MADDPG actor-critic 算法。

## 问题与动机 (Problem & Motivation)
真实多智能体应用中，智能体（尤其是仿真训练得到的）往往无法精确知道模型（其它智能体的 reward、联合 transition），导致 sim-to-real gap，仿真中得到的策略在实际部署中表现差。单智能体 RL 已有 robust MDP / robust RL 框架处理此类不确定性，但 MARL 几乎未在问题形式化与算法设计上考虑模型不确定性。加入额外对手后博弈不再是 two-agent zero-sum，而落入更难求解的 general-sum 范畴。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 每个状态 s 上为 reward（与可选地 transition）定义紧致的不确定性集 R̄ⁱ_s、P̄_s；不确定性视为一个隐式 nature 玩家的决策，nature 在每个状态对每个 agent 选取最坏情况模型数据。distribution-free（无需先验概率信息）。文中为简化主要聚焦 reward 不确定性。
- **设定**: cooperative 与 competitive 混合（general-sum Markov game）；centralized-training-decentralized-execution (CTDE)；online（model-free Q-learning / actor-critic）。

## 方法 (Method)
- 将问题建模为 robust Markov game，给出 Bellman 型不动点方程：每个 agent 在 max 自身策略的同时 min over 不确定性集（nature），定义 robust Markov perfect Nash equilibrium (RMPNE) 及带 nature 的等价形式 NRMPNE。
- 证明在有限状态-动作、紧致不确定性集下 RMPNE 存在，且 nature 的最优策略可取为确定性。
- 已知模型时给出 value iteration；model-free 时给出 tabular Q-learning 更新（需维护所有 agent 的 Q 值并每步求解 general-sum 均衡），在一定条件下有收敛保证。
- 推导 robust MARL 的 policy gradient 定理（对 agent 策略类似标准 PG，对 nature 确定性策略类似 deterministic PG），据此设计两时间尺度 actor-critic（Robust-MADDPG），支持函数逼近与 mini-batch。

## 理论贡献 (Theoretical Contributions)
- RMPNE 存在性证明（Proposition 2.2）。
- Q-learning 在特定条件下（沿用 Nash-Q 的假设）的收敛保证。
- robust MARL 的 policy gradient 定理（Lemma 3.1，含对 agent、nature 及 transition 参数的梯度）。

## 实验 (Experiments)
- **环境/Benchmark**: Multi-agent particle environments：cooperative navigation、keep-away、physical deception、predator-prey。
- **Baselines**: MADDPG（无鲁棒性）、M3DDPG（针对对手策略变化的鲁棒性）。
- **评估指标**: 累计 reward、success rate、占据 landmark 数/最小距离、占据目标平均步数、prey 被捕获次数等。通过在不同 reward 不确定性水平 λ（truncated Gaussian 噪声）下交叉组合评估。

## 主要结果 (Key Results)
- 无不确定性时三种方法表现相近；随 λ 增大，R-MADDPG 在各环境中显著优于 MADDPG 和 M3DDPG。
- Cooperative navigation 中 R-MADDPG 仍能占据多数 landmark、success rate 更高。
- Keep-away / physical deception / predator-prey 中固定一方为 R-MADDPG 时其鲁棒性表现一致更好。

## 局限与未来工作 (Limitations & Future Work)
- 一般 general-sum robust Markov game 的 Q-learning 收敛仅在受限条件下成立，每步求均衡计算代价高；需维护所有 agent Q 值。
- 主要聚焦 reward 不确定性，transition 不确定性仅做理论说明。
- 未来：应用于更多 MARL 场景，并在真实机器人（如 multi-car racing 平台）评估 sim-to-real 性能。

## 与综述的关联 (Relevance to Survey)
robust MARL 的奠基性工作之一，确立了 robust Markov game / robust Nash equilibrium 的理论框架与 nature-player 建模范式，是后续 distributionally robust MARL、minimax 对抗训练等方向的基础引用。属于"模型/环境不确定性"主线与"博弈论均衡 + 对抗训练"方法线。
