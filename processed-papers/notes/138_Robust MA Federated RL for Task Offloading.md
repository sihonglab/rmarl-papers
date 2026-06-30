# 138. Robust Multi-agent Federated Reinforcement Learning for Task Offloading

## 元信息 (Metadata)
- **标题**: Robust Multi-agent Federated Reinforcement Learning for Task Offloading
- **作者**: Dibao Yan, Yongfeng Wang, Wenjing Hou, Huanhuan Song, Hong Wen, et al.
- **机构**: University of Electronic Science and Technology of China (UESTC), Chengdu, China
- **发表**: WCNA 2023 (LNEE 1361, Springer), 2025
- **链接/arXiv**: https://doi.org/10.1007/978-981-96-2409-6_21

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 联邦学习中的恶意节点 / 奖励投毒（reward inversion / reward flip attack）、Byzantine 容错
- **方法范式**: 异常检测（Euclidean distance + Modified Z-score）+ 鲁棒联邦聚合（FedAvg）+ 多智能体 TD3
- **关键词**: task offloading, malicious node detection, federated learning, multi-agent DRL, reward inversion

## TL;DR（一句话总结）
在多智能体联邦强化学习（基于 TD3）的任务卸载框架中，通过 Euclidean 距离与 Modified Z-score 检测并剔除受奖励反转攻击的恶意节点，使聚合后的策略在攻击下仍能收敛到接近无攻击时的性能。

## 问题与动机 (Problem & Motivation)
边缘计算中的任务卸载需在多样复杂场景下学习策略以最小化时延与能耗。借助联邦学习聚合多个边缘设备的训练策略可提升泛化性，但联邦聚合中存在节点是否安全可靠的问题：恶意节点可通过奖励反转破坏聚合模型，导致策略不收敛。需要在保持联邦聚合优势的同时抵御此类攻击。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 参与联邦聚合的某些节点为恶意节点，在本地训练时修改训练集 / 在经验回放池中反转奖励（reward inversion），从而学到最差策略并污染聚合参数。
- **设定**: cooperative（多边缘设备协作学习卸载策略）；分布式联邦训练 + 中心聚合节点；online

## 方法 (Method)
- 任务卸载建模为最小化时延与能耗的能效函数优化问题，用多智能体 DRL 求解，单体算法采用 TD3（双 Critic、延迟策略更新、目标策略平滑）。
- 每轮联邦聚合后所有节点参数一致，随分布式训练参数应朝同一方向迭代；计算各节点神经网络参数间的 Euclidean 距离。
- 用 Modified Z-score（基于 median 与 MAD，对离群点不敏感）对距离做离群检测，超过阈值的节点判为恶意并剔除。
- 对剩余可靠节点用 FedAvg 聚合参数并下发，循环本地训练与聚合。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证。

## 实验 (Experiments)
- **环境/Benchmark**: 自建任务卸载仿真，5 个卸载场景、5 个决策智能体，共 10000 轮聚合，每轮本地 10 次更新，batch size 128。
- **Baselines**: 无攻击 FedAvg；有攻击但仅 FedAvg（无检测）；有攻击 + Modified Z-score 检测（本文）。
- **评估指标**: 奖励收敛曲线（能效函数取反后的 reward）。

## 主要结果 (Key Results)
- 无攻击 FedAvg 在约 3700 轮收敛到约 −230。
- 有恶意节点且无检测时，聚合奖励在 [−350, 350] 区间波动、无收敛趋势。
- 加入 Modified Z-score 检测后，约 3800 轮收敛，曲线接近无攻击场景，验证可抵御奖励反转攻击。

## 局限与未来工作 (Limitations & Future Work)
仅考虑单一奖励反转攻击与小规模仿真，未提供理论保证；攻击类型、节点数量、阈值选择与更复杂 Byzantine 攻击的鲁棒性未充分探讨（正文未明确列出未来工作）。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"联邦 / 分布式 MARL 的 Byzantine 容错与奖励投毒防御"线，将经典异常检测（Modified Z-score）引入联邦 RL 聚合，与通信攻击、奖励投毒、容错聚合等主题相关，应用于边缘计算任务卸载。
