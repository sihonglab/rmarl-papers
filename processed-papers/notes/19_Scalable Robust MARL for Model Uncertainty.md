# 19. Scalable Robust Multi-Agent Reinforcement Learning for Model Uncertainty

## 元信息 (Metadata)
- **标题**: Scalable Robust Multi-Agent Reinforcement Learning for Model Uncertainty
- **作者**: Younkyung Jwa, Minseon Gwak, Jiin Kwak, Chang Wook Ahn, PooGyeon Park（前三位 equal contribution）
- **机构**: GIST（光州科学技术院）、POSTECH（浦项科技大学）、UNIST（蔚山科学技术院），韩国
- **发表**: 2023 62nd IEEE Conference on Decision and Control (CDC) 2023
- **链接/arXiv**: DOI: 10.1109/CDC49753.2023.10383458（arXiv 未明确）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 模型不确定性 (model uncertainty)，具体建模为奖励函数的不确定性（noisy reward），以及由此导致的 transition 不确定性
- **方法范式**: robust Markov game / robust Nash equilibrium、nature actor（虚拟对抗 agent 的 minimax/zero-sum 思想）、attention-based MADDPG、进化课程学习 (evolutionary population curriculum)
- **关键词**: scalable robust MARL, model uncertainty, robust Nash equilibrium, nature actor, attention, population curriculum, evolutionary learning

## TL;DR（一句话总结）
针对智能体数量增多时鲁棒 NE 搜索空间爆炸的问题，提出 EDPC（进化保多样性种群课程）框架 + RA-MADDPG（基于 attention 的 nature actor 鲁棒 MADDPG），通过分阶段扩大博弈规模与保持种群多样性，在大规模、有模型不确定性的环境中高效找到鲁棒策略。

## 问题与动机 (Problem & Motivation)
鲁棒 MARL（如 R-MADDPG 用 nature actor 找鲁棒 NE）在 agent 数量增加时，搜索空间指数膨胀，鲁棒性显著下降；而已有可扩展 MARL 方法（如 EPC 进化种群课程）忽略模型不确定性，且其种群生成规则限制了多样性。robustness 与 scalability 兼顾的 MARL 研究不足。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 每个 agent 的奖励从截断高斯分布采样（均值为原奖励，标准差为噪声率 σ，截断阈值 [−θ, θ]），不确定性集 R̄i 为可能奖励值集合。鲁棒 NE 定义为最大化 worst-case 期望奖励（对不确定性集做 min）。nature actor 作为虚拟对抗 agent 与各 agent 构成 zero-sum game。
- **设定**: fully-cooperative（食物收集）；CTDE（中心化 critic + 分散 actor，nature actor 作分散奖励估计器）；online 训练，train/test 环境存在差异

## 方法 (Method)
- **RA-MADDPG**: 在 MADDPG 上引入 nature actor（输出在奖励不确定性集内的保守奖励），critic 用 nature actor 的奖励而非实际奖励训练以产生鲁棒 Q 值；nature actor 朝缩小预测奖励与观测奖励差距且降低预测奖励的方向更新。
- **Attention 网络**: actor/critic/nature actor 均用 self-attention 模块，使网络参数量固定，可处理变化的 agent 数量（global attention embedding 为其他 agent 编码的加权和），支撑课程中环境规模扩展。
- **EDPC 框架**: 课程分多阶段（agent 数 3→6→12），从基因算法视角把阶段视为 generation、agent 集视为 individual、agent 视为 gene，奖励作 fitness。每阶段用两个父代合并（agent 数翻倍）生成下一代。
- **Reward-proportionate parent selection**: 按缩放后的 fitness（指数映射 e^{α|r_A|/r_max}）成比例选父代，使低奖励个体也有被选概率，保持多样性。
- **Reward-guided mutation**: 以概率 µ 用同一 individual 内更高奖励的 agent 替换（cooperative + reward-guided 候选集），在保持协作的同时提升多样性与达到鲁棒 NE 的概率。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（沿用 [18] 的 robust NE 公式定义，本文贡献为可扩展框架与算法设计 + 实验验证，无新的收敛性/样本复杂度证明）

## 实验 (Experiments)
- **环境/Benchmark**: food collection 环境（N 个协作 agent 占领 N 个食物、避免碰撞，奖励含噪声），目标系统 12 agent
- **Baselines**: MADDPG、R-MADDPG、EPC，对比本文 EDPC
- **评估指标**: 全协作设定下所有 agent 的平均奖励（噪声环境训练、To=10^4 episode 测试），分 3/6/12 agent 系统评估

## 主要结果 (Key Results)
- 噪声率 σ=1,2,3,6 下，EDPC 在 6 与 12 agent 系统均取得最高平均奖励；例如 σ=6 的 12-agent 系统 EDPC 达 54.151，而 EPC 仅 7.751、R-MADDPG 为 -1.754。
- MADDPG/R-MADDPG 奖励随噪声增大而下降，说明 R-MADDPG 因 scaling 无法很好找到鲁棒 NE；EPC 在低噪声尚可但高噪声急剧下降。
- 随阶段演化，EDPC 在 agent 数增加时性能反而提升。
- 消融：reward-guided mutation 与 reward-proportionate parent selection 两组件各自叠加均提升鲁棒奖励，验证保持种群多样性有助于发现更优鲁棒 NE。

## 局限与未来工作 (Limitations & Future Work)
未来工作：在存在非协作 agent 的环境中验证 EDPC，发展更通用、更多场景适用的 MARL 算法。隐含局限：仅在单一协作 food collection 环境验证、不确定性仅限奖励噪声、缺乏理论保证。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"模型不确定性 + robust Nash equilibrium（nature actor / 博弈论 minimax）"主线，并独特地将 scalability（attention + 进化课程学习）与 robustness 结合，填补大规模鲁棒 MARL 空白。与 R-MADDPG (Zhang et al. 2020)、EPC、minimax MARL 等工作直接关联。
