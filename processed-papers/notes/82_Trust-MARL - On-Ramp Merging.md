# 82. Trust-MARL: Trust-Based Multi-Agent Reinforcement Learning Framework for Cooperative On-Ramp Merging Control in Heterogeneous Traffic Flow

## 元信息 (Metadata)
- **标题**: Trust-MARL: Trust-Based Multi-Agent Reinforcement Learning Framework for Cooperative On-Ramp Merging Control in Heterogeneous Traffic Flow
- **作者**: Jie Pan, Tianyi Wang, Christian Claudel, Jing Shi
- **机构**: Department of Civil Engineering, Tsinghua University; Dept. of Civil, Architectural, and Environmental Engineering, University of Texas at Austin
- **发表**: arXiv preprint 2025（Preprint submitted to Arxiv, June 2025）
- **链接/arXiv**: 未明确

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 异质智能体不确定性（不可预测的 human-driven vehicle 行为）、mixed-autonomy 交互鲁棒性
- **方法范式**: 动态信任机制、博弈论决策（cooperative/non-cooperative game）、MARL (MASAC 基础)、LSTM 时序编码、课程学习、reward shaping
- **关键词**: cooperative on-ramp merging, dynamic trust mechanism, game theory, heterogeneous traffic, MARL, CAV/HV

## TL;DR（一句话总结）
提出 Trust-MARL 框架，将动态信任机制与 trust-triggered 博弈论决策嵌入 MARL（MASAC 基础），使 CAV 能根据对邻车（包括不可预测的人类车辆）的实时信任评估自适应调整合作策略，提升异质交通流中匝道合流的安全、效率与舒适度。

## 问题与动机 (Problem & Motivation)
智能交通中 CAV 需在异质交通流中与人类驾驶车辆 (HV) 安全高效协作，尤其在匝道合流瓶颈处，HV 行为高度多变难以预测。纯博弈论方法计算复杂、适应性差；传统 MARL 多用静态奖励、假设完全合作，缺乏对多智能体交互中信任的结构化建模，且现有信任方法多视信任为静态/线性变量并局限于同质智能体。本文将信任建模为动态、行为敏感的变量以增强 mixed-autonomy 鲁棒协作。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不确定性来自 HV 的多变、不可预测行为（异质交通流）；HV 用 IDM 车跟驰 + MOBIL 换道模型建模。CAV 需在不同 CAV 渗透率与交通密度下保持鲁棒。
- **设定**: mixed（CAV 协作 + 与 HV 竞争/协作并存）；decentralized 执行的 POMDP 智能体（局部观测，100m scan range，10Hz 状态交换）；online

## 方法 (Method)
- POMDP 建模 CAV，动作含离散横向 (KeepLane/ChangeLeft/ChangeRight) 与连续纵向加速度；观测分 Ego/Local/Group 三尺度特征，经 LSTM 时序编码捕捉行为趋势。
- 动态信任机制：T_ij(t)∈[0,1] 用指数加权更新 T_ij(t+1)=(1-α)T_ij(t)+α·δ(a_j)，δ 表示邻车行为是否被感知为合作。
- 信任驱动 reward shaping：总奖励 R=(1-λ_i)·R^self + λ_i·R^coop，cooperation factor λ_i 由信任值决定；cooperative reward 为邻车 self-reward 的 trust-weighted 平均。self-reward 含 safety/comfort/efficiency 三项。
- Trust-aware 博弈论决策：按信任阈值判定交互为 cooperative（非零和博弈）或 non-cooperative game，进而调整 payoff 与策略；低信任触发保守行为，高信任触发让行/留间隙等合作动作。
- 基础学习器为 MASAC，采用 curriculum learning（逐步提高密度与异质性，最后随机回放阶段）。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（框架与机制设计 + 大量仿真实验）

## 实验 (Experiments)
- **环境/Benchmark**: SUMO 仿真，10km 双车道高速 + 匝道合流场景；4 种 CAV 渗透率 (0/30/70/100%)，3 种交通密度 (300/600/900 veh/h)，10 随机种子
- **Baselines**: MADDPG、MAPPO、MAA2C、MASAC（均用相同奖励/观测设计）；消融对比 Game-Theory-only、MARL-only、MARL+GameTheory；以及 Rule-Based baseline
- **评估指标**: 安全 (collision rate / conflicts / TTC)、效率 (travel time / throughput)、舒适 (longitudinal jerk)、适应性 (recovery time)

## 主要结果 (Key Results)
- Trust-MARL 比四个 MARL baseline 收敛更快、最终回报更高、跨种子方差更低；MASAC 是最强 baseline 故选为基础学习器。
- 消融（相对 rule-based，高密度）：完整 Trust-MARL 将碰撞率降至 1.2%、平均行程时间降 3.8%、jerk 降 7.4%，优于各部分组合；信任层防止伙伴行为异常时的急刹。
- 跨渗透率/密度的对比实验显示 Trust-MARL 在安全、效率、舒适、适应性上一致改进。

## 局限与未来工作 (Limitations & Future Work)
- 仅在 SUMO 仿真验证，未涉及真实部署；HV 行为用 IDM/MOBIL 规则模型近似。
- 偏实证，缺乏理论保证（收敛性/均衡性）。
- 信任的二值合作判定 δ 与阈值化较简单，可进一步精细化。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"对抗/异质智能体不确定性"与"信任机制"主题在自动驾驶 mixed-autonomy 场景的应用，与本批 80 (Trust-Based Information Filtering)、83 (信任与欺骗建模) 同属 trust-based 协作鲁棒方法线；将 game theory + 动态信任 + MARL 三者融合，是博弈论均衡与 reward shaping 在异质交通鲁棒协调中的代表性工作。
