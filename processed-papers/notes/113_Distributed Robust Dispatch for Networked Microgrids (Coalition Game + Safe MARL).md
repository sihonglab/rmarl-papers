# 113. Distributed Robust Dispatch for Networked Microgrids With Coalition Game-Guided Multiagent Adversarial Safe Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Distributed Robust Dispatch for Networked Microgrids With Coalition Game-Guided Multiagent Adversarial Safe Reinforcement Learning
- **作者**: Tianjiao Pu, Shuai Du, Lei Dong, Ji Qiao
- **机构**: China Electric Power Research Institute（北京）；North China Electric Power University
- **发表**: IEEE Transactions on Industrial Informatics, Vol. 22, No. 1, January 2026（DOI: 10.1109/TII.2025.3609841）
- **链接/arXiv**: 未明确（IEEE Xplore）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 源-荷（RES/load）不确定性与波动、状态转移分布不确定性（distributional uncertainty）、安全约束、通信数据完整性/隐私（HMAC 容错）
- **方法范式**: 分布式鲁棒（DR-CMDP / DR-MDP）、对抗训练（adversary via WGAN-GP）、Safe RL（CMDP/CPO + CVaR 约束）、博弈论（coalition game / Shapley / Aumann-Shapley）、minimax
- **关键词**: Adversarial Safe RL, Distributionally Robust, Networked Microgrids, Coalition Game, WGAN-GP, CVaR, Privacy-Preserving

## TL;DR（一句话总结）
提出 coalition game 引导的多智能体对抗 Safe RL 方法，用 WGAN-GP 构造对抗体来模拟源-荷转移概率的分布不确定性（DR-CMDP），在隐私保护与安全约束下实现网络化微电网的分布式鲁棒经济调度。

## 问题与动机 (Problem & Motivation)
分布式能源（DER）引入需求侧灵活性与不确定性，给网络化微电网（NMGs）经济调度带来挑战。模型驱动优化（SOCP/DRO 等）难扩展、在线决策慢；现有 MARL 多以惩罚项处理约束导致不安全决策，且依赖全局 critic 共享状态/动作泄露隐私；现有 Safe RL 假设预定义的源-荷分布，鲁棒性不足；现有对抗训练给对抗体与主角相同动作空间，不适配源-荷波动场景。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不确定性建模为状态转移概率 p 的分布 μ 落在 ε-Wasserstein ambiguity set 内（围绕参考动态 μ0）。对抗体（WGAN-GP，参数 ϕ）仅扰动与源-荷波动强相关的 PV/load 转移分布 p(s2|s)，而非主角动作空间。通信层用 HMAC 检测数据篡改（每若干 episode 检测一次），容错丢弃受损 episode。
- **设定**: cooperative（NMGs 协作调度，coalition game）；distributed / privacy-preserving（不共享本地状态动作，仅用边界功率 P_BB）；offline 训练 + online 决策

## 方法 (Method)
- 将单微电网调度建模为 DR-CMDP (s,a,R,C,ρ,p)：CMDP 安全约束界定动作空间 + DR-MDP 在转移概率上加分布不确定性。
- 对抗 SRL 求解 max-min：主角 maximize 折扣回报、对抗体 minimize（寻找最坏分布）；对抗体用 WGAN-GP（Wasserstein 距离）拟合源-荷经验分布并生成最坏情形。
- 主角用 CVaR (α=0.05) 约束的 Safe RL（CPO/trust region + importance sampling + GAE + entropy），并提出 gradient penalty 利用 coalition benefit 改善收敛；CVaR 近似为高斯闭式。
- Coalition game 引导框架：用 mid-market rate (MMR) 保证 superadditivity、Shapley/Aumann-Shapley 值分配收益保证 nonempty core，仅用边界功率 P_BB 调整奖励实现全局收敛；HMAC 保数据完整性；domain randomization 随机化拓扑增强适应性。

## 理论贡献 (Theoretical Contributions)
偏实证为主；提供博弈论结构性保证（coalition 稳定性：superadditivity 与 nonempty core，rationality + convergence 满足 Nash 均衡的两性质），CVaR 闭式近似与 Wasserstein 约束推导，但无形式化收敛/样本复杂度定理。

## 实验 (Experiments)
- **环境/Benchmark**: 改造的 IEEE-123 总线系统（分 3 个 MG）；实际电网衍生的 716 总线 MG（6 个 MG，4296 总线大系统）做可扩展性测试；CAISO 真实 PV/load 数据。
- **Baselines**: 模型驱动（SOCP、DMPC、DRO）；RL/SRL（PPO、PPO-Lag、MASAC、MASAC-Lag、FOCOPS）；非 CVaR 版自身消融。
- **评估指标**: 运行总成本、约束违反（CV）次数、在线决策时间、不同预测误差/季节/拓扑下的鲁棒性、电压幅值安全性。

## 主要结果 (Key Results)
- 在源-荷波动（Case III）下取得无约束违反的最低成本，鲁棒性可比 DRO 但在线决策时间大幅缩短。
- 相比 PPO/MASAC（惩罚项）频繁违反约束、Lag/FOCOPS 仍有 CV 且依赖预定义分布，本方法兼顾安全与鲁棒；CVaR 消融验证其作用。
- 预测误差约 6% 时即优于模型驱动方法；对季节变化、5 种随机辐射状拓扑（无重训）、大规模系统均保持安全鲁棒；电压维持在 [0.968, 1.050] p.u.。
- Coalition game 引导消融显示去掉后收敛变慢、最终奖励变差；HMAC 可安全丢弃受损 episode 保证收敛；agent 数≥6 时改用 Aumann-Shapley 降计算时间。

## 局限与未来工作 (Limitations & Future Work)
依赖准确历史数据来预训练 WGAN-GP；面向实际配电系统的层级结构时可扩展性仍受限。未来拟引入与配电系统运营商（DSO）的层级协调机制。

## 与综述的关联 (Relevance to Survey)
典型的“分布鲁棒 + 对抗训练 + Safe RL + 博弈论”融合工作，落地于智能电网/微电网调度。串联 robust MARL 多条主线：DR-MDP/DR-CMDP 理论、minimax 对抗（区别于同动作空间对抗）、风险敏感（CVaR）、博弈论均衡（coalition game）、以及通信安全/隐私（HMAC 容错），是 robust MARL 在能源系统应用的代表性案例。
