# 141. Air Combat Autonomous Maneuver Decision for One-on-One Within Visual Range Engagement Based on Robust Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Air combat autonomous maneuver decision for one-on-one within visual range engagement based on robust multi-agent reinforcement learning
- **作者**: Weiren Kong, Deyun Zhou, Kai Zhang, Zhen Yang
- **机构**: Northwestern Polytechnical University, Xi'an, China
- **发表**: 2020 IEEE 16th International Conference on Control & Automation (ICCA), 2020
- **链接/arXiv**: 未明确（IEEE Xplore, 978-1-7281-9093-8/20）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对手策略变化导致的脆弱策略 / 竞争环境非平稳性（worst-case opponent perturbation）
- **方法范式**: minimax（M3DDPG）、对抗训练、Zero-sum Markov Games、Robust MADDPG、potential-based reward shaping
- **关键词**: Robust MADDPG, air combat, reinforcement learning, maneuver strategy, minimax, zero-sum game

## TL;DR（一句话总结）
将 UCAV 一对一近距空战建模为零和马尔可夫博弈，使用引入 minimax 模块（M3DDPG 风格的最坏情况对手扰动）的 Robust MADDPG 学习鲁棒机动决策策略，并辅以 potential-based reward shaping 加速训练。

## 问题与动机 (Problem & Motivation)
UCAV 视距内（WVR）空战（dogfight）对实时性要求高，现有自主决策方法（BFM 库、优化、AI）各有局限。单智能体 RL 因环境非平稳无法收敛；MADDPG 在强竞争环境中易学到只针对特定均衡的脆弱策略，对手改变策略时易被攻破。需要鲁棒的 MARL 方法。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 对手（红方）策略的最坏情况扰动；通过 minimax Q 函数 min_o Q(s,a,o)，并用一步梯度下降近似最坏对手动作 o*=o−α∇_o Q（局部最坏扰动），即 MAAL 对抗训练思想。
- **设定**: competitive（两方零和 ZSMG）；CTDE（集中式 critic、分散执行）；offline（作者明确指出仅离线学习）

## 方法 (Method)
- 将 1v1 WVR 空战建模为两方零和马尔可夫博弈（ZSMG），状态含双机位置/速度/航向/滚转角，连续动作为推力加速度与滚转角速率，奖励基于 ATA 与 AA 进入尾后攻击区。
- 基础算法为 MADDPG（集中训练分散执行），在此之上加入 minimax 模块得到 Robust MADDPG：用一步梯度近似最坏对手扰动 b_ε，只需一次额外梯度计算，端到端训练。
- 采用 potential-based reward shaping（PBRS），设计 orientation/distance/velocity 三个势函数组合加速收敛，且理论上不改变 Nash 均衡。
- 仿真环境采用两机 2-DOF 运动学/动力学模型，蓝方机动性略优于红方避免互咬尾。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（沿用 M3DDPG 的 minimax 目标与 PBRS 不改变 Nash 均衡的已有结论，本文无新理论）。

## 实验 (Experiments)
- **环境/Benchmark**: 自建 Python 1v1 WVR 空战仿真（2-DOF 动力学），最大 episode 长度 15，回放池 10000。
- **Baselines**: MADDPG、Approximate Dynamic Programming (ADP)。
- **评估指标**: 每 episode 平均奖励（等价于优势步数比 / advantage steps ratio）、对战胜率。

## 主要结果 (Key Results)
- Robust MADDPG 与 MADDPG 平均奖励均收敛到较高值，但 Robust MADDPG 全程收敛曲线优于 MADDPG。
- 策略对战中 Robust MADDPG 对 MADDPG 胜率约 60%；ADP 策略最差。
- 验证了 minimax 模块缓解策略脆弱性、提升对手鲁棒性。

## 局限与未来工作 (Limitations & Future Work)
仅限离线学习，使用策略时不再持续学习，限制较大；未来计划引入 lifelong learning 等机制实现分布式在线学习。实验规模小（仅 1v1、2-DOF、同平面）。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"竞争 / 零和博弈下的 minimax 对抗鲁棒"线（M3DDPG 系），针对对手策略不确定性，应用于军事空战机动决策，体现 minimax + 对抗训练范式在真实控制任务的落地。
