# 32. Enhancing the Robustness of QMIX against State-adversarial Attacks

## 元信息 (Metadata)
- **标题**: Enhancing the Robustness of QMIX against State-adversarial Attacks
- **作者**: Weiran Guo, Guanjun Liu, Ziyuan Zhou, Ling Wang, Jiacun Wang
- **机构**: Tongji University（同济大学，计算机/交通工程）；Monmouth University（USA）
- **发表**: 未明确（arXiv:2307.00907，2023-07-03；推测会议论文）
- **链接/arXiv**: arXiv:2307.00907v1

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测对抗扰动（state-adversarial attacks on observations）
- **方法范式**: 对抗训练、SARL 鲁棒方法向 MARL 的迁移（gradient-based、policy regularization、ATLA、PA-AD）、minimax、价值分解（QMIX）
- **关键词**: multi-agent reinforcement learning, robustness, state-adversarial attacks, QMIX, adversarial training

## TL;DR（一句话总结）
以 QMIX 为例，将单智能体 RL 的四种鲁棒训练技术（gradient-based adversary、policy regularization、ATLA、PA-AD）迁移到合作 MARL 场景，并在 SMAC 上交叉攻击对比四种方法的优缺点。

## 问题与动机 (Problem & Motivation)
DRL 易受状态对抗攻击（不改变环境只扰动观测）。已有大量单智能体（SARL）鲁棒方法，但 MARL 鲁棒性研究较少；而多智能体场景普遍且更难，单个智能体被攻击会拖累整个系统总回报。需要将 SARL 的鲁棒训练技术系统性地迁移并比较到 c-MARL。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 状态对抗 Dec-POMDP（含对抗状态集 Bi，M 个被攻击智能体）；扰动作用于观测 o→õ，受 l∞ 预算 ε 约束；实验取最极端 dense attack（M=N，每个时间步攻击所有智能体）。
- **设定**: cooperative；CTDE（QMIX 价值分解）；online。目标为 max_{π} min_{õ} 形式的 max-min。

## 方法 (Method)
- 基于 QMIX 单调性约束推导被攻击单智能体的 max-min 目标，并定义攻击策略目标（最小化折扣总回报）。
- Gradient-based adversary：用 FGSM 生成最大范数扰动 δ=ε·sign(∇L)，以交叉熵损失推动动作偏离最优动作。
- Policy Regularization：加 hinge 型正则项 Lreg（约束扰动后最优动作不变，用 total variation 距离衡量动作分布差异），Ltot=L+κ·Lreg。
- ATLA in MARL：训练一个对手网络（用 MAPPO）输出最优状态扰动，奖励为受害者回报的相反数，与 QMIX 交替（cross-train）训练。
- PA-AD in MARL：用 director（指出最优扰动方向，用 RL 求解）+ actor（沿该方向用 FGSM 生成攻击）分解，缩小动作空间、简化训练。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（引用已有结论：最优联合对抗扰动存在且唯一、价值函数扰动可被动作分布差异界定；本文主要是方法迁移与实证比较）。

## 实验 (Experiments)
- **环境/Benchmark**: SMAC 四张地图（2m vs 1z、3m、3s vs 3z、2s3z）。
- **Baselines**: Vanilla QMIX，以及用 FGSM / Policy Regularization / ATLA / PA-AD 训练的鲁棒 QMIX；测试期用 FGSM/ATLA/PA-AD 交叉攻击。
- **评估指标**: 胜率（Win rate）与回报（Reward），每轮测试 32 次。

## 主要结果 (Key Results)
- Vanilla QMIX 在各种攻击下几乎全面失败（胜率降至 0）。
- FGSM 训练简单有效，但提供的攻击不够强，对更强攻击（如最优对手）鲁棒性不足。
- Policy Regularization 在更强干扰（最优对手）下表现差，且在 clean 状态下不稳定（如 3m 地图 No Attack 胜率仅 0.34）。
- ATLA 在 MARL 中因需为多个智能体生成大量扰动，状态/动作空间倍增，出现梯度爆炸，效果很差。
- PA-AD 通过分解扰动方向缩小动作空间，整体最稳健（多地图各攻击下仍保持高胜率/回报），是四者中综合最优。

## 局限与未来工作 (Limitations & Future Work)
ATLA 在 MARL 中训练困难（梯度爆炸、空间爆炸）；Policy Regularization clean 性能不稳；仅在 QMIX 与 SMAC 上验证。未来优化对抗网络、探索兼顾高效与效果的鲁棒训练，并推广到 QMIX 之外的 MARL 算法。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"状态/观测对抗 + 对抗训练"主线，主要价值是把 SARL 的四类代表性鲁棒方法系统迁移到 c-MARL 并实证比较，为综述中"SARL→MARL 方法迁移"与"价值分解算法（QMIX）鲁棒化"提供基准对照；与 ATLA、PA-AD、RMA3C、RoMFAC 等工作直接相关。
