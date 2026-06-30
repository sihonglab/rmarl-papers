# 157. Efficient Adversarial Attacks on Online Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Efficient Adversarial Attacks on Online Multi-Agent Reinforcement Learning
- **作者**: Guanlin Liu, Lifeng Lai
- **机构**: Department of Electrical and Computer Engineering, University of California, Davis
- **发表**: NeurIPS 2023；arXiv:2307.07670 (2023)
- **链接/arXiv**: arXiv:2307.07670

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 奖励投毒 (reward poisoning) + 动作投毒 (action poisoning)，由外生攻击者实施；目标是把智能体引向 target policy 或最大化攻击者自选奖励
- **方法范式**: 在线 MARL 攻击理论、Markov Game (NE/CE/CCE)、white/gray/black-box 攻击策略、regret/cost 分析
- **关键词**: adversarial attack, reward poisoning, action poisoning, mixed attack, online MARL, Markov game

## TL;DR（一句话总结）
研究在线 MARL 中坐落于智能体与环境之间的外生攻击者，证明只用动作投毒或只用奖励投毒在某些 Markov Game 上必然低效/失败，进而提出同时使用二者的 mixed attack 策略，可在对环境与算法无先验（gray/black-box）的情况下，以 sub-linear cost 与 sub-linear loss 强迫任意 sub-linear-regret 的 MARL 智能体收敛到攻击者指定的 target policy。

## 问题与动机 (Problem & Motivation)
MARL 被广泛用于安全攸关场景，理解对抗攻击的影响是构建可信系统的前提。单智能体 RL 的奖励/动作投毒攻击已有大量研究，但 MARL 攻击工作很有限，且多假设攻击者控制某个学习者或针对离线设置。本文系统研究在线 MARL 攻击：攻击者可监视状态、动作与奖励信号，并在智能体收到前篡改 feedback 或在环境收到前篡改 action，目标是在最小化篡改量（cost）的同时引导智能体学到 target policy 或最大化攻击者自选奖励。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 外生攻击者位于智能体与环境之间，可做 reward poisoning 和/或 action poisoning；分 white-box（已知环境）、gray-box（不知环境/算法但知 target policy）、black-box（连 target policy 也未知）三档信息能力
- **设定**: tabular episodic Markov Game（含 cooperation 与 competition），学习目标为 NE/CE/CCE；online；以 V-learning 等去中心化算法为受害者

## 方法 (Method)
- 用 loss（智能体偏离 target policy 的累计次数，或对攻击者最优策略的 regret）与 cost（动作与奖励篡改的累计量）评估攻击有效性
- 先给出**不可能性/局限性结果**：即便 white-box，存在某些 MG 使任何"仅动作投毒"或"仅奖励投毒"的 Markov 攻击策略都无法高效成功；并给出二者可高效的充分条件及对应攻击策略与 cost/loss 分析
- 提出 gray-box 下的 **mixed attack**（动作+奖励联合投毒）与 black-box 下的 **approximate mixed attack**
- 证明 mixed attack 可强迫任意 sub-linear-regret 智能体按 target policy 行动，且 cost 与 loss 均 sub-linear
- 在去中心化算法 **V-learning** 上具体分析 approximate mixed attack 的影响

## 理论贡献 (Theoretical Contributions)
给出仅动作/仅奖励投毒的不可能性结果与其高效成功的充分条件；证明 mixed attack 对任意 sub-linear-regret MARL 智能体可达 sub-linear cost 与 sub-linear loss 地强制收敛到 target policy；提供对 V-learning 的攻击代价/损失界。

## 实验 (Experiments)
- **环境/Benchmark**: 以理论为主，结合对 V-learning 等去中心化 MARL 算法的攻击分析（含数值验证）
- **Baselines**: 仅动作投毒 / 仅奖励投毒攻击作为对照
- **评估指标**: 攻击 cost（篡改累计量）与 loss（偏离 target policy 次数 / regret）

## 主要结果 (Key Results)
- 单一手段（仅动作或仅奖励投毒）存在本质局限，某些 MG 下无法高效成功
- mixed attack 在无环境/算法先验时即可以 sub-linear cost、sub-linear loss 强制智能体学到攻击者 target policy
- black-box 的 approximate mixed attack 同样能有效攻击 V-learning 等 sub-linear-regret 算法

## 局限与未来工作 (Limitations & Future Work)
分析限于 tabular episodic MG 与 sub-linear-regret 智能体假设；mixed attack 需同时操控动作与奖励两个通道，现实可行性受限；缺少针对此类攻击的防御机制设计（防御侧留待未来）。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中"攻击者视角/最坏情况投毒"线的代表性理论工作，刻画了在线 MARL 的攻击可行性边界，为 [[奖励投毒]]、[[动作投毒]] 威胁模型提供严格的 cost/loss 刻画；其不可能性结果与 mixed attack 的高效性为后续 [[鲁棒/容错 MARL]] 防御设计提供了攻击基线。
