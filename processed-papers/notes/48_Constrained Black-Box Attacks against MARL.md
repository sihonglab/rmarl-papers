# 48. Constrained Black-Box Attacks Against Cooperative Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Constrained Black-Box Attacks Against Cooperative Multi-Agent Reinforcement Learning
- **作者**: Amine Andam, Jamal Bentahar, Mustapha Hedabou
- **机构**: Mohammed VI Polytechnic University；Khalifa University；Concordia University
- **发表**: 未明确（arXiv preprint）2026
- **链接/arXiv**: arXiv:2508.09275v2

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动（test-time、black-box 观测攻击）；攻击协作所需的"perception alignment"
- **方法范式**: 对抗攻击（攻击侧）；misalignment 度量 + PGD；structured perturbation（Hadamard 正交矩阵）；critical-agent 识别
- **关键词**: black-box attack, test-time attack, c-MARL, observation perturbation, misalignment, Hadamard matrix, sample efficiency

## TL;DR（一句话总结）
提出在极受限 black-box 测试时威胁模型下攻击协作 MARL：核心思想是制造 agent 间感知"misalignment"，给出 Align attack（仅用 1000 条观测训练对齐网络再 PGD 扰动）、无任何访问权限的 Hadamard free attack（正交结构扰动）以及结合二者的 targeted attack。

## 问题与动机 (Problem & Motivation)
c-MARL 在敏感领域部署前需理解其对抗脆弱性。已有工作多为训练时攻击或不现实的白盒/代理策略（需要 policy 权重、动作、训练环境或查询能力）。本文研究更现实、更弱访问的威胁模型：攻击者只能收集并扰动已部署 agent 的观测（甚至完全无访问权），探索这种条件下能否有效破坏系统。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: test-time、black-box；不能控制动作，只能给观测加 ε-bounded ℓ∞ 扰动。两类设定：(1) 仅能收集观测（无动作/权重）；(2) free attack——完全无访问，只能盲扰动。SMAC 中 agent 会死亡导致动态/部分访问。
- **设定**: cooperative；decentralized execution / 部署阶段（attacker 视角）；主要针对 partially observable 任务

## 方法 (Method)
1. 直觉：协作依赖 agent 对环境的对齐感知（如 focus fire 选最弱敌人）；制造 misalignment 即可瓦解协调（divide-and-conquer）。
2. Align attack：用收集的对齐观测训练网络 f_θ 使 f_θ(o_-i)≈o_i（MSE），高损失对应 misalignment；通过 PGD 最大化 J(o+δ) 生成扰动（同时加在输入和输出上）。仅需约 1000 样本，无需 policy。
3. Targeted Align：选取观测最互相对齐（最可能协作）的 m 个 agent 子集攻击，提升效率与隐蔽性。
4. Free Hadamard attack：无访问下用 partial Hadamard 矩阵 δ=ε×H̃ 生成满足"行正交 + 预算约束"的结构化扰动，使各 agent 被推往正交方向；用 Sylvester 构造，padding 处理维度。
5. Targeted Hadamard：用观测识别关键 agent + Hadamard 快速生成，轻量高效。

## 理论贡献 (Theoretical Contributions)
偏方法/实证；理论支撑主要是用正交（Hadamard）矩阵满足正交性与预算约束以诱导 misalignment 的构造性论证，无收敛性/复杂度证明。

## 实验 (Experiments)
- **环境/Benchmark**: Level-Based Foraging (LBF, 10 个环境，含全可观/高协作/部分可观)、Multi-Robot Warehouse (RWARE, 三种部分可观度、高维观测 71–351)、SMAC（大规模、动态访问）；共 3 benchmark、22 个环境
- **Baselines**: 随机噪声注入（free attack 主流做法）；与白盒/代理策略方法对比访问假设
- **评估指标**: IQM Return（团队回报）；样本效率

## 主要结果 (Key Results)
1. 仅 1000 条收集样本即可显著破坏 c-MARL，相比此前方法所需的百万级样本大幅提升样本效率。
2. Misalignment 原则在全可观、部分可观、高协作多种设定下均有效，跨多种算法与 22 个环境验证。
3. 完全无访问的 Hadamard free attack 优于随机噪声；targeted 版本兼顾 Align 的关键 agent 识别与 Hadamard 的快速生成，轻量高效。

## 局限与未来工作 (Limitations & Future Work)
攻击依赖 misalignment 假设（高度协作/感知重叠时更有效）；Hadamard 仅在特定维度存在需 padding；正文未深入防御方法；动态访问（agent 死亡）下的覆盖有限。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 攻击侧、强调威胁模型现实性（black-box、最弱访问、test-time），用信息对齐视角而非 value/policy 梯度发起攻击，并显著降低样本需求，可作为评估 c-MARL 部署期观测鲁棒性的强现实威胁基准。
