# 192. Data Poisoning to Fake a Nash Equilibrium in Markov Games

## 元信息 (Metadata)
- **标题**: Data Poisoning to Fake a Nash Equilibrium in Markov Games
- **作者**: Young Wu, Jeremy McMahan, Xiaojin Zhu, Qiaomin Xie
- **机构**: University of Wisconsin–Madison
- **发表**: AAAI 2024（AAAI-24）
- **链接/arXiv**: doi:10.1609/aaai.v38i14.29529

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 奖励/数据投毒（offline data poisoning），伪造（fictitious）唯一 Nash equilibrium
- **方法范式**: 攻击建模、unique Nash set 几何刻画、线性规划求最优攻击、博弈论均衡（MPE）
- **关键词**: data poisoning, Markov game, unique Nash equilibrium, offline MARL, linear program, reward polytope

## TL;DR（一句话总结）
刻画对 offline MARL 的数据投毒攻击：攻击者修改两人零和 Markov game 的离线数据集，以最小代价将任意（可为虚构的）联合策略安装为唯一 Markov-perfect Nash equilibrium；提出 unique Nash set（使目标策略成为唯一 NE 的 Q 函数集合）作为核心几何对象，攻击成功当且仅当所有 plausible games 被推入该集合，并用线性规划高效求最优攻击。

## 问题与动机 (Problem & Motivation)
数据投毒在监督学习和单智能体 RL 中已有充分研究，但对 Markov game/MARL 是否构成威胁尚不清楚。MARL 与单智能体 RL 关键不同：没有最优策略只有均衡，且可能存在多个差异巨大的均衡，故"把目标策略安装为唯一均衡"很难。朴素做法（改所有动作或把匹配目标策略的奖励抬到上界）要么因数据覆盖不足失败、要么代价非最优。需先理解攻击结构，才能设计更鲁棒的 MARL 算法。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 攻击者可离线修改数据集 D→D†（如 reward poisoning），支付代价 C(D,D†)；目标是任意纯策略对 π†=(π†₁,π†₂)，使学习者从 D† 学到 π† 且最小化 C；不要求 full data coverage
- **设定**: competitive（two-player zero-sum Markov game）；offline MARL；学习者计算 Markov Perfect Equilibrium (MPE)

## 方法 (Method)
- 提出 Unique Nash set (UN)：使目标 π† 成为唯一 NE 的 Q 函数集合；uniqueness 确保 agents 不在多 NE 间任意 break tie
- 提出攻击者的 Theory of Mind (ToM)：攻击者认为 agents 在收到 D† 后会考虑的 plausible Q 函数集合（confidence region）
- 攻击成功 ⟺ 通过控制 D† 把 ToM 集合整体移入 UN 集合；最小代价的成功攻击为最优
- 对零和 Markov game，inverse Nash set 与 plausible games 集合在 Q 空间均为多面体 (polytope)，故可用线性规划高效计算最优 reward poisoning

## 理论贡献 (Theoretical Contributions)
- 给出确定性策略是零和 Markov game 唯一 Markov-perfect NE 的几何刻画（UN set），将 IRL 中的 reward polytope 推广到 MARL
- 证明 inverse Nash set 与数据诱导的 plausible set 均为 Q 空间多面体，攻击可化为 linear program
- 表明对基于 confidence region 的一大类 model-based/model-free offline MARL 学习者，适当参数的攻击可成功

## 实验 (Experiments)
- **环境/Benchmark**: 偏理论；以 normal-form game 与两人零和 Markov game 说明并验证 LP 攻击
- **Baselines**: 朴素攻击（改全部动作 / 抬奖励至上界）作为对照
- **评估指标**: 攻击成功与否、攻击代价 C(D,D†) 最优性

## 主要结果 (Key Results)
- 在温和条件下，攻击者可以最小代价将任意虚构 NE 安装为唯一 MPE，威胁 offline MARL 安全
- UN/ToM/LP 框架（"ToM moves to the UN"）统一刻画最优投毒，且不要求 full coverage，弱于此前 DSMPE+full-coverage 假设
- 对大量已有 offline MARL 学习者攻击可普遍奏效

## 局限与未来工作 (Limitations & Future Work)
聚焦两人零和 Markov game 与 reward poisoning，一般和/多智能体、其他投毒形式有待扩展；攻击假设学习者计算均衡且其 plausible set 为 confidence region；论文定位为攻击分析，防御/鲁棒算法留作后续。

## 与综述的关联 (Relevance to Survey)
属"[[data poisoning]] / 奖励投毒攻击 MARL"线的代表性理论工作，从攻击者视角刻画 offline MARL 的脆弱性，是设计鲁棒/认证 MARL 算法的前置基础；与 §对抗攻击、§博弈论均衡（Nash/MPE）以及 IRL 的 reward polytope 思想相关联。
