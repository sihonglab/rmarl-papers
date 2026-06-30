# 132. Robust UAV-Oriented Wireless Communications via Multi-Agent Deep Reinforcement Learning to Optimize User Coverage

## 元信息 (Metadata)
- **标题**: Robust UAV-Oriented Wireless Communications via Multi-Agent Deep Reinforcement Learning to Optimize User Coverage
- **作者**: Mahfizur Rahman Khan, Gowtham Raj Veeraswamy Premkumar (共同一作), Bryan Van Scoy (通讯)
- **机构**: Department of Electrical and Computer Engineering, Miami University, Oxford, OH, USA
- **发表**: Drones (MDPI) 2025, 9, 321（Published 22 April 2025）
- **链接/arXiv**: https://doi.org/10.3390/drones9050321 ；数据/代码: https://github.com/vanscoy/data-uav-rl/

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: (1) 用户分布的随机性/分布偏移 (stochastic user distributions, OOD 用户场景)；(2) 通信攻击——jamming 干扰导致 UAV 失联/失效
- **方法范式**: Multi-Agent Deep Q-Learning (MADQL)、centralized vs decentralized (共享网络)、随机环境训练增强鲁棒、jamming 后重配置启发式算法
- **关键词**: UAV、Deep Q-Learning、MADRL、User Coverage、Jamming、Robustness

## TL;DR（一句话总结）
用集中式与分散式 (共享网络) 多智能体深度 Q-learning 优化无人机作为动态基站的部署以最大化地面用户覆盖，通过在随机用户分布上训练提升对未见分布的鲁棒性，并设计在部分 UAV 被 jamming 失联后重新调整其余 UAV 位置的算法以维持覆盖。

## 问题与动机 (Problem & Motivation)
在缺乏固定基站基础设施的区域 (灾后、临时大型活动、农村)，UAV 作为飞行基站可提供按需无线覆盖，但 3D 部署自由度高、飞行时间受限、传播环境多变使部署优化困难。已有研究多只比较集中或分散方法之一、且训练与测试用同一用户分布、对 jamming 攻击研究有限。本文填补这三处空白：集中 vs 分散对比、随机分布训练的鲁棒性、jamming 下的覆盖维持。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: (1) 用户按已知概率分布随机生成，测试时用不同分布评估策略迁移；(2) jamming 攻击：某 UAV 到达最优位置后被干扰、与其他 UAV 失联/失效。
- **设定**: cooperative（多 UAV 协同覆盖，UAV 间最小信息交换）；提供 centralized 与 decentralized (共享神经网络) 两种范式；online

## 方法 (Method)
1. **集中式 MADQL**: 所有 UAV 同时训练，联合状态-动作空间，协调性好但规模扩展难、训练量大。
2. **分散式 MADQL**: 每个 UAV 自主决策但共享同一神经网络，实现个体化学习，可扩展性更好。
3. **随机环境训练**: 在按概率分布随机生成的用户分布上训练策略，使其对多样/未见用户分布鲁棒；实证评估跨分布迁移。
4. **抗 jamming 重配置算法**: 当部分 UAV 被 jamming 失联，未受影响的 UAV 重新分配位置以尽量维持地面用户连接，提升网络韧性。
5. 用分散网络权重初始化集中网络隐藏层以加速集中式训练。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（无收敛性/认证鲁棒性证明，纯仿真工程研究）

## 实验 (Experiments)
- **环境/Benchmark**: 自建 UAV 基站用户覆盖仿真（不同规模 UAV/用户数；含 jamming 场景与多种用户分布）
- **Baselines**: 集中式 vs 分散式方法相互对比；与优化方法/单智能体 Q-learning 在 Table 1 定性对比
- **评估指标**: 覆盖用户数/覆盖率、网络连通性、训练时间/收敛平滑度

## 主要结果 (Key Results)
1. 小规模场景下集中式优于分散式（如覆盖 54/60 用户 vs 48/60），学习曲线更平滑；但集中式随 UAV/用户增多扩展性差。
2. 用分散网络权重初始化集中网络可将集中算法运行时间从 157 min 降到 63 min，且不降性能。
3. 随机分布训练使策略对不同用户分布表现出可迁移性与鲁棒性。
4. 抗 jamming 重配置算法在干扰下显著缓解覆盖率下降，提升系统韧性与可靠性。

## 局限与未来工作 (Limitations & Future Work)
集中式扩展性受联合状态-动作空间膨胀限制；分散式难以达到全局协调；实际部署中 UAV 电池/飞行时间、内存与算力受限未充分建模——这些为未来工作。研究无理论保证，规模有限。

## 与综述的关联 (Relevance to Survey)
robust MARL 中"通信攻击 (jamming) + 分布鲁棒/泛化"主题线在 UAV 无线通信的应用案例，鲁棒性兼含用户分布偏移泛化与对抗干扰韧性两方面；与其他通信网络鲁棒 MARL (127/128 路由)、抗干扰/对抗通信工作相关，可作为应用领域实例。
