# 27. GOV-REK: Governed Reward Engineering Kernels for Designing Robust Multi-Agent Reinforcement Learning Systems

## 元信息 (Metadata)
- **标题**: GOV-REK: Governed Reward Engineering Kernels for Designing Robust Multi-Agent Reinforcement Learning Systems
- **作者**: Ashish Rana, Michael Oesterle, Jannik Brinkmann
- **机构**: Institute for Enterprise Systems, University of Mannheim, Germany
- **发表**: AAMAS 2024 (Extended Abstract)；arXiv:2404.01131v2 (2024)
- **链接/arXiv**: arXiv:2404.01131；github.com/arana-initiatives/gov-rek-marls

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 环境配置随机扰动、稀疏奖励下的学习稳健性（robust jumpstart / 容错），并非对抗攻击鲁棒
- **方法范式**: 奖励塑形 (reward shaping)、potential-based reward shaping (PBRS)、governance kernel (类 Gaussian kernel 先验)、Hyperband-like (Successive Halving) 搜索、CTCE/CTDE
- **关键词**: reward engineering, governance kernels, sparse reward, PBRS, Hyperband, cooperative MARL

## TL;DR（一句话总结）
提出 GOV-REK 框架，在智能体与环境之间引入"治理层"，用基于状态/联合动作空间几何相似性的 governance kernels 动态分配附加奖励分布，并以 Hyperband 式迭代搜索自动找到问题无关的奖励模型，从而在稀疏奖励 MARL 中稳健地加速收敛。

## 问题与动机 (Problem & Motivation)
MARL 的奖励工程通常需投入大量针对特定问题的人工设计，且无法迁移到其他问题，当系统动态剧烈变化时这些努力被浪费；在稀疏奖励场景下问题更严重，因为解轨迹随规模指数爆炸而奖励信号稀疏。已有奖励塑形方法依赖领域知识或模仿学习，问题特定且不泛化，并易陷入"正奖励循环陷阱"。需要一种自动、问题无关、稳健的奖励信号定义方式。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 非对抗性。考察对环境配置随机化、解轨迹阻挡物 (blocker objects)、规模/复杂度增长以及合作贡献对称性变化的稳健性。不确定性以随机化环境配置建模。
- **设定**: cooperative；全可观下 CTCE、部分可观下 CTDE；online

## 方法 (Method)
1. **Governance kernels**: 定义类 Gaussian 的奖励分布核（如 squared exponential、periodic、linear；3D 用 ellipsoid/hyperboloid/diagonal 曲面核），仅依据状态或联合动作空间的几何相似性生成附加奖励 r'_i = r_i + g_{r,i}（agent-specific）或 R' = R + G_r（agent-agnostic）。
2. **PBRS 约束**: 对每个核的奖励归一化，保证满足 potential-based reward shaping 的策略不变性，避免改变最优策略。
3. **超叠加与变异**: 核可像 Gaussian kernel 一样叠加、旋转、变异，构造复杂奖励地形（叠加概率 s=0.5，变异概率 m=0.5）。
4. **GOV-REK 搜索**: 用重复的 Hyperband-like / Successive Halving 算法，以指数递增的训练预算 (factor η=3) 迭代搜索不同核配置，逐轮剪除表现差的配置，选出累计奖励高且平均 episode 长度短的核。
5. **decaying kernels**: 对已访问状态衰减奖励，鼓励更全局、多样的轨迹探索以应对规模扩展。

## 理论贡献 (Theoretical Contributions)
偏实证。理论层面主要论证 governance kernels 在归一化后满足 PBRS 的策略不变性充要条件，并引入"exploration expectation"假设 E_a[R(s,a,s')] → R'(s,s')。无收敛率/样本复杂度证明。

## 实验 (Experiments)
- **环境/Benchmark**: 2D-grid road 与 3D-grid drone 的稀疏 package delivery 协作任务（5×5、10×10、3×3、5×5 等规模）；N-player sequential social dilemma（16 智能体、16 步）。
- **Baselines**: 基线 PPO (Stable Baselines3 / RLlib)，对比 Multi-Objective Reward Shaping (MORS)；亦试 A2C。
- **评估指标**: 平均累计奖励、平均 episode 长度、收敛速度、随 blocker/规模/随机化变化的稳健性。

## 主要结果 (Key Results)
1. governed MARLS 比 MORS 收敛更快（尤其随机初始配置），且 episode 长度更短、不易陷入正奖励循环，更容错。
2. 对增加的 blocker 物体和随机化环境扰动表现稳健（奖励基本维持，但 episode 长度随扰动上升）。
3. decaying kernels 提升大规模 (10×10) 环境的可扩展性与收敛速度。
4. 在非空间 social dilemma 中（同质/异质、稀疏 payoff）治理智能体平均奖励更高，zero-mean 核效果尤佳。

## 局限与未来工作 (Limitations & Future Work)
基线 PPO 在大规模下无法持续满足 exploration expectation 假设，导致次优；核为简单几何形状限制了表达力与性能。未来拟结合 RND、NGU、Agent57 等好奇心/探索方法，并探索在刚性简单核与完全流动学习状态相似性之间折中的范式。

## 与综述的关联 (Relevance to Survey)
属于通过奖励塑形/课程式自动奖励设计提升 MARL 学习稳健性与可迁移性的工作线，强调对环境随机扰动与稀疏性的鲁棒收敛，而非对抗鲁棒。可作为"robustness via reward shaping / training-stability"分支的代表，与课程学习、治理式多智能体系统 (GMAS/NorMAS) 主题相关。
