# 152. Attacking Cooperative Multi-Agent Reinforcement Learning by Adversarial Minority Influence

## 元信息 (Metadata)
- **标题**: Attacking Cooperative Multi-Agent Reinforcement Learning by Adversarial Minority Influence (AMI)
- **作者**: Simin Li, Jun Guo, Jingqiao Xiu, Yuwei Zheng, Pu Feng, Xin Yu, Jiakai Wang, Aishan Liu, Yaodong Yang, Bo An, Wenjun Wu, Xianglong Liu
- **机构**: Beihang University；Zhongguancun Laboratory；Peking University；Nanyang Technological University 等
- **发表**: arXiv:2302.03322（v3, 2024；NeurIPS 2023 相关）
- **链接/arXiv**: arXiv:2302.03322

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 对抗智能体攻击（合作 MARL 中的恶意少数体），黑盒、无需受害者参数
- **方法范式**: 对抗攻击、unilateral influence filter、targeted adversarial oracle
- **关键词**: c-MARL attack, adversarial minority influence, black-box, robot swarm, worst-case evaluation

## TL;DR（一句话总结）
针对合作 MARL (c-MARL) 现有观测攻击受限于白盒、忽视多智能体交互与合作目标的问题，提出黑盒强攻击 **AMI**：通过 unilateral influence filter 与 targeted adversarial oracle，让单个对抗"少数"智能体单方面误导多数受害者陷入集体最坏情形，首次成功攻击真实机器人集群并在 SMAC、Multi-agent Mujoco 上奏效。

## 问题与动机 (Problem & Motivation)
评估 c-MARL 的最坏情况性能对真实部署至关重要，但现有基于观测的攻击受白盒假设约束，未考虑 c-MARL 复杂的智能体间相互影响与合作目标，导致攻击不实际且能力有限。需要既实用（黑盒）又强力（利用合作结构）的攻击来刻画 c-MARL 真实脆弱性。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 一个对抗智能体（少数）混入合作队伍，黑盒、不知受害者参数，通过自身行为单方面影响其余智能体
- **设定**: cooperative（受害者为合作 MARL）；test-time 黑盒攻击；含仿真与真实机器人集群

## 方法 (Method)
- **Adversarial Minority Influence (AMI)**：把"少数对抗体影响多数"形式化为对受害者联合策略的最坏化误导
- **Unilateral influence filter**：刻画/优化对抗体对受害者的单向影响，避免受害者反向影响干扰
- **Targeted adversarial oracle**：将受害者诱导至特定（次优/最坏）协作目标
- 黑盒：无需受害者参数即可发动

## 理论贡献 (Theoretical Contributions)
无 / 偏实证（攻击框架与机制设计），给出对 c-MARL 合作结构的可利用性分析。

## 实验 (Experiments)
- **环境/Benchmark**: StarCraft II (SMAC)、Multi-agent Mujoco、真实机器人集群 (robot swarm)
- **Baselines**: 现有基于观测/白盒的 c-MARL 攻击
- **评估指标**: 受害者团队回报下降、攻击成功率、是否将群体导入最坏情形

## 主要结果 (Key Results)
- 单一对抗少数体即可把合作多数诱导进集体最坏场景，显著降低团队回报
- 首个成功攻击真实世界机器人集群的 c-MARL 攻击；黑盒、实用、强力

## 局限与未来工作 (Limitations & Future Work)
聚焦攻击，未给出对应防御；攻击有效性依赖对合作结构的利用，对高度异构/通信受限队伍的可迁移性待验证。

## 与综述的关联 (Relevance to Survey)
属 §3 对抗攻击线中"利用合作结构的智能体级黑盒攻击"代表作（被本语料 5× 引用），为 robust c-MARL 防御提供强威胁模型；与 [[59_On the Robustness of Cooperative MARL]]、[[98_Robustness Testing for MARL - State Perturbations on Critical Agents]] 等攻防工作对照。
