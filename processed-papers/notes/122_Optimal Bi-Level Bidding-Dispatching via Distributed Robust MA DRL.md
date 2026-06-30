# 122. Optimal Bi-Level Bidding and Dispatching Strategy Between Active Distribution Network and Virtual Alliances Using Distributed Robust Multi-Agent Deep Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Optimal Bi-Level Bidding and Dispatching Strategy Between Active Distribution Network and Virtual Alliances Using Distributed Robust Multi-Agent Deep Reinforcement Learning
- **作者**: Ziqing Zhu, Ka Wing Chan（通讯）, Shiwei Xia, Siqi Bu
- **机构**: The Hong Kong Polytechnic University；North China Electric Power University
- **发表**: IEEE Transactions on Smart Grid, Vol. 13, No. 4, July 2022（DOI: 10.1109/TSG.2022.3164080）
- **链接/arXiv**: 未明确（IEEE Xplore）

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 净负荷预测误差不确定性（RDG/负荷）、奖励函数与状态转移不确定性、市场对手（其他 DVA）策略不可观测
- **方法范式**: 鲁棒 MDP + robust Nash equilibrium (RNE)、minimax/risk-averse、对抗式价值函数、多智能体 DDPG（全分布式）、博弈论均衡、双层（bi-level）规划
- **关键词**: Active Distribution Network, Distributed Virtual Alliance, Bidding Strategy, Robust Nash Equilibrium, Multi-Agent DDPG, Risk-Averse

## TL;DR（一句话总结）
针对去管制主动配电网中虚拟联盟（DVA）与 DSO 的双层竞价-调度问题，提出基于 robust Nash equilibrium 的全分布式 Distributed Robust Multi-Agent DDPG（DRMA-DDPG），在净负荷预测不确定性下得到风险厌恶的最优竞价/调度策略且无需共享他方私密信息。

## 问题与动机 (Problem & Motivation)
去管制 ADN 中虚拟微电网（VMG）、虚拟电厂（VPP）等 DVA 自主参与日前（DA）市场竞价，由 DSO 调度并定出清价（MCP）。RDG 与负荷的不确定性导致净负荷预测误差，带来实时平衡成本与惩罚，复杂化市场规则与竞价/调度决策。已有数学规划/MPC 方法静态、需精确预测；传统 RL（Q-learning/WoLF-PHC）受限于离散空间与维度灾难；已有 DDPG 方法仍需获取其他 DVA 的机密竞价信息、且未纳入净负荷不确定性及其对决策的影响。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 净负荷预测误差 μ0,k 落在不确定性集 Ẽk_t 内（带概率分布的场景集）。决策需对该不确定性导致的惩罚风险鲁棒；同时奖励函数 R 与状态转移存在不确定性。建模为 robust MDP，求解 robust Nash equilibrium（RNE）。
- **设定**: competitive/mixed（多个 DVA 竞价 + DSO 调度，双层博弈）；fully distributed（各 stakeholder 训练不需他方信息）；online

## 方法 (Method)
- 将 DA-RT 协调下 DVA 与 DSO 的双层最优竞价-调度（OBDS）建模为随机动态规划，含 DA 失约惩罚，再重构为（robust）MDP。
- 定义 robust Nash equilibrium：每个 agent 的价值函数为 max-min 形式 V = Max_μ Min_{R∈R / μ0∈Ẽ} 期望回报，即在最坏（worst-case）预测误差/奖励场景下追求最大回报，使策略风险厌恶。
- 提出 DRMA-DDPG：在 MA-DDPG 基础上，将 RNE 概念嵌入价值函数得到 robust（risk-averse）更新；全分布式训练，每个 DVA/DSO 无需他方私密竞价信息，并能推断其他 DVA 的竞价策略以稳定梯度。
- DA 失约惩罚机制激励 DVA 提升预测精度、补偿实时平衡成本。

## 理论贡献 (Theoretical Contributions)
偏实证为主；理论层面引入 robust MDP + RNE 的 max-min 价值函数定义，并论证算法收敛到 RNE（实验验证收敛），无形式化收敛率/样本复杂度证明。

## 实验 (Experiments)
- **环境/Benchmark**: 含 5 个 DVA 的测试市场，基于改造的 IEEE 33-Node Bus 网络；真实小时级 RDG/负荷曲线与预测误差场景；竞价价格区间 [1, 1.5] RMB/kWh。
- **Baselines**: MA-DDPG、DDPG、Deep Q-Learning。
- **评估指标**: 收敛速度（episode 数）、平均/总奖励、最坏情况下最低奖励、MCP 与负荷/惩罚关系、DSO 调度成本与奖励。

## 主要结果 (Key Results)
- DRMA-DDPG 在约 8000 episode 内收敛，而 MA-DDPG/DDPG/DQN 因奖励与他方策略不确定性导致梯度不稳定而发散。
- 不仅总奖励更高，最坏情况下的最低奖励也明显高于基线，体现有效风险缓解。
- 揭示惩罚机制对竞价的强影响：高惩罚下 DVA 会“故意抬价”使竞标失败以避免负奖励；惩罚降到约 30% 时低谷期出价更低、利于社会福利，但会削弱提升预测精度的激励——市场监管参数需谨慎设定。
- DSO 用 DRMA-DDPG 做更保守的调度（少用高风险 VPP1/VPP2 容量），个别时段成本略增、奖励略降，但在多数时段缓解实时不平衡的巨额惩罚、整体奖励提升。

## 局限与未来工作 (Limitations & Future Work)
惩罚参数的确定需进一步深入研究；测试规模为 5 个 DVA 的 IEEE 33 节点系统。定位为新兴电力市场早期阶段的风险厌恶竞价模拟与均衡计算工具，可为市场运营提供理论与实践支撑。

## 与综述的关联 (Relevance to Survey)
robust MARL 中“robust MDP + robust Nash equilibrium + 风险厌恶/minimax”理论与电力市场（竞价/调度）应用的结合。把不确定性建模为最坏情况对抗（max-min 价值函数），并在竞争性多智能体、全分布式、信息不可观测设定下求 RNE，与 DRMG 理论、博弈论均衡、风险敏感 MARL 等主线直接相关，是 robust MARL 在能源市场博弈的早期代表工作（2022）。
