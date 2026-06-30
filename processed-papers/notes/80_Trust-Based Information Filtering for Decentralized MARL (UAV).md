# 80. Trust-Based Information Filtering for Robust Decentralized Execution of Pre-Trained MARL Policies in UAV Swarms

## 元信息 (Metadata)
- **标题**: Trust-Based Information Filtering for Robust Decentralized Execution of Pre-Trained MARL Policies in UAV Swarms
- **作者**: Ernests Rudzītis, Alessandro Chiumento
- **机构**: Pervasive Systems Group, EEMCS Faculty, University of Twente, The Netherlands
- **发表**: 16th IFIP Wireless and Mobile Networking Conference (WMNC) 2025
- **链接/arXiv**: 未明确（©2025 IFIP, IEEE Xplore）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信不可靠/通信攻击（消息冻结、偏置、噪声注入），传感器故障
- **方法范式**: post-hoc 信任过滤、无监督异常检测 (Local Outlier Factor)、spatio-temporal 特征工程、消息恢复启发式
- **关键词**: trust-based filtering, anomaly detection, UAV swarm, post-hoc robustness, MAPPO, communication reliability

## TL;DR（一句话总结）
提出 Trust-Based Information Filtering (TIF)，一个 post-hoc、去中心化的信任过滤层，利用从正常运行学到的 spatio-temporal 期望评估接收消息可信度并恢复异常消息，无需重训练即可增强预训练 MARL 策略对不可靠通信的鲁棒性。

## 问题与动机 (Problem & Motivation)
MARL 驱动的无人机群依赖 inter-agent 通信（位置、速度、编队意图），但通信可能有噪声、传感器故障或被对手操纵，导致任务失败。已有方法多需在训练阶段集成对策（限制算法选择、需昂贵重训练）或需预配置加密协议，而简单 post-hoc 离群检测缺乏上下文理解。本文目标是无需攻击数据、无需重训练即可为预训练策略叠加鲁棒性。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 接收端消息不可靠，三种模式：Message Freezing（陈旧/重放）、Message Offset（持续偏置/被攻陷 agent）、Random Noise Injection（信道噪声）。TIF 在接收端工作，评估来自 peer 的消息。
- **设定**: cooperative；CTDE 训练 + decentralized execution；post-hoc（基础策略已用 MAPPO 训练完毕），TIF 在执行阶段添加

## 方法 (Method)
- 三模块 post-hoc 系统，独立集成于每个 agent，位于通信数据与预训练 MARL 策略之间，无需中心权威。
- Trust Assessment Module：抽取五组 spatio-temporal 一致性特征（Temporal、Inter-Agent、Motion、Formation-Aware、Anomaly Pattern），用无监督异常检测（Local Outlier Factor, n_neighbors=20）输出二元可信判断。
- Information Filtering Logic：可信消息直接通过；不可信消息用轻量恢复启发式——Historical Average Recovery（历史窗口平均，平滑）或 Trend Extrapolation Recovery（线性外推）。
- 数据驱动自配置：从约 100 episode（60,000 特征向量）正常运行数据拟合基线，统一用 contamination=0.05 设阈值，无需攻击数据或复杂调参。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（系统/原型设计 + 实验验证）

## 实验 (Experiments)
- **环境/Benchmark**: 自建 2D PettingZoo 仿真环境，3 架 UAV 的 V 形编队控制任务；基础策略用 MAPPO（CTDE，每 agent 独立 critic）训练 2M steps
- **Baselines**: 无 TIF 的基础预训练 MAPPO 策略
- **评估指标**: 异常检测 F1-score / accuracy；mean formation error 及其改进百分比

## 主要结果 (Key Results)
- 异常检测：comprehensive 特征组 (T,M,I,F) F1≈0.999；单独 temporal_only 也达 0.997，是最有效且通用的特征。
- 鲁棒性：TIF 总体降低 mean formation error 6.8%；对 sensor noise 最有效 (9.5%)，offset 6.8%，message freezing 最难 (3.8%)；最高单场景改进 33.6%。
- Historical Average 恢复平均比 Trend Extrapolation 有效约 13%。
- 在 10%/20%/30% 受损消息率下分别改进 8.3%/6.1%/6%，随通信质量下降效果递减但仍有保护作用。

## 局限与未来工作 (Limitations & Future Work)
- 仅在 3 架 UAV、V 形编队的小规模任务验证；inter-agent 特征随群规模 O(N) 增长，扩展性待验证。
- 对 message freezing（缓慢变化时不立即违反一致性）检测较弱。
- 偏原型/实证，无理论保证；通信建模为理想广播。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"通信攻击/不可靠通信"主题，代表 post-hoc、execution-time、无需重训练的轻量防御线，与 AME (ablated message ensemble)、消息重构两阶段协议、Gaussian Process 一致性建模等通信鲁棒方法相关，也与本批 trust-based 工作（82 Trust-MARL）形成同一信任机制主题。
