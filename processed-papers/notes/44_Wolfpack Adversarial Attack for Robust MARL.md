# 44. Wolfpack Adversarial Attack for Robust Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Wolfpack Adversarial Attack for Robust Multi-Agent Reinforcement Learning
- **作者**: Sunwoo Lee, Jaebak Hwang, Yonghyeon Jo, Seungyul Han
- **机构**: Graduate School of Artificial Intelligence, UNIST (Ulsan National Institute of Science and Technology), South Korea
- **发表**: ICML 2025 (PMLR 267)
- **链接/arXiv**: arXiv:2502.02844v3；代码 https://github.com/sunwoolee0504/WALL

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体 / 协同动作攻击（coordinated adversarial attack，针对多个 agent 的动作）
- **方法范式**: 对抗训练、attacker-defender、value-based CTDE、planner-based 关键时步选择（Transformer 预测 Q 值下降）
- **关键词**: cooperative MARL, coordinated adversarial attack, Wolfpack, CTDE, QMIX, robust policy

## TL;DR（一句话总结）
提出受狼群狩猎启发的 Wolfpack 对抗攻击——先攻击一个初始 agent，再攻击前来支援的"跟随" agent 组以瓦解协作；并提出 WALL 防御框架，通过在该协同攻击下做对抗训练，培养系统级协作以提升 MARL 鲁棒性。

## 问题与动机 (Problem & Motivation)
现有 MARL 对抗攻击/鲁棒方法大多每次只攻击单一 agent，忽视合作 MARL 中 agent 间的相互依赖，使得训练出的策略在多个 agent 被同时/协同攻击时脆弱。当初始 agent 被攻击后，其他 agent 会调整动作（治疗、护卫）来补救；若攻击者转而攻击这些"支援者"，则破坏力远超传统攻击，且现有鲁棒策略无法防御。需要新的协同攻击范式与相应防御。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 在 Limited Policy Adversary Dec-POMDP (LPA-Dec-POMDP) 框架下，攻击者 π_adv: S×A×N→A 在一回合内最多攻击 K 次，将选定 agent 的动作改为最小化 Q_tot 的动作。Wolfpack 攻击分初始攻击（随机选一 agent，时步 t_init）+ 跟随组攻击（随后 t_WP 步攻击响应 agent 组 N_follow-up）；总攻击步数 K = K_WP×(t_WP+1)，约束 m < (n−1)/2。
- **设定**: cooperative（Dec-POMDP）；value-based CTDE；online

## 方法 (Method)
1. **Wolfpack 攻击**: 初始攻击随机选一个 agent，将其动作改为 argmin Q_tot；后续步骤识别并攻击响应该初始攻击的"跟随" agent 组。
2. **Follow-up group selection**: 选取对初始攻击行为调整最大的 agent 作为跟随组目标，放大序列攻击的整体影响。
3. **Planner-based attacking step selector**: 用 Transformer 预测各时步攻击造成的未来 Q 值下降 ΔQ_WP，以更高概率在关键时步发起初始攻击，最大化破坏并提升鲁棒训练效果；并训练单独模型预测 ΔQ_WP 以降低评估时的规划开销。
4. **WALL 算法**: 在带 Wolfpack 攻击者的 LPA-Dec-POMDP 上做对抗 MARL 训练（适用于 QMIX/VDN/QPLEX 等 value-based CTDE），交替更新价值函数与 planning Transformer，培养系统级协作而非依赖特定 agent 子集。

## 理论贡献 (Theoretical Contributions)
偏实证为主；沿用 LPA-Dec-POMDP 可化为由 π_adv 诱导的另一 Dec-POMDP、最优策略收敛性（Yuan et al. 2023）的结果，本文未给出新的收敛性证明。

## 实验 (Experiments)
- **环境/Benchmark**: MPE Predator-Prey（PP 3/1、PP 6/2、PP 9/3）与 SMAC（2s3z、3m、3s_vs_3z、8m、MMM、1c3s5z）
- **Baselines**: 攻击方面与 Natural/Random Attack 等对比；鲁棒方法与 Vanilla QMIX、RANDOM、ROMANCE 对比；CTDE 主用 QMIX，附录含 VDN/QPLEX
- **评估指标**: 各场景平均回报/分数（5 个随机种子的均值±标准差）；攻击严重性、关键时步选择有效性的消融

## 主要结果 (Key Results)
1. Wolfpack 协同攻击对传统鲁棒 MARL 策略破坏性显著强于现有单 agent 攻击。
2. WALL 在 Natural、Random Attack 等多种场景下回报均优于 Vanilla QMIX、RANDOM、ROMANCE（如 PP 9/3 Natural 802.5 vs Vanilla 661.9）。
3. Planner（Transformer 预测 ΔQ_WP）选择关键时步攻击优于随机步选择，消融验证各组件有效。

## 局限与未来工作 (Limitations & Future Work)
攻击/防御依赖访问 Q_tot 与全局信息（白盒式）；planner 需额外训练 Transformer 增加复杂度；超参（m、K_WP、t_WP）需搜索；主要在 MPE/SMAC 验证。未来可扩展到观测/通信等其他攻击面与更大规模系统。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中"对抗智能体 / 动作攻击 + 对抗训练防御"主线，强调合作 MARL 中协同（多 agent）攻击这一被忽视的威胁面；与 ROMANCE、LPA-Dec-POMDP、value-decomposition 攻击（Phan et al.）、critical-agent/critical-step 选择等工作直接相关。
