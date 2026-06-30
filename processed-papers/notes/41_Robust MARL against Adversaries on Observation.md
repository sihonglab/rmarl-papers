# 41. Robust Multi-Agent Reinforcement Learning Against Adversaries on Observation

## 元信息 (Metadata)
- **标题**: Robust Multi-Agent Reinforcement Learning Against Adversaries on Observation
- **作者**: Anonymous authors（双盲审稿，作者未公开）
- **机构**: 未明确
- **发表**: ICLR 2023 (under review / 投稿稿)
- **链接/arXiv**: 未明确

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动（合作 MARL 中对 agent 观测的对抗攻击，含随机噪声与定向扰动）
- **方法范式**: 对抗训练、attacker-victim 交替训练、attacker pool（历史对手池）、防御模块（扰动检测 + 观测重构）
- **关键词**: cooperative MARL, observation perturbation, adversarial attack, hybrid action space (HyAR), QMIX

## TL;DR（一句话总结）
提出 ROMAO 框架，通过一个在混合动作空间（先选 agent、再生成扰动向量）上学习的 black-box attacker 与受害团队交替训练，并配合可选的扰动检测/观测重构防御模块，提升合作 MARL 策略对观测扰动的鲁棒性。

## 问题与动机 (Problem & Motivation)
神经网络对对抗扰动脆弱，合作 MARL 在实际部署中最易受攻击的是传感器（观测）。即使对单个 agent 观测施加微小扰动也会破坏协调，导致整个多智能体系统失败。已有工作多关注队友背叛或动作被恶意篡改，对观测扰动（尤其是 black-box、每个 agent 都可能被攻击的情形）研究稀少；最相关的 Lin et al. (2020) 仅攻击单一 agent 且为间接攻击。本文聚焦黑盒观测攻击及其防御。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 扰动加在各 agent 观测 {O_i} 上；attacker 共享全局 state，但无法访问 victim 的 Q 函数参数（black-box）。攻击为混合动作：离散选 agent ID + 连续扰动向量。约束所有扰动的 ℓ1 范数 ≤ 常数 C。考虑三类攻击：随机 agent + 随机噪声、特定 agent + 随机噪声、特定 agent 特定观测维度。
- **设定**: cooperative；CTDE；online

## 方法 (Method)
1. **Hybrid action attacker**: 将攻击建模为 Parameterized Action MDP，采用 HyAR 构造可解码的统一隐空间表示，用 TD3 在隐空间学习策略，输出离散动作（攻击哪个 agent）+ 连续动作（该 agent 观测的扰动），reward = -R（最小化 victim 团队回报）。
2. **交替训练（robust training）**: 固定 victim 训 attacker，固定 attacker 训 victim；每轮把 attacker 存入 attacker pool 并重置探索/replay buffer 以消除偏差。
3. **Attacker pool**: 训练 victim 时从历史 attacker 池随机采样，使 victim 对当前及历史多样攻击都鲁棒；框架与具体 MARL 算法无关。
4. **可选防御模块**: 训练扰动检测器判断 agent 是否被攻击，并利用视野内队友观测重构被扰动 agent 的观测（需通信，集中训练阶段可获得原始/扰动观测来监督）。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证

## 实验 (Experiments)
- **环境/Benchmark**: SMAC（2s3z、3m、3s_vs_5z、5m_vs_6m 等）、Predator-Prey (PP) 网格世界
- **Baselines**: Vanilla QMIX、Random QMIX（随机噪声训练）、One-agent QMIX
- **评估指标**: 不同攻击模式下的胜率/test win rate；attacker 多样性用 PCA 可视化

## 主要结果 (Key Results)
1. ROMAO 在多张 SMAC 地图、多种攻击模式下胜率优于 Vanilla/One-agent QMIX，在难图 5m_vs_6m 等也有提升（如 Attack Mode 1 下 68.8% vs Vanilla 58.3%）。
2. 生成的 attacker 多样（PCA 显示扰动模式分布广），能精准定位合作策略弱点。
3. 防御模块（扰动检测 + 观测重构）可进一步增强对观测攻击的防御能力。

## 局限与未来工作 (Limitations & Future Work)
防御模块依赖 agent 间通信和视野重叠，并非通用；评估主要在 SMAC/PP，且基于 QMIX 一类 value-based 方法；black-box 假设下 attacker 仍需全局 state。未来可扩展到更现实的部分可观测攻击与无通信防御。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"观测/状态扰动 + 对抗训练"主线，与 SA-MDP/state-adversarial、attacker-victim 交替训练、historical adversary pool 等方法相关；是合作 MARL 黑盒观测攻击与防御的代表性实证工作。
