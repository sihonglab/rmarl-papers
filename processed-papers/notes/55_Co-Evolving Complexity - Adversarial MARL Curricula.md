# 55. Co-Evolving Complexity: An Adversarial Framework for Automatic MARL Curricula

## 元信息 (Metadata)
- **标题**: Co-Evolving Complexity: An Adversarial Framework for Automatic MARL Curricula
- **作者**: Brennen A. Hill
- **机构**: Department of Computer Science, University of Wisconsin-Madison
- **发表**: NeurIPS 2025 Workshop: Scaling Environments for Agents (SEA)
- **链接/arXiv**: arXiv:2509.03771v3 [cs.LG]

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体 / 环境复杂度与多样性不足（通过对抗生成环境提升泛化与鲁棒性）
- **方法范式**: 对抗训练 / 自动课程学习（automatic curriculum）；co-evolution（协同进化）；adversarial procedural content generation（PCGRL）；CTDE + MAPPO（PPO）；近零和 POMG 博弈
- **关键词**: adversarial curriculum, co-evolution, procedural content generation, MARL, MAPPO, emergent behavior

## TL;DR（一句话总结）
将环境生成本身建模为对抗博弈：一个生成式 Attacker 智能体不断程序化生成越来越难的敌方单位配置以击败一支协作 Defender 团队，二者协同进化形成自扩展的无限课程，从而自动涌现复杂协作/对抗策略并提升智能体鲁棒性。

## 问题与动机 (Problem & Motivation)
通用智能体能力受限于训练环境；手工设计环境有限且带偏见，难以扩展复杂度、多样性与交互性，导致智能体过拟合固定场景、难以获得可泛化、鲁棒的技能。作者主张像 scaling model/data 一样 scaling 环境复杂度。已有 PCGML 受训练数据束缚（imitative），PCGRL 用静态手工奖励，Generator-Solver 框架只面向单 solver 静态关卡。本文将其扩展到多智能体协作团队和动态自扩展课程。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: Attacker 作为对手在组合巨大的参数空间（lane、health、damage、speed、range、regeneration、leech、defenses、penetration、type 等）中程序化生成敌方单位，针对 Defender 当前弱点动态制造挑战；生成单位的能量代价是参数的超线性函数，迫使数量/质量权衡。Defender 对 Attacker 内部状态（能量、策略）部分可观测。
- **设定**: mixed-motive——Defender 团队 fully cooperative，Defender vs Attacker fully competitive（近零和）；formalized as 两队 partially observable Markov game (POMG)；CTDE（训练用全局信息，执行用局部观测）；online co-evolution

## 方法 (Method)
- 形式化为两队近零和 POMG：N=4 个异构（各有独特角色/特殊能力）协作 Defender vs 单个生成式 Attacker，10×30 网格、离散时间。
- Attacker 每步选择"生成带参数 θ 的单位"或"不动以保存能量"；生成单位按硬编码行为前进/攻击，复杂度来自 Attacker 的生成选择而非单位 AI。
- Defender 共享策略、无显式通信通道，动作空间含移动/射击/治疗/特殊能力/不动（各有能量成本）。
- 两方均用 PPO（MAPPO 范式）训练；Attacker 的奖励动态来自 Defender 的表现，构成自适应"学习到的损失函数"，形成 co-evolutionary arms race（Red Queen 动态），驱动无限新颖课程。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（系统与机制论证，强调非平稳性与协同进化作为开放式学习驱动，未给收敛/均衡理论）

## 实验 (Experiments)
- **环境/Benchmark**: 自建 2D 网格塔防式 POMG（10 lanes × 30 tiles，4 Defender + 1 Attacker）
- **Baselines**: 双方均匀随机动作的 random baseline；消融：训练方 vs 随机对手（Defender vs random Attacker、Attacker vs random Defender）
- **评估指标**: 平均 episode 长度（Defender 存活步数）、四种 signature 涌现策略（Tandem、Flanking、Cooperative Spreading、Cooperative Focusing）的使用率与每局次数（100 次独立运行平均，500 episodes 训练）

## 主要结果 (Key Results)
- 训练后涌现复杂策略：Attacker 的 Tandem（98.2%）、Flanking（94.0%）；Defender 的 Cooperative Spreading（92.6%）、Focusing（81.4%），而随机基线下这些策略出现率均 <11%。
- 训练智能体平均存活 83 步，约为随机基线（19 步）的 4 倍多。
- 消融证明 co-evolution 是关键：Defender 对抗随机 Attacker 时几乎不学协作策略（Spreading 13.2%）；Attacker 对抗随机 Defender 时策略深度消失（Flanking 13.7%、Tandem 21.2%）。存活曲线非单调振荡，体现 arms race。

## 局限与未来工作 (Limitations & Future Work)
- 仅在消费级硬件训练 500 episodes，更长训练可能涌现更复杂策略；自建简化环境，泛化性待验证。
- 未来：引入 LLM 作为 Attacker（高层策略目标）或 Defender 的高层规划/通信；扩展生成器至修改地形/障碍/新单位类型（tool-use/compositional）；用 XAI 分析学得策略；population-based training 多物种协同进化。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"对抗训练 / 课程学习 / 自动环境生成提升鲁棒性与泛化"线，强调用 adversarial co-evolution 产生开放式、自扩展课程对抗过拟合与脆弱策略；与 unsupervised environment design (POET)、adversarial curricula、self-play 鲁棒训练相关，也呼应通过对手生成挑战来增强协作策略鲁棒性的主题（可与 #57 进化式辅助对抗攻击者等对照）。
