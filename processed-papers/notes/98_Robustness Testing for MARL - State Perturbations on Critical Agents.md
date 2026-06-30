# 98. Robustness Testing for Multi-Agent Reinforcement Learning: State Perturbations on Critical Agents

## 元信息 (Metadata)
- **标题**: Robustness Testing for Multi-Agent Reinforcement Learning: State Perturbations on Critical Agents
- **作者**: Ziyuan Zhou, Guanjun Liu
- **机构**: Department of Computer Science, Tongji University, Shanghai, China
- **发表**: ECAI 2023 (IOS Press, doi:10.3233/faia230632)；arXiv 预印本 2023
- **链接/arXiv**: arXiv:2306.06136v1

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动（adversarial state perturbation），针对“critical agents”的对抗攻击
- **方法范式**: 鲁棒性测试 / 对抗攻击；Differential Evolution (DE) 优化 + Sarsa-based 联合动作价值评估 + FGSM 目标攻击；SA-Dec-POMDP 建模
- **关键词**: Robustness Testing, MARL, Critical Agents, Adversarial Attack, Differential Evolution, State Perturbation

## TL;DR（一句话总结）
提出 RTCA——首个允许“受害智能体可变”的 MARL 鲁棒性测试框架，用差分进化（DE）从所有智能体中选出关键智能体（critical agents）并给出其最坏联合动作，再以 FGSM 生成对抗观测，在攻击更少智能体的同时更有效地破坏团队合作策略。

## 问题与动机 (Problem & Motivation)
MARL 广泛用于智能交通、UAV 等，但对状态扰动脆弱；鲁棒性测试是确认模型可信度的关键步骤。多智能体场景相比单智能体有三大挑战：(1) 受害者不确定，无法直接建模为 Stochastic Game；(2) 某智能体次优动作未必导致团队失败；(3) 集中式训练过程在测试时通常不可用，且其基于“所有智能体最优”的假设，难以准确评估次优动作下的团队回报。已有 MARL 攻击方法（如 PAAD、基于 MARL adversary）均假设受害者固定，受害者改变即需重训。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 定义 SA-Dec-POMDP（agent State Adversarial Dec-POMDP）。攻击者向选定受害者的观测加 ℓ∞ 范数受限扰动（范围 0.1），目标是最小化团队期望累积折扣回报。受害者集合 M 可在每个时间步变化（stealthy）。仅攻击观测，不需训练，黑盒友好。
- **设定**: cooperative；CTDE（VDN/QMIX 受害模型）；测试/部署期攻击（execution-time），无需训练 adversary

## 方法 (Method)
- 步骤一（选关键智能体 + 最坏动作）：用 DE 全局优化求解 v_de(τ)=argmin_{M,{a^i}} Q_jt(τ, a^M, a^{-M})，候选解编码为 M 个受害者索引及其联合最坏动作（2M 元组），种群 400、F=0.5。DE 不要求 Q_jt 可微、不需网络结构，且 M 可灵活变化无需重训。
- 步骤二（团队合作策略评估）：因部署时无法访问集中式 Q_jt（且 VDN/QMIX 的 Q_jt 在次优动作下评估不准），用 Sarsa 在执行阶段以 ε-greedy 探索训练一个神经网络 Q̃_jt（输入状态 s 与联合动作 a）作为 DE 的目标函数。
- 步骤三（生成对抗观测）：已知受害者索引与目标最坏动作后，用 FGSM 解目标攻击优化（式13/14），使受害者策略输出靠近目标动作、远离真实动作。
- 整体 RTCA 流程每步重选受害者集合，攻击更隐蔽。

## 理论贡献 (Theoretical Contributions)
偏方法/实证；形式化定义 SA-Dec-POMDP 并说明其最优 adversary 联合策略等价于求解对应 Dec-POMDP 的最优联合策略（动作空间即对抗观测空间），从而可用 CTDE-based MARL 求解；但未提供新的收敛/复杂度定理（引用 SASG 的存在性与收缩性结果）。

## 实验 (Experiments)
- **环境/Benchmark**: StarCraft Multi-Agent Challenge (SMAC)，4 张地图：8m、2s3z、3s5z、3s6z；受害模型由 VDN、QMIX 训练 200 万步。
- **Baselines**: Random noise、FGSM、ATLA（PPO/MAPPO 训练的 adversary）、PAAD（director+actor 两步攻击，受害者固定）。
- **评估指标**: 胜率（Winning Rate, WR）与团队平均累积奖励（越低越好）；32 episode；扰动 ℓ∞=0.1。

## 主要结果 (Key Results)
- RTCA 在攻击较少智能体（尤其异质智能体场景与 |M|=2）时显著优于基线：如 QMIX 在 3s5z、|M|=2 时 WR 降至 0.00；VDN 多场景同样降至接近 0，奖励最低。
- Random noise 几乎无效（有时反而提升胜率，说明部分噪声对 MARL 决策有正面作用）；ATLA 因联合观测空间随智能体数指数增长，难学到 clean→adversarial 映射，效果差；FGSM 只考虑个体策略不考虑团队合作；PAAD 考虑团队但受害者必须固定。
- 消融：QMIX 的 Q_jt 比 VDN 更能准确表征联合策略质量；用 Sarsa 学的 Q̃_jt 效果与 QMIX 的 Q_jt 相当，在复杂场景（3s5z、3s6z）甚至更好，且 VDN 的 Q_jt 不适合作 DE 目标。
- 迁移性：QMIX 采样训练的 Q̃_jt 可成功攻击 VDN 智能体，反之亦然，显示 Q̃_jt 具备黑盒攻击的迁移潜力。

## 局限与未来工作 (Limitations & Future Work)
仅在 SMAC 离散动作空间验证；VDN 在 2s3z 表现弱导致 Q̃_jt 学习质量下降、攻击效果受限。未来工作：将 RTCA 扩展到连续动作空间方法（MADDPG、MAAC），测试其对关键智能体观测扰动的鲁棒性。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中“鲁棒性测试/对抗攻击”主题线，核心贡献是引入“critical/victim agent 可变”的攻击范式，与固定受害者的 MARLSafe（Guo et al.）、PAAD、ROMFAC、state-uncertainty robust MARL（He et al.）等形成对照，可作为综述中评估 CTDE 价值分解方法（VDN/QMIX）脆弱性、以及非梯度（DE）攻击优化的代表性工作。
