# 161. Adversarial Attacks in Consensus-Based Multi-Agent Reinforcement Learning

## 元信息 (Metadata)
- **标题**: Adversarial Attacks in Consensus-Based Multi-Agent Reinforcement Learning
- **作者**: Martin Figura, Krishna Chaitanya Kosaraju, Vijay Gupta
- **机构**: Department of Electrical Engineering, University of Notre Dame
- **发表**: American Control Conference (ACC) 2021；arXiv:2103.06967 (2021)
- **链接/arXiv**: arXiv:2103.06967；doi:10.23919/ACC50511.2021.9483080

## 分类 (Taxonomy)
- **鲁棒性针对的扰动类型**: 内部对抗智能体（malicious participating agent）对 consensus/critic 更新的攻击，即通信/共识层面的攻击；非外部数据投毒
- **方法范式**: 网络化 MARL、consensus-based actor-critic、收敛性分析、漏洞揭示（attack design）
- **关键词**: consensus MARL, adversarial agent, networked agents, resilience, distributed actor-critic, convergence

## TL;DR（一句话总结）
研究基于共识（consensus）的协作分布式 MARL 算法在内部对抗智能体下的脆弱性，证明只要单个恶意智能体不执行共识更新、向邻居广播相同的（自利）信号，整个网络都会被诱导去优化该攻击者所选的效用函数，从而表明标准 consensus-based MARL 算法对此类攻击是脆弱的，亟需 resilient consensus MARL 设计。

## 问题与动机 (Problem & Motivation)
协作分布式 MARL 中，各智能体只见自身局部奖励，需通过 consensus 协议传播信息以共同最大化团队平均回报（同时保护各自奖励/动作的隐私）。Zhang et al. 的 consensus actor-critic（[9, Algorithm 2]）可在时变通信图上保证收敛到团队最优策略。但现实通信链路常中断或信号被篡改，consensus 的一个经典结论是：共识矩阵的拓扑决定收敛极限值，单个不做共识更新的恶意节点会使极限值等于该对手的值。作者由此追问：单个参与的对抗智能体能否阻止收敛，甚至诱导其他智能体去优化它选择的效用函数。

## 鲁棒性设定 (Robustness Setting)
- **威胁模型 / 不确定性集**: 网络中存在单个内部 malicious agent，可篡改自身的 consensus 与 critic 更新，并向邻居发送相同的（贪婪最大化自身目标的）信号；区别于外部 data/reward poisoning
- **设定**: cooperative（团队平均回报）；decentralized / networked agents，基于 consensus 的分布式 actor-critic；折扣奖励；online 训练

## 方法 (Method)
- 在网络化 MDP 与 consensus-based actor-critic（[9, Algorithm 2]）框架下，设定一个恶意智能体不执行正常共识更新、转而向所有邻居传播相同信号
- 设计该恶意智能体贪婪最大化其自定义目标函数的攻击策略
- 给出类比原算法的渐近收敛性分析，证明在该攻击下其余智能体的更新被拉向对手目标
- 通过数值仿真验证：全网最终都在最大化对手的目标函数

## 理论贡献 (Theoretical Contributions)
证明在单个恶意智能体破坏 consensus/critic 更新下，consensus-based MARL 仍渐近收敛，但收敛到使所有智能体最大化对手效用函数的结果（即攻击成功的收敛性证明），从理论上揭示标准 consensus MARL 的脆弱性。

## 实验 (Experiments)
- **环境/Benchmark**: 数值仿真（networked MDP，第 4 节）
- **Baselines**: 无攻击下的 consensus MARL 收敛行为作为对照
- **评估指标**: 各智能体策略/目标的收敛结果（是否趋向对手目标）、收敛性

## 主要结果 (Key Results)
- 单个内部恶意智能体即可使整个网络收敛到优化"对手所选目标函数"，而非团队平均最优
- 攻击源于 consensus 的拓扑性质：不做更新的恶意节点决定共识极限值
- 标准 consensus-based MARL 对此类内部攻击本质脆弱，凸显设计 resilient consensus MARL 的必要性

## 局限与未来工作 (Limitations & Future Work)
仅考虑单个恶意智能体与特定 consensus 算法；未提出防御/弹性算法（仅揭示漏洞，resilient consensus MARL 留作动机性未来工作）；实验为小规模数值仿真。

## 与综述的关联 (Relevance to Survey)
本文属 robust MARL 中 [[通信攻击]] 与 [[Byzantine/容错]] 线的早期奠基工作，把控制论中 resilient consensus 的脆弱性结论引入 networked/decentralized MARL，揭示 [[对抗智能体]] 在共识层的破坏力，为后续 [[resilient/Byzantine-robust 共识 MARL]] 提供问题动机与威胁模型。
