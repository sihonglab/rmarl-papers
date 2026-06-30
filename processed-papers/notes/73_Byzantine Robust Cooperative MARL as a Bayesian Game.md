# 73. Byzantine Robust Cooperative MARL as a Bayesian Game

## 元信息 (Metadata)
- **标题**: Byzantine Robust Cooperative Multi-Agent Reinforcement Learning as a Bayesian Game
- **作者**: Simin Li, Jun Guo, Jingqiao Xiu, ..., Yaodong Yang, Xianglong Liu et al.
- **机构**: Beihang University (SKLSDE Lab); Zhongguancun Laboratory; Peking University & BigAI; Hefei Comprehensive National Science Center
- **发表**: ICLR 2024
- **链接/arXiv**: arXiv:2305.12872v3；代码 https://github.com/DIG-Beihang/EIR-MAPPO

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体 / Byzantine 失效（任意 agent 被控制执行 worst-case 动作）、动作扰动；亦覆盖随机失效、观测扰动、迁移攻击
- **方法范式**: Bayesian game（Harsanyi 类型）、minimax robust、ex interim Markov perfect Bayesian equilibrium、two-timescale actor-critic、信念推断（posterior belief）
- **关键词**: c-MARL, Byzantine robustness, Bayesian game, non-oblivious adversary, RMPBE, belief inference

## TL;DR（一句话总结）
将合作 MARL 的 Byzantine 失效建模为由 nature 指派 type 的 Bayesian 博弈（BARDec-POMDP），提出基于后验信念的 ex interim 鲁棒均衡及收敛的 actor-critic 算法（EIR-MAPPO），在保持合作性能的同时抵御多种攻击。

## 问题与动机 (Problem & Motivation)
现实中合作 MARL 的任一队友可能因硬件/软件故障或被对手控制而执行任意 worst-case 动作（Byzantine 失效），破坏全合作假设。已有 robust MARL（如 M3DDPG、ROMAX）假设所有 agent 都可能是对手，相当于追求保守的 ex ante 均衡，掩盖了合作与鲁棒之间的权衡且过度保守，因为对手实际控制全部 agent 的概率很低。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: episode 开始时 nature 指派 type θ（θ_i=1 为对手），被指派 agent 的动作被 worst-case 对手策略 ˆπ 替换；动作扰动概率 P_α。假设每个 episode 仅一个对手、type 在 episode 内不变；防御者训练时可用全局信息，测试时仅有局部观测且不知道他人 type，需抵御 worst-case 对手。
- **设定**: cooperative；CTDE；online

## 方法 (Method)
1. 提出 BARDec-POMDP：把 Byzantine 对手视作由 nature 指派的 type，经独立 transition 表达动作扰动。
2. 解概念为 ex interim robust Markov perfect Bayesian equilibrium（RMPBE）：每个 agent 依 Bayes 规则更新对他人 type 的后验信念 b，并在该信念下最大化期望价值，从而兼顾合作与鲁棒。
3. 推导 robust Harsanyi-Bellman 方程更新 Q 函数（区分扰动前后两个 Q），用 TD loss 估计。
4. 给出 robust MARL 的 policy gradient 定理，采用 two-timescale actor-critic：对手快时间尺度更新、防御者慢时间尺度更新，certain assumptions 下几乎必然收敛到 ex interim RMPBE。
5. 用神经网络近似 belief（二元交叉熵训练），部署时无需访问他人策略。

## 理论贡献 (Theoretical Contributions)
- 证明 worst-case 对手存在性（Prop 2.1）；ex ante 与 ex interim 混合策略 RMPBE 存在性（Kakutani 不动点，Prop 2.2）。
- 证明 t→∞ 时 ex interim 策略弱占优（weakly dominate）ex ante 策略（Prop 2.3）。
- robust Harsanyi-Bellman 方程收敛性（contraction mapping + Banach，Prop 3.1）；two-timescale 更新几乎必然收敛（stochastic approximation）。

## 实验 (Experiments)
- **环境/Benchmark**: 玩具迭代 matrix game、Level-Based Foraging (LBF, 12x12-4p-3f-c)、SMAC (4m vs 3m)
- **Baselines**: MADDPG, M3DDPG, MAPPO, RMAAC, EAR-MAPPO（ex ante 消融）, True Type（理想上界）
- **评估指标**: 合作 reward；在 non-oblivious 攻击、随机 agent、ℓ∞ 观测噪声(ε∈{0.2,0.5,1.0})、迁移攻击下的鲁棒 reward（5×N 次攻击, 95% CI）

## 主要结果 (Key Results)
1. EIR-MAPPO 在三个环境下对 non-oblivious 攻击的鲁棒性显著优于 baselines，接近 True Type 理想上界，同时合作性能与 MAPPO 相当。
2. 在多种不确定性平均下，EIR-MAPPO 较 baselines 提升约 Toy 5.81%、LBF 5.88%、SMAC 25.45%。
3. 即使未训练过观测攻击，EIR-MAPPO 仍鲁棒（观测攻击最终归结为动作不确定性）；学到 kiting 与 focused fire 等精细微操。

## 局限与未来工作 (Limitations & Future Work)
- 主要假设单一对手、二元 type 空间、每 episode 仅一个 agent 易受扰；多对手/间歇/非二元 type 留作扩展。
- 缺乏无限制假设下的有限样本全局收敛保证（open problem）。
- 未来应用于机器人集群控制、交通信号、电网维护。

## 与综述的关联 (Relevance to Survey)
robust c-MARL 中针对“对抗/Byzantine 队友（动作扰动）”这条主线的代表作，独特之处在于用 Bayesian game 与后验信念区分合作/对抗 type，提出 ex interim 均衡突破以往 ex ante 的过度保守，连接 robust MDP、state-adversarial MDP 与 ad hoc coordination 三条理论线。
