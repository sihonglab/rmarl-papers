# 143. Multi-Agent Reinforcement Learning for Cyber Defence: Transferability and Scalability

## 元信息 (Metadata)
- **标题**: Multi-Agent Reinforcement Learning for Cyber Defence Transferability and Scalability
- **作者**: Andrew Thomas, Matthew Yates, Oliver Osborne
- **机构**: Raytheon Strategic Research Group, Raytheon UK, Harlow, Essex, UK
- **发表**: Applied AI Letters, 2026; 7:e70015 (Wiley)
- **链接/arXiv**: https://doi.org/10.1002/ail2.70015

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 网络规模变化（scalability）、攻击场景/网络活动变化、分布外(OOD)任务变化；对抗智能体（red agent 网络攻击）
- **方法范式**: CTDE MARL（MAPPO/IPPO/HAPPO）、zero-shot transfer learning、任务分解（node-level POMDP）、Spatial Pyramidal Pooling (SPP) 标准化观测
- **关键词**: autonomous cyber defence (ACD), multi-agent RL, transfer learning, zero-shot transfer, scalability, PrimAITE

## TL;DR（一句话总结）
将自治网络防御（ACD）任务分解为与网络规模无关的机器(node)级局部 POMDP，用 CTDE MARL（MAPPO）训练小网络上的局部 agent，再零样本映射到更大网络，实现对网络规模、攻击场景与活动变化鲁棒且可扩展的网络防御。

## 问题与动机 (Problem & Motivation)
RL 对简单 ACD 任务有效，但难落地真实硬件：样本效率低、可迁移性差（环境微小变化即需重训）、随网络规模扩大动作/观测空间膨胀导致单智能体训练不稳定/难优化。传统 transfer learning 受限于固定动作-状态空间（网络规模需一致）。MARL 在 ACD 中尚属欠开发领域。目标：实现跨网络规模、跨动作/观测空间的零样本迁移。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: red agent 发起网络攻击（如 DDOS、序列入侵节点），green 为合法用户活动；鲁棒性针对网络规模(6/15/30 节点)、攻击模式、网络活动水平（low/medium/high/RAO/GAO）的变化，含 IID 与 OOD 零样本测试。形式化为 Contextual-MDP (CMDP)。
- **设定**: cooperative（共享全局 reward）；CTDE（MAPPO 共享 critic 训练，分布式执行）；online；零样本迁移（训练于小网络，无需重训部署到大网络）。

## 方法 (Method)
- **任务分解**: 将全局网络防御任务划分为机器(node)级管理 POMDP，每个局部 agent 仅观测单节点属性与相连链路信息，动作仅为该节点级动作，故与整体网络规模无关。
- **零样本迁移**: 训练好的局部 agent 按"节点类型 + 链路数相似度"一对多映射到新网络节点，无需额外训练（可复制 agent 控制多节点）。
- **CTDE / MAPPO**: 用 MAPPO（共享 critic 提供全网络上下文）训练局部 agent，保留单智能体的全局 reward 鼓励协作；对比 IPPO（独立）、HAPPO（顺序更新、单调改进）。
- **观测标准化**: 链路信息随规模可变，两种处理——padded（补零至 M 链路，有上限）与 pooled（1D SPP 层池化为固定长度 12 向量，理论上任意规模）。
- **环境贡献**: 扩展 DSTL PrimAITE 为 MA-PrimAITE，支持每步多个机器级操作同时执行。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证。指出独立多智能体(IPPO)环境非平稳使单智能体收敛保证失效，但无新理论证明。

## 实验 (Experiments)
- **环境/Benchmark**: MA-PrimAITE 三种规模网络（small 6 / medium 15 / large 30 节点），多种攻击与活动场景（proportional、low/medium/high、red-only、green-only）。
- **Baselines**: 原生训练的 MARL 局部 agent（直接训练于目标网络）、单智能体多动作 PPO、单动作 PPO。
- **评估指标**: 每 episode 平均 reward（越接近 0 越好，50 episodes 均值）；跨规模 reward 下降百分比；不同 agent 映射的方差。

## 主要结果 (Key Results)
- MAPPO 表现最佳，约匹配单动作 PPO；IPPO/HAPPO 略逊（HAPPO 更稳定）；多动作 PPO 因动作空间过大几乎无法学习，凸显 MARL 对分布式控制的优势。
- 迁移 agent 显著优于原生训练：Transfer Padded 在 medium/large 上 reward 比原生低 39%/64%；Transfer Pooled 提升 56%/78%。
- 跨规模鲁棒性：medium→large reward 下降，原生 125%/137%，Transfer Padded 仅 34%、Transfer Pooled 仅 13%，说明零样本性能对规模不敏感。
- 对活动变化鲁棒：除 red-activity-only(RAO，迁移反高 21%)外，迁移 agent 在各活动场景普遍优于原生 7%~27%；但 OOD 偏离过大时改进幅度收窄。
- Pooled(SPP) 迁移更好但方差更大、对节点映射更敏感。

## 局限与未来工作 (Limitations & Future Work)
agent 并行动作产生不必要动作；依赖有效的 agent-to-node 映射；MARL 对超参高度敏感；OOD augment 程度有限。未来：action masking 减少无效动作、学习自动最优映射（grid-wise/encoder-decoder）、分层 ACD（检测/推荐/动作 agent + manager）、基于 bisimulation 的表示学习、迁移到更真实的 emulated 网络(如 Imaginary YAK)。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 应用线（自治网络防御 ACD），鲁棒性体现为对网络规模、攻击场景与活动分布变化的零样本泛化/迁移鲁棒（generalisation robustness），而非形式化对抗扰动或认证。与 CTDE、可扩展性、迁移/泛化、网络安全应用主题相关，可作为 cyber defence 中"规模不变零样本迁移"的代表案例。
