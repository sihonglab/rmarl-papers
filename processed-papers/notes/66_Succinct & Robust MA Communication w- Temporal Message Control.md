# 66. Succinct and Robust Multi-Agent Communication With Temporal Message Control (TMC)

## 元信息 (Metadata)
- **标题**: Succinct and Robust Multi-Agent Communication With Temporal Message Control
- **作者**: Sai Qian Zhang, Jieyu Lin, Qi Zhang（后两位 equal contribution）
- **机构**: Harvard University; University of Toronto; Microsoft
- **发表**: NeurIPS 2020
- **链接/arXiv**: 代码 https://github.com/saizhang0218/TMC ；demo https://tmcpaper.github.io/tmc/

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信传输丢包 / 有损通信信道（transmission loss），带宽受限
- **方法范式**: 时间平滑正则化（temporal smoothing）、消息缓冲机制（message buffering）、value decomposition (QMIX/VDN)、CTDE
- **关键词**: cooperative MARL, communication efficiency, transmission loss robustness, temporal message control, value decomposition

## TL;DR（一句话总结）
TMC 通过对智能体消息施加时间平滑正则化 + 接收端消息缓冲，使消息只在含新信息时才发送，从而大幅降低通信开销（最多 80%），并天然增强对有损信道丢包的鲁棒性。

## 问题与动机 (Problem & Motivation)
现有 MARL 通信方案假设可靠信道、运行时交换大量冗余消息，实际部署（自动驾驶、无人机）中信道带宽受限且有损（突发丢包）。连续观测间有用信息高度时间相关，导致消息冗余且噪声大。既有效率工作（如 VBC）不考虑丢包；Message-Dropout 用固定随机丢包训练无法泛化到动态丢包模式且开销高。需要同时实现简洁与鲁棒的通信。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 无线信道丢包，用多状态 Markov 模型建模突发丢包（state 0 无丢、state i 表示 i 个包的丢失突发）；真实采集 802.11ac trace 拟合出 light/medium/heavy 三种丢包模型（平均丢包率 1.5%/8.2%/15.6%）。非对抗性，属于环境通信不确定性。
- **设定**: cooperative；CTDE（centralized training, decentralized execution）；online

## 方法 (Method)
- **网络结构**: 每个 agent 含 local action generator (GRU+MLP)、message encoder (MLP)、combining block，以及 sent/received message buffer（每条消息带 valid bit）。全局 Q 值由本地 Q 值与缓冲中有效消息逐元素相加：Qglb = Qloc + Σ_{val=1} m_n。
- **平滑正则化 L_s**: 在窗口 ws 内惩罚同一 agent 消息的时间变化，使相邻消息相似，从而无需重复发送相似消息。
- **置信度正则化 L_r**: 最大化全局 Q 值中最大与次大元素之差，提升动作选择置信度，避免小幅消息变化导致错误动作。总损失 L = TD 误差 + λ_s·L_s − λ_r·L_r。
- **通信协议**: 仅当新消息与上次发送消息的 Euclidean 距离超阈值 δ 或超时（t−t_last > ws）才广播；接收端缓存最新消息，超过 ws 未更新则置 valid=0。
- **鲁棒性来源**: 每条已送达消息可被重用最多 ws 步，即使后续消息丢失，接收方仍可用缓冲消息（因消息时间相关性高，丢失消息与最近送达消息相似度大）。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（无收敛或认证半径分析；提供经验性分析说明丢失消息与最近送达消息的 l2 距离相关性高）。

## 实验 (Experiments)
- **环境/Benchmark**: SMAC（3s5z, 3s_vs_4z, 2c_vs_64zg, 3s_vs_5z, 6h_vs_8z, 6z_vs_24zg）；Predator-Prey；Cooperative Navigation（后两者含视线遮挡导致通信丢失）
- **Baselines**: QMIX（无通信）、SchedNet、VBC（+QMIX）、AC（全通信，TMC 去正则版）、AC(light)/AC(heavy)（含 Message-Dropout 训练）
- **评估指标**: 胜率（winning rate）、通信开销（通信 agent 对占比）、不同丢包模式下的胜率、归一化奖励

## 主要结果 (Key Results)
- 相比现有方案平均胜率高约 23%，通信开销最多降低 80%；困难场景（3s_vs_5z, 6h_vs_8z, 6z_vs_24zg）优于 AC/VBC。
- 通信开销比 VBC、SchedNet 分别低 1.3×、3.7×。
- 重度丢包下 VBC 和 SchedNet 胜率几乎降为 0，而 TMC 在三种丢包模式下均保持最佳；含固定丢包训练的 AC(light/heavy) 仅在匹配的丢包模式下有效。
- PP/CN 中 TMC+VDN 奖励比其他方法高 1.24×/1.35×，通信开销低 3.2×/2.9×。

## 局限与未来工作 (Limitations & Future Work)
- 训练阶段不含丢包；阈值 δ、窗口 ws 等超参需按场景调；依赖消息的强时间局部性假设，在快速变化任务中收益可能下降。
- 安全/双刃剑问题（可被滥用控制无人机）被作者列为未来关注点；建议将思想推广到 federated learning、HCI 等领域。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"通信鲁棒性"主题线，针对的是非对抗性的信道丢包/带宽受限（区别于通信对抗攻击 ADMAC、Certified Communication 等）。结合 value decomposition (CTDE) 与轻量级时间平滑正则，是面向真实有损网络的实用化通信方案，可与通信攻击防御、效率优化通信工作对照。
