# 154. A Robust and Constrained Multi-Agent Reinforcement Learning Electric Vehicle Rebalancing Method in AMoD Systems

## 元信息 (Metadata)
- **标题**: A Robust and Constrained Multi-Agent Reinforcement Learning Electric Vehicle Rebalancing Method in AMoD Systems
- **作者**: Sihong He, Yue Wang, Shuo Han, Shaofeng Zou, Fei Miao
- **机构**: University of Connecticut；University at Buffalo (SUNY)；University of Illinois Chicago
- **发表**: IROS 2023；arXiv:2209.08230
- **链接/arXiv**: arXiv:2209.08230；doi:10.1109/IROS55552.2023.10342342

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态转移核 (state transition kernel) 模型不确定性，叠加运行约束
- **方法范式**: robust constrained MARL、robust natural policy gradient (RNPG)、应用（EV AMoD 调度）
- **关键词**: model uncertainty, constrained MARL, EV rebalancing, AMoD, robust natural policy gradient

## TL;DR（一句话总结）
针对电动车 (EV) 在 AMoD 系统中独特充电模式加剧模型不确定性、且须同时满足约束的难题，设计带状态转移核不确定性的 robust constrained MARL 框架，提出 **ROCOMA** 算法（用 robust natural policy gradient, RNPG）学习在模型不确定下兼顾供需平衡与充电利用率的鲁棒调度策略，公平性 +19.6%、调度成本 -75.8%。

## 问题与动机 (Problem & Motivation)
AMoD 是节能交通的重要方案，EV 因充电模式使系统状态转移概率等模型不确定性更大，而训练与真实环境普遍失配；已有 EV AMoD 调度工作未显式考虑模型不确定性，且"模型不确定性 + 决策须满足约束"的并存使问题更难。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 状态转移核落在不确定性集内，求最坏情况下满足约束的鲁棒策略
- **设定**: cooperative（多区域/多智能体协同调度）；constrained（供需比、充电利用率约束）；centralized 训练，应用部署

## 方法 (Method)
- 将 EV AMoD 调度建模为带 state-transition-kernel 不确定性的 robust + constrained MARL
- 提出 **ROCOMA**：在 robust 目标下用 **robust natural policy gradient (RNPG)** 训练策略，兼顾鲁棒性与约束满足
- 学习平衡全城供需比与充电利用率的鲁棒再平衡策略

## 理论贡献 (Theoretical Contributions)
给出 robust constrained MARL 的算法框架与 RNPG 更新（鲁棒自然策略梯度）；以应用驱动，理论保证为辅。

## 实验 (Experiments)
- **环境/Benchmark**: EV AMoD 城市调度仿真（真实城市出行数据驱动）
- **Baselines**: 非鲁棒 MARL 调度方法
- **评估指标**: 系统公平性、调度成本、供需平衡、模型扰动下的鲁棒性

## 主要结果 (Key Results)
- ROCOMA 学到有效且鲁棒的再平衡策略，在模型不确定性下优于非鲁棒 MARL
- 系统公平性提升 19.6%，再平衡成本降低 75.8%

## 局限与未来工作 (Limitations & Future Work)
聚焦 EV AMoD 场景；不确定性集形式与约束类型的一般化、向更大城市规模与在线学习的扩展待探索。

## 与综述的关联 (Relevance to Survey)
属 §9 安全+鲁棒应用线中"模型不确定性 + 约束"的代表（被本语料 5× 引用），与同组 [[28_Robust MARL with State Uncertainty]]、[[1_Robust MARL with Model Uncertainty]] 等共同支撑"鲁棒 MARL 落地交通/能源"的应用主线。
