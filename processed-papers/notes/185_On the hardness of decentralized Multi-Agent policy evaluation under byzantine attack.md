# 185. On the Hardness of Decentralized Multi-Agent Policy Evaluation under Byzantine Attacks

## 元信息 (Metadata)
- **标题**: On the Hardness of Decentralized Multi-Agent Policy Evaluation under Byzantine Attacks
- **作者**: Hairi, Minghong Fang (co-primary), Zifan Zhang, Alvaro Velasquez, Jia Liu
- **机构**: University of Wisconsin-Whitewater；University of Louisville；North Carolina State University；University of Colorado Boulder；The Ohio State University
- **发表**: IFIP WiOpt 2024（Int. Symp. on Modeling and Optimization in Mobile, Ad Hoc, and Wireless Networks），pp. 257–，ISBN 978-3-903176-65-2
- **链接/arXiv**: 未明确（IFIP/IEEE Xplore proceedings）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: Byzantine faulty agents（model poisoning）、heterogeneous local rewards、不一致信息（向不同邻居发不同值）
- **方法范式**: 不可能性 / hardness 证明、Byzantine-tolerant decentralized temporal difference (TD)、scalar function approximation、consensus + convergence 分析
- **关键词**: multi-agent policy evaluation, Byzantine attack, model poisoning, temporal difference learning, decentralized MARL, hardness

## TL;DR（一句话总结）
研究存在至多 f 个 Byzantine（model poisoning）智能体时的全去中心化多智能体 policy evaluation 问题：证明评估 normal 智能体奖励 uniform average 的理想目标不可达、且不存在能保证正权重数超过 |N|−f 的正确算法，进而提出一个在 scalar function approximation 下保证 asymptotic consensus 的 Byzantine-tolerant 去中心化 TD 算法并实验验证。

## 问题与动机 (Problem & Motivation)
Policy evaluation 是 cooperative MARL（actor-critic 的 critic 步）的重要子问题，已在无故障设定下被充分研究。但在全去中心化系统中，智能体仅通过通信网络共享参数，Byzantine 智能体可将本地参数改成任意值、且可向不同邻居发送不一致信息，比中心化服务器设定更难。现有 MARL 文献缺乏在 heterogeneous 局部奖励下针对这些挑战的鲁棒设计研究。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 至多 f 个 Byzantine 智能体，model poisoning——可发送任意/精心构造的值，并向不同邻居发不一致信息；normal 智能体集合 N，奖励异构
- **设定**: cooperative；fully decentralized（无中心服务器，仅邻居通信）；policy evaluation（给定策略 π）；TD learning + scalar function approximation

## 方法 (Method)
- 形式化理想目标：评估 normal 智能体奖励的 uniform average 值函数 V(s)；证明 Theorem 1——该目标不可达
- 退化为 relaxed 问题：评估 normal 智能体的适当 weighted average reward 值函数
- 进一步证明不存在能保证正权重总数超过 |N|−f 的正确算法（刻画可达性的根本限制）
- 提出 Byzantine-tolerant decentralized TD 算法，在 scalar function approximation 下保证 asymptotic consensus

## 理论贡献 (Theoretical Contributions)
两条 hardness/不可能性结果：(1) 无法评估 normal 智能体 uniform average 值函数；(2) 任何正确算法都无法保证正权重个数超过 |N|−f。并给出所提 Byzantine-tolerant TD 算法在 scalar function approximation 下的 asymptotic consensus 保证。

## 实验 (Experiments)
- **环境/Benchmark**: 去中心化多智能体 policy evaluation 数值实验
- **Baselines**: 未明确（与非鲁棒 / 受攻击 TD 对比）
- **评估指标**: consensus 达成情况、对 Byzantine model poisoning 的容忍性、值函数估计有效性

## 主要结果 (Key Results)
- 理论上确立 Byzantine 攻击下去中心化 policy evaluation 的根本难度：理想 uniform-average 目标不可达，且正权重数受 |N|−f 限制
- 所提 Byzantine-tolerant 去中心化 TD 算法在 scalar function approximation 下实证有效，能在攻击下达成 asymptotic consensus

## 局限与未来工作 (Limitations & Future Work)
理论保证限于 scalar function approximation；只解决 relaxed（weighted average）目标，无法恢复 uniform average；实验规模与 baseline 信息有限；未扩展到完整 control / 线性或非线性 function approximation。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中 [[Byzantine / fault-tolerance]] 线的核心理论工作，刻画去中心化 critic（policy evaluation）在 model poisoning 下的可达性边界，与 resilient consensus、[[robust distributed TD / actor-critic]]、heterogeneous-reward MARL 主题紧密相关，为去中心化鲁棒价值评估提供 hardness 基准。
