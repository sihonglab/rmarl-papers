# 42. Attention-Enhanced Multi-Agent Reinforcement Learning Against Observation Perturbations for Distributed Volt-VAR Control

## 元信息 (Metadata)
- **标题**: Attention-Enhanced Multi-Agent Reinforcement Learning Against Observation Perturbations for Distributed Volt-VAR Control
- **作者**: Xu Yang, Haotian Liu, Wenchuan Wu
- **机构**: State Key Laboratory of Power Systems, Department of Electrical Engineering, Tsinghua University, Beijing
- **发表**: IEEE Transactions on Smart Grid, Vol. 15, No. 6, November 2024
- **链接/arXiv**: DOI 10.1109/TSG.2024.3423700

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动（测量噪声、通信误差、网络攻击 cyber-attack 对 agent 观测的扰动）
- **方法范式**: 价值分解（value network factorization）+ attention 机制 + 鲁棒正则项（robust regularizer，基于策略平滑/KL 散度，而非对抗训练）
- **关键词**: Volt-VAR control, CTDE, MASAC, attention mechanism, robust regularizer, smart grid

## TL;DR（一句话总结）
针对配电网分布式 Volt-VAR 控制，提出 RASAC——在 CTDE 软 actor-critic 框架下用 agent-level attention 增强 mix network 实现协调，并在策略损失中加入基于 KL 散度的鲁棒正则项以低成本提升对观测扰动/网络攻击的鲁棒性。

## 问题与动机 (Problem & Motivation)
高渗透分布式新能源使配电网（ADN）电压越限、网损加剧，需实时 Volt-VAR 控制（VVC）。集中式优化有单点故障和通信负担；CTDE 多智能体 RL（MADDPG/MASAC/MATD3）依赖中央价值网络，存在维数灾难。现有 value factorization（VDN/QMIX）mix network 过于简单，大规模下协调性能差。同时 RL 策略对观测高度敏感，测量噪声、通信误差乃至网络攻击会严重扭曲控制动作，而现有方法缺乏对扰动的考虑；传统对抗训练计算量大、调参繁、训练不稳。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 真实观测 o_n 被扰动至邻域 B(o_n, ε)，∥õ_n − o_n∥∞ ≤ ε。包括随机测量噪声与故意网络攻击（攻击者甚至已泄露策略网络参数，用 SGLD 寻找最坏扰动以最大化动作扭曲）。
- **设定**: cooperative Markov game；CTDE（云端集中训练，边缘 PV 逆变器分散执行）；online

## 方法 (Method)
1. **建模**: 每个 PV 逆变器为一个 RL agent，分布式 VVC 建模为 cooperative Markov game，目标最小化电压偏差与网损。
2. **Attention-enhanced mix network**: 在 value factorization 框架下，云端维护小规模 mix network，用 agent-level attention 将每个 agent 作为 attention 输入，结合全局信息与局部特征动态计算 agent 间相关性/重要性，实现协调并避免维数灾难。
3. **鲁棒正则项**: 基于"最小化 πθ(o) 与 πθ(õ) 之间距离即可提升鲁棒性"的思想（替代昂贵对抗训练），用 KL 散度定义 R_θ(o, ε) = max_{õ∈B(o,ε)} D_KL(πθ(o)‖πθ(õ))，加入策略损失，几乎不增计算。
4. **求解**: 用 SGLD（步长 ε/K，K 步）近似求邻域内最坏扰动来估计该正则项。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（基于已有策略平滑鲁棒性思想，主要为方法与工程贡献）

## 实验 (Experiments)
- **环境/Benchmark**: IEEE 33-bus 与 141-bus 配电系统，使用 Elia group 真实 3 年数据（测试取每月典型日共 36 天 / 约 1.7 万时步）
- **Baselines**: ASAC（无鲁棒正则的本方法）、CSAC（集中式 SAC）、QMIXSAC、VDNSAC、FMASAC（作者前作）、No Control
- **评估指标**: 电压偏差、网损、不同噪声/攻击强度 ε′ 下的总奖励、电压剖面

## 主要结果 (Key Results)
1. 无扰动时 RASAC 电压偏差最低，接近集中式 CSAC，且训练收敛稳定（FMASAC/VDNSAC 发散）；加入鲁棒正则不损害正常性能（RASAC ≈ ASAC）。
2. 33-bus 随机噪声测试：ε′ 增至 2.5 时 ASAC 奖励下降近 75%，RASAC 几乎保持稳定。
3. 141-bus 网络攻击测试（攻击者已知策略、用 SGLD 制造过压/欠压）：ASAC 动作被严重扭曲导致电压越限，RASAC 能在很大程度上避免动作扭曲、保障安全运行。

## 局限与未来工作 (Limitations & Future Work)
鲁棒正则依赖对邻域内最坏扰动的 SGLD 近似且对 ε 选取敏感；实验聚焦电压偏差（网损差异不明显）；评估限于 IEEE 33/141-bus；未给出鲁棒性理论保证。可扩展到更大系统、更强自适应威胁与多目标权衡。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 在电力系统（smart grid / Volt-VAR）的应用，代表"观测扰动 + 策略平滑正则（非对抗训练）"方法线；与 SA-MDP/state-adversarial、CTDE value factorization、attention 协调机制相关，是低成本鲁棒正则在工业控制中的实证案例。
