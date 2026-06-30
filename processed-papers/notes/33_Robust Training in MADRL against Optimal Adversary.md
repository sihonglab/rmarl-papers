# 33. Robust Training in Multiagent Deep Reinforcement Learning Against Optimal Adversary

## 元信息 (Metadata)
- **标题**: Robust Training in Multiagent Deep Reinforcement Learning Against Optimal Adversary
- **作者**: Weiran Guo, Guanjun Liu, Ziyuan Zhou, Jiacun Wang, Ying Tang, Miaomiao Wang
- **机构**: Tongji University（同济大学）；Monmouth University；Rowan University；Beijing Institute of Control Engineering（北京控制工程研究所）
- **发表**: IEEE Transactions on Systems, Man, and Cybernetics: Systems, Vol.55 No.7, July 2025
- **链接/arXiv**: DOI 10.1109/TSMC.2025.3561276

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测对抗攻击（state-adversarial attacks on observations）
- **方法范式**: 对抗训练、minimax（max-min worst-case return）、state-attack↔policy-attack 等价、actor-director（PA-AD 训练期化）、价值分解（QMIX/VDN）+ SEAC
- **关键词**: Industry 5.0, multi-agent RL, robustness, state-adversarial attack, optimal adversary, MAPDA

## TL;DR（一句话总结）
将测试期的 PA-AD 攻击思想搬到训练期，提出 PA-Dec-POMDP 建模与 MAPDA（multiagent policy-directed adversary）攻击框架，通过求解最优策略对手并与受害者交替训练，提升 QMIX/VDN/SEAC 在状态对抗攻击下的鲁棒性（面向 Industry 5.0）。

## 问题与动机 (Problem & Motivation)
MADRL 对观测的微小变化（传感器噪声、恶意攻击）极敏感，sim-to-real gap 严重影响 Industry 5.0 中的协作机器人/自动驾驶/无人机集群。SADRL 鲁棒方法不能直接照搬到 MADRL（状态动作空间更大、易梯度爆炸；智能体相互关联）。现有 MADRL 鲁棒方法或对手空间过大、或缺最优攻击、或正则化效果不足、或缺乏理论且局限于单一算法类型。需要一个不限算法类型、能在训练中施加最优攻击的鲁棒训练框架。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: SA-Dec-POMDP 扩展为 PA-Dec-POMDP；扰动作用于受害者观测，受 l-范数预算 ε 约束（õ∈B_ε）；实验中攻击所有智能体（M=N）。
- **设定**: cooperative；CTDE（QMIX/VDN，价值分解 + IGM）与 SEAC（共享经验 actor-critic，奖励可不同）两种范式；online；目标 max_π min_õ 折扣回报。

## 方法 (Method)
- 把鲁棒训练分解为内层 min（找最优对手）+ 外层 max（在最优对手下训练受害者）。
- 理论：证明 state attack 与 policy attack 等价（Property 1），把扰动空间从 |O| 降到 |A|；最优 state 对手等价于最优 policy 对手（Property 2）；最优对抗策略总位于对抗策略集边界（Property 3）；局部最优对手在 QMIX/VDN（IGM/单调）与 SEAC（独立训练）下即全局最优。
- MAPDA：director f（m 个对抗智能体，输出使受害者回报最小的方向 ā=f(o)）+ actor g（把策略沿 ā 拉到 C_ε 边界，生成扰动 õ=g(ā,o)）；构成零和博弈（对手奖励为 −r）。
- 实现：director 可用受害者算法或 MAPPO；actor 用 FGSM/PGD；VDN/QMIX 用全局 Q 共享损失式(20)，SEAC 用个体损失式(21)。受害者与对手交替/同时训练，得到 RoQMIX/RoVDN/RoSEAC。

## 理论贡献 (Theoretical Contributions)
给出 state↔policy 攻击等价性、最优 state/policy 对手等价、最优对抗策略位于边界、局部最优=全局最优（在 IGM/SEAC 下）的若干性质（Property 1-3），为把 PA-AD 迁移到 MADRL 训练提供理论依据；收敛性等无形式化证明，偏方法+实证。

## 实验 (Experiments)
- **环境/Benchmark**: MARL_CAVs（匝道 CAV/HDV，3 与 5 CAVs）、RWARE 仓储机器人（2ag/4ag，10x11 网格）、SMAC（2s_vs_1sc）。
- **Baselines**: Original QMIX/VDN/SEAC（无鲁棒训练）、FGSM 训练、PGD、ATLA（用 MAPPO 直接训练 state 对手）。
- **评估指标**: episode return、crash rate（CAVs）、平均 return、win rate（SMAC）；测试用 random noise、Gaussian noise、FGSM 在递增扰动强度下评估；并评估 clean 观测下性能。

## 主要结果 (Key Results)
- 对弱扰动（random/Gaussian）有稳定小幅提升（RoQMIX 在 5CAVs 最小 +2.7% 到最大 +9.8%；RoVDN 最高 +12.6%；RoSEAC 最高 +14.5%）。
- 对强攻击 FGSM 提升显著（RoQMIX 在 3CAVs 最高 +857.6%；RoVDN +40.8%~63.4%；RoSEAC +51.8%~176.5%）。
- 泛化性好：随扰动强度增大性能下降最小，FGSM 下仍保持优势；在 SMAC 上同样超过所有 baseline，证明跨环境通用性。
- clean 观测下多数情况优于鲁棒 baseline，偶有轻微下降（过拟合噪声），但在可接受范围；crash rate 提升不明显（clean 下各方法都能完成基本防撞）。

## 局限与未来工作 (Limitations & Future Work)
clean 观测下偶有性能轻微下降（对噪声过拟合）；理论基础仍待加强；未考虑摩擦等物理因素。未来改进 MAPDA、设计更高效训练框架、优化最优攻击搜索、并探索 backdoor 等其他攻击形式。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"状态/观测对抗 + 对抗训练 + minimax"主线，是 PA-AD（SADRL 测试期攻击）向 MADRL 训练期的迁移与理论化（state↔policy 等价），并跨价值分解（QMIX/VDN）与策略梯度（SEAC）两类算法验证；与同作者 QMIX 鲁棒化工作（条目32）、RMA3C、RoMFAC 等紧密相关，面向 Industry 5.0 实际应用。
