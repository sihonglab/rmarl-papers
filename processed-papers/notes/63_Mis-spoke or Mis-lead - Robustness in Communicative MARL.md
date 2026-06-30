# 63. Mis-spoke or mis-lead: Achieving Robustness in Multi-Agent Communicative Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Mis-spoke or mis-lead: Achieving Robustness in Multi-Agent Communicative Reinforcement Learning
- **作者**: Wanqi Xue, Wei Qiu, Bo An, Zinovi Rabinovich, Svetlana Obraztsova, Chai Kiat Yeo
- **机构**: Nanyang Technological University (NTU), Singapore
- **发表**: AAMAS 2022
- **链接/arXiv**: arXiv:2108.03803v2

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信攻击（恶意/对抗消息）、对抗智能体、Byzantine 失效（不知道谁是恶意方）
- **方法范式**: 对抗训练、minimax / 两人零和博弈、博弈论均衡（PSRO/Double Oracle）、消息重构防御、异常检测
- **关键词**: multi-agent communication, adversarial messages, message filter, PSRO, Nash equilibrium, robustness

## TL;DR（一句话总结）
系统研究 MACRL 中的对抗通信问题：提出可学习的最优消息攻击方法、基于"异常检测+消息重构"的两阶段消息过滤防御，并将攻防建模为两人零和博弈用 PSRO 框架（ℜ-MACRL）求近似 Nash 均衡以提升最坏情况鲁棒性。

## 问题与动机 (Problem & Motivation)
MACRL 通过智能体间通信显著提升协调能力，但若某些智能体恶意发送被精心设计的消息，多智能体协调会迅速瓦解。已有工作要么只考虑随机噪声攻击（低效）、要么局限于特定竞争性博弈或特定 attention-based 通信方法，缺乏系统的攻击与有效防御研究，对协作场景（通信更关键）几乎未涉及。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 在 Dec-POMDP-Com 框架下，存在 N_adv 个恶意智能体，持有额外的对抗策略 ξ 生成对抗消息 δ_adv，通过凸组合或求和注入到原消息（m_adv = m_out + δ_adv）。黑盒攻击。两条假设：Byzantine 失效（不知谁恶意）、Concealment（恶意方互不通信，伪装成正常智能体）。攻击目标为最小化团队累计回报。
- **设定**: cooperative（显式通信，含 CD/LC/CC 三类）；CTDE；online

## 方法 (Method)
- 攻击：用 DNN f_μ 参数化高斯对抗策略 ξ，PPO 优化，目标为最小化团队回报，同时约束 m_out 与 m_adv 的距离（隐蔽性）。
- 防御（两阶段消息过滤器）：异常检测器 h_d 输出每条消息是否需重构的概率；消息重构器 g_r 对判定为恶意的消息进行恢复；用真实标签作正则引导，并以正常消息训练重构器为恒等映射以容忍检测误判。
- 鲁棒化（ℜ-MACRL）：将攻防建模为两人零和博弈 ⟨Π, U⟩，求解 MaxMin 目标逼近 Nash 均衡；基于 PSRO/Double Oracle 迭代维护策略种群，交替训练 best response 并扩展种群、求解 meta-game 混合策略。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（采用博弈论 NE 作为解概念并用 PSRO 近似，但无收敛/复杂度证明）

## 实验 (Experiments)
- **环境/Benchmark**: Predator Prey (PP)、Traffic Junction (TJ)、StarCraft II / SMAC（3bane_vs_hM、4bane_vs_hM、1o_2r_vs_4r、1o_3r_vs_4r）
- **Baselines**: 代表性 MACRL 方法 CommNet (CD)、TarMAC (LC)、NDQ (CC)；vanilla 单一防御器 vs. ℜ-MACRL
- **评估指标**: test return、test win/success rate、defender 期望效用 u_ζ

## 主要结果 (Key Results)
- 学习型攻击显著降低性能：CommNet 在 PP 上下降约 40%（p=0）/33%（p=-0.5），TarMAC、NDQ 同样明显下降，证明 SOTA MACRL 普遍脆弱（随机噪声则难以奏效）。
- 两阶段消息过滤器能恢复协调（如 NDQ 胜率回升至约 55-60%），但面对自适应攻击者会被利用、性能退化（CommNet 再降约 20-30%）。
- ℜ-MACRL 在所有算法与环境上期望效用一致优于 vanilla 防御，鲁棒性更强；可扩展到多攻击者场景。
- 消融：异常检测器与重构器缺一不可。

## 局限与未来工作 (Limitations & Future Work)
聚焦显式通信（隐式通信攻击易被察觉而被排除）；假设恶意方互不协作；PSRO 训练计算开销较大；缺乏理论保证。未来可扩展白盒攻击、协作型攻击者及理论分析（正文未详述）。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"通信鲁棒性 / 通信攻击与防御"主题线的早期系统性工作，结合了对抗训练与博弈论均衡（PSRO）两条方法线；与其他消息认证/信息瓶颈/消息过滤类工作（如本批次 64-68）密切相关，是该子领域的代表性基线。
