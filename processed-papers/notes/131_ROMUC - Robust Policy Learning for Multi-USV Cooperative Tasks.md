# 131. ROMUC: A Robust Policy Learning Method for Multi-USV Cooperative Tasks

## 元信息 (Metadata)
- **标题**: ROMUC: A Robust Policy Learning Method for Multi-USV Cooperative Tasks
- **作者**: Peng Li, Shaofei Chen, Ao Ma, Jing Chen (通讯)
- **机构**: College of Intelligence Science and Technology, National University of Defense Technology (国防科技大学), Changsha, China
- **发表**: 2025 Asian Conference on Artificial Intelligence Technology (ACAIT)（DOI: 10.1109/ACAIT67930.2025.11522108, IEEE）
- **链接/arXiv**: IEEE Xplore (ACAIT 2025)；arXiv 未明确

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 双重风险——(1) 环境不确定性 (洋流、风速、礁石、探索风险、含随机队友的 noise 风险)；(2) 决策方法本身的固有误差 (overestimation error)
- **方法范式**: 分布式 RL (distributional RL / implicit quantile network)、value decomposition (QMIX monotonic mixing)、value averaging + operator switching、risk-aware policy、CTDE
- **关键词**: multi-USV、distributional RL、IQN、value averaging、operator switching、cooperative robustness

## TL;DR（一句话总结）
ROMUC 针对多无人水面艇 (USV) 协同任务的双重风险，用 implicit quantile network 学习动作值的完整分布以应对环境不确定性，并结合 value averaging + operator switching 抑制 MARL 固有的过估计误差，在 QMIX 值分解框架下学习更鲁棒的协同策略。

## 问题与动机 (Problem & Motivation)
开阔水域中多 USV 系统同时面临环境不确定性 (洋流/风/礁石) 与自身协同策略 (决策方法误差) 的双重风险，挑战协同策略鲁棒性。现有多 USV MARL 工作 (QMIX/VDN/MADDPG/MA-POCA 等) 多不考虑风险；基于扰动注入的鲁棒 MARL 只能应对特定扰动、无法刻画多样环境风险，也不能处理方法自身误差；VAOS 仅处理方法误差风险而不应对环境风险。需要同时处理两类风险的方法。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 环境风险 (exploration 风险：减慢探索率衰减提高协作难度；noise 风险：队友中存在以 30% 概率随机选动作的随机智能体) + 方法误差风险 (Q 值过估计)。建模为 Dec-POMDP。
- **设定**: cooperative；CTDE（集中训练访问全局状态，分散执行用局部观测）；online

## 方法 (Method)
1. **动作值分布表示**: 用 distributional RL 的 implicit quantile network (IQN) 近似回报分布 Zi (E[Zi]=Qi)，其中分位函数 F⁻¹(s,u|ω)=f(φ(o)⊙φ(ω))，将环境风险等级 ω 融入策略学习，生成 risk-aware 策略，更全面学习环境不确定性。
2. **分布式值分解**: 借鉴 QMIX 单调 mixing network 将联合策略值分布分解为各 agent 分布，满足 distributional IGM 原则。
3. **Value averaging + operator switching**: 借鉴 Averaged DQN/VAOS，对多个网络输出的值做平均并切换算子以减少过估计误差、提升训练稳定性，缓解方法固有误差风险。
4. 同时应对环境风险与方法误差风险（区别于只做其一的既有工作）。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（基于 distributional IGM 与 QMIX 单调性的方法组合，未给出新收敛性/认证证明）

## 实验 (Experiments)
- **环境/Benchmark**: 两个典型多 USV 任务——Pursuit (三红方 USV 协同追击) 与 Denial (两蓝方 USV 突破红方封锁)；含 standard / exploration / noise 三种设置
- **Baselines**: QMIX (SOTA MARL)、VAOS 与 Sub-Avg (误差缩减方法)、DRIMA (risk-sensitive 算法)
- **评估指标**: 测试 reward（期望与方差，3 个随机种子）；含组件/超参 (分位数数量、网络数量) 消融

## 主要结果 (Key Results)
1. 在 standard 设置下 ROMUC 在 pursuit 与 denial 任务测试 reward 均高于所有 baseline，能有效减少方法误差风险、稳定训练。
2. 在 exploration 与 noise 风险下 ROMUC 均取得最优性能，因其同时应对决策误差缩减与环境风险缓解。
3. 消融显示 ROMUC 在风险设置下优于仅做误差缩减的 VAOS；性能对分位数数量较稳定，增加网络数量略有提升但计算量上升、效率下降。

## 局限与未来工作 (Limitations & Future Work)
任务场景做了简化假设；增加网络数量带来计算负担、效率下降；评估仅在两个仿真 USV 任务，规模有限；缺乏理论鲁棒性保证。（论文未详列 future work）

## 与综述的关联 (Relevance to Survey)
robust MARL 中"风险敏感 (risk-aware/distributional) + 价值分解"主题线在海上多智能体 (multi-USV) 的应用，同时处理环境不确定性与算法过估计误差两类风险；与 distributional/risk-sensitive MARL (如 13)、QMIX 鲁棒性增强 (32)、扰动注入鲁棒训练等线相关，可作为应用案例。
