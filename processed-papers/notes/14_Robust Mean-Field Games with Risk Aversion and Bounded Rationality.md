# 14. Robust Mean-Field Games with Risk Aversion and Bounded Rationality

## 元信息 (Metadata)
- **标题**: Robust Mean-Field Games with Risk Aversion and Bounded Rationality
- **作者**: Bhavini Jeloka, Yue Guan, Panagiotis Tsiotras
- **机构**: School of Aerospace Engineering, Georgia Institute of Technology, Atlanta, GA, USA
- **发表**: arXiv preprint 2026（venue 未明确）
- **链接/arXiv**: arXiv:2602.13353v1 [cs.MA], 2026

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 初始种群分布的不确定性（distributional uncertainty over initial mean-field distribution）、认知约束（有限理性）
- **方法范式**: mean-field game (MFG)、风险敏感/风险厌恶（convex risk measures）、bounded rationality（quantal response / 凸正则化）、博弈论均衡（新均衡概念 MF-RQE）、fixed-point iteration / fictitious play / actor-critic RL
- **关键词**: mean-field games, risk aversion, bounded rationality, quantal response equilibrium, distributional robustness, scalable MARL

## TL;DR（一句话总结）
将风险厌恶（针对初始种群分布不确定性）与有限理性（凸正则化的 quantal response）同时引入 mean-field game，提出新均衡概念 mean-field risk-averse quantal response equilibrium (MF-RQE)，给出存在性与收敛性证明及可扩展 RL 算法，使大规模去中心化策略对分布不确定性鲁棒。

## 问题与动机 (Problem & Motivation)
经典 MFG 通过无限智能体极限将大规模多智能体问题降为代表性 agent 与种群分布(mean-field)的交互，但依赖强假设：固定初始种群分布、完全理性、风险中性。实际中 agent 跨不同初始分布运行，逐条件重算 MFE 计算上不可行，且需实时 mean-field 反馈（通信/感知/隐私上常不可得）；同时人类决策存在偏差、错误（有限理性）。需同时刻画风险厌恶与有限理性。已有工作 Mazumdar et al. (2025) 的 RQE 仅限有限智能体且受维数灾难困扰。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 初始分布从有限集合 M 中随机抽取（名义概率 Γ*_M），用 convex risk measure ρ 对初始分布不确定性做风险厌恶处理（对偶表示 → KL-penalty 下 log-sum-exp 闭式聚合）；τ→∞ 时初始分布选择可视为完全对抗（worst-case）。策略对 mean-field 为 open-loop（无实时 MF 反馈）。
- **设定**: 非合作 MFG（infinite-population），代表性 agent vs 种群；去中心化（仅依赖局部状态）；finite-horizon, discrete-time；model-based 与 model-free(RL) 均覆盖。

## 方法 (Method)
- **风险厌恶目标**: 用 convex risk measure 对不同初始分布诱导的价值函数 V^π_{µ,t}(x) 取风险，借 Föllmer-Schied 对偶表示重写为"虚构对抗者最大化代价但受 KL 惩罚约束"形式；KL 惩罚给出 log-sum-exp 闭式 c^π_t。
- **有限理性**: 在目标中加入严格凸正则项 αν(π_t(·|x))（温度 α 控制有限理性程度），泛化 entropy regularization 到一般凸正则器（如 log-barrier），得到 RQ-MFG 博弈元组 ⟨X,U,T,f,r,ν,M,Γ*_M,D⟩。
- **新均衡 MF-RQE**: 定义算子 B^RQE_opt 与 B^RQE_prop 的一致不动点 (π*_RQE, S*_M)。
- **算法**: (1) RQ-FPI（不动点迭代，DP 计算 best response）；(2) RQ-Fictitious Play（策略平均）；(3) D-RQ-FPI（深度 RL，model-free，维护 |M| 个 critic + 时变 actor，TD loss 更新 critic，actor 求解风险厌恶 quantal response 目标）。

## 理论贡献 (Theoretical Contributions)
- Proposition 1: MF-RQE 存在性（Assumptions 1-2）。
- Theorem 2: MF-RQE 策略在有限 N 智能体博弈中是 ϵ-RQE（连接无限/有限种群，克服 Mazumdar et al. 的维数灾难）。
- Theorem 3: 在 ν m-强凸假设下，FPI 对足够大 α 收敛到 MF-RQE。
- Theorem 4: RQ-Fictitious Play 对足够大 α 收敛到 MF-RQE。

## 实验 (Experiments)
- **环境/Benchmark**: MFGLib benchmark——epidemiological SIS game、新提出的 1D congestion game，及其他 MFGLib 环境。
- **Baselines**: entropy-regularized Nash equilibrium 策略（单一初始分布）、风险中性 π*_avg（对初始分布平均期望回报最大化）、各单一初始分布最优策略 π*_{µ_0}。
- **评估指标**: exploitability-like 度量 ∆c(π)（对分布不确定性的敏感性/可利用性）、平均回报（10000 episodes × 5 seeds）、mean-field flow 距离 d_S（经验 vs 解析）。

## 主要结果 (Key Results)
- MF-RQE 策略 non-exploitable（∆c(π)=0），对初始分布不确定性鲁棒；风险中性/单分布策略在实际初始分布偏离名义时 exploitability 更高。
- 鲁棒性以适度降低期望回报为代价（robustness-return trade-off），但各策略间期望回报差异较小。
- RQ-Fictitious Play 与 RQ-FPI 在所有环境恢复相同策略；D-RQ-FPI 经验 exploitability 降至 10⁻²~10⁻⁴、d_S<10⁻³，接近解析解。
- 消融：无凸正则（无有限理性）时无法保证可解性与收敛，凸正则可超越 entropy（如 log-barrier）。

## 局限与未来工作 (Limitations & Future Work)
当前限于有限初始分布集合 M（连续/紧集留待未来）；有限样本随机性使 deep RL 下 exploitability 无法精确收敛到零。未来：扩展到异质与团队 mean-field 设定（MFTG），风险厌恶可针对对抗性种群。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"分布鲁棒 + 风险敏感 + 博弈论均衡"理论线，并通过 mean-field game 解决大规模可扩展性。结合 risk aversion（worst-case 初始分布）、bounded rationality（quantal response）与新均衡 MF-RQE 及完整存在性/收敛性理论，是面向大规模去中心化、分布不确定性鲁棒的代表性理论工作，与 DRMG、风险敏感 RL、均衡分析等主题相关。
