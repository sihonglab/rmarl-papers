# 49. Black-box Adversarial Robustness Testing with Partial Observation for Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Black-box Adversarial Robustness Testing with Partial Observation for Multi-Agent Reinforcement Learning
- **作者**: Bang Zhang, Wenjian Luo*, Kesheng Chen, Yujiang Liu, Shuhan Qi, Xuan Wang
- **机构**: Guangdong Provincial Key Laboratory of Novel Security Intelligence Technologies, Institute of Cyberspace Security, School of Computer Science and Technology, Harbin Institute of Technology, Shenzhen
- **发表**: IEEE ICPADS 2025 (31st International Conference on Parallel and Distributed Systems)
- **链接/arXiv**: DOI 10.1109/ICPADS67057.2025.11323102

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动（合作 MARL 中针对 agent 观测的黑盒对抗攻击 / 鲁棒性测试）
- **方法范式**: 黑盒对抗攻击（query attack + substitute model）、稀疏攻击、victim/时步选择（基于 ΔQ）、鲁棒性测试框架
- **关键词**: c-MARL, black-box attack, robustness testing, partial observation, sparse attack, QMIX

## TL;DR（一句话总结）
提出首个在部分观测、黑盒条件下对合作 MARL 进行对抗鲁棒性测试的两步框架：第一步在 Ally/Enemy Observation Attack 两种受限信息场景下选 victim agent 与攻击时步，第二步用黑盒（query/substitute model）方法生成扰动加到 victim 观测上，以更少扰动步数大幅降低 QMIX 团队胜率与回报。

## 问题与动机 (Problem & Motivation)
合作 MARL 策略对观测对抗攻击脆弱，但现有鲁棒性测试方法多忽视现实可实施性：(1) 选 victim/时步常需 MARL 算法或差分进化，依赖大量先验、训练或实时计算，环境变化即需重训重算；(2) 通常需访问所有 agent 的观测，现实不可行；(3) 要么假设可直接改 agent 动作，要么白盒需模型参数。需要既具破坏性、又隐蔽（稀疏）、且现实可实施的测试方法。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 攻击者只能访问部分观测（AOA：仅用受害方 agent 的部分观测；EOA：仅用敌方的部分观测），黑盒（无模型参数）；扰动加在选定 victim 的观测上，受扰动步数（稀疏）约束。考虑 query attack 与 substitute model attack 两种黑盒生成方式。
- **设定**: cooperative（c-MARL，对战脚本敌人）；CTDE / QMIX；测试/攻击阶段（针对已训练策略）

## 方法 (Method)
1. **两步框架**: 第一步选 victim agent 并筛选攻击时步；第二步生成并注入对抗扰动到 victim 观测。
2. **AOA (Ally Observation Attack)**: 仅用己方 agent 的部分观测，依据 ΔQ（攻击造成的最大 Q 值变化）选择 victim 与关键时步。
3. **EOA (Enemy Observation Attack)**: 仅用敌方部分观测来决定攻击，仅在 agent 与敌交战时发起，信息更受限、更难。
4. **黑盒扰动生成**: 扩展黑盒对抗攻击，分别用 query-based（直接查询）与 substitute model（训练替代模型，sAOA）两种方式生成扰动；用环境特征作为观测引导提升效果。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证

## 实验 (Experiments)
- **环境/Benchmark**: SMAC 多张地图（2s3z、MMM 等），受害团队由 QMIX 训练
- **Baselines**: 需访问全部 agent 观测的现有攻击方法；victim 随机选 vs 基于 ΔQ 选 (AOA)；query 黑盒 vs substitute model (sAOA)
- **评估指标**: 团队胜率 win rate、团队回报 team reward、所需扰动步数；消融研究

## 主要结果 (Key Results)
1. AOA 仅用部分观测就能以更低扰动步数显著降低 QMIX 团队胜率与回报，效果接近甚至优于需全观测的对比方法；ε≈0.3 时性能趋于收敛。
2. EOA 信息更受限、只在交战时攻击，效果弱于 AOA 且随环境复杂度上升而下降。
3. substitute model 版本 (sAOA) 性能接近 query-based 黑盒方法，且无需在线查询，进一步提升实用性。

## 局限与未来工作 (Limitations & Future Work)
EOA 在复杂环境下效果有限；评估限于 SMAC + QMIX；为"测试/攻击"工作而非防御方法，未提出鲁棒训练方案；扰动有效性依赖 ΔQ 等启发式。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中"观测扰动攻击 / 鲁棒性测试"主线，强调现实可实施性（黑盒 + 部分观测 + 稀疏），可作为评估 c-MARL 鲁棒性的攻击基准；与稀疏对抗攻击、critical-agent/critical-step 选择、黑盒攻击等工作相关。
