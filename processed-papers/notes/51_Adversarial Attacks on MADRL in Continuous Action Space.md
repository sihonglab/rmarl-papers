# 51. Adversarial Attacks on Multiagent Deep Reinforcement Learning Models in Continuous Action Space

## 元信息 (Metadata)
- **标题**: Adversarial Attacks on Multiagent Deep Reinforcement Learning Models in Continuous Action Space
- **作者**: Ziyuan Zhou, Guanjun Liu, Weiran Guo, MengChu Zhou
- **机构**: Department of Computer Science, Tongji University, Shanghai; Macau University of Science and Technology; New Jersey Institute of Technology
- **发表**: IEEE Transactions on Systems, Man, and Cybernetics: Systems, Vol. 54, No. 12, December 2024
- **链接/arXiv**: DOI 10.1109/TSMC.2024.3454118

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动（对 critical agent 观测的对抗攻击，含连续动作空间下的最坏联合动作）
- **方法范式**: 对抗攻击/鲁棒性测试、critical agent 选择（梯度信息 GI + 差分进化 DE）、SARSA 学习联合动作价值、目标攻击（PGD/SGLD）
- **关键词**: adversarial attack, MADRL, continuous action space, critical agents, CTDE, industry 5.0

## TL;DR（一句话总结）
提出连续动作空间 MADRL 对抗攻击框架 AMCA：用梯度信息/差分进化识别随时间变化的 critical agents 并确定其最坏联合动作（以 SARSA 学习的联合动作价值 SJAV 为目标），再对这些 agent 做目标攻击（PGD/SGLD），仅扰动一两个 agent 即可严重破坏团队协作。

## 问题与动机 (Problem & Motivation)
MADRL（应用于 industry 5.0、自动驾驶、机器人等）对状态扰动敏感，少数 agent 状态被扰动即可破坏团队协作策略。现有 MADRL 攻击假设受害 agent 集合固定（可建模为 stochastic game），无法处理受害 agent 随时间变化的情形；且 CTDE 去中心执行时联合动作价值/中央 critic 未知，原估计在 agent 取次优动作时不准确。需解决：(1) 选哪些 critical agent；(2) 受害集不确定下的最坏联合动作；(3) 测试中如何评估动作对团队策略的影响。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 攻击者扰动随时间变化的"critical agents"的观测，使其执行最坏联合动作以最小化团队累积回报；约束受害 agent 数量极少（一到两个）以求隐蔽。连续动作空间。
- **设定**: cooperative MADRL；CTDE（MADDPG / FACMAC）；测试/攻击阶段（针对已训练模型）

## 方法 (Method)
1. **两步框架 AMCA**: 第一步用梯度信息 (GI) 或差分进化 (DE) 识别 critical agents 并求其最坏联合动作（最小化团队累积奖励）；第二步以新型损失为目标做目标攻击生成扰动。
2. **SJAV**: 提出基于 SARSA 学习联合动作价值函数，刻画个体动作与累积奖励的关系，作为第一步识别 critical agent 的目标函数（能评估次优行为，弥补中央 critic 在 CTDE 执行期不可得/估计不准的问题）。
3. **扰动生成**: 采用 PGD、SGLD 等目标攻击对 critical agent 观测加扰动。
4. critical agent 集合随时间动态变化，突破固定受害集（stochastic game 建模）的限制。

## 理论贡献 (Theoretical Contributions)
证明了 SJAV（SARSA 学习联合动作价值）的收敛性（Theorem 1，基于 Q-learning 收敛的经典随机逼近论证）。

## 实验 (Experiments)
- **环境/Benchmark**: CUME、MAMuJoCo、MPE（含两个工业相关环境），受害模型由 MADDPG、FACMAC 训练
- **Baselines**: 现有固定受害集攻击方法；鲁棒训练对手 FACMAC_ATLA、FACMAC_PAAD；随机/对比攻击
- **评估指标**: 攻击后团队 reward（越低越强）、攻击成功率、运行时间/内存开销；消融与跨算法迁移

## 主要结果 (Key Results)
1. AMCA 仅攻击一两个 agent 即可显著破坏协作策略，扰动能力强于现有方法。
2. 跨算法迁移性强：用 MADDPG 轨迹/价值攻击 FACMAC（及反之）在多数情形仍有高成功率。
3. 对抗训练防御 FACMAC_ATLA、FACMAC_PAAD 在 CUME/MAMuJoCo 等下并未稳定提升鲁棒性，有时反而劣于原始 FACMAC，说明现有防御不足。

## 局限与未来工作 (Limitations & Future Work)
真实场景中直接施加噪声可能造成实际危害且 sim-to-real 困难；目标攻击损失/优化方法待优化；缺乏针对 AMCA 的自适应防御。未来计划用 meta-learning/domain randomization 弥合 sim-to-real 差距并开发更鲁棒防御。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中"观测/动作扰动攻击 + 鲁棒性测试"主线，聚焦连续动作空间与动态 critical-agent 选择；与 SA-MDP、ATLA、PAAD、critical-agent 攻击、stochastic-game 对手建模等工作相关，并暴露现有对抗训练防御的不足。
