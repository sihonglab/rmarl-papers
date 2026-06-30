# 126. Distributionally Robust Multi-Agent Reinforcement Learning for Dynamic Chute Mapping

## 元信息 (Metadata)
- **标题**: Distributionally Robust Multi-Agent Reinforcement Learning for Dynamic Chute Mapping
- **作者**: Guangyi Liu, Suzan Iloglu, Michael Caldara, Joseph W. Durham, Michael M. Zavlanos
- **机构**: Amazon Robotics; Duke University (Dept. of Mechanical Engineering and Materials Science)
- **发表**: ICML 2025（arXiv:2503.09755v1, cs.LG, 12 Mar 2025；正文被引为 ICML Vancouver 2025）
- **链接/arXiv**: arXiv:2503.09755v1

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 奖励/需求分布的分布偏移（induction rate distribution shift），OOD 需求模式（非对抗攻击，而是分布不确定性）
- **方法范式**: group DRO、distributionally robust Bellman operator、minimax worst-case、Value Decomposition Network (VDN)、contextual-bandit worst-case 预测器
- **关键词**: DRMARL、Group DRO、Contextual Bandit、Chute Mapping、Resource Allocation、Distribution Shift

## TL;DR（一句话总结）
将 group DRO 引入 MARL，为 Amazon 机器人分拣仓库的"目的地-滑槽映射"问题学习对 induction rate 分布偏移鲁棒的策略，并用 contextual-bandit worst-case reward predictor 把最坏组识别复杂度从 O(m) 降到 O(1)，平均减少包裹再循环约 80%。

## 问题与动机 (Problem & Motivation)
分拣仓库中目的地-滑槽映射决定吞吐能力，但包裹 induction rate 高度时变（季节性/运营模式）。作者既往 MARL 策略假设部署分布与训练分布一致，遇到分布偏移时性能显著退化、再循环增加。现有 robust/DRRL 多关注转移概率的不确定性，无法刻画 induction 分布变化；本文聚焦奖励函数分布的分布鲁棒优化，并解决 DRMARL 训练计算成本高的问题。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 不确定性作用于 induction generating distribution（建模为 multinomial）。用历史数据按周聚成 m 个组 {Pg}（21 组/9 组），ambiguity set M 为各组的凸组合（simplex）。目标为对 M 内最坏分布的期望奖励做优化。
- **设定**: cooperative Markov game（每个目的地为一 agent，VDN 值分解 + budget 约束整数规划求联合动作）；中心化训练；online 仿真，需对 OOD 分布鲁棒

## 方法 (Method)
1. **MARL 基础**: 每目的地一 agent，观测含再循环数/可分配滑槽数/已分配滑槽数，动作为分配新滑槽数；联合 Q 分解为共享局部 Q' 之和 (VDN)，联合动作通过预算约束整数规划 (OR-Tools/Xpress) 求解。
2. **Group DRO**: Lemma 3.1 证明在凸组合 ambiguity set 上的最坏分布期望奖励等价于在有限 m 组上取 inf，将无穷维 DRO 化为有限维。
3. **Distributionally Robust Bellman operator** (Lemma 3.2): 用 worst-case 即时奖励 r̃(s,a)=inf_g E_{X~Pg}[r(s,a;X)] 构造鲁棒 Bellman 算子并训练鲁棒 Q；区别于直接最小化最坏 Bellman error。
4. **CB-based Worst-Case Reward Predictor**: 训练独立 DQN QCB(s,a,g) 预测每个 (s,a) 的最坏分布组，避免对所有组穷举前向仿真，将 worst-case 组识别从 O(m) 降到 O(1)；QCB 预训练后在 DRMARL 训练中固定。

## 理论贡献 (Theoretical Contributions)
- Lemma 3.1: group ambiguity set 下最坏分布期望奖励 = 有限组上的 inf（LP 顶点最优）。
- Lemma 3.2: 给出针对 MARL 的 distributionally robust Bellman operator，并证明其为 ℓ∞ 下的 γ-收缩映射，故 Q-learning 收敛到 Q̃*。
- 首次将 contextual bandit 与 group DRO + MARL 集成以降低 DRRL 计算成本。

## 实验 (Experiments)
- **环境/Benchmark**: 简化分拣仓库仿真 (10 滑槽/20 目的地/5h episode) 与大规模 Amazon 机器人分拣仓库仿真 (187 滑槽/120 目的地/11h episode，21 组跨年数据)
- **Baselines**: 普通 MARL；DRMARL(random group)；DRMARL(exhaustive search)；group-specific MARL (理论最优上界)
- **评估指标**: recirculation rate、throughput、recirculation amount、训练时间/收敛速度、预测损失

## 主要结果 (Key Results)
1. DRMARL(QCB) 在 9 组上 recirculation rate 0.56%，远优于 MARL(2.16%)，接近 group-specific 最优 (0.53%) 与 exhaustive (0.55%)。
2. 大规模仿真中（21 组），DRMARL 相对 MARL 平均 recirc rate 降低约 79.97%、吞吐增加 5.62%、recirc 量降低 33.64%。
3. QCB 把最坏组识别从 O(m) 降到 O(1)：简化环境 <300s 收敛 vs exhaustive ≥2900s；大规模 exhaustive 约需 924 小时。
4. 即便测试分布在 ambiguity set M 之外，DRMARL 仍保持一致性能，泛化良好。

## 局限与未来工作 (Limitations & Future Work)
依赖历史数据能张成代表性分布组的假设；group DRO 的最坏组随策略演化而变，静态/软重加权在 MARL 中效果有限（故引入 CB）；数据因商业保密仅报告相对改进。框架可推广到资源分配、协作机器人、仓库自动化等需分布鲁棒的 MARL 应用（未来方向）。

## 与综述的关联 (Relevance to Survey)
robust MARL 中"分布鲁棒 (DRMARL/group DRO)"主题线的代表性工业落地工作，与同作者团队 traffic control (123) 共享 CB-WCE/worst-case 重加权思路；理论上提供 DR Bellman operator 收缩性证明，可与 RMG、ERNIE (30)、DRNVI、Sample-Efficient Robust MARL (2)、Breaking Curse of Multiagency (3) 等转移动态鲁棒工作对照（本文聚焦奖励分布而非转移）。
