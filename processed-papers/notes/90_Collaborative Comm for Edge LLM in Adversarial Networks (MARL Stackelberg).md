# 90. Collaborative Communication for Edge LLM Servicing in Adversarial Networks: An MARL-Empowered Stackelberg Game Approach

## 元信息 (Metadata)
- **标题**: Collaborative Communication for Edge LLM Servicing in Adversarial Networks: An MARL-Empowered Stackelberg Game Approach
- **作者**: Liqi Hong, Shengli Pan, Fan Feng, Chengbo Jiao
- **机构**: Beijing University of Posts and Telecommunications（School of Cyberspace Security）；Guangxi Key Laboratory of Digital Infrastructure
- **发表**: IEEE Internet of Things Journal, Vol. 12, No. 20, 2025
- **链接/arXiv**: DOI 10.1109/JIOT.2025.3583280

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体 / 恶意中继节点的通信延迟注入攻击（communication delay injection attack）
- **方法范式**: Stackelberg Game（leader-follower 博弈）、MARL（分布式 actor-critic / DDPG）、博弈论均衡
- **关键词**: collaborative communication, edge LLM servicing, MARL, Stackelberg game, delay injection attack

## TL;DR（一句话总结）
针对 6G 边缘 LLM 服务中恶意中继注入延迟的攻击，提出将边缘设备与恶意节点的交互建模为 Stackelberg 博弈、用分布式 MARL（DDPG）求解的协作通信框架，使边缘设备协同识别并规避恶意中继、提升网络韧性。

## 问题与动机 (Problem & Motivation)
6G/IoT 时代边缘 LLM 服务依赖中继节点协作转发，但恶意中继注入延迟会严重破坏延迟敏感应用的性能与安全。现有方法多假设良性环境、依赖集中控制，且把边缘设备视为竞争而非协作主体，缺乏在动态对抗环境下分布式、低通信开销地协同识别恶意中继的机制。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 恶意中继节点随机对中继链路注入延迟（建模为附加项 D=0.1·σ²_noise 降低信道增益），时变信道（Gaussian-Markov block fading）带来不完全信息。
- **设定**: 协作通信（隐式合作）+ leader-follower 博弈（中继为 leader 设防御性定价，源节点为 follower 选择中继）；decentralized / distributed 训练；online

## 方法 (Method)
- 建立端到端无线+有线信道模型与威胁模型，量化延迟注入对信道容量的影响。
- 将源节点与中继节点交互建模为 Stackelberg 博弈：中继 alliance 作 leader 设能量价格（效用 Ur），源节点作 follower 决定能量购买（效用 Us），含资源-风险权衡的 penalty 项与功率耦合约束。
- 用分布式 MARL（DDPG actor-critic）求解博弈均衡：定义 leader/follower 的 state（基于上一时隙 CSI）、action（功率/定价/中继选择）、reward（=博弈效用）。
- 采用经验回放、目标网络与软更新训练，使边缘设备隐式共享恶意节点信息、协同规避。
- 集成 MoE 专家模块按需加载以平衡通信成本（快速响应 vs 高安全）。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证。借用 Stackelberg 均衡与 backward induction 概念，但无新收敛性/均衡存在性证明，主要为工程框架与数值验证。

## 实验 (Experiments)
- **环境/Benchmark**: 自建边缘智能通信网络仿真（多源/中继/目的节点，含 MoE 服务）。
- **Baselines**: Random、DQN、Adaptive Greedy（约束优化）。
- **评估指标**: 边缘/中继节点效用（reward）、收敛速度、奖励方差（稳定性）、不同攻击强度/流量负载/中继定价下的性能下降比例、资源利用率、延迟、脆弱性。

## 主要结果 (Key Results)
- 收敛快（边缘节点约 50 轮、中继约 85 轮），效用高于 Random/DQN/Greedy，方差最小（如 0.0114 vs DQN 0.0163）。
- 攻击强度 0→1 时性能下降 48.1%（低功率）/53.3%（高功率），优于基线；流量增大时下降幅度也更小、更稳定。
- 综合相比基线：资源利用率 +27.5%、延迟 -21%、系统脆弱性 -35.6%、稳定性 +27.3%、能耗 -18.6%、吞吐 +35.7%。

## 局限与未来工作 (Limitations & Future Work)
仅小规模仿真验证；延迟攻击模型较简化；缺乏理论保证；未来计划扩展到大规模部署并集成联邦学习增强隐私与安全。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 在通信/网络安全中的应用，将博弈论均衡（Stackelberg）与对抗节点防御结合，连接「对抗智能体/通信攻击」与「博弈论均衡」主线，是面向 LLM 边缘服务的鲁棒 MARL 落地案例。
