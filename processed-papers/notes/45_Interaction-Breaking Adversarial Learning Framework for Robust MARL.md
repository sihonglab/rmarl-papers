# 45. Interaction-Breaking Adversarial Learning Framework for Robust Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Interaction-Breaking Adversarial Learning Framework for Robust Multi-Agent Reinforcement Learning
- **作者**: Sunwoo Lee, Mingu Kang, Yonghyeon Jo, Seungyul Han
- **机构**: Graduate School of Artificial Intelligence, UNIST (Ulsan National Institute of Science and Technology), South Korea
- **发表**: ICML (PMLR) 2026
- **链接/arXiv**: arXiv:2605.18024v2; https://sunwoolee0504.github.io/IBAL

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动 + 动作扰动（联合攻击）；尤其针对 inter-agent interaction structure 的破坏；并覆盖 agent-missing / 智能体失效等非参数扰动
- **方法范式**: 对抗训练；information-theoretic（mutual information）攻击设计；CTDE（QMIX 主干）；JA-Dec-POMDP 形式化
- **关键词**: interaction breaking, mutual information, robust MARL, adversarial training, CTDE, coordination

## TL;DR（一句话总结）
提出 IBAL 框架：用互信息（MI）量化跨组（cross-group）影响，构造同时遮挡观测和扰动动作的"打断交互"攻击，并据此对抗训练，使协作策略在交互结构被破坏（甚至队友缺失）时仍保持鲁棒。

## 问题与动机 (Problem & Motivation)
CTDE 下的协作 MARL 依赖 inter-agent 协调，但学到的协调在外部扰动下脆弱。已有 robust MARL 多采用 value-oriented（价值最小化）攻击或简单扰动，未显式建模"智能体如何相互影响"，因此无法捕捉对交互结构本身的破坏。当协调部分崩塌时性能会急剧下降，在紧耦合协作任务中尤为严重。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 将智能体分为两组 G1、G2，用 conditional MI 度量跨组影响。观测攻击 f_adv 对 G1 观测中关于 G2 信息量最大的 L 个维度做 zero-masking（基于 data-processing inequality 与 dimension-wise MI 上界，用 CLUB 估计）；动作攻击 π_adv 以概率 P_act 选择最小化 action-level MI 的动作（KL 估计 group-wise MI）。攻击者目标是最小化跨组互信息而非价值。
- **设定**: cooperative；CTDE（主用 QMIX，也验证 MAPPO）；online

## 方法 (Method)
1. 形式化 Joint-Adversarial Dec-POMDP (JA-Dec-POMDP)，攻击者同时扰动观测与动作；证明其价值等价于具有扰动动态的诱导 Dec-POMDP（Theorem 4.2），从而可用标准 MARL 算法在诱导环境中优化得到鲁棒策略。
2. 用 MI 链式法则把跨组影响拆为 observation-level MI 与 action-level MI 两项，分别由观测攻击与动作攻击最小化。
3. Observation attacker：选择 dimension-wise MI 最大的 L 个维度做零遮挡（precompute 一次即可在分组变化时聚合，降低开销）。
4. Action attacker：以 P_act 概率把 G1 动作替换为最小化 action-level MI 的动作。
5. 实现：每 episode 随机采样分组（K≤n/2），观测攻击对称遮挡两组，动作攻击概率用 adaptive schedule（依据成功率/回报逐步增强）。

## 理论贡献 (Theoretical Contributions)
- Theorem 4.2：JA-Dec-POMDP 价值等价于带扰动动态的诱导 Dec-POMDP，使在诱导环境训练得到的策略可保持鲁棒。
- Lemma 4.3：group-wise observation-level MI 可由 dimension-wise MI 之和加群冗余项上界，且冗余项可忽略，支撑高效遮挡选择。

## 实验 (Experiments)
- **环境/Benchmark**: SMAC（3m, 3s_vs_3z, 2s3z, 8m, 1c3s5z, MMM）、Level-Based Foraging (LBF)、SMACv2
- **Baselines**: 攻击端 Natural/Random/FGSM/EGA/Wolfpack 及本文攻击；防御端 Vanilla QMIX、Rand-Obs、Rand-Act、FGSM、ATLA、ERNIE、ROMANCE、WALL
- **评估指标**: test win rate（5 seeds 均值±std）

## 主要结果 (Key Results)
1. 在多种对抗攻击下 IBAL 一致优于已有 robust MARL 方法；FGSM/WALL 等只对自身攻击有效，在 interaction-breaking 攻击下急剧下降。
2. 非参数扰动（Dis-ℓ 禁用队友、HP-h 降低初始血量）下 IBAL 优势明显，多数基线在队友缺失时崩塌，IBAL 因训练时见过多样分组而保持自适应协调。
3. 在 LBF、SMACv2 及 MAPPO 主干上均有效（不依赖 value 信息或 IGM 性质）；消融显示观测攻击、动作攻击、MI 引导遮挡与自适应概率均有贡献，zero-masking 优于 Gaussian/FGSM 变体。

## 局限与未来工作 (Limitations & Future Work)
引入额外超参数（最大组大小 K、遮挡预算 L），需调参；MI 估计带来额外计算开销（作者称中等可接受）。未来可扩展到更广泛 CTDE 算法与更复杂场景。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"对抗训练 + 观测/动作攻击"主线，但创新点在于用 information-theoretic（MI）视角攻击 inter-agent 交互结构，区别于主流 value-minimizing 攻击；同时通过 agent-missing 实验连接到智能体失效/容错主题，可作为攻击设计与协调鲁棒性的代表性工作。
