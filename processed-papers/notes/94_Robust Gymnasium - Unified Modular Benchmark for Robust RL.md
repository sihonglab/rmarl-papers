# 94. Robust Gymnasium: A Unified Modular Benchmark for Robust Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Robust-Gymnasium: A Unified Modular Benchmark for Robust Reinforcement Learning
- **作者**: Shangding Gu, Laixi Shi (equal contribution), Muning Wen, Ming Jin, Eric Mazumdar, Yuejie Chi, Adam Wierman, Costas Spanos
- **机构**: UC Berkeley; Caltech; Shanghai Jiao Tong University; Virginia Tech; Carnegie Mellon University
- **发表**: ICLR 2025
- **链接/arXiv**: arXiv:2502.19652v1；网站 https://robust-gym.github.io/

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动、奖励扰动、动作扰动、环境（转移核/动力学/外部 workspace）不确定性、对抗扰动（含 LLM 对抗者）、安全约束、智能体失效；覆盖 sim-to-real gap 全链路
- **方法范式**: benchmark / 统一模块化框架（MDP with disruption）、标准 RL / robust RL / safe RL / MARL 评测
- **关键词**: robust RL benchmark, disruptors, sim-to-real, modular framework, multi-agent RL, LLM adversary

## TL;DR（一句话总结）
提出 Robust-Gymnasium，一个面向 robust RL 的统一模块化 benchmark，将扰动 (disruptor) 解耦到 agent 观测状态/奖励、动作、环境等所有交互环节，覆盖 60+ 个跨控制机器人、safe RL、MARL 的任务，并用它系统评测标准/鲁棒/安全/多智能体 RL 算法，揭示现有方法在各类扰动下的明显不足。

## 问题与动机 (Problem & Motivation)
标准 RL 在理想训练环境学到的策略因 sim-to-real gap、不确定性、噪声、恶意攻击而在真实部署灾难性失败。robust RL 旨在提升对物理世界与人类行为复杂变化的韧性，但现有 robust RL 工作通常只针对单一扰动类型（如仅观测状态），且在彼此孤立、可能过拟合算法的一次性环境上评测。缺乏标准化、覆盖多扰动来源与阶段的统一 benchmark 是 robust RL 进步的关键瓶颈。理想 benchmark 应提供多样任务、覆盖交互全过程的不确定性与扰动。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 提出 Disrupted-MDP 框架 M_dis=(S,A,T,P,r,D_s,D_r,D_a)，三类 disruptor：observation-disruptor（扰动观测状态 s̃=D_s(s) 与观测奖励 r̃=D_r(r)）、action-disruptor（扰动执行动作 ã=D_a(a)）、environment-disruptor（扰动转移核/奖励/外部 workspace，制造非平稳）。disruptor 有四种模式（random、adversarial、internal dynamic shift、external disturbance）与可变频率（step/episode/间歇）。
- **设定**: 涵盖 single-agent / safe RL / cooperative MARL；online 与 offline 任务基；两种评测流程——In-training（训练+测试均扰动）与 Post-training（仅测试扰动）

## 方法 (Method)
- 统一 robust RL 框架：在标准 finite-horizon MDP 上插入 disruption 模块，把文献中各类不确定性归类到 observation/action/environment 三类 disruptor。
- 模块化任务构造三步：选任务基（11 套，60+ 任务：Box2D、MuJoCo、Maze、Fetch、Franka Kitchen、Dexterous Hand、Adroit、HumanoidBench、Robosuite、Safety MuJoCo、MAMuJoCo）→ 选 disruptor 与模式 → 设定交互过程与频率。
- 支持高级模式：多 disruptor 组合（如观测噪声+外部扰动同时）、可变频率（间歇/随机）。
- 新任务：Robosuite 的 MultiRobustDoor（对抗机械臂阻碍另一臂）测试鲁棒性。
- 特色：用 LLM 作为对抗 disruptor 生成对抗状态扰动。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（benchmark 与统一框架贡献，非理论分析）。

## 实验 (Experiments)
- **环境/Benchmark**: 自身 Robust-Gymnasium 60+ 任务，代表性如 HalfCheetah-v4、Ant-v5、Hopper-v5、Robosuite DoorCausal/LiftCausal、SafetyWalker2d、MA-HalfCheetah (MAMuJoCo)
- **Baselines**: 标准 RL: PPO、SAC；robust RL: OMPO、RSC、ATLA、DBC；safe RL: PCRPO、CRPO；MARL: MAPPO、IPPO
- **评估指标**: 部署/原始环境平均回报（默认 robust metric），安全任务用 episode cost 与 cost limit；也提及 CVaR、worst-case/average 等其他 robust metric

## 主要结果 (Key Results)
- 标准 RL (PPO/SAC) 随扰动增大性能快速退化，尤其 Post-training（训练未感知扰动）下更严重。
- robust RL baselines：OMPO 在非平稳环境性能显著下降；外部语义扰动下 RSC 比 ATLA、DBC 更鲁棒但训练效率待提升（需在线生成增广数据）。
- safe RL：CRPO 在扰动下快速退化，PCRPO 更鲁棒，且适当扰动训练甚至提升性能。
- MARL：MAPPO 与 IPPO 在对所有 agent 的 state/action/reward 扰动下均退化；也支持仅扰动部分智能体。
- LLM 对抗扰动比 uniform 噪声导致 PPO 更大性能下降，高频攻击退化更严重。
- 总体：现有算法即便面对单一阶段扰动也常不达预期，凸显需要新的 robust RL 方法。

## 局限与未来工作 (Limitations & Future Work)
- 作为 benchmark 不提出新算法；某些 robust baseline（如 RSC）训练效率需改进。
- 并非所有任务基都支持所有扰动类型。
- 未来：基于该平台发展覆盖多阶段扰动的新 robust RL 算法，进一步探索 LLM 在 robust RL 中的对抗/评测潜力，以及非平稳任务。

## 与综述的关联 (Relevance to Survey)
属于 robust (MA)RL 的"评测基础设施 / benchmark"主题，是首个统一覆盖状态/观测、奖励、动作、环境全链路扰动并跨 single-agent、safe RL、MARL 的标准化平台。其 MARL 评测（MAMuJoCo 上对全部/部分智能体的状态/动作/奖励扰动、对抗机械臂）直接服务于 robust MARL 综述的实验评估与方法比较，是连接各类鲁棒性威胁模型与统一评测协议的关键参考。
