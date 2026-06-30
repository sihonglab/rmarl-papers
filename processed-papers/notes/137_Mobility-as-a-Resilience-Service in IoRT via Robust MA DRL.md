# 137. Mobility-as-a-Resilience Service in Internet of Robotic Things Through Robust Multiagent Deep Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Mobility-as-a-Resilience Service in Internet of Robotic Things Through Robust Multiagent Deep Reinforcement Learning
- **作者**: Shi Li, Jiong Jin, Mahbuba Afrin, Xiaohua Ge, Jing Fu, Yu-Chu Tian
- **机构**: Swinburne University of Technology、Curtin University、RMIT University、Queensland University of Technology（澳大利亚）
- **发表**: IEEE Internet of Things Journal, Vol. 12, No. 23, December 2025
- **链接/arXiv**: DOI 10.1109/JIOT.2025.3535148

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 模型不确定性（reward/transition 未知）、观测噪声（observation noise）、奖励不确定性（reward uncertainty）、硬件失效/网络不稳定（resilience）
- **方法范式**: robust MADDPG（RMADDPG）、nature player 对抗式 domain randomization、POMG 博弈论、CTDE、minimax/worst-case
- **关键词**: IoRT, MADRL, RMADDPG, smart farm, task allocation, resilience

## TL;DR（一句话总结）
针对智能农场 IoRT 系统的 UAV 失效问题，提出 Mobility-as-a-Resilience Service (MaaRS)，用主动 UAV 移动重定位实现系统恢复，并设计 RMADDPG（MADDPG + nature player 对抗者）在模型/观测/奖励不确定性下实现鲁棒的动态任务分配。

## 问题与动机 (Problem & Motivation)
IoRT（Internet of Robotic Things）在可持续农业（如牲畜监测）中部署面临网络不稳定与硬件失效，UAV 故障会导致数据采集失败、buffer overflow deadline 导致关键数据丢失。已有 MADRL（如 MADDPG）忽视真实环境中模型不确定性（不知其他机器人 reward/系统转移动态）及农业环境的噪声/扰动，鲁棒性与一致性未被充分探索。需要鲁棒 MADRL 实现失效时的快速系统恢复与任务再分配。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 用 nature player（虚拟对抗 agent）生成 domain randomization 参数 u∈U，确定性地影响 transition P 与 reward w_r，模拟最坏情况；额外建模观测噪声（乘性 Gaussian: ō_r = o_r·(1+N(0,σ²))）与 reward 不确定性。使用简单不确定性集，无需先验概率信息。
- **设定**: cooperative（共享 team reward，最小化恢复时间与能耗）；CTDE（centralized critic + decentralized actor）；建模为 partially observable Markov game (POMG)；online。

## 方法 (Method)
- **MaaRS 模型**: 利用主动 UAV 的移动性作为韧性服务，当某 UAV 连接失效无法采集数据源数据时，另一 UAV 重定位到附近收集数据，最大化利用现有资源实现快速恢复（含 relocation/upload/preprocessing/commit 时间与能耗模型）。
- **多目标优化**: min Σ(α·τ' + β·e')（时间 vs 能耗权衡，α=β=0.5），约束含任务 deadline (C4) 与 UAV 可用能量 (C5)。
- **POMG + RMADDPG**: 将动态任务分配建模为 POMG，状态/动作（移动位置 + 任务分配）/共享 reward = −(ατ'+βe')；RMADDPG = MADDPG + nature player 对抗者，agent 在 worst-case 下最大化回报。
- **nature player 训练**: 损失 Loss_np = α_np·w̄ + β_np·MSE(o_ξ, ξ)，平衡对抗难度（降低 agent 平均 reward）与随机性；与主 agent 同时训练，随 agent 适应而生成更难场景。
- **训练稳定化**: 各 agent 独立 replay buffer、target networks 软更新、centralized critic 提供全局视角。

## 理论贡献 (Theoretical Contributions)
- 给出含不确定性 u 的 POMG Bellman 方程，并基于 [11] 论证 POMG 中存在 perfect Nash equilibrium（π* = (π*_1,...,π*_R)）。
- 复杂度分析：训练空间复杂度 O(|R|×B)，时间复杂度 O(KT|R|I²_max)，约为单智能体 MDQN 的 |R| 倍。（无新收敛速率/样本复杂度证明，偏应用）

## 实验 (Experiments)
- **环境/Benchmark**: 基于真实数据的牲畜监测智能农场仿真（Python 3.8 + PyTorch 2.0，改造自 Multi-Agent Particle Environment）；UAV 初始位置/电量随机。
- **Baselines**: decentralized DDPG、MADDPG、closest-UAV 启发式分配算法（及 MDQN [7] 复杂度对比）。
- **评估指标**: 累计/运行平均 reward、收敛性、不同观测噪声(1%/3%/5%)与 reward 不确定性(3%/6%/9%)下的稳定性，超参敏感性（lr、hidden units、batch size、γ）。

## 主要结果 (Key Results)
- RMADDPG 在性能、效率、稳定性上显著优于 SOTA（DDPG、MADDPG、heuristic）。
- 在观测噪声与 reward 不确定性逐级增大时，RMADDPG 保持更鲁棒、稳定的累计 reward（5 次运行 95% 置信区间）。
- 超参选定：lr=0.01、64 hidden units、batch size=1024、γ=0.95 在收敛速度与稳定性间最优。

## 局限与未来工作 (Limitations & Future Work)
正文未单列局限段落；可推断局限：仿真为主（无真机验证）、不确定性集较简单、计算复杂度随 UAV 数线性增长。未来方向正文未明确详述（聚焦扩展资源调度与韧性）。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"模型/观测/奖励不确定性 + nature player 对抗训练"主线（与 #135 同源的 nature player / robust Markov game 思路），并强调系统韧性（resilience/容错）应用。CTDE + POMG + Nash 均衡 + domain randomization 的组合，是 robust MADDPG 在 IoRT/智慧农业资源分配的代表性应用案例。
