# 105. Evaluating the Robustness of Deep Reinforcement Learning for Autonomous Policies in a Multi-Agent Urban Driving Environment

## 元信息 (Metadata)
- **标题**: Evaluating the Robustness of Deep Reinforcement Learning for Autonomous Policies in a Multi-Agent Urban Driving Environment
- **作者**: Aizaz Sharif, Dusica Marijan
- **机构**: Simula Research Laboratory, Oslo, Norway
- **发表**: IEEE QRS 2022 (22nd International Conference on Software Quality, Reliability and Security)
- **链接/arXiv**: DOI: 10.1109/QRS57517.2022.00084；代码 https://github.com/AizazSharif/Benchmarking-QRS-2022

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 多智能体非平稳性 (non-stationarity)；不同驾驶场景/环境配置下的分布变化（competitive 其他车辆与行人带来的扰动），而非显式对抗攻击
- **方法范式**: benchmarking / 系统性比较评估；independent (non-shared) multi-agent DRL；多目标奖励函数设计；偏实证
- **关键词**: deep RL, autonomous driving, multi-agent, robustness benchmarking, CARLA

## TL;DR（一句话总结）
提出一个开放可复用的端到端基准框架与多目标奖励函数，在 CARLA 多智能体城市驾驶环境下系统比较 6 种 DRL 算法（4 离散 + 2 连续动作）训练的自动驾驶策略的鲁棒性，发现 A3C 与 TD3 在单/多智能体场景下最稳健。

## 问题与动机 (Problem & Motivation)
自动驾驶研究多用 DRL 但缺乏在视觉城市驾驶下对各 DRL 算法的系统比较；多数研究将 AC 当作单智能体、非通信问题，忽视未来必然的多智能体非平稳场景；也缺乏面向多目标的综合奖励函数用于公平比较鲁棒性。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 非对抗——鲁棒性指策略在单智能体 vs 多智能体竞争场景、5 种不同道路环境（直道/三叉/四叉/环岛/汇入）下的稳定表现；多智能体非平稳性是核心挑战
- **设定**: mixed/competitive（独立非通信竞争 agent + 自动控制车辆模拟人类驾驶）；decentralized（非共享多智能体，POMDP/POSG/Markov Game 形式化）；先多智能体训练，再单/多智能体测试

## 方法 (Method)
- 构建基于 CARLA (Town03) + RLlib + Macad-gym 的端到端视觉驾驶基准框架，输入 84×84×3 前视相机图像，输出离散 9 动作或连续 2 维（Steer/Throttle/Brake）。
- 设计多目标奖励函数 RAC：Safety（碰撞车辆/物体/行人惩罚 -50）+ Efficiency（接近目标距离与速度 +10）+ Lane Keeping（offroad 惩罚 -0.5）+ 探索惩罚常数 φ。
- 基准化 6 种 model-free DRL：PPO、A3C、IMPALA、DQN（离散）；DDPG、TD3（连续），用 Population Based Training (PBT) 调参。
- 用 6 个驾驶性能指标（CV/CO/CP 碰撞率、OS offroad、TTFC 首次碰撞时间、SPEED）评估，并聚合为 Safety/Efficiency/Lane Keeping 成功率。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（基准框架与比较研究）。

## 实验 (Experiments)
- **环境/Benchmark**: CARLA Town03 的 5 个驾驶环境（Straight、Three Way、Four Way、Roundabout、Merge），含行人
- **Baselines**: 6 种 DRL 算法互相比较（PPO/A3C/IMPALA/DQN/DDPG/TD3）
- **评估指标**: CV/CO/CP/OS 误差百分比、TTFC、SPEED、DISTANCE，聚合 Safety/Efficiency/Lane Keeping

## 主要结果 (Key Results)
- A3C（离散）与 TD3（连续）在单/多智能体场景下整体最鲁棒：碰撞少、offroad 误差低、覆盖距离多。
- TD3 以较低速度换取更安全、更好的车道保持，明显优于 DDPG；IMPALA（非共享）最弱。
- 多智能体非平稳环境显著降低 AC 驾驶表现，凸显仅在单智能体下评估的现有研究的有效性威胁。

## 局限与未来工作 (Limitations & Future Work)
仅 6 种算法、依赖 RLlib/CARLA 特定版本；超参敏感；多智能体非平稳性为主要 validity 威胁。未来探索 A3C/TD3 在更高速度下的安全权衡、DQN 的连续扩展、更广算法与超参搜索。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 的"鲁棒性评估与基准"线（应用于自动驾驶），核心关注多智能体非平稳性下策略鲁棒性的系统比较，提供可复现的评估框架与多目标奖励设计，呼应综述中对 robustness benchmarking 与分布/环境变化鲁棒性的讨论。
