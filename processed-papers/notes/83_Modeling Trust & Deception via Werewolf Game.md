# 83. Modeling Trust and Deception in Multi-Agent Reinforcement Learning Using the Werewolf Game

## 元信息 (Metadata)
- **标题**: Modeling Trust and Deception in Multi-Agent Reinforcement Learning Using the Werewolf Game
- **作者**: Pathikkumar Dharmeshbhai Patel（导师 Dr. Manfred Huber）
- **机构**: The University of Texas at Arlington（CSE 系硕士学位论文）
- **发表**: M.S. Thesis, UT Arlington, May/Spring 2025（MavMatrix）
- **链接/arXiv**: https://mavmatrix.uta.edu/cse_theses/529

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体 / 隐藏角色欺骗（deception）、不完全信息下的信任建模；环境分布偏移下的鲁棒性
- **方法范式**: 符号化启发式 + 概率信任建模 (Agent vA)、模块化 Q-learning (Agent vB)、self-play、social deduction game 博弈
- **关键词**: trust modeling, deception, Werewolf, social deduction, Q-learning, hidden-role games

## TL;DR（一句话总结）
以 Werewolf 社会推理游戏为仿真框架，构建并对比两类智能体（符号化信任启发式 vA 与模块化 Q-learning vB），研究在隐藏角色、不完全信息下信任、欺骗与适应策略如何作为习得行为而非硬编码地涌现。

## 问题与动机 (Problem & Motivation)
随着 AI 嵌入现实应用（自动驾驶协调、金融市场、机器人团队），智能体需在不确定、不完全信息、存在欺骗性协作者/对手的环境中推理他人信念、意图与可信度。社会推理游戏 Werewolf 提供了信任建立、联盟形成、策略性误导等涌现行为的理想测试床。核心研究问题：RL 智能体能否在部分可观测、角色制环境中学会策略性建立信任或欺骗？欺骗能否仅通过 RL 自然涌现而非硬编码？

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 隐藏角色（Werewolf 知情少数 vs Villager 不知情多数），不对称信息，存在策略性欺骗与误导。鲁棒性体现为对人口规模、角色分布变化（环境 shift）和未见配置的适应。
- **设定**: mixed（合作 + 竞争并存的 social deduction）；decentralized（每 agent 局部观测，符号化通信）；online self-play

## 方法 (Method)
- Agent vA（符号化启发式）：手工 trust 模型 + 概率角色信念 + 有界记忆窗（5 轮 replay）+ 跨局持久记忆；决策由演化的 trust score 驱动，仅用轻量 RLAgent（epsilon-greedy）调制投票与发言策略；稀疏的赛后奖励。
- Agent vB（模块化 Q-learning）：按游戏阶段拆为三个独立 Q-table（night / day conversation / day vote），状态压缩为可哈希字符串（phase、num_alive、role、accused_flag、发现狼数、max suspicion），TD 更新（α=0.1, γ=0.95），epsilon 从 1.0 退火到 0.1；dense 的 role-specific reward shaping + 标量 suspicion (EMA)。
- 通信协议：结构化语句 accuse/reveal/support/agree。
- 训练支持 reset-per-episode 与 persistent memory 两种模式（主实验用后者），7–49 人、角色每局随机化以防身份过拟合。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（含与理论最少胜利轮数 heatmap 基线对比，但无形式化保证）

## 实验 (Experiments)
- **环境/Benchmark**: 自建 Python Werewolf 仿真（4 角色：Werewolf/Seer/Medic/Villager），7–49 玩家；vA 训练 500,000 局，vB 训练约 100,000 局
- **Baselines**: vA vs vB 头对头 hybrid 对战；理论 attrition 最少胜利轮数基线
- **评估指标**: 按角色 win rate、voting accuracy、deception success、survival duration、trust alignment

## 主要结果 (Key Results)
- vB 的 Werewolf 胜率约 0.69 收敛；vA self-play 中 Werewolf 团队 56.8% 胜率（284,109 vs 215,891）。
- 角色对比：vA 在需推理/欺骗的角色更强（Seer 74.2% vs 62.5%；Werewolf 66.1% vs 63.3%）；vB 在反应型角色更强（Medic 69.0% vs 58.7%；Villager 67.8% vs 55.4%）。
- hybrid 对战中 vA 初期占优，约 5,000 局后 vB 适应并基本追平。
- 欺骗行为（最少发言、mirroring、反应式投票）在无硬编码规则下自然涌现，验证 RL/符号系统均可习得欺骗与协作。
- vA 状态空间持续增长（扩展性差）；vB 状态压缩、约 100,000 局更早收敛、扩展性与适应性更强。

## 局限与未来工作 (Limitations & Future Work)
- 游戏机制简化（无非语言线索/情感/语言歧义）；角色仅 4 种；假设所有 agent 能力对等。
- 通信为固定符号语言原语，未用自然语言；采样状态空间有限，存在过拟合训练域风险。
- 早期版本探索偏差（过早收敛）；vA 信任系统部分硬编码（trust decay 手工标定，未学习）。
- 未来：多模态通信、更多角色、curriculum/transfer/meta-RL、学习式 trust embedding（attention/神经网络）、intrinsic curiosity 探索。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"对抗智能体 / 欺骗 / 信任建模"主题，与本批 80、82 的 trust-based 方法线相关，但聚焦 hidden-role social deduction 这一对手为策略性欺骗者的设定。对比符号推理 vs RL 的鲁棒性/适应性权衡，与 DeepRole、Bayesian Belief Manipulation、LLM-based Werewolf agent 等社会推理博弈工作相承，对设计能在欺骗性、社会复杂域中鲁棒的可信 AI 有借鉴意义。
