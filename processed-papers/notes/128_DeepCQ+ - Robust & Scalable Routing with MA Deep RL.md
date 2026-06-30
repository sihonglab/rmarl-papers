# 128. DeepCQ+: Robust and Scalable Routing with Multi-Agent Deep Reinforcement Learning for Highly Dynamic Networks

## 元信息 (Metadata)
- **标题**: DeepCQ+: Robust and Scalable Routing with Multi-Agent Deep Reinforcement Learning for Highly Dynamic Networks
- **作者**: Saeed Kaviani, Bo Ryu, Ejaz Ahmed, Kevin Larson, Anh Le, Alex Yahja, Jae H. Kim
- **机构**: EpiSys Science, Inc.; Boeing Research and Technology
- **发表**: MILCOM 2021 - IEEE Military Communications Conference (DOI: 10.1109/MILCOM52596.2021.9652948)
- **链接/arXiv**: IEEE Xplore (MILCOM 2021)；arXiv 对应版本见 127 (arXiv:2101.03273)

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 高动态网络（拓扑变化、节点移动、链路中断、流量动态）、战术网络的干扰/jamming 背景、训练范围外 (OOD) 的网络规模/移动/流量配置（鲁棒性偏"泛化/可扩展性 + 可靠性"工程意义）
- **方法范式**: MADRL、CTDE、参数共享、PPO、Dec-POMDP、hybrid (CQ+ 协议结构 + deep RL 替换手工阈值规则)
- **关键词**: MANET、DeepCQ+、Robust Routing、MADRL、Scalability、Adaptive Flooding

## TL;DR（一句话总结）
DeepCQ+ 将 MADRL（PPO+CTDE+参数共享）嵌入基于 Q-learning 的 CQ+ 路由协议结构，用学习的 agent 替代静态阈值与手写规则来决策自适应广播/单播，仅在单一网络规模训练即可泛化到未训练的更大规模/动态/流量，相比 CQ+ 节省 10–25% overhead 并提升 1–5% delivery ratio（127 工作的 MILCOM 2021 发表版）。

## 问题与动机 (Problem & Motivation)
战术 MANET 高度动态、不可预测（移动、拓扑、干扰、jamming），传统路由需频繁重算路由导致吞吐周期性损失；CQ+ 路由 (SRR/R2DN) 用置信度 C 值 + 自适应广播提升可靠性，但其广播/单播切换仅依赖单一参数（best-path 置信度），视角局部、未考虑拓扑高变率与拥塞。现有 MADRL 路由为节点训练专属策略，规模可扩展性差、新增节点需重训练。需要同时可扩展且鲁棒的策略。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不确定性来自高动态网络 (Gauss-Markov 移动)、变网络规模、变动态等级/区域尺度、多数据流；目标是训练分布之外的鲁棒泛化。战术场景隐含 jamming/干扰。无显式对抗博弈。
- **设定**: cooperative（Dec-POMDP，同质节点共享策略）；CTDE（仿真离线集中训练，分布式在线执行，执行时不需参数共享，C/H 值经 ACK 实时更新）；online 执行

## 方法 (Method)
1. **保留 CQ+ 协议结构**: 仅用 MADRL 替换静态阈值/手写规则来决策广播 vs 单播（自适应 flooding）；next-hop 仍由 CQ+ 规则选取（本版聚焦广播/单播动作）。
2. **可扩展输入**: 从邻居中按 h·(1-c) 选最佳 K 个固定维度输入 FCNN，使策略与规模解耦；观测含 C/H 值、其时间变化率及上一动作。
3. **奖励设计**: type 1 复现 CQ+ 概率广播；type 2 引入归一化 overhead 最小化项（含 delivery 奖励、no-ACK 惩罚、Nack/N 估计额外传输），在保持/提升 goodput 下降低 overhead。
4. PPO + 参数共享训练（Ray/RLlib，50M steps），可灵活调节 goodput/broadcast/delay 之间的权衡。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（含将 CQ+ 策略重构为 RL 最优策略的推导以指导奖励设计，无收敛/泛化界）

## 实验 (Experiments)
- **环境/Benchmark**: 自研 CQ+ 路由仿真器 (Ray/RLlib)，benchmark 拓扑基于 AR/CQ+ 工作，Gauss-Markov 移动、分区域速度；训练单一规模 (N=12)，测试 N=12–30 (更大动态/区域随机化)
- **Baselines**: CQ-routing、SRR/CQ+ routing (R2DN, 非 DRL 基线)；Q-routing 谱系
- **评估指标**: goodput/delivery ratio、normalized overhead (类型1/2)、broadcast rate、跳数/端到端延迟

## 主要结果 (Key Results)
1. 仅在 12 节点训练的 PPO 策略可泛化到 N=12–30 (乃至 >50)，保持性能，体现可扩展鲁棒性。
2. 相比 CQ+ 基线，DeepCQ+ 需要约 10–25% 更少 overhead，同时 delivery ratio 提升约 1–5%，且广播比例更低、节省资源。
3. 端到端延迟（跳数）无明显退化；MADRL 框架可适配不同部署目标 (goodput/broadcast/delay 权衡)，这是 CQ+ 不具备的。

## 局限与未来工作 (Limitations & Future Work)
本版动作空间仅含广播/单播选择，next-hop 仍由 CQ+ 决定；计划扩展动作空间至 unicast 模式下的 next-hop 选择并采用其他 MADRL 技术；计划用 RNN 单元策略以捕捉更高增益。未做显式对抗 jamming 鲁棒性评估。

## 与综述的关联 (Relevance to Survey)
robust MARL "可扩展性/泛化鲁棒 + CTDE 参数共享"工程线在战术通信网络路由的代表性应用（127 arXiv 版的正式发表版）。鲁棒性指对 OOD 网络配置的泛化与可靠性，可与对抗/Byzantine 通信鲁棒工作 (60, 61, 73) 对照，作为应用领域案例。
