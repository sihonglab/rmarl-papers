# 168. The Emergence of Adversarial Communication in Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: The Emergence of Adversarial Communication in Multi-Agent Reinforcement Learning
- **作者**: Jan Blumenkamp, Amanda Prorok
- **机构**: University of Cambridge, Department of Computer Science and Technology
- **发表**: Conference on Robot Learning (CoRL) 2021（PMLR）；arXiv:2008.02616（标注 CoRL 2020）
- **链接/arXiv**: arXiv:2008.02616；代码 https://github.com/proroklab/adversarial_comms

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗/操纵性通信（adversarial communication）——self-interested 智能体通过可微通信信道误导/操纵协作团队
- **方法范式**: GNN（AGNN/GCNN）可微通信、self-interested 多目标 MARL、policy gradient（VPG）、post-hoc 可解释性可视化
- **关键词**: Graph Neural Networks, adversarial communication, self-interested agents, differentiable communication channel, interpretability

## TL;DR（一句话总结）
提出一个支持非共享个体奖励、并在全体智能体间共享同一可微通信信道的学习模型，证明仅靠"忽视他人奖励"的 self-interested 智能体即可自发涌现出高度操纵性的对抗通信策略，并用 post-hoc 可解释性技术可视化这些消息，揭示单个自利智能体可显著压制整支协作团队。

## 问题与动机 (Problem & Motivation)
基于 GNN 的可微通信已能让协作 MARL 学到复杂协调策略，但这些工作都假设全体智能体共享同一全局目标。当智能体有各自的 self-interested 目标时，标准做法是把它们建成相互独立的学习系统，从而无法存在单一可微通信信道，也就无法学习"跨智能体的通信策略"。本文填补这一空白，研究自利智能体能否在共享可微信道下学到非协作甚至对抗性的通信，并主张"理解对抗通信如何涌现"是日后防御它的第一步。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 攻击来自通信内容本身——一个或多个 self-interested 智能体在共享可微信道上发送可操纵其他智能体行为的消息；这些智能体并非"为攻击而设计"，只是无视他人奖励
- **设定**: mixed cooperative-competitive（部分协作 + 部分自利）；decentralizable（GNN 局部多跳通信）；online 强化学习

## 方法 (Method)
- 设计一个 monolithic 但可去中心化执行的神经架构，容纳多个不同的奖励函数与一个全体共享的可微通信信道，使跨智能体的通信策略可被端到端学习
- 通信骨干采用 Aggregation Graph Neural Networks (AGNN)/GCNN，通过图位移算子在多跳邻居间聚合并传递连续消息
- 用 Vanilla Policy Gradient (VPG) 训练各自利智能体群体，使对抗通信"自发涌现"，无需显式以操纵为优化目标
- 引入 post-hoc 可解释性技术，可视化智能体相互发送的消息，分析操纵行为的语义

## 理论贡献 (Theoretical Contributions)
无 / 偏实证。核心是模型与现象学层面的贡献（可微共享信道 + 对抗通信涌现的实证验证），未给出收敛性或博弈均衡的形式化结果。

## 实验 (Experiments)
- **环境/Benchmark**: 多智能体 coverage（覆盖）与 path planning（路径规划）任务，含协作智能体与自利智能体的混合
- **Baselines**: 纯协作团队（全体共享全局奖励）的 GNN 通信策略
- **评估指标**: 自利智能体回报相对协作团队的优势、通信消息的可解释可视化、涌现条件分析

## 主要结果 (Key Results)
- 单个 self-interested 智能体能学到高度操纵性的通信策略，显著超越整支协作团队
- 当局部奖励来自有限资源池、或资源处于竞争状态时，对抗通信会自发涌现
- 操纵性自利智能体无需"为对抗而设计"，仅无视他人奖励即可产生攻击性行为；可解释性可视化揭示其消息内容

## 局限与未来工作 (Limitations & Future Work)
本文聚焦"展示对抗通信如何涌现"，未给出防御/鲁棒化方法；实验限于 coverage 与 path planning 等较小规模任务；缺少形式化理论与对更大智能体团队的可扩展性验证。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中 [[通信攻击]] 线的奠基性"攻击侧/威胁建模"工作，首次展示可微 GNN 通信下对抗消息的自发涌现，为后续 [[communication-robust MARL]]（如 MA3C 等防御方法）提供了威胁模型与动机；与 [[GNN 通信]]、[[mixed cooperative-competitive]] 主题相关。
