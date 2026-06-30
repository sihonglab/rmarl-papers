# 174. Robust Multi-Agent Q-Learning in Cooperative Games with Adversaries

## 元信息 (Metadata)
- **标题**: Robust Multi-agent Q-learning in Cooperative Games with Adversaries
- **作者**: Eleni Nisioti, Daan Bloembergen, Michael Kaisers
- **机构**: Centrum Wiskunde & Informatica (CWI), Amsterdam, The Netherlands
- **发表**: AAAI 2021（Reinforcement Learning in Games workshop）
- **链接/arXiv**: 代码 https://github.com/eleninisioti/robust-marl

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体——一队 adversaries 在随机时刻到来，对目标智能体进行最坏情况的"选谁攻击 + 执行什么动作"的双重选择，直接操纵被选智能体的动作
- **方法范式**: minimax decision rule、robust Bellman operator、Q-learning（temporal difference）、linear programming 求解最坏情况
- **关键词**: RoM-Q, multi-agent adversarial attack, minimax-Q, worst-case agent selection, robust temporal difference

## TL;DR（一句话总结）
提出 RoM-Q——一种类 Q-learning 算法，针对"知晓最优多智能体 Q 函数、并对'攻击哪些智能体 + 执行哪些动作'做最坏情况选择"的新型 multi-agent adversarial attack；训练时在中心化联合状态-动作空间上"想象"该攻击并对最坏情况更新 Q 值，从而无需在训练中真正模拟攻击即可学到鲁棒策略，实验中对各类对抗攻击都获得最高回报。

## 问题与动机 (Problem & Motivation)
现实多智能体系统（通信网络、电网等）有高度不安全的危险区域，传统离线学习假设所有智能体都最大化共同目标，导致策略对哪怕单个智能体的异常行为都不鲁棒，部署时易被攻击。本文提出一种新型攻击：一队固定数量的 adversaries 在随机时间步到来，做"目标智能体选择 + 动作选择"的对抗性最坏情况组合，直接操纵被选智能体动作——这把经典"最坏情况动作选择"扩展到了"跨多个智能体的对抗性选择"，在某些智能体更脆弱/更关键、其异常会引发级联失效的系统中尤为重要。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 固定数量 adversaries，知晓最优多智能体 Q 值；随机时刻发动，对"选哪些智能体 + 让其执行哪些动作"做最坏情况（worst-case）选择，直接篡改动作；为单步/短视攻击（选择当前状态下回报最低的动作）
- **设定**: cooperative game with adversaries；centralized 训练（智能体观测全体状态-动作、在联合状态-动作空间学 Q）；offline 风格、无需训练时模拟攻击

## 方法 (Method)
- 设计 robust 时序差分算法 RoM-Q：目标策略的价值在"假设 multi-agent adversarial attack 正在发生"的前提下计算
- 评估目标策略时，枚举给定数量 adversaries 的所有可能选择，对最坏情况（worst-case selection）更新 Q 值
- 每次更新需求解多个 linear programs，每个采用与 minimax-Q 相同的形式；LP 个数取决于智能体数与 adversary 数
- 攻击效果基于智能体自身价值函数计算，故无需 adversary 模型，也无需在训练时真正模拟攻击；训练用 ε-greedy，评估用 greedy

## 理论贡献 (Theoretical Contributions)
无 / 偏实证为主。主要贡献是把 minimax-Q 的最坏情况动作选择扩展为"跨多智能体的对抗选择"这一新型 robust Bellman 更新（通过求解多个 LP 实现），形式化定义了 multi-agent adversarial attack；正文未给出完整收敛性证明。

## 实验 (Experiments)
- **环境/Benchmark**: 一个抽象化的 load balancing 问题（受计算机网络/智能电网启发），建模为节点网络执行任务、最小化运行成本并避免 over-flow
- **Baselines**: Q-learning、minimax-Q（以及由各方法导出的相应对抗攻击）
- **评估指标**: 在各种对抗攻击下累积的回报（鲁棒性）

## 主要结果 (Key Results)
- 用 RoM-Q 学得的策略比 Q-learning 与 minimax-Q 更鲁棒，在所有考察的对抗攻击下都取得最高回报
- 无需在训练中模拟攻击即可获得鲁棒性——攻击效果完全基于智能体自身价值函数"想象"得到
- 验证了"对抗性选择目标智能体"这一新威胁维度的重要性，尤其在个别智能体更脆弱/更关键的系统中

## 局限与未来工作 (Limitations & Future Work)
更新需求解的 LP 数随智能体与 adversary 数量增长，扩展性受限；采用表格型 Q、依赖中心化联合状态-动作信息；攻击为短视单步、未覆盖长期/观测操纵型攻击；实验仅在抽象 load balancing 上验证。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 中 [[对抗智能体]] 与 [[minimax]] 线的工作，将单智能体 robust RL 的"想象最坏情况"算子（robust operator）与 [[minimax-Q]] 推广到"对抗性挑选受害智能体"的协作博弈场景；与 [[安全约束/critical MAS]]、[[动作扰动]] 主题相关。
