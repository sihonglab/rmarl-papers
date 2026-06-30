# 59. On the Robustness of Cooperative Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: On the Robustness of Cooperative Multi-Agent Reinforcement Learning
- **作者**: Jieyu Lin, Kristina Dzeparoska, Sai Qian Zhang, Alberto Leon-Garcia, Nicolas Papernot
- **机构**: University of Toronto；Harvard University；Vector Institute
- **发表**: IEEE Symposium on Security and Privacy Workshops (SPW) 2020
- **链接/arXiv**: DOI 10.1109/SPW50608.2020.00027

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 状态/观测扰动（对单个智能体观测施加对抗样本）
- **方法范式**: 对抗攻击（攻击者视角）、对抗策略 + 梯度对抗样本、黑盒+白盒攻击
- **关键词**: c-MARL, adversarial examples, QMIX, observation perturbation, attack surface

## TL;DR（一句话总结）
首个对协作式 MARL（c-MARL）鲁棒性的分析，提出两步攻击（RL 学习对抗策略 + 定向对抗样本 d-JSMA），仅扰动单个智能体观测即可把 SMAC 团队胜率从 98.9% 打到 0%。

## 问题与动机 (Problem & Motivation)
c-MARL 被用于交通灯、自动驾驶、基站控制等关键基础设施，但其在对抗操纵下的鲁棒性尚未被研究。直接套用单智能体 RL 攻击有三大困难：(1) 团队奖励难估计且 QMIX 含不可微的 max 操作；(2) 误分类率高不等于奖励下降；(3) 输入特征维度低，限制扰动方式。需要刻画"单个智能体被攻击"暴露的攻击面。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 攻击者预先选定一个受害智能体，可修改其局部观测 o（受 L1 扰动预算约束）；目标是最小化团队总奖励 R。第一步仅需黑盒访问（查询策略与环境），第二步需白盒梯度访问（可扩展到黑盒迁移）。
- **设定**: cooperative；CTDE（QMIX）；execution 阶段攻击（online 推断时）

## 方法 (Method)
- **两步攻击框架**：第一步用 RL 学习"对抗策略"，找出受害者若执行则最大降低 R 的目标动作；第二步用梯度定向对抗样本诱导受害者执行该动作。
- **第一步 OW/OWR**：将其余智能体视为固定环境，把攻击化为单智能体 RL（最小化 R），用 DQN 训练。OWR 在损失中加正则项 λ·d_diff²（目标动作与原最优动作的 Q 值差），使目标动作更易被对抗样本实现。
- **第二步 d-JSMA**：扩展 JSMA 以适配低维特征——同时扰动两个特征（解决单特征扰动使所有动作 Q 值同向变化的问题），并采用动态步长 θ（从小到大重试），构造定向对抗样本。
- 还提出 it-FGSM（定向迭代 FGSM，对目标 Q 值取梯度），但效果不及 d-JSMA+OWR。

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（攻击方法论与实证分析）。

## 实验 (Experiments)
- **环境/Benchmark**: StarCraft Multi-Agent Challenge (SMAC)，"2s3z" 地图（受害者为一名 Stalker）
- **Baselines**: Random / Local Worst (LW) / QMIX Worst 动作选择；FGSM、it-FGSM、JSMA 等对抗样本方法的组合
- **评估指标**: 平均团队奖励、团队胜率、目标动作成功率、误分类率、扰动 L1 范数预算

## 主要结果 (Key Results)
- 仅控制单个智能体动作（OW/OWR）即可把奖励从 20 降到约 9.4、胜率降为 0%。
- 两步攻击 d-JSMA+OWR 仅扰动观测即达到 10.62 的奖励降幅，接近直接控制动作的 10.65，平均 L1 扰动仅 8.33。
- 正则化（OWR vs OW）在两步组合中带来明显收益，降低所需扰动预算。
- 攻击下受害者表现出"躲藏直到队伍快被消灭再主动送死/诱导队友"等行为。

## 局限与未来工作 (Limitations & Future Work)
仅在 SMAC 单一地图、单一受害者上验证；第二步白盒假设较强。防御方面仅作讨论（未实现）：建议各智能体估计他者动作值/奖励以识别恶意智能体（结合 IRL、model-based RL），或在集中训练中把所有智能体视为潜在对手。

## 与综述的关联 (Relevance to Survey)
属于 robust MARL 中"观测/状态扰动 + 对抗攻击"线的奠基性工作，首次刻画 c-MARL 的攻击面，为后续认证鲁棒、对抗训练防御提供威胁模型与基准（SMAC + QMIX）。
