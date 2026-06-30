# 95. StarCraft+: Benchmarking Multi-agent Algorithms in Adversary Paradigm

## 元信息 (Metadata)
- **标题**: StarCraft+: Benchmarking Multi-agent Algorithms in Adversary Paradigm
- **作者**: Yadong Li, Tong Zhang, Bo Huang, Zhen Cui
- **机构**: Nanjing University of Science and Technology（Yadong Li 兼 Zaozhuang University）
- **发表**: 未明确（IEEE 期刊投稿格式，arXiv 预印本）
- **链接/arXiv**: arXiv:2512.16444v1；代码 https://github.com/dooliu/SC2BA

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体 / 可进化对手 (evolvable opponents)、对未见对手的泛化、场景布局变化（对称/非对称兵力）；区别于固定 built-in AI 对手带来的策略偏置
- **方法范式**: benchmark / 评测平台、algorithm-vs-algorithm 对抗范式、self-play 式动态对手、价值分解/policy-based MARL 评测
- **关键词**: MARL benchmark, evolvable opponents, dual-algorithm paired adversary, multi-algorithm mixed adversary, SMAC, StarCraft II

## TL;DR（一句话总结）
针对 SMAC 中敌方由固定 built-in AI 控制导致评测多样性不足的问题，构建 algorithm-vs-algorithm 的 StarCraft II Battle Arena (SC2BA) 平台与 APyMARL 库，让红蓝双方均由 MARL 算法控制并动态对抗（dual-algorithm paired 与 multi-algorithm mixed 两种模式），从而更全面评测算法的泛化性、策略多样性与对抗鲁棒性。

## 问题与动机 (Problem & Motivation)
深度合作 MARL 蓬勃发展，SMAC 是广泛使用的 benchmark，但其敌方单位由固定规则的 built-in AI 控制，造成评测多样性与通用性不足：(1) 对手非单调性缺失——agent 易利用预设 AI 的潜在致命规则，学到有偏策略，面对不同战法对手时性能差；(2) 对手不可进化——静态规则下 agent 很快学会取胜技巧但难泛化，缺乏对手动态变化；(3) 双方均可进化时的对抗公平性评估问题；(4) 系统易用性与可定制性。现实对抗环境中对手具进化能力，被多数 MAS 忽略。需要一个支持算法间持续对抗的平台来更好评测/训练鲁棒 MARL。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 对手不再是固定 built-in AI，而是由其它 MARL 算法控制并在对抗过程中持续优化（evolvable/dynamic opponent）。两种对抗模式：dual-algorithm paired（成对算法互搏）、multi-algorithm mixed（面对一组算法的多种行为）。对称与非对称（兵力不等）战斗场景。
- **设定**: competitive（双队对抗，队内合作）；CTDE / decentralized micromanagement（沿用 SMAC 范式）；online 对抗训练与评测

## 方法 (Method)
- 平台 SC2BA：基于 StarCraft II（SMAC/SC2LE 之上），模块化设计——configuration module（统一地图文件、文本化可控场景配置、可指定双队算法）、interaction module（双队各自获取观测、由各自算法决策）、bottom-level control module。
- 双队均由 MARL 模型控制，起点可随机或用已训练模型（如对 built-in AI 训得），训练时双方算法相互适应。
- 两种对抗模式：paired（一对一算法对抗）与 mixed（对一组算法的多对手对抗），以评测泛化、多样性、对抗能力。
- 开源 APyMARL 库：基于 PyTorch、模块化可扩展，提供易用接口配置。
- 设计对称/非对称战斗场景（高维输入、部分可观测、丰富动态、联合协调挑战）。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（benchmark 平台与库的贡献，无理论分析）。

## 实验 (Experiments)
- **环境/Benchmark**: SC2BA 自身的对称场景（3m, 8m, 2s3z, 3s5z, MMM, 1c3s5z, 25m 等）与非对称场景（5m_vs_6m, 10m_vs_11m, MMM2）
- **Baselines**: 八种经典 MARL 算法（含 QMIX、VDN、MAPPO、DOP 等 value-based 与 policy-based）；三种训练模式对比：dual-algorithm、mixed-algorithm（来自 SC2BA）、built-in AI（来自 SMAC）
- **评估指标**: median test win rate（跨场景中位胜率）、胜率提升场景数、与 PCA+MeanShift 的联合动作多样性可视化

## 主要结果 (Key Results)
- 在 SC2BA 两种对抗模式训练的 agent，对战仅用 built-in AI 训练的 agent 时胜率更高；paired 模式略优于 mixed 模式，归因于可进化动态对手隐式增加策略-反策略博弈的多样性/复杂度。
- PCA+聚类显示：paired/mixed 模式学到的联合动作多样性明显高于 built-in AI 模式（paired 略高于 mixed），印证对抗模式提升策略多样性。
- one-vs-multiple（mixed）对抗即便在简单场景也具挑战性；需要复杂策略的场景（如某些异构场景）多数算法胜率不足 40%。
- 非对称场景仍很难，算法对兵力轻微不均敏感；异构单位场景（MMM2）中 VDN 等表现突出。
- 总体：algorithm-adversary 能提升策略多样性、模型鲁棒性与泛化能力，并暴露场景布局敏感性、异构难度、对抗波动、多对手联合进化等待研究问题。

## 局限与未来工作 (Limitations & Future Work)
- 揭示但未解决的问题：对场景布局（兵力）敏感、异构场景困难、算法对抗的波动性、多对手联合进化等，需新算法及重新审视游戏机制（奖励函数、运动规律等）。
- 未来：探索动态 multi-algorithm mixed adversary，设计更多非对称场景进一步优化平台。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 的"评测平台 / benchmark + 对抗智能体鲁棒性"主题，针对"固定对手导致策略偏置、对未见对手不鲁棒"这一核心痛点，用 algorithm-vs-algorithm 的可进化对手范式（接近 self-play / 对手建模）评估泛化与对抗鲁棒性。与 SMAC、对手不确定性、对抗训练、self-play 等主题相关，为综述中 competitive 设定下的鲁棒性评估提供了新的实验基础设施。
