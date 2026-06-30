# 99. Towards Comprehensive Testing on the Robustness of Cooperative Multi-agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Towards Comprehensive Testing on the Robustness of Cooperative Multi-agent Reinforcement Learning
- **作者**: Jun Guo, Yonghong Chen, Yihang Hao, Zixin Yin, Yin Yu, Simin Li
- **机构**: Beihang University (State Key Lab of Software Development Environment); Yangzhou Collaborative Innovation Research Institute; No. 38 Research Institute of CETC
- **发表**: CVPR 2022 Workshops（IEEE/CVF）；arXiv:2204.07932
- **链接/arXiv**: arXiv:2204.07932

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动、动作扰动（adversarial policy / "traitor"）、奖励投毒（reward poisoning / flipping）——多方面综合
- **方法范式**: 鲁棒性测试框架；对抗攻击（FGSM 状态攻击、reward sign-flip、adversarial policy 动作攻击）；MMDP 建模
- **关键词**: c-MARL, Robustness Testing, Adversarial Attack, Reward Poisoning, Adversarial Policy, MARLSafe

## TL;DR（一句话总结）
提出 MARLSafe——首个从 state、action、reward 三个方面综合测试合作 MARL（c-MARL）鲁棒性的框架，并为各方面设计对抗攻击作为测试算法，在 SMAC 上揭示 SOTA c-MARL（QMIX、MAPPO）在所有方面均鲁棒性低下（可被降至接近 0% 胜率）。

## 问题与动机 (Problem & Motivation)
c-MARL 应用于交通、电力、UAV 等安全攸关场景，但其策略易被对抗样本扰动。现有针对 MARL 的攻击/测试只关注单一方面（state、action 或 reward），而 c-MARL 模型可能在某一方面鲁棒却被攻击者从其他方面攻破——一个真正鲁棒的算法必须同时在所有方面鲁棒。此前无工作从多方面综合测试 c-MARL 鲁棒性（state 攻击方面也仅 Lin et al. 一篇）。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 基于 MMDP (S, {A_i}, R, P, γ)，引入 adversary ν(·)∈B(·) 扰动 state / action / reward 三类元素，目标最小化折扣回报 G，扰动预算受限。State 攻击为测试时白盒/黑盒；reward 攻击为训练时投毒；action 攻击通过控制一个 agent 作为 traitor。
- **设定**: cooperative；CTDE（QMIX、MAPPO）；同时覆盖 training-time（reward）与 test-time（state/action）攻击；白盒（state）与黑盒（action）

## 方法 (Method)
- State Test：对 agent 观测施加 FGSM 非定向攻击 ν(s)=s−ε·sign(∇Q_s(s,a*;π))，抑制最优动作 logits，诱使选择次优动作（ε=0.05, ℓ∞）。
- Reward Test：训练时翻转每个 episode 中最大 k%（实验 10%）奖励的符号（ν(r)=−r if r>r_thresh），毒化奖励使策略学坏。
- Action Test：把一个 agent 作为 "traitor"，固定其余 agent 策略，用 DRQN 训练 traitor 以最大化“反向团队奖励”（同盟受伤/死亡得正奖励、敌人受伤/胜利得负奖励），借鉴 adversarial policy 但适配合作设定（traitor 无全局状态/他人观测访问）。
- 三类攻击共同覆盖 MMDP 元素、训练/测试时、白盒/黑盒，构成综合测试框架。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证。将已有攻击统一形式化到 MMDP 框架并按 state/reward/action 元素分类，但无收敛性/复杂度等理论结果。

## 实验 (Experiments)
- **环境/Benchmark**: SMAC（StarCraft II Multi-Agent Challenge），EPyMARL 框架；地图 2s3z 与 11m（由 10m_vs_11m 改造以平衡双方单位）。
- **Baselines**: 被测算法为 QMIX（value-based）与 MAPPO（policy-based）；与无攻击基线对比（二者无攻击时胜率 100%）。
- **评估指标**: 胜率（WR）、团队奖励（TR）、平均阵亡盟友数（mDA）、平均击杀敌人数（mDE）；每实验 32 episode。

## 主要结果 (Key Results)
- State Test：QMIX 胜率从 100% 降至 9.38%（2s3z）/0%（11m），MAPPO 降至 65.62%/31.25%；MAPPO 比 QMIX 更鲁棒，推测集中式训练网络（mixer / critic）在鲁棒性中起重要作用（二者去中心化网络结构相同）。
- Reward Test：仅翻转 10% 奖励即可使 QMIX、MAPPO 胜率全降至 0%；智能体学会“逃跑”行为（避免被杀但也不击杀敌人），表明 reward 维度鲁棒性常被忽视却极脆弱。
- Action Test：单个 traitor 即可使两算法胜率降至 0%（QMIX 在 11m 偶有 6.25%）；即使盟友数量占优（10 打 11 本可近 100% 取胜）加入 traitor 后表现大幅恶化。
- 行为分析：state 攻击下 agent 表面正常但失去协作；reward 攻击下集体逃跑；action 攻击下 traitor 先躲后影响队友并最终送死。结论：c-MARL 面临严重鲁棒性问题，需联合覆盖 state/action/reward 的综合防御。

## 局限与未来工作 (Limitations & Future Work)
仅在 SMAC 两张地图、两种 CTDE 算法上验证；攻击方法各方面相对基础（FGSM、固定比例 sign-flip、单 traitor）。未来需探索同时覆盖 state、action、reward 三方面的综合防御方法以提升 c-MARL 鲁棒性。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 的“鲁棒性测试/对抗攻击 benchmark”主题线，是被广泛引用的早期综合测试框架（MARLSafe），首次将 state/action/reward 三类威胁统一评估。可作为综述中威胁建模分类（按 MMDP 元素）、reward poisoning 与 adversarial policy（traitor）攻击的代表性参考，与 RTCA（critical agent state perturbation）、state-uncertainty robust MARL 等工作互补。
