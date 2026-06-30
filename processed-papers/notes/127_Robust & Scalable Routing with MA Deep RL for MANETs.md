# 127. Robust and Scalable Routing with Multi-Agent Deep Reinforcement Learning for MANETs

## 元信息 (Metadata)
- **标题**: Robust and Scalable Routing with Multi-Agent Deep Reinforcement Learning for MANETs (DeepCQ+ routing)
- **作者**: Saeed Kaviani, Bo Ryu, Ejaz Ahmed, Kevin Larson, Anh Le, Alex Yahja, Jae H. Kim
- **机构**: EpiSys Science, Inc.; Boeing Research and Technology
- **发表**: arXiv 2021（arXiv:2101.03273v2, cs.NI, 29 Mar 2021）；venue 未明确（疑似会议/期刊投稿）
- **链接/arXiv**: arXiv:2101.03273v2

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 网络环境高动态/拓扑变化、节点移动、链路中断、流量动态、跨网络规模的分布外 (OOD) 配置（鲁棒性偏"泛化/可扩展性"工程意义，含战术网络的干扰/jamming 背景）
- **方法范式**: MADRL、CTDE、参数共享、PPO、Dec-POMDP、hybrid (Q-learning/CQ+ routing + deep RL)
- **关键词**: MANET、Robust Routing、DeepCQ+、MADRL、Scalability、Dec-POMDP

## TL;DR（一句话总结）
提出 DeepCQ+ 路由，将 MADRL（PPO + CTDE + 参数共享）与基于 Q-learning 的 CQ+ 路由协议混合，仅在有限网络参数范围训练，却能在未训练过的网络规模、移动性与流量动态下保持高吞吐、低开销（效率提升约 10–15%），首次在 MANET 路由上展示 MADRL 的可扩展鲁棒性。

## 问题与动机 (Problem & Motivation)
高动态 MANET（尤其战术网络，含地形/干扰/jamming）中路由极具挑战：传统链路状态协议在频繁链路中断时需频繁重算路由、丢失吞吐；CQ+ 路由用置信度 C 值 + 自适应广播提升鲁棒性，但其广播/单播决策仅依赖单一参数（最佳路径置信度），视角局部、未考虑拥塞与参数变化率。现有 MADRL 路由为每个 agent 训练独立策略，可扩展性差、对网络规模变化泛化不明。需要一个对规模、动态、流量都鲁棒可扩展的策略。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不确定性来自高动态网络（节点移动用 Gauss-Markov / random waypoint 建模）、变规模 (5≤N≤50)、多数据流、不同动态等级；目标是训练分布 (单一规模/单流/小动态范围) 之外的鲁棒泛化。无显式对抗者，但战术场景隐含 jamming/干扰。
- **设定**: cooperative（Dec-POMDP，同质节点共享策略 πθ）；CTDE（离线仿真集中训练，分布式在线执行，C/H 值经 ACK 实时更新）；online 执行

## 方法 (Method)
1. **混合框架**: 保留 CQ+ 路由的 ACK 驱动 C-（置信度）/H-（跳数）值传播协议，仅用 DRL 优化传输/路由决策策略（广播 vs 单播 + next-hop）。
2. **可扩展输入预处理**: 从 N-1 个邻居中按 h·(1-c) 升序选最佳 K=4 个邻居，固定维度输入 FCNN，使策略与网络规模解耦。
3. **观测特征**: ot = [ct, ht, Δct, Δht, at-1, pt-1]，含 C/H 值及其时间变化率与上一动作，用全连接网络捕捉时序变化。
4. **奖励设计**: Reward 1 复现 CQ+ 概率广播策略；Reward 2 = w1·delivery − w2·no-ACK惩罚 − w3·(Nack/N)，直接最小化归一化 overhead，同时保持 goodput ≥ CQ+。
5. 用 PPO (clipped objective) + 参数共享训练；在 Ray/RLlib 平台实现。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（给出将 CQ+ 路由策略重构为零视野 RL 最优策略的推导以设计奖励，但无收敛/泛化界证明）

## 实验 (Experiments)
- **环境/Benchmark**: 自研 Python CQ+ 路由仿真器 (Ray/RLlib)，benchmark 拓扑基于 AR[13]/CQ+[19]，800m×300m 区域、150m 通信距离、Gauss-Markov 移动、5 区域分组速度
- **Baselines**: Q-routing、CQ-routing、SRR/CQ+ routing（非 DRL 基线）
- **评估指标**: goodput/delivery rate、normalized overhead (NTX/ND/N)、broadcast rate、端到端延迟、跳数

## 主要结果 (Key Results)
1. DeepCQ+ (reward 2) 在保持与 CQ+ 相同 goodput 的同时，归一化 overhead 至少降低约 15%、广播率更低，整体效率提升 10–15%。
2. 仅在单一网络规模 (如 N=12) + 单流训练，却在 N=5–50、多流 (1–4)、更大动态等级的测试场景保持相似性能增益，验证可扩展鲁棒性。
3. 在 12 节点训练的策略与在 10–30 变规模训练的策略性能相当，表明无过拟合、扩规模训练增益不大。

## 局限与未来工作 (Limitations & Future Work)
仅优化 next-hop 与广播/单播模式选择，未考虑 network coding；假设无传输间干扰以聚焦路由层；奖励中端到端延迟未直接优化；缺乏对抗 jamming 的显式鲁棒性评估。未来可结合 NC、加入延迟优化与显式对抗扰动测试。

## 与综述的关联 (Relevance to Survey)
robust MARL 中"可扩展性/泛化鲁棒 + CTDE 参数共享"工程线在通信网络路由的应用；与其期刊扩展版 (128 DeepCQ+) 同源。鲁棒性此处指对 OOD 网络配置的泛化而非对抗攻击，可作为应用领域案例，与对抗/Byzantine 通信鲁棒工作 (60, 61, 73) 形成对照。
