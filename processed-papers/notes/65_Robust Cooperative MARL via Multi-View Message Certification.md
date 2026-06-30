# 65. Robust Multi-Agent Communication via Multi-View Message Certification (CroMAC)

## 元信息 (Metadata)
- **标题**: Robust Multi-Agent Communication via Multi-View Message Certification
- **作者**: Lei Yuan, Tao Jiang, Lihe Li, Feng Chen, Zongzhang Zhang, Yang Yu（通讯 Yang Yu）
- **机构**: National Key Laboratory for Novel Software Technology, Nanjing University；Polixir.ai
- **发表**: 未明确（arXiv preprint，A PREPRINT）
- **链接/arXiv**: arXiv:2305.13936v1 [cs.MA]

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 通信攻击 / 消息扰动（message perturbation，所有消息通道在任意时刻都可能被 ℓ∞-norm 有界扰动/攻击）
- **方法范式**: 认证鲁棒（certified robustness，guaranteed lower bounds + interval bound propagation）；multi-view / multi-modal 表示学习；MVAE（multi-view VAE + product-of-experts）；潜空间扰动；价值分解（QMIX）整合；CTDE
- **关键词**: robust communication, certified robustness, multi-view VAE, product-of-experts, message perturbation, cooperative MARL

## TL;DR（一句话总结）
提出 CroMAC：把多智能体通信建模为 multi-view 问题（每条收到的消息是状态的一个视图），用带 product-of-experts 推断网络的 MVAE 提取带认证保证的联合消息表示，并在状态潜空间施加扰动得到认证的状态表示，使训练出的智能体在最坏情况消息扰动下仍能获得 state-action value 的有保证下界并选择最优鲁棒动作。

## 问题与动机 (Problem & Motivation)
合作 MARL 需通信促进协调，但 DNN 脆弱、CMARL 在状态/动作/奖励/通信扰动下鲁棒性低。通信策略的鲁棒性尤其复杂（何时对哪些消息通道施加何种扰动）。已有鲁棒通信工作或研究对抗通信涌现、或假设受扰动的消息通道数量有限（如不超过半数 agent 受攻击，如 AME），这些约束限制了复杂场景下的鲁棒性完整性、远离真实条件（现实中所有通道都可能被扰动），且缺乏每个 agent 收到消息与决策之间的形式化鲁棒保证/认证。本文目标：在每个消息通道任意时刻都可能被扰动的设定下获得带认证的鲁棒通信策略。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: N-agent 系统中每个 agent 收到 N-1 条消息，所有消息通道在任意时刻都可能遭受 ℓ∞-norm（实验聚焦 p=∞）有界预算 ϵ 的扰动/攻击（含 Random、PGD、FGSM 等）；不限制受扰动通道数量。
- **设定**: cooperative（CMARL）；CTDE；online；基于 QMIX/价值分解

## 方法 (Method)
- 将消息接收过程建模为 multi-view（multi-modal）问题，每条消息是状态的一个视图；用 MVAE + product-of-experts 推断网络从各收到消息聚合出联合消息表示。
- 通过 interval bound propagation 推导联合消息表示（及单消息表示的均值/方差）在 ℓ∞ 攻击预算 ϵ 下的上下界，建立联合消息表示与每条消息间的认证关系（POE 对应 Harmonic Mean，借其性质推断上下界）。
- 优化阶段：先把状态编码进潜空间，在该潜空间做扰动以获得潜变量与 agent Q-value 之间的认证关系（认证状态表示）；再训练消息表示去逼近认证的潜变量，从而隐式保证每条消息与 Q-value 间的认证。
- 直接在潜空间施加扰动，避免为辅助对手设计具体动作空间（绕开 adversary 动作空间随 agent 数膨胀的问题）。

## 理论贡献 (Theoretical Contributions)
偏认证鲁棒（提供 state-action value 的 guaranteed lower bounds 与基于 interval bound propagation 的认证保证；给出 POE/Harmonic Mean 下消息表示上下界的推导与证明），但非收敛/样本复杂度类理论。

## 实验 (Experiments)
- **环境/Benchmark**: Hallway（4x5x6、3x3x4x4 等）、Level-Based Foraging (LBF，改为仅一个 agent 可观测地图)、Traffic Junction (TJ，slow/fast)、SMAC 两张图（1o2r_vs_4r、1o10b_vs_1r）；基于 QMIX/PyMARL2 实现
- **Baselines**: QMIX（无通信）、AME（假设少于半数 agent 受扰动的 ensemble 防御）、Full-Comm（无扰动全通信，性能上界）、REC；消融 CroMAC w/o robust、CroMAC w/o adv
- **评估指标**: average test win rate（1000 测试 episode × 5 随机种子），在 Natural、Random、PGD、不同预算 FGSM 等多种扰动下；可视化（PCA 投影、Q-value 上下界）

## 主要结果 (Key Results)
- 无扰动时 CroMAC（w/o adv）协调能力可比 Full-Comm，说明其特殊设计不显著损失性能；QMIX（无通信）在所有环境最差，证明通信必要。
- 在多种消息扰动（Random/PGD/FGSM 多预算）下，CroMAC 总体优于 AME，尤其在更强攻击（如 FGSM 大预算、TJ、SMAC 1o10b_vs_1r）下鲁棒性优势明显，且不受"受扰动通道数量"假设限制。
- 可视化显示：无鲁棒机制的消息表示在扰动下会越出认证上下界导致错误决策，而 CroMAC 的消息表示与 Q-value 保持在认证界内，从机制上解释其鲁棒性；方法对不同 baseline/条件有较强通用性。

## 局限与未来工作 (Limitations & Future Work)
- 训练阶段攻击次数固定（虽测试时可泛化到不同预算/攻击方法）。
- 在线学习通信策略；如何在 offline MARL 中学到鲁棒通信策略是有价值的开放挑战。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"通信鲁棒性 / 认证鲁棒（certified robustness）"线，针对消息扰动/通信攻击，方法上承接单智能体认证鲁棒（CARRL、CROP）与 multi-view/VAE 表示学习，放宽了"受扰动通道数量有限"的假设。可与 AME（#56?/通信防御）、ADMAC（#60）、certifiably robust communication（#61）、certified policy smoothing（#62）、GIB 鲁棒通信（#64）、#63 等通信鲁棒工作对照；与同组 ROMANCE（#57）同属南大 LAMDA 的鲁棒 CMARL 系列，是认证型鲁棒通信的代表。
