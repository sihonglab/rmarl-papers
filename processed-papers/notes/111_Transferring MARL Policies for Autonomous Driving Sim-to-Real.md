# 111. Transferring Multi-Agent Reinforcement Learning Policies for Autonomous Driving using Sim-to-Real

## 元信息 (Metadata)
- **标题**: Transferring Multi-Agent Reinforcement Learning Policies for Autonomous Driving using Sim-to-Real
- **作者**: Eduardo Candela*, Leandro Parada*, Luis Marques*, Tiberiu-Andrei Georgescu, Yiannis Demiris, Panagiotis Angeloudis（*共同一作）
- **机构**: Imperial College London（Centre for Transport Studies；Personal Robotics Laboratory）
- **发表**: IEEE/RSJ IROS 2022（DOI: 10.1109/IROS47612.2022.9981319）
- **链接/arXiv**: 未明确（IEEE Xplore）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 模型/动力学不确定性、Sim-to-Real reality gap、测量噪声、智能体间异步与异质性
- **方法范式**: Domain Randomization、MAPPO（CTDE）、域泛化以提升迁移鲁棒性
- **关键词**: Sim-to-Real, Domain Randomization, MARL, Autonomous Driving, MAPPO, Duckietown

## TL;DR（一句话总结）
提出一个模拟 Duckietown 多机器人平台的多智能体自动驾驶 gym 环境（Duckie-MAAD），用带不同程度 domain randomization 的 MAPPO 训练策略并迁移到真实车队，证明 domain randomization 可将 reality gap 缩小约 90%。

## 问题与动机 (Problem & Motivation)
多智能体自动驾驶需要高度协调，MARL 是可扩展的控制框架，但因安全原因只能在仿真训练后迁移到现实。Sim-to-Real 的 reality gap 在多智能体场景下更大（额外的 control architecture gap、observation gap、communication gap、智能体异步与异质性）。已有 Sim-to-Real 工作多集中在单智能体机器人操作与环境泛化，缺少针对多智能体自动驾驶策略真实世界迁移的研究。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不确定性来自仿真与现实的动力学失配（对称质量、电机稳态假设）、Inverse Kinematics 参数（K、gain、trim、steering factor）的车间差异、转向角观测误差、OptiTrack 定位误差、智能体异步执行。通过对这些参数施加 Normal/Uniform 分布的随机化（none/medium/high 三档）建模不确定性集。
- **设定**: cooperative（共享 actor/critic 网络、共享观测与奖励思路）；CTDE（中心化 critic、去中心化 actor）；online（仿真训练）

## 方法 (Method)
- 构建 Duckie-MAAD 多智能体环境（基于 Gym-Duckietown 扩展），建模为 Dec-POMDP；动作为离散高层决策（加速/刹车/换道/保持）。
- 用 MAPPO（CTDE，RNN actor/critic）训练协作策略；奖励 R = v − 5c − 5t − 0.5l（速度、碰撞、出界、换道惩罚）。
- 对 Inverse Kinematics 关键参数（steering factor、K、gain、trim、steering error）施加 domain randomization，训练三档（无/中/高）策略以覆盖真实环境分布。
- 迁移流程：策略输出高层动作→Path Following 选路点并算 (v, ω)→差速 Inverse Kinematics 得轮速→仿真用 Non-linear Dynamics 更新位姿，现实用 OptiTrack MoCap 测位姿。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证

## 实验 (Experiments)
- **环境/Benchmark**: Duckie-MAAD 仿真环境与 Duckietown 真实测试台；3 个移动智能体 + 3 个静止停车障碍；10 Hz，MoCap 120 Hz。
- **Baselines**: 规则方法（Gipps 换道模型 + RSS 安全距离）；无 D.R.、中 D.R.、高 D.R. 三档 MAPPO 策略。
- **评估指标**: 平均奖励、measured speed、出界次数、碰撞次数、换道次数；仿真与现实各 30 次运行。

## 主要结果 (Key Results)
- Domain randomization（medium 档）将 reality gap 缩小近 90%。
- 所有 MARL 策略在仿真与现实均显著优于规则基线；无 D.R. 在仿真最好但现实表现最差。
- Medium D.R. 综合最优；high D.R. 策略过于保守（速度最低、出界最少但奖励不如 medium），显示 domain randomization 收益递减。
- 带 D.R. 的策略在现实中换道更频繁以规避碰撞，medium D.R. 现实碰撞最少。

## 局限与未来工作 (Limitations & Future Work)
Domain randomization 收益递减，无法在不提升仿真保真度的前提下完全消除 reality gap；最优随机化程度依任务而定，缺乏选择理论；reality gap 的量化与刻画仍待研究。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中“环境/动力学不确定性 + Sim-to-Real 迁移鲁棒性”一线，用 domain randomization 作为提升迁移鲁棒性的实证手段，是少数将多智能体鲁棒策略真正部署到真实机器人车队验证的工作，与对抗训练、模型不确定性鲁棒（如 Zhang et al. 2020）等方法线互补。
