# 24. Robust Multi-Agent Reinforcement Learning Driven by Correlated Equilibrium

## 元信息 (Metadata)
- **标题**: Robust Multi-Agent Reinforcement Learning Driven by Correlated Equilibrium
- **作者**: 未明确（匿名，双盲评审）
- **机构**: 未明确（匿名投稿）
- **发表**: ICLR 2021（Under review，conference paper under double-blind review）
- **链接/arXiv**: 未明确

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 队内智能体失误 / 对抗智能体（一个 agent 偶尔犯错或对抗性行为，machine malfunctioning），属于内部 agent 失效 / adversarial agent
- **方法范式**: 博弈论均衡（correlated equilibrium vs decentralized equilibrium）、team mini-max stochastic game、对抗训练 (adversarial training)、global latent variable + 互信息 (mutual information, InfoGAN 思想)、价值分解 (QMIX)
- **关键词**: cooperative MARL, robustness, correlated equilibrium, mutual information, global random variable, QMIX, team mini-max game

## TL;DR（一句话总结）
指出在含对抗/失误 agent 的协作 MARL 中，CTDE 得到的 decentralized equilibrium 可能远差于 correlated equilibrium，因此提出用全局随机变量 + 互信息正则鼓励非对抗 agent 学习 correlated equilibrium，从而在保留 CTDE 便利性的同时显著提升鲁棒性。

## 问题与动机 (Problem & Motivation)
协作 MARL (CMARL) 要部署到真实世界必须鲁棒：若个别 agent 犯错或对抗，整队可能严重失败。现有 robust MARL 多用 vanilla 对抗训练且遵循 CTDE。但作者发现：当环境含对抗 agent 时（不再 fully cooperative），CTDE 得到的 decentralized equilibrium 性能可能远逊于 correlated equilibrium。已有 team mini-max 博弈理论显示二者差距可观，本文将其推广到 stochastic game。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: worst-case mini-max——某个（或任意）agent 以概率 ε 执行"错误/最差"动作（QMIX 中即 arg min Qi），约束 D(πi,mis||πi) ≤ ε（错误不能太大）。考虑两种设定：固定一个 agent 犯错；所有 agent 随机犯错（每步至多一个）。失误既可对抗性（worst action）也可随机。
- **设定**: cooperative（含对抗/失误 agent 使其变为 team mini-max）；CTDE（但执行时需引入 correlation）；online；基于 QMIX 实现，SMAC 部分可观

## 方法 (Method)
- 理论上将 robust CMARL 形式化为 team mini-max stochastic game，证明 decentralized equilibrium 可任意差于 correlated equilibrium，从而 robust MARL 需要 correlated equilibrium。
- 提出用跨 agent 共享的全局随机变量 z（额外输入 Q 网络：Qi(oi, z, ai)），让 agent 据 z 值协调出 correlated policy，同时只需共享随机数生成器与种子即可保持 CTDE 的去中心化执行。
- 为避免 agent 忽略 z，最大化 z 与动作的（条件）互信息 I(z; a|o)，用变分下界（类 InfoGAN）近似，总损失 Ltot = LRL + λI·LI。
- 在 QMIX 上实现：训练与评估时注入失误动作（Eq.2），把 mini-max 弱化为"以 ε 概率执行最差动作"的可解形式。

## 理论贡献 (Theoretical Contributions)
- **Proposition 1**: 存在 stochastic game 使 Ecor/Edec > m^{n-2}（≥ m^{2n-4}(1-γ)^2），即 correlated 与 decentralized equilibrium 差距在 stochastic game 中比 normal form game 更大。
- **Proposition 2**: 对任意固定 k，存在 stochastic game 使 Ecor/Edec ≥ O(m^{k(n-2)})，差距可任意大。
- **Proposition 3**: 全可观有限离散动作环境中，给所有 agent 一个全局连续随机变量 z，存在确定性策略 µi(s,z) 等价于团队最优 correlated（随机）策略。

## 实验 (Experiments)
- **环境/Benchmark**: SMAC（StarCraft Multi-Agent Challenge），4 张地图 8m、2s3z、3m、3s5z
- **Baselines**: NP（正常策略测对抗）、VA（vanilla 对抗训练）、GV（对抗训练+全局变量无 MI）、GM（对抗训练+全局变量+互信息）；附加 NG（正常训练+全局变量+MI）
- **评估指标**: 测试胜率（不同对抗率/随机率下，1000 episode），5 次运行的 25%/75% 误差棒

## 主要结果 (Key Results)
- GM（全局变量+互信息）在大多数地图/agent 设定下胜率优于 VA 与 GV；GV 仅有时优于 VA（无 MI 时 agent 易忽略 z）。
- 对抗测试（如 2s3z Agent2 50% 对抗率）GM 达 90.5% vs VA 78.5%；3s5z Agent3 GM 73.5% vs VA 45.7%。
- NG/NP 的提升普遍小于 GM/VA，佐证"correlation 在 robust 设定下比在正常设定下更重要"。
- 随机失误测试中 GM 也略优。

## 局限与未来工作 (Limitations & Future Work)
- 鲁棒策略有时会轻微降低非鲁棒性能，需平衡 performance 与 robustness。
- 仅解了弱化的 worst-case mini-max（ε 概率最差动作），能否解真正对抗的 Eq.(1) 待研究。
- 仅考虑单 agent 犯错，未来可考虑所有 agent 都可能犯错。
- 仅用最直接的 correlation 方法，更复杂的 correlation 是否更优仍开放。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"对抗/失效智能体 + 博弈论均衡 (correlated equilibrium / team mini-max)"线路的代表性理论+实证工作，强调执行阶段 correlation 对鲁棒性的必要性，与 M3DDPG (minimax MADDPG)、Lin et al. 的 CMARL 鲁棒性、价值分解 (QMIX) 鲁棒化等主题密切相关；为综述提供"均衡概念选择影响鲁棒性"的独特视角。
