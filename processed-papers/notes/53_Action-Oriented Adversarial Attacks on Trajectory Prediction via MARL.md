# 53. Action-Oriented Adversarial Attacks on Trajectory Prediction in Connected Autonomous Vehicles via Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Action-Oriented Adversarial Attacks on Trajectory Prediction in Connected Autonomous Vehicles via Multi-Agent Reinforcement Learning
- **作者**: Xiaofeng Zhao, Dengfeng Sun
- **机构**: School of Aeronautics and Astronautics, Purdue University, West Lafayette, IN, USA
- **发表**: 未明确（preprint, not peer reviewed；SSRN abstract 5348784，submitted to Elsevier）
- **链接/arXiv**: https://ssrn.com/abstract=5348784

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗攻击（针对基础设施级轨迹预测模型输出的有界扰动；CAV 安全监督逻辑的脆弱性）
- **方法范式**: 对抗 MARL / 鲁棒性评估、CTDE、prediction-adversarial MDP (PA-MDP)、action-oriented 优化（缓解维数灾难）、Bellman 压缩
- **关键词**: MARL, connected autonomous vehicles, trajectory prediction, adversarial machine learning, CTDE, reliability evaluation

## TL;DR（一句话总结）
提出 AO-PA-MARL——一个基于 CTDE 的对抗 MARL 框架，作为黑盒攻击者协同地对基础设施级（RSU）轨迹预测输出施加有界扰动以误导下游安全监督逻辑；通过 action-oriented 优化缓解多智能体轨迹空间的维数灾难，并证明最优对抗策略存在，用于评估 CAV 轨迹规划模型的鲁棒性。

## 问题与动机 (Problem & Motivation)
CAV 依赖基础设施辅助（V2I/RSU/边缘云）的集中式轨迹预测与协同规划，但其集中性带来网络安全脆弱：攻陷预测模块可同时危及多个自动驾驶 agent 的安全。已有对抗工作多针对感知噪声、规划注入或直接状态操纵，且常需白盒/策略级访问；基础设施级轨迹预测这一现实攻击面研究不足。需要一个不需白盒、仅扰动预测输出、且能系统评估预测驱动的 CAV 协同鲁棒性的框架。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 黑盒攻击者攻陷 RSU 处的轨迹预测模块，仅扰动预测模型的输出（不改动车载感知/执行），扰动受物理约束有界（如 crowd navigation ±0.2 m）；建模为 prediction-adversarial MDP (PA-MDP)。
- **设定**: cooperative/mixed（多车 + 行人/骑行者）；CTDE（中央 critic 训练、去中心执行，每车 150 m 局部观测）；针对已部署预测/规划系统的对抗评估阶段

## 方法 (Method)
1. **PA-MDP 形式化**: 将基础设施级预测对抗建模为 prediction-adversarial MDP；通过证明 Bellman 算子为 γ-压缩映射（Banach 不动点）得到唯一最优对抗策略，可迭代 Bellman 算子求解。
2. **维数灾难问题**: 连续轨迹动作空间维度 = agent 数 × 预测时域 × 状态特征，DDPG/TD3/MADDPG 难以收敛；朴素离散化则组合爆炸。
3. **Action-oriented 优化**: 不在完整连续/离散轨迹空间搜索，而限制对手到每车有限、结构化、语义有意义的离散候选行为；每个对抗 agent 输出风险动作 â 与参考安全动作集 ă 的分布。
4. **轨迹优化**: 构造扰动联合预测 ζ̃，增大风险动作 â 相关的 inter-agent 距离、减小安全动作 ă 相关距离，从而最大化误导安全监督并提升碰撞率，同时保持扰动对监督者"可信/合理"。

## 理论贡献 (Theoretical Contributions)
证明了 PA-MDP 下 Bellman 算子为 γ-压缩映射、最优对抗策略存在且唯一（Banach 不动点定理），并可通过迭代 Bellman 算子收敛求得。

## 实验 (Experiments)
- **环境/Benchmark**: crowd navigation（3 车 + 3 行人）、highway on-ramp merging（OpenAI Gym / highway-env）
- **Baselines**: continuous-action PA-MARL，分别用 MAPPO（PA-MAPPO）与 multi-agent SAC（PA-MASAC）实现
- **评估指标**: 训练/评估 reward、碰撞率 collision rate、收敛速度与稳定性

## 主要结果 (Key Results)
1. AO-PA-MARL 在两个环境中评估 reward 与收敛速度均优于 PA-MAPPO、PA-MASAC，训练更稳定。
2. 显著提高碰撞率：在 crowd navigation 中碰撞率较 baseline 提升约一个数量级，尤其在密集交互环境中更有效。
3. 结果揭示预测驱动的安全监督器存在系统性脆弱，验证 AO-PA-MARL 作为可扩展对抗压力测试工具的有效性。

## 局限与未来工作 (Limitations & Future Work)
为 preprint 未经同行评审；为攻击/评估框架而非防御方法；动作离散候选集需人工设计（限定语义行为）；评估限于两个仿真环境。结论部分提到框架的局限并展望进一步工作（如更现实威胁与防御）。

## 与综述的关联 (Relevance to Survey)
属 robust MARL 在自动驾驶/CAV 的应用，代表"对抗 MARL 作为鲁棒性评估工具"这一方向，聚焦基础设施级轨迹预测的黑盒攻击面；与对抗 MDP（最优对手存在性）、CTDE、维数灾难缓解、安全关键系统鲁棒性评估等主题相关。
