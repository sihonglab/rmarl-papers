# 124. Decentralized Multi-Agent Reinforcement Learning with Visible Light Communication for Robust Urban Traffic Signal Control

## 元信息 (Metadata)
- **标题**: Decentralized Multi-Agent Reinforcement Learning with Visible Light Communication for Robust Urban Traffic Signal Control
- **作者**: Manuel Augusto Vieira, Gonçalo Galvão, Manuela Vieira, Mário Véstias, Paula Louro, Pedro Vieira
- **机构**: DEETC-ISEL/IPL, UNINOVA-CTS/LASI, NOVA School of Science and Technology, INESC INOV, Instituto de Telecomunicações (葡萄牙)
- **发表**: Sustainability (MDPI) 2025, 17, 10056（Published 11 November 2025）
- **链接/arXiv**: https://doi.org/10.3390/su172210056

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信不可靠/部分通信失效、不完整或噪声数据、动态异构交通模式（鲁棒性偏"resilience/可靠性"工程意义，而非对抗攻击）
- **方法范式**: decentralized MARL (DQN + 邻居 Q 聚合)、VLC 通信增强感知、queue-request-response 机制、SAPA 动态相位时长、多策略训练
- **关键词**: MARL、DQN、Visible Light Communication (VLC)、Traffic Signal Control、Smart City、Pedestrian Safety

## TL;DR（一句话总结）
提出一个去中心化 MARL（DQN）交通信号控制框架，原生集成可见光通信 (VLC) 提供低延迟、高可靠的车-路-人本地信息交换，借助 queue-request-response 与 SAPA 动态相位机制提升车辆与行人流的效率、安全与能效，并在 SUMO + 初步实景实验中验证鲁棒性。

## 问题与动机 (Problem & Motivation)
城市车辆与行人流快速增长加剧拥堵、延误与安全风险；传统集中式信号控制可扩展性差、对动态异构交通适应性有限。现有 MARL 信号控制多依赖通用无线链路（DSRC/C-V2X），存在延迟、干扰、频谱拥塞与安全隐患，且常忽略行人流，对不完整/噪声信息下的鲁棒性不足。论文主张将 MARL 与 VLC 原生集成以填补该空白。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不确定性来自动态多模态交通需求与通信链路质量（VLC 在恶劣天气/强环境光下退化）。框架借助 VLC 高精度低延迟感知 + RF 互补，宣称可在部分通信失效下维持性能；并通过五种不同需求偏置策略评估对多样交通情景的鲁棒性。
- **设定**: cooperative（同质路口共享统一 DQN，邻居 Q 值聚合实现协调）；decentralized 执行 + 共享经验回放训练；online 仿真

## 方法 (Method)
1. **V-VLC 通信层**: LED 发射机 (OOK 调制) + PIN-PIN 光电二极管接收，街灯作 geo-transmitter (L2V)，信号灯作 edge node，支持 V2I/I2V、P2I/I2P，承载位置/速度/相位/行人请求等实时数据。
2. **去中心化 MARL (DQN)**: 每路口一智能体局部观测 (164 维位置/速度/等待 cells)，5 隐层×400 神经元，输出 9 个相位 Q 值；目标 Q 在常规 Bellman 基础上加邻居 Q 聚合项 (权重 β=0.3) 促进协调；奖励为车辆+行人累计等待时间的减少。
3. **Queue-Request-Response 机制**: 车辆/行人发起过街请求，信号灯应答并动态调整相位以避免冲突、优先紧急/应急移动。
4. **SAPA (Strategic Anti-Blocking Phase Adjustment)**: 基于 VLC 采集的队列与下游车道占用率动态调整绿灯时长 (如占用<40% 按队长延长绿灯，否则给最小绿灯) 防止溢出/阻塞。
5. 训练 5 种交通控制策略 (balanced 及偏置 circular/radial、inbound/outbound)，每策略一专用网络。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（无收敛性或认证鲁棒性证明，纯工程框架与仿真验证）

## 实验 (Experiments)
- **环境/Benchmark**: SUMO 微观仿真，基于葡萄牙里斯本市中心真实区域标定；5 个同质四臂路口 (C0–C4，C1 为中心枢纽)；初步实景 VLC 实验
- **Baselines**: 五种自设交通控制策略 (Network 1 balanced 与 Network 2–5 不同优先级) 之间的对比；与固定周期/平衡策略对照（未与外部 MARL baseline 系统对比）
- **评估指标**: 累计奖励、平均等待时间、吞吐量、车辆/行人 halting 时间、能效与行人安全

## 主要结果 (Key Results)
1. 各策略对应的 DQN 均收敛并适应其需求偏置；有方向优先的策略 (如 Network 2、4) 比 balanced (Network 1) 获得更高奖励、更短等待时间。
2. 中心路口 C1 是最关键节点，halting 时间波动最大；balanced 策略在 C1 拥堵明显，但其余路口性能稳定（限制局部化）。
3. 行人 halting 在五种策略间总体均衡，表明框架能在不显著增加延误下整合行人流。
4. VLC 实时支撑 V2I/V2V/P2I/I2P 通信，提升态势感知，降低平均等待/行程时间与队列，并改善能效（减少怠速）。

## 局限与未来工作 (Limitations & Future Work)
结果基于仿真趋势而非正式统计分析；网络规模小 (5 路口)；VLC 在雾/雨/雪及强环境光下信号退化，需 RF 互补；鲁棒性主张 (部分通信失效下维持性能) 缺乏定量压力测试。未来可扩展更大异构网络、做严格统计与失效场景评估。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中"通信可靠性/resilience"工程线在交通信号控制的应用，强调通信层 (VLC) 对鲁棒协调的支撑；与对抗通信攻击类工作 (如 ADMAC 60、认证通信鲁棒 61) 形成对照——本文关注物理层可靠通信而非对抗防御，可作为应用场景背景与正反例对比。
