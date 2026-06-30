# 67. Robust and Efficient Communication in Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Robust and Efficient Communication in Multi-Agent Reinforcement Learning
- **作者**: Zejiao Liu, Yi Li, Jiali Wang, Junqi Tu, Yitian Hong, Fangfei Li, Yang Liu, Toshiharu Sugawara, Yang Tang（前三位 equal contribution）
- **机构**: East China University of Science and Technology; Zhejiang Normal University; Waseda University
- **发表**: arXiv 2025（arXiv:2511.11393v1，2025年11月）；未明确正式 venue
- **链接/arXiv**: arXiv:2511.11393

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信不完美（message perturbations/噪声/丢包、对抗通信攻击、Byzantine、传输延迟与异步、带宽受限），兼及观测/状态扰动
- **方法范式**: 综述（survey）；涵盖随机平滑认证、鲁棒 Q-learning/均衡、对抗训练、信息瓶颈、event-triggered、消息压缩/调度、延迟感知、federated MARL
- **关键词**: communication-robust MARL, communication efficiency, message perturbation, transmission delay, limited bandwidth, Dec-POMDP

## TL;DR（一句话总结）
一篇系统综述，聚焦现实通信约束（消息扰动/攻击、传输延迟、带宽受限）下 MARL 的鲁棒与高效通信策略，并以协同自动驾驶、分布式 SLAM、联邦学习三大应用串联，倡导通信-学习-鲁棒性协同设计。

## 问题与动机 (Problem & Motivation)
现有 MARL 普遍假设通信瞬时、可靠、无限带宽，但真实部署中信道存在噪声、对抗攻击、延迟、丢包、异步到达和带宽限制，会破坏协调甚至导致系统失效。已有综述多聚焦开放环境、算法范式、分布式训练或泛泛的对抗鲁棒性，缺乏对"非理想通信条件下通信鲁棒性与效率"的专门系统梳理，本文填补该空白。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 多类并存——(1) 消息扰动：message loss(Ploss)、Gaussian 外部干扰、message jumble、概率性无界替换(ADMAC, 概率 p)、lp 范数有界扰动(MA3C/R-MACRL)、凸组合攻击、FGSM/PGD/Monte-Carlo 等;(2) 信道模型：BSC、AWGN、Bursty Noise(两状态 Markov);(3) Byzantine（少于半数被攻陷, AME）;(4) 延迟：固定/时变(Gaussian)延迟、异步到达、丢失数据;(5) 带宽限制。统一以 Markov game / Dec-POMDP / MA-POMDP / 各类扩展(DT-Dec-POMDP, DACOM-MDP)建模。
- **设定**: 主要 cooperative；CTDE 为主，亦涉及 decentralized；online 为主，涵盖 federated 设定

## 方法 (Method)
作为综述，按主题归纳代表性方法：
- **通信鲁棒性（消息/状态扰动）**: CertifyCMARL（randomized smoothing + FDR 控制，认证奖励下界）、RMAQ/RMAAC（状态对抗鲁棒均衡）、RoMFAC、stochastic adversary、TMC（时间平滑+缓冲）、joint learning over noisy channels(Tung et al.)、GPMFM（GP 置信权重过滤）、ADMAC（主动评估消息可靠性, reliability estimator + 可分解聚合网络）、R-MACRL（两阶段异常检测+重构, 零和博弈逼近 Nash）、MA3C（auxiliary adversary 群体）、AME（ablated message ensemble, Byzantine 认证）、CroMAC（多视图 VAE + interval bound propagation）、MAGI（graph information bottleneck）。
- **带宽受限**: 分"何时/谁发"（SchedNet 调度、VBC 方差门控、ETCNet 事件触发、ExpoComm 指数拓扑）与"发什么/速率"（NDQ 互信息最小化、autoencoder/DVQ 压缩、MAIC 激励消息、PMAC/CACOM 个性化/上下文感知、COCOM 隐式共识）。
- **通信延迟**: VFFAC+GRU(固定延迟)、CoDe(DT-Dec-POMDP, intent+timeliness 双对齐)、MAAMIF(神经网络预测+三次样条插值)、DACOM(TimeNet 学习等待阈值)、DAMARL/DAMIAN(延迟感知)。
- **效率**: 消息压缩/稀疏化、信息瓶颈(IMAC)、语义/任务导向压缩、隐式通信(ICP)。
- **应用**: 协同自动驾驶、分布式 SLAM、federated learning。

## 理论贡献 (Theoretical Contributions)
综述性质，本身无新理论；归纳了被综述方法的理论结果：AME 的 Byzantine 容错保证（<半数被攻陷）、CertifyCMARL 的认证奖励下界、CroMAC 的 interval bound propagation 鲁棒保证、federated MARL 的收敛界（周期平均下通信频率-收敛权衡）。

## 实验 (Experiments)
- **环境/Benchmark**: 综述无自有实验；引用文献中常见 SMAC、MPE、Predator-Prey、Cooperative Navigation 及自动驾驶/SLAM/FL 场景
- **Baselines**: 不适用（survey）
- **评估指标**: 总结了通信 MARL 鲁棒性常用指标：winning rate、累计奖励、完成时间步、最坏情况性能、认证下界、对未见扰动的迁移性

## 主要结果 (Key Results)
- 提出统一视角：通信应被视为与任务性能紧耦合的"决策变量"，而非固定信道。
- 给出带宽方法分类表（who/when vs what/rate）与消息级策略分类表（效率 vs 鲁棒/安全），并梳理消息攻击形式表（对抗 vs 非对抗）。
- 指出现有鲁棒方法多只针对单一扰动类型，面对混合威胁（如随机衰落+故意干扰+欺骗信号）仍脆弱。

## 局限与未来工作 (Limitations & Future Work)
未来方向：(A) 应对混合威胁的内生鲁棒+认证结合、自适应防御与统一对抗 benchmark；(B) 异步/乱序/链路失效下的延迟鲁棒（意图预测+时间对齐、双对齐）；(C) 将通信作为资源约束下的显式动作、语义与阶段自适应协议；(D) federated MARL 的事件触发上传、跨层与 Byzantine 鲁棒聚合；(E) 大模型驱动的语义通信与可解释通信审计。整体倡导通信理论与 MARL 跨层协同设计及标准化 benchmark。

## 与综述的关联 (Relevance to Survey)
本身即一篇与本综述高度重叠的"robust & efficient communication in MARL"专题综述，是组织通信鲁棒性主题线（消息扰动/Byzantine/延迟/带宽）的重要参照与分类骨架，可直接对照本批次其他通信鲁棒论文（如 TMC #66、ADMAC #60、Certified Communication #61/#62、Mis-spoke/R-MACRL #63、Byzantine #73-75）进行定位与归类。
