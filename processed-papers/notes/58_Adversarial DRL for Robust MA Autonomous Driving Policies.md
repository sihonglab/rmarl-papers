# 58. Adversarial Deep Reinforcement Learning for Improving the Robustness of Multi-agent Autonomous Driving Policies

## 元信息 (Metadata)
- **标题**: Adversarial Deep Reinforcement Learning for Improving the Robustness of Multi-agent Autonomous Driving Policies
- **作者**: Aizaz Sharif, Dusica Marijan
- **机构**: Simula Research Laboratory, Oslo, Norway
- **发表**: APSEC 2022（29th Asia-Pacific Software Engineering Conference），IEEE
- **链接/arXiv**: 代码 https://github.com/T3AS/MAD-ARL

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体 / 对抗驾驶行为（通过对手车制造"自然但对抗"的视觉观测扰动，导致碰撞/偏离车道的失效状态）
- **方法范式**: 对抗训练（两步法：对抗测试发现失效 + 对抗重训练防御）；adversarial RL；PPO；vision-based end-to-end DRL；black-box 对手
- **关键词**: autonomous driving, adversarial RL, multi-agent, robustness, PPO, CARLA

## TL;DR（一句话总结）
提出 MAD-ARL 框架：第一步训练对抗驾驶智能体（adversary 车）把被测自动驾驶车（victim AC）引入碰撞/偏离车道等失效状态以发现错误，第二步用这些对抗输入重训练 victim，从而显著降低碰撞与偏离车道错误、提升基于 DRL 的多智能体自动驾驶策略鲁棒性。

## 问题与动机 (Problem & Motivation)
自动驾驶车（AC）易受对抗攻击且 DRL 软件难验证。已有 AC 测试研究多只做错误检测不做纠正、且常在单智能体、低维全可观测（如车道保持）的简化场景下，缺乏在真实多智能体、vision-based、部分可观测城市驾驶环境中既发现错误又改进鲁棒性的综合方法。未来道路上多 AC 与人类驾驶共存，非平稳多智能体测试是关键新问题。本文用 ARL 找有效攻击输入并据此提升鲁棒性。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 对手 α 是一辆独立、非通信的竞争性 AC，无 victim 的白盒访问（仅能从 πT 采样到动作状态），训练时 victim 权重冻结，故两人 Markov game 退化为对手的单智能体 MDP（model-free）。对手通过自身驾驶行为（如过路口时偏离）制造对 victim 看似"自然"但实为对抗的视觉观测噪声。
- **设定**: mixed/competitive（victim 协作完成驾驶目标、adversary 竞争制造失效）；decentralized、independent non-communicating；vision-based、部分可观测；online 仿真训练

## 方法 (Method)
- 两步法 MAD-ARL：Step 1 在 victim 权重冻结下训练 adversary πα，用其暴露 victim 的失效驾驶场景；Step 2 解冻 victim 权重、保留 adversary 于环境中重训练 victim 以提升鲁棒性。
- 所有 agent 用 PPO（on-policy），输入为 84×84×3 前置相机图像，经卷积网络输出 9 个离散动作（Steer/Throttle/Brake）。
- 设计两种对手奖励函数对比：R_collision（最大化碰撞+偏离）与 R_offroad（仅最大化偏离车道），论证仅靠偏离驱动的对手即足以制造有效对抗动作。
- victim 奖励鼓励安全到达目的地、惩罚碰撞与偏离车道；对手仅训练单一 victim 即可泛化攻击多个 victim。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（工程框架与实验，无理论分析）

## 实验 (Experiments)
- **环境/Benchmark**: CARLA Town 3 的 T 形路口城市驾驶（部分可观测），经 Macad-gym + RLlib(Ray) + TensorFlow 实现；2 个 victim AC + 1 adversary
- **Baselines**: 无对手训练的 baseline victim 策略；两种对手奖励（R_collision vs R_offroad）；重训练前后对比
- **评估指标**: CV（与车碰撞率）、CR（与物体碰撞率）、OS（偏离车道率）、TTFC（首次碰撞时间）；50 episodes × 2000 步平均

## 主要结果 (Key Results)
- RQ1：加入对手后 victim 碰撞与偏离车道错误显著上升（如 baseline 与车碰撞 0.0 → R_collision 下 Victim1 达 0.55、偏离 0.91），证明对抗策略能有效发现失效场景；单一训练的对手可同时攻击多个 victim。
- RQ2：用对抗输入重训练后，victim 的碰撞/偏离错误大幅回落（如与车碰撞降至 ~0.07–0.08、偏离 ~0.04），优于 baseline，证明对抗重训练是有效防御。
- R_offroad 对手收敛更快更稳定，且"无碰撞、最小偏离"奖励即足以制造有效对抗，无需以碰撞为主的奖励。

## 局限与未来工作 (Limitations & Future Work)
- 场景较受限（单一 T 形路口、3 辆车），未含行人、密集交通、红绿灯网络。
- 未来：扩展到 mass-traffic 大状态空间混合竞争场景找边界用例；研究重训练对手对 victim 的影响；比较不同 DRL 算法在不同对手下的鲁棒性；调整训练/测试 episodic 步数评估。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 的应用线（autonomous driving）与"对抗训练/对抗测试提升鲁棒性"方法线，强调用 adversarial RL 在多智能体、vision-based、非通信驾驶环境中既发现失效又通过重训练防御。可与其他自动驾驶鲁棒/对抗工作（如 #52、#105、#110）及通用对抗训练鲁棒 MARL 方法对照，是软件工程/AI 测试视角下的实证性贡献。
