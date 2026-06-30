# 7. Strategically Robust Multi-Agent Reinforcement Learning with Linear Function Approximation

## 元信息 (Metadata)
- **标题**: Strategically Robust Multi-Agent Reinforcement Learning with Linear Function Approximation
- **作者**: Jake Gonzales, Max Horwitz, Eric Mazumdar, Lillian J. Ratliff
- **机构**: University of Washington (ECE)；California Institute of Technology (CMS)
- **发表**: arXiv 2026（arXiv:2603.09208v1，2026年3月）；未明确正式 venue
- **链接/arXiv**: arXiv:2603.09208 ；代码 https://jakeagonzales.github.io/linear-rqe-website/

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 策略/对手不确定性（opponent misspecification, partner perturbation）、收益估计误差（payoff/approximation error）、环境（转移/奖励）不确定性
- **方法范式**: 博弈论均衡（Risk-Sensitive Quantal Response Equilibrium, RQRE）、风险敏感、bounded rationality、optimistic value iteration、linear function approximation、distributionally robust optimization (DRO)
- **关键词**: general-sum Markov games, RQRE, risk sensitivity, bounded rationality, linear function approximation, regret bounds, distributional robustness

## TL;DR（一句话总结）
提出 RQRE-OVI——一种在线性函数近似下计算 Risk-Sensitive Quantal Response Equilibrium 的乐观值迭代算法，证明其有限样本 regret 界、Lipschitz 稳定性与分布鲁棒性，用风险敏感+有限理性替代不可解且脆弱的 Nash，获得可扩展、可调、更鲁棒的均衡学习。

## 问题与动机 (Problem & Motivation)
一般和 Markov game 中 Nash 均衡计算上不可解、且因均衡多重性与对近似误差的敏感性而脆弱（payoff 微小扰动可致选中的均衡策略不连续跳变）。现有 NQ-OVI 虽将 Nash Q-learning 推广到线性近似并给出与特征维度相关的 regret 界，但每个 stage game 每个 episode 都需求解 Nash，继承其不可解性与不稳定性。需要一种同时"计算可解、对收益扰动稳定、可被可扩展 RL 学习并有形式保证"的均衡概念。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 通过 convex risk measure 的对偶表示（worst-case expectation over adversarial perturbations）建模三类不确定性——(1) environment risk（下一状态转移随机性）；(2) policy risk（对手动作随机性，策略性风险规避）；(3) opponent/payoff misspecification。风险参数 τ 控制风险规避程度（τ→0 风险中性，τ→∞ minimax 最坏情况），bounded rationality 参数 ϵ 控制平滑/正则化程度。RQRE 被证明等价于带惩罚的 DRO 并广义化 ambiguity-set DRO 与 Nash。
- **设定**: general-sum Markov game（competitive/mixed），n 智能体；linear function approximation（大/连续状态空间）；online、episodic、有限 horizon H

## 方法 (Method)
- **均衡概念 RQRE**: 每个玩家最小化 risk-adjusted loss + 严格凸正则项（1/ϵ·ν），ℓ_i(π_i,π_{-i})=ρ_i(-u_i)，通过 convex risk measure 对偶得到对抗分布解释。在 Markov game 中按 stage-wise 应用，定义 environment risk operator 与 policy risk operator 及风险正则化的 Bellman 递推。
- **算法 RQRE-OVI (Algorithm 1)**: 在线性 Markov game 假设下（转移/奖励线性、Q 函数线性可实现）做乐观值迭代；每个 stage 用子程序 RQREε 求近似 RQRE（替代 Nash oracle），加置信 bonus β√(ϕᵀΛ⁻¹ϕ) 实现乐观探索，岭回归估计参数 w。
- **熵风险特例**: policy-risk 惩罚取 KL、正则取负熵时，policy-risk value 有 log-sum-exp 闭式，值范围 B=H(1+log|A_i|/ϵ)。
- **求解器**: RQREε 可用 no-regret 动力学（multiplicative weights / extragradient / mirror-prox），强单调时指数收敛。

