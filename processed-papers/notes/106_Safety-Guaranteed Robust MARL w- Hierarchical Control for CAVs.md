# 106. Safety Guaranteed Robust Multi-Agent Reinforcement Learning with Hierarchical Control for Connected and Automated Vehicles

## 元信息 (Metadata)
- **标题**: Safety Guaranteed Robust Multi-Agent Reinforcement Learning with Hierarchical Control for Connected and Automated Vehicles (Safe-RMM)
- **作者**: Zhili Zhang, H M Sabbir Ahmad, Ehsan Sabouni, Yanchao Sun, Furong Huang, Wenchao Li, Fei Miao
- **机构**: University of Connecticut; Boston University; University of Maryland College Park
- **发表**: ICRA 2025 (IEEE International Conference on Robotics and Automation)
- **链接/arXiv**: arXiv:2309.11057v2

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测不确定性（noisy sensor、state estimation、通信误差导致的 state uncertainty）+ 硬安全约束
- **方法范式**: 分层控制 (hierarchical)、robust MARL (RMAPPO + worst-case Q network)、MPC + robust Control Barrier Functions (CBF)、safe RL
- **关键词**: CAV, hierarchical control, robust MAPPO, worst-case Q, Control Barrier Function, MPC, safety guarantee

## TL;DR（一句话总结）
提出 Safe-RMM 分层框架：高层用 Robust MAPPO（借助 worst-case Q network 在不模拟扰动训练下获得对状态不确定性的鲁棒性）生成协同规划动作，低层用带 robust CBF 的 MPC 控制器通过前向不变性保证 CAV 在混合交通下的硬安全约束。

## 问题与动机 (Problem & Motivation)
连接自动驾驶车辆 (CAV) 在含人类驾驶车辆 (HDV) 的混合交通中需协调控制，但现有 safe RL 方法有两大局限：(i) 假设状态信息精确；(ii) 安全通常仅定义在轨迹期望上。实际中传感器噪声、状态估计、通信误差带来 state uncertainty，安全与状态正确性高度相关（如 HDV 位置被扰动会误导 CAV 判断不会碰撞）。难以在状态不确定下每个时间步保证硬安全约束同时优化多智能体协调。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 测试期存在 state uncertainties（noisy sensor / 估计 / 通信），包括 random error e_rand 与两种 targeting error ERRV、ERRT；训练时不模拟不确定性，靠 worst-case Q 与 robust CBF 应对。
- **设定**: cooperative（CAV 间协作，环境含 HDV）；分层；MARL 训练 + 部署；online 训练，测试时面对扰动

## 方法 (Method)
1. 分层框架 Safe-RMM：高层 Robust MARL ("RM") 生成离散规划动作，条件于其他 CAV/HDV 行为；低层 MPC ("M") + CBF 执行规划并保证安全。
2. 高层 RMAPPO：在 MAPPO 基础上额外训练一个 worst-case Q network 作为 critic，使策略在不模拟潜在 state uncertainty 的情况下学得鲁棒性，只需多训一个 critic、无需先验知识。
3. 低层 MPC 配 robust CBF：利用 CBF 的 forward invariance 性质，在 state uncertainty 下保证安全约束并跟踪高层规划路径。
4. 通过 ablation 验证 robust CBF MPC 改进 MARL、分层 robust MARL 也改进 MPC-CBF 控制器。

## 理论贡献 (Theoretical Contributions)
依赖 robust CBF 的 forward invariance 性质提供安全约束（forward invariant set）的形式化保证；整体偏算法与实证，无新的收敛性/样本复杂度定理。

## 实验 (Experiments)
- **环境/Benchmark**: CARLA simulator，Intersection 与 Highway 两个混合交通场景（3 CAV vs 2/3 HDV，含 HDV 闯红灯/急刹）
- **Baselines**: 非鲁棒 Safe-MM（同框架）、MCP（MARL-PID + CBF safety shield）、MP（MARL+PID 无安全屏蔽）、RULE（rule-based planner + robust MPC）
- **评估指标**: 安全性（碰撞次数）、效率（discounted efficiency return），在 None/e_rand/ERRV/ERRT 四种不确定性配置、各 50 episodes 评估

## 主要结果 (Key Results)
- Safe-RMM 在含不确定性的挑战性混合交通中取得最佳综合安全与效率。
- MP（无安全屏蔽）安全性差；MCP 安全但在不确定性下过于保守、效率低；Safe-RMM 兼顾安全与效率。
- Ablation 表明 robust CBF MPC 与 robust MARL 相互增益。

## 局限与未来工作 (Limitations & Future Work)
某些情况下分层与保守约束可能导致次优；正文提及算法在特定场景可能受限。未来可扩展到更复杂场景、更多车辆与更一般不确定性建模（正文未详尽）。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"状态/观测扰动 + 安全约束"应用线（CAV/自动驾驶），结合 worst-case Q (SA-MDP 思路) 的鲁棒训练与控制论 CBF/MPC 的安全保证，是 robust + safe MARL 在安全关键真实系统落地的代表，与 state-adversarial robust RL、safe MARL 主题密切相关。
