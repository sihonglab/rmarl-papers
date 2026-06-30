# 108. 5G-enabled Safe and Robust Deep Multi-Agent Reinforcement Learning Framework for CAV Coordination

## 元信息 (Metadata)
- **标题**: 5G-enabled Safe and Robust Deep Multi-agent Reinforcement Learning Framework for CAV Coordination
- **作者**: Fei Miao, Song Han
- **机构**: University of Connecticut（与 USDOT OST-R / New England University Transportation Center 合作）
- **发表**: USDOT / NEUTC Final Research Report，June 2025（项目结题技术报告，Grant #69A3552348301）
- **链接/arXiv**: 报告见 NEUTC 网站 www.umass.edu/neutc；相关论文 arXiv:2309.11057 (Safe-RMM, ICRA 2025) 与 arXiv:2506.00982 (RSR-RSMARL)

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测不确定性（noisy sensor、通信、state estimation）、通信延迟/质量、模型不确定性 + 硬安全约束
- **方法范式**: 分层 robust + safe MARL (Safe-RMM / RMAPPO + worst-case Q)、MPC + robust CBF、5G-based V2X 实时 flow scheduling、Real-Sim-Real
- **关键词**: CAV, 5G V2X, robust MARL, safety guarantee, Control Barrier Function, flow scheduling

## TL;DR（一句话总结）
USDOT 资助项目的结题报告，整合了一套 5G-enabled 安全鲁棒深度 MARL 框架用于 CAV 协调：高层 Robust MAPPO（worst-case Q）+ 低层 MPC/robust CBF 提供安全保证（Safe-RMM），并辅以面向 V2X 的实时通信 flow scheduling，覆盖从仿真到 F1/10 实车的验证。

## 问题与动机 (Problem & Motivation)
在含人类驾驶车辆的混合交通中协调控制 CAV，需在 state uncertainty（传感器噪声、通信、状态估计）下每个时间步保证硬安全约束并优化多智能体协调。现有 safe RL 假设状态精确、且安全仅定义在轨迹期望上。同时 5G/V2X 能扩展个体感知能力，但安全关键决策对通信质量有定量要求，需要联合设计通信、机器学习与控制。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 测试期 state uncertainties（random / targeting errors）、通信延迟与资源约束、多样驾驶场景；训练时不模拟扰动，靠 worst-case Q 与 robust CBF 应对。
- **设定**: cooperative（混合交通含 HDV）；分层；MARL 训练 + 部署全程安全；仿真 + 小规模实车

## 方法 (Method)
1. Safe-RMM 分层方案：高层 Robust MAPPO (RMAPPO)，训练一个 worst-case Q network 作为 critic，使策略在不模拟不确定性下对测试期 state uncertainty 鲁棒；低层 MPC + robust CBF 利用 forward invariance 保证安全并跟踪高层规划。
2. 设计计算可行的 safe MARL 算法，依需求严格保证 AV 安全且对多种驾驶场景鲁棒。
3. 基于 MARL 的定量通信需求，开发面向 5G-based V2X 的实时 flow scheduling 框架，通过时-频-空资源分配提供 per-flow 实时可调度性保证，确保安全关键决策/控制的通信质量。
4. 在 CARLA 仿真与 F1/10 比例实车（带 V2V）上验证（与 RSR-RSMARL 框架一致）。

## 理论贡献 (Theoretical Contributions)
依赖 robust CBF 的 forward invariance 提供形式化安全保证，并对 5G flow scheduling 提供 per-flow 实时可调度性保证；整体为框架/算法与系统集成，无独立的收敛/样本复杂度新定理。

## 实验 (Experiments)
- **环境/Benchmark**: CARLA simulator（Intersection、Highway 等混合交通场景）+ F1/10 比例自动驾驶实车测试台（带 V2V 通信）
- **Baselines**: Safe-RMM 与非鲁棒/无安全屏蔽的基线（同 Safe-RMM 论文，如 MCP、MP、RULE 等）
- **评估指标**: 安全（碰撞）、效率（discounted return / completion time）

## 主要结果 (Key Results)
- Safe-RMM 在含不确定性的混合交通中取得最佳安全与效率，优于基线。
- F1/10 实车（带 V2V）实验证明 RSR-RSMARL 框架在多种配置下提升驾驶安全与协调。
- 强调联合设计鲁棒策略表示与模块化安全架构对可扩展、可泛化 Real-Sim-Real 迁移的重要性。

## 局限与未来工作 (Limitations & Future Work)
报告形式，技术细节散见于其支撑论文 (106/107)。未来计划向 CT DOT 演示硬件性能、在 5G 基站部署增强 5G 模块、与 Nvidia/Qualcomm 合作扩展到更实际的自动驾驶场景。

## 与综述的关联 (Relevance to Survey)
是同一团队 Safe-RMM（编号 106，ICRA 2025）与 RSR-RSMARL（编号 107）工作的 USDOT 项目级总览/结题报告，新增 5G V2X 通信 flow scheduling 的系统视角。在 robust MARL 全景中定位于"状态/观测扰动 + 通信约束 + 安全约束"的 CAV 应用线，连接 worst-case Q 鲁棒训练、CBF/MPC 安全保证与通信-学习-控制协同设计。