## 理论贡献 (Theoretical Contributions)
- **有限样本 regret 界（Theorem 2）**: reg(K) ≤ Õ(L_env·B·√K·d³H³) + KH(ε_env + L_env(ε_pol+ε_eq))，首个在线性近似下、含风险敏感与近似均衡计算（不依赖 Nash oracle）的乐观 MARL regret 保证；明确刻画 rationality(ϵ) 与 risk-sensitivity(τ) 如何影响样本复杂度（更强风险规避放松求解器精度要求 ε_eq=O(B√(Δeq/τmin))）。
- **分布鲁棒性（Proposition 1, 2）**: RQRE 严格广义化 ambiguity-set DRO 均衡与 Nash（RQRE ⊃ Penalized DRO ⊃ Hard ambiguity-set DRO ⊃ Nash）；Markov game 中 RQRE 对策略、对手、环境转移分布鲁棒。
- **Lipschitz 稳定性（Corollary 2）**: RQRE 策略映射对估计收益 Lipschitz 连续（‖π(Q)-π(Q̃)‖₁≤(c/µ)‖Q-Q̃‖∞，µ=1/ϵ+τ²），而 Nash 选择映射可不连续（Example 3 给出发散反例）。
- **策略收敛（Proposition 3）**: 在参数估计误差 δ_h 下，‖π̂_h-π*_h‖₁≤(c/µ)δ_h，值函数误差受控；揭示 expected performance 与 robustness 间的 Pareto frontier，Nash 在完全理性+风险中性极限处恢复。

## 实验 (Experiments)
- **环境/Benchmark**: dynamic Stag-Hunt（改自 Melting Pot, 9×9 grid 协调博弈）；Overcooked（JaxMARL 实现，洋葱汤协作）
- **Baselines**: QRE-OVI（风险中性）、NQ-OVI（Cisneros-Velarde & Koyejo 2023, Nash 基线）；RQRE-OVI 跨多档 τ
- **评估指标**: self-play 团队回报；cross-play retention R(δ)/R(0)（扰动 partner，δ 概率偏离）；cross-play 未见 partner 配对回报

## 主要结果 (Key Results)
- self-play 中 τ 控制收敛到 payoff-dominant (stag) 还是 risk-dominant (hare) 均衡，验证理论预测的风险-回报权衡。
- cross-play 扰动 partner 下，低 τ（更风险规避）智能体在各噪声水平保持高 retention，而低风险规避者（含 Nash/QRE）在 stag 脆弱均衡上随 δ 急剧退化；moderate τ 在 δ=0.3 保持 60-80% 性能，NQ-OVI/QRE 跌破 40%。
- Overcooked self-play 中 RQRE/QRE 优于 NQ-OVI（后者因 Nash 均衡多重性导致跨步选择不一致、破坏持续协调）。
- cross-play 未见 partner：RQRE 普遍优于或持平 partner（moderate τ 达 NQ-OVI 的 2-3×），且 QRE 与 NQ-OVI 相当，说明 risk aversion 而非单纯 bounded rationality 是鲁棒优势的关键驱动。

## 局限与未来工作 (Limitations & Future Work)
依赖线性 Markov game 假设（转移/奖励线性、Q 可实现）；bonus 项为集中式，未去中心化；仅验证 2 智能体协调任务。未来：去中心化 bonus 项（利用无限 horizon RQRE 单调性条件）；更细粒度理解风险敏感作用，包括风险偏好（risk-seeking）与玩家间非对称风险画像。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中"博弈论均衡 + 风险敏感 + 理论保证（DRMG/regret）"主题线，提供从 Nash 转向 RQRE 的"策略鲁棒性"理论框架，将 bounded rationality、risk sensitivity 与 distributional robustness 统一。可与同系列风险敏感/均衡计算工作（如 #11 Tractable Equilibrium via Risk Aversion、#13/#14 风险敏感 MARL、#24 correlated equilibrium、#3/#4 curse of multiagency + linear function approximation）对照，是少数提供有限样本 regret 与稳定性证明的"strategically robust"理论贡献。
