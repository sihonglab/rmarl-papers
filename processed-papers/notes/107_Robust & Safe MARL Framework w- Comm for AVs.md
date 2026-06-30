# 107. Robust and Safe Multi-Agent Reinforcement Learning with Communication for Autonomous Vehicles: From Simulation to Hardware

## 元信息 (Metadata)
- **标题**: Robust and Safe Multi-Agent Reinforcement Learning with Communication for Autonomous Vehicles: From Simulation to Hardware (RSR-RSMARL)
- **作者**: Keshawn Smith, Zhili Zhang, H M Sabbir Ahmad, Ehsan Sabouni, Mainak Mondal, Song Han, Wenchao Li, Fei Miao
- **机构**: University of Connecticut; Boston University
- **发表**: 未明确（arXiv 预印本 [cs.RO]，疑似 CoRL 风格 robot-learning 投稿）
- **链接/arXiv**: arXiv:2506.00982v3

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信延迟与异步（V2V latency，固定与时变）、状态估计误差、模型不确定性、sim-to-real gap + 安全约束
- **方法范式**: delay-aware training、robust MARL、CBF-based Safety Shield、Real-Sim-Real (zero-shot) transfer、controller-agnostic 分层
- **关键词**: CAV, V2V communication delay, robust MARL, Control Barrier Function, sim-to-real, safety shield

## TL;DR（一句话总结）
提出 RSR-RSMARL 框架：用硬件实测的 V2V 通信延迟统计参数化"延迟感知"的状态共享，在固定与时变延迟模型下训练鲁棒 MARL 策略，并配模块化 CBF Safety Shield 提供形式化安全保证，实现 CARLA 到 1/10 比例实车的 Real-Sim-Real 零样本迁移。

## 问题与动机 (Problem & Motivation)
深度 MARL 在仿真中对 CAV 表现良好，但多数工作假设瞬时、完美同步的智能体间通信，导致难以可靠迁移到硬件——真实 V2V 通信本质上有延迟和异步。共享信息存在可测量的延迟与传输变异，却很少被纳入 MARL 训练或硬件验证。同时安全关键性要求在训练与部署全程都有安全保证，而 sim-to-real gap、状态估计误差、通信延迟、模型不确定性都挑战鲁棒性。缺少支持端到端 MARL CAV 开发评估的开源测试平台。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 通信延迟（fixed delay 与 time-varying delay，硬件实测统计参数化，训练注入随机 latency，如 [0,5] 采样）、状态估计误差、模型不确定性、障碍密度变化等扰动。
- **设定**: cooperative（多 CAV）；分层（高层 robust MARL + 低层 controller-agnostic，可接 PID/MPC）；training 与 deployment 全程安全；Real-Sim-Real（仿真训练 + 实车零样本迁移）

## 方法 (Method)
1. 硬件实测 V2V 通信延迟，用统计参数化 delay-aware state sharing 用于仿真训练。
2. 在 fixed 与 time-varying 延迟模型下训练鲁棒 MARL 策略（处理 lane-keeping / lane-changing 高层决策），注入随机 latency 模拟真实无线延迟以获得延迟鲁棒协调。
3. 模块化 CBF-based Safety Shield：在训练与部署中动态过滤不安全动作，提供形式化安全约束，controller-agnostic（PID/MPC 均可，不改学习公式）。
4. 在 CARLA 与物理 1/10 比例 CAV 上验证，进行随延迟递增的 ablation 与零样本迁移。

## 理论贡献 (Theoretical Contributions)
依赖 CBF 提供形式化安全保证（动态过滤不安全动作）；整体偏系统与实证，无新收敛/复杂度定理。

## 实验 (Experiments)
- **环境/Benchmark**: CARLA 仿真 + 物理 1/10 比例 CAV（带车载 V2V）；3-Lane Highway、2-Lane Oval Highway 等场景
- **Baselines**: RSR-MARL（无延迟建模/无 shield 等非鲁棒变体）、Non-robust 变体、去掉 Safety Shield 的变体；对比 TV（time-varying）与 F-2/F-5（fixed-delay）变体
- **评估指标**: 安全（collisions）、效率（discounted return / completion time），50 test episodes 平均，不同通信延迟与障碍密度配置

## 主要结果 (Key Results)
- 延迟感知变体（TV 与 fixed-delay F-2/F-5）在延迟与障碍密度增加下保持零碰撞，TV 模型效率最佳；RSR-MARL baseline 随障碍密度增大而退化、出现碰撞。
- 去掉 Safety Shield 显著增加碰撞频率并导致学习不稳定，验证 shield 的必要性。
- 结果证明结构化 latency 建模能提升 sim-to-hardware 的可靠零样本迁移与安全-性能权衡。

## 局限与未来工作 (Limitations & Future Work)
当前在 1/10 比例平台与特定高速场景验证；延迟建模依赖实测统计。未来可扩展到更大规模车队、更复杂城市场景与更丰富的通信攻击/丢包模型（正文未详尽列出）。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 的"通信扰动（延迟/异步）+ 安全约束 + sim-to-real"应用线（CAV），与同团队的 Safe-RMM（编号 106）一脉相承，强调把通信延迟鲁棒性与 CBF 安全保证整合进训练并验证到真实硬件，关联通信鲁棒 MARL、safe MARL 与 sim-to-real 迁移主题。
