# 74. Bayesian Robust Cooperative MARL Against Unknown Adversaries

## 元信息 (Metadata)
- **标题**: Bayesian Robust Cooperative Multi-Agent Reinforcement Learning Against Unknown Adversaries
- **作者**: Kiarash Kazari, György Dán
- **机构**: KTH Royal Institute of Technology, Stockholm, Sweden
- **发表**: ICLR 2026
- **链接/arXiv**: 代码 https://github.com/kiarashkaz/BATPAL

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体（部署时目标未知的对手）、动作/观测扰动、智能体失效；非 worst-case 对手
- **方法范式**: Bayesian Dec-POMDP game、perfect Bayesian equilibrium (PBE)、type space 离散化（severity 分区）、externally-constrained RL (EC-PPO)、min-oracle 对抗训练、belief 推断
- **关键词**: c-MARL, unknown adversary, Bayesian regret, type partitioning, externally constrained RL, PBE

## TL;DR（一句话总结）
针对部署时目标未知（非 worst-case）的对手，提出带连续对手类型的 Bayesian Dec-POMDP，并按对手“严重度”将策略空间分区、对每个分区训练代表性 worst-case 对手，进而学习自适应信念的鲁棒合作策略 BATPAL，以最小化 Bayesian regret。

## 问题与动机 (Problem & Motivation)
现有 robust c-MARL 多假设 worst-case 对手并求 max-min/saddle-point 策略，存在三大缺陷：(1) 无法刻画目标非“最小化团队奖励”的对手与故障行为，导致策略对实际攻击次优；(2) 非凸优化易陷入局部稳定点，得到的只是 local Stackelberg 均衡；(3) 对单一对手策略的扰动过拟合，面对部署时未见的新型对手无法适应、甚至达不到 max-min 的最低保证。需要能适应多样对手行为的鲁棒策略。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 对手目标和受害者身份对合作 agent 未知，episode 内 type 不变；假设对手控制单个受害 agent v，对手策略 ρ_{v,θv}。用连续 type 空间 Θ_i=[0,1] 表示不同奖励函数（θ_i=0 合作，θ_i=1 最小化团队奖励）。
- **设定**: cooperative；CTDE（参数共享）；execution-time robustness（部署期鲁棒）

## 方法 (Method)
1. 提出 Bayesian Dec-POMDP，泛化已有合作/混合/单 worst-case 对手设定；以 Bayesian regret 为鲁棒性目标（PBE 最小化之）。
2. Reference-value 分区：用对手相对参考策略 π0 造成的 severity η∈[0,1] 把策略空间分成 K 个不相交子集 Π_z，每个子集用其 worst-case 策略作为代表 type，保证暴露于多样对手。
3. Externally-constrained RL：求每个分区内最劣对手是一个目标与约束分别来自不同 MDP（MDP1/MDP0）的约束优化，用 log-barrier 近似并给出 policy gradient；实践中引入 PPO clipping 得到可行高效的 EC-PPO。
4. Bayesian 对抗训练：把 ˆM_B 视作 N+1 玩家的部分可观随机博弈，用 simultaneous gradient / two-timescale SGDA（α_n≥β_n，对手近似 min-oracle）更新；用 RNN 信念模型 b_χ(θ_{-i}|τ_i)（交叉熵训练）输入策略网络。

## 理论贡献 (Theoretical Contributions)
- Prop 3.1 分区非空；ˆM_B 的 PBE 对应式(4)、最小化 Bayesian regret。
- Prop 3.2/3.3：基于 reference value 的 KL 散度下界与对手策略集多样性下界，证明分区带来多样性。
- Prop 3.4：分区将任意对手的 regret 上界从 (Vmax−Vmin) 收紧到 severity 相关的 k/K·(Vmax−Vmin)。
- Prop 4.1/4.2：EC-PPO 的 policy gradient 表达式；在给定条件下虽梯度有偏，仍以高概率收敛到约束问题的 (ε近似) KKT 点。

## 实验 (Experiments)
- **环境/Benchmark**: SMAC (2s3z, MMM；附录含 1c3s5z, 11m)、LBF (10x10-5p-10f-c)、MPE-Spread；均基于 MAPPO
- **Baselines**: EIR-MAPPO, Gen-Maxmin, RAP, vanilla MAPPO；Known Type (KT) 作经验上界；附录含 ROMANCE
- **评估指标**: SMAC 团队胜率、其它环境归一化平均 episodic reward；Bayesian regret；对 10 种对手策略（含 A-X 迁移对手与 ACT/DYN-1/DYN-2 未见动态对手）评估

## 主要结果 (Key Results)
1. BATPAL 在无攻击下性能与 vanilla MAPPO 相当（鲁棒化不损失正常性能），并在所有环境/对手类型下收敛。
2. 即使只训练单一合作策略，它在对手面对其专门训练的攻击时几乎总优于各鲁棒 baseline；许多情况下接近 near no-regret（接近 KT 上界），包括未见攻击。
3. 其它 baseline 的最差表现常出现在面对 BATPAL 生成的攻击时，印证单一 max-min 训练易陷局部稳定点、而分区搜索更有效。
4. 消融显示 belief 模块重要（No Belief 性能下降，Perfect Belief 接近上界）。

## 局限与未来工作 (Limitations & Future Work)
- 假设至多一个受害 agent、type 在 episode 内固定；分区数 K 需选择。
- 仍可能陷入局部最优（仅缓解）；收敛保证依赖理想化条件。
- KT 为经验上界，未必为真上界。（未来工作未在正文明确展开）

## 与综述的关联 (Relevance to Survey)
属于 robust c-MARL 中“对抗智能体 + 未知/非 worst-case 对手”主线，是对 EIR-MAPPO（73 号）等 worst-case Bayesian 方法的直接推进：用连续 type + severity 分区把过度保守的 max-min 推广到自适应多类型对手，连接 robust RL、constrained/safe RL 与 Bayesian game 三条线，强调部署期对未见对手的泛化鲁棒性。
