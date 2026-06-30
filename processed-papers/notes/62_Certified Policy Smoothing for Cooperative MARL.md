# 62. Certified Policy Smoothing for Cooperative Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Certified Policy Smoothing for Cooperative Multi-Agent Reinforcement Learning
- **作者**: Ronghui Mu, Wenjie Ruan, Leandro Soriano Marcolino, Gaojie Jin, Qiang Ni
- **机构**: Lancaster University；University of Exeter；University of Liverpool（UK）
- **发表**: AAAI 2023 (The Thirty-Seventh AAAI Conference on Artificial Intelligence)
- **链接/arXiv**: https://github.com/TrustAI/CertifyCMARL （arXiv:2212.11746）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动（每步对每个智能体观测施加 ℓ2 范数有界扰动）
- **方法范式**: 认证鲁棒 (certified robustness)、randomized smoothing、policy smoothing、FDR/多重假设检验校正、tree-search 奖励下界
- **关键词**: c-MARL certification, randomized smoothing, false discovery rate, certified radius, QMIX/VDN

## TL;DR（一句话总结）
首个对协作 MARL (c-MARL) 进行鲁棒性认证的工作：用随机平滑构造平滑策略并推导每个智能体每步动作的认证半径，通过引入 agent 重要性因子的 FDR 校正解决多重假设检验问题，并用 tree-search 求出全局团队奖励的认证下界。

## 问题与动机 (Problem & Motivation)
c-MARL 用于安全攸关场景，但其鲁棒性认证此前从未被研究。相比单智能体，c-MARL 认证有两大挑战：(1) 智能体数增多导致联合动作空间指数增长、每步需同时认证多个智能体使不确定性累积；(2) 改变单个智能体的动作未必改变团队奖励，需要新的鲁棒性评估准则。已有 RL 认证方法（如 CROP）只适用于单智能体。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 攻击者每步对每个智能体观测加 ℓ2 范数有界扰动 ϵ；要求平滑策略在扰动下仍选与未扰动时相同的最可能动作。可扩展到 ℓp（换采样分布）。
- **设定**: cooperative；value-based c-MARL（VDN/QMIX）；Dec-POMDP；CTDE；执行/推断阶段认证

## 方法 (Method)
- **平滑策略 (Definition 1)**：对每个智能体观测注入 i.i.d. 高斯噪声 N(0,σ²I)，平滑策略选取在扰动下最频繁出现的动作；用 Monte Carlo 采样（10000 次）估计最高频与次高频动作概率。
- **逐智能体逐状态认证半径**：基于 Cohen 等的 randomized smoothing 给出 dn = (σ/2)(Φ⁻¹(p_am,n)−Φ⁻¹(p_ar,n))；该状态的整体半径取最弱智能体 D=min{dn}。
- **多重假设检验校正 (CRSC)**：N×T 次检验导致错误率累积；采用 Benjamini-Hochberg (BH) 程序控制 selective FDR，并将每个智能体的 importance factor（基于 COMA counterfactual advantage）乘到 p 值上，剔除影响小的智能体，避免被低影响 agent 拖低半径。
- **全局奖励下界 (T-CRGR)**：tree-search——在某步无法认证时让 agent 取次频动作分出新轨迹分支，遍历所有轨迹取最小奖励作为全局奖励认证下界，并用剪枝（要求 per-step reward 非负）控制树规模。

## 理论贡献 (Theoretical Contributions)
- Proposition 1 / Corollary 1-2 / Theorem 2：给出平滑策略每步动作的高概率认证半径（置信 1-α）及逐智能体认证集 Icert 的保证。
- 将 FDR/selective testing 引入多智能体认证以控制 type I error；tree-search 给出全局团队奖励的认证下界。比 SOTA RL 认证（CROP-LORE）半径更紧。

## 实验 (Experiments)
- **环境/Benchmark**: 单智能体 Freeway（OpenAI Gym）；c-MARL：Checkers（2 agents）、Switch（4 agents，ma-gym）；附录含 Traffic Junction
- **Baselines**: 单智能体对比 CROP-LORE (Wu et al. 2021)；c-MARL 无现成方法，用 PGD 攻击验证认证界有效性
- **评估指标**: 认证扰动半径 ϵ_cert、全局奖励认证下界（对比 PGD 经验值），不同 σ（0.03/0.06/0.1）

## 主要结果 (Key Results)
- 单智能体上认证界比 CROP-LORE 更紧（基于动作选择概率而非 Lipschitz 平滑值函数）。
- c-MARL：VDN 奖励更高但更不鲁棒（ϵ_cert 更低），QMIX 网络更复杂、各 agent 学得更均衡因而更鲁棒。
- 逐状态认证显示 agent 间鲁棒性差异（VDN 中 Agent2 远比 Agent1 鲁棒，因 VDN 仅加和奖励致部分 agent 偷懒）。
- FDR + 重要性因子校正使每步局部半径不必总取所有 agent 的最小值，避免低影响 agent 拖累。

## 局限与未来工作 (Limitations & Future Work)
tree-search 剪枝要求奖励非负（QMIX-Switch 奖励为负时需跑完整轨迹）；认证依赖大量采样，计算开销较大。可扩展到 ℓp 范数与更多智能体（论文已部分讨论）。

## 与综述的关联 (Relevance to Survey)
robust MARL 中"观测扰动 + 认证鲁棒"线的开创性工作，首次把 randomized smoothing/policy smoothing 推广到协作多智能体，并用统计多重检验与 tree-search 解决多智能体特有难题，与 AME（通信认证）形成 c-MARL 认证防御的两条互补线。
