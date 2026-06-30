# 114. Robust Voltage Control for Active Distribution Networks via Safe Deep Reinforcement Learning Against State Perturbations

## 元信息 (Metadata)
- **标题**: Robust Voltage Control for Active Distribution Networks via Safe Deep Reinforcement Learning Against State Perturbations
- **作者**: Meng Tian, Xiaoxu Li, Ziyang Zhu（通讯）, Zhengcheng Dong, Li Gong, Jingang Lai
- **机构**: Wuhan University of Technology；Wuhan University；Huazhong University of Science and Technology
- **发表**: Protection and Control of Modern Power Systems, Vol. 11, No. 1, January 2026（DOI: 10.23919/PCMP.2024.000342）
- **链接/arXiv**: 未明确

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动（measurement noise、instrument error，建模为 truncated Gaussian）、安全约束（电压越限）
- **方法范式**: Safe RL（CMDP + Lagrange）、对抗训练（state adversary，worst-case）、价值分解/CTDE（MADDPG）、鲁棒正则化损失、minimax
- **关键词**: Active Distribution Network, Robust Voltage Control, State Perturbation, Safe DRL, MADDPG, CMDP

## TL;DR（一句话总结）
将主动配电网电压控制建模为 CMDP，提出 safety-augmented MADDPG（S-MADDPG）并引入“robust regulation loss”对抗状态扰动，得到 RS-MADDPG，在保证电压安全约束、降低线损的同时显著提升对观测噪声的鲁棒性。

## 问题与动机 (Problem & Motivation)
高比例 PV 接入使主动配电网（ADN）出现电压偏差与电能质量问题。传统方法（droop 控制、SOCP/遗传/内点等优化）依赖精确物理模型、计算瓶颈、难以实时；普通 DRL/MARL 不保证电压在安全限内；现有 Safe DRL 性能上限略低且需要无扰动观测才能发挥；现有鲁棒优化方法过于保守。实际配电网观测不可避免存在测量误差与噪声（state perturbation），需要兼顾安全与鲁棒的 model-free 方法。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 观测状态被零均值 truncated Gaussian 噪声污染（乘性噪声因子，σ 控制扰动幅度，保证噪声集紧致）。训练时用 state adversary（C-MRC attacker，经梯度上升同时最大化 reward 与 cost）生成最坏扰动状态。
- **设定**: cooperative（每个 PV 为一个 agent，协作稳压）；CTDE / decentralized execution；model-free；online 训练 + 实时执行

## 方法 (Method)
- 将电压控制建模为多智能体 CMDP（state/observation 分离，cost 为电压越限的二值惩罚，上限 0.001）；目标最小化电压偏差与线损。
- S-MADDPG：在 MADDPG (CTDE) 基础上加入独立的 cost value network、Lagrange 乘子（ReLU 保非负，约束转为 max-min）、参数共享，强制将电压约束作为独立 cost。
- Robust regulation loss：基于 worst-case 思想，actor 目标扩展为 maxmin min（带扰动），用 l2 正则项约束自然状态策略 π(s) 与受扰策略 π(s̃) 的偏差上界，使输出在最坏扰动下稳定。
- 用 C-MRC state adversary 求解最坏扰动；扰动尺度采用渐进上升调度（progressive ascent schedule）。

## 理论贡献 (Theoretical Contributions)
偏实证；给出一个理论性质：最坏扰动下 Q 值与自然 Q 值之差被策略偏差 D(π(s), π(s̃)) 上界界定（据此设计 robust regulation loss）。无收敛/样本复杂度证明。

## 实验 (Experiments)
- **环境/Benchmark**: 改造的 IEEE 33-bus（6 PV）与 141-bus（22 PV）系统（MATPOWER/Pandapower）；真实葡萄牙负荷数据 + Elia PV 数据，3 年、3 分钟采样。
- **Baselines**: Model-based SOCP（GUROBI）、vanilla MADDPG、S-MADDPG；泛化对比 RS-MATD3、RS-MAPPO、Lyapunov-based SDRL。
- **评估指标**: Power Loss (PL)、Controllable Rate (CR，电压合规时间比)；5 个随机种子并行；扰动尺度 σ∈{0.5,1.0,1.5,2.0,2.5,3.0}。

## 主要结果 (Key Results)
- 无扰动时 model-based 仍最优；但有状态扰动时 RS-MADDPG 在 CR 上几乎全场最佳，在严重扰动（σ=2.5）下 33-bus/141-bus 的 CR 仍保持 ≥93%/≥99%。
- 大扰动（σ>2）时 RS-MADDPG 在线损上也反超 model-free 基线；CMDP 架构本身在轻扰动下即赋予一定抗扰能力（S-MADDPG），robust regulation loss 在中重扰动下进一步增强鲁棒性。
- 提出的 robust safety 框架（CMDP + robust regulation loss）可泛化到 MATD3、MAPPO 等 MARL 算法，普遍提升其安全与鲁棒性；MAPPO 因保守更新收敛慢、波动大，最不适配该任务。
- 相比 Lyapunov-based SDRL，本框架在扰动加剧时更稳健。

## 局限与未来工作 (Limitations & Future Work)
仅考虑状态扰动；无扰动时不如 model-based；面向三相不平衡配电网、以及拓扑/网络参数/PV 与负荷不确定性等其他“worst-case”维度的鲁棒综合尚待研究。

## 与综述的关联 (Relevance to Survey)
robust MARL 中“状态/观测扰动鲁棒 + Safe RL（CMDP）”交叉线的电力系统应用代表。结合了 state adversary（worst-case 对抗）、价值分解 CTDE（MADDPG）、风险/安全约束与鲁棒正则化，并验证框架在多种 MARL 算法上的可移植性，与 SA-MDP 状态对抗鲁棒、安全 MARL 等主题直接相关。
